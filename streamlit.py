import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("diet_model.pkl")

st.title("🍽️ AI Diet Recommendation System")
st.write("Smart, personalized diet plans based on your health profile.")

# Collect user input
age = st.number_input("Age", min_value=10, max_value=100, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.number_input("Weight (kg)", min_value=10.0, max_value=200.0, step=0.5)
height = st.number_input("Height (cm)", min_value=100, max_value=220, step=1)
disease = st.selectbox("Disease Type", ["None", "Diabetes", "Hypertension", "Heart Disease"])
severity = st.selectbox("Severity", ["None", "Low", "Moderate", "High"])
activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
dietary_restrictions = st.text_input("Dietary Restrictions (comma separated)", "None")
allergies = st.text_input("Allergies (comma separated)", "None")

if st.button("Get My Diet Plan"):
    user_df = pd.DataFrame([{
        "Age": age,
        "Gender": gender,
        "Weight_kg": weight,
        "Height_cm": height,
        "Disease_Type": disease,
        "Severity": severity,
        "Physical_Activity_Level": activity,
        "Dietary_Restrictions": dietary_restrictions,
        "Allergies": allergies
    }])

    prediction = model.predict(user_df)[0]

    st.subheader("Recommended Diet:")
    st.success(prediction)

    # Diet Chart Templates
    DIET_CHART = {
        "Balanced": {
            "Breakfast": "Oats + Fruits + Milk",
            "Lunch": "Rice / Roti + Dal + Sabzi + Curd",
            "Snack": "Peanuts / Fruit Salad",
            "Dinner": "Chapati + Vegetables + Soup"
        },
        "Low_Carb": {
            "Breakfast": "Egg/Oats + Nuts",
            "Lunch": "Grilled Paneer/Chicken + Salad",
            "Snack": "Cucumber / Greek Yogurt",
            "Dinner": "Low-carb roti + Veggies"
        },
        "Low_Sodium": {
            "Breakfast": "Poha without salt + Fruits",
            "Lunch": "Chapati + Dal (low salt) + Veggies",
            "Snack": "Fruit bowl",
            "Dinner": "Khichdi + Curd (low salt)"
        }
    }

    st.subheader("Your Personalized Diet Chart:")

    chart = DIET_CHART.get(prediction, {})

    if chart:
        for meal, item in chart.items():
            st.write(f"**{meal}:** {item}")
    else:
        st.warning("No chart available for this diet type.")
