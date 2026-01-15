import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import random
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="AI Diet Recommendation System",
    page_icon="🥗",
    layout="wide"
)

# Custom CSS for Cards (Video jaisa look dene ke liye)
st.markdown("""
    <style>
    .meal-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border-top: 4px solid #00CC66;
        margin-bottom: 10px;
        height: 120px;
        color: white;
    }
    .meal-title {
        color: #00CC66;
        font-weight: bold;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# ===================== DUMMY DATA (For logic) =====================
DIET_TEXT = {
    "Balanced": ["Oats with Berries", "Grilled Chicken Salad", "Greek Yogurt", "Baked Salmon with Veggies"],
    "Keto": ["Avocado & Eggs", "Steak with Butter", "Almonds", "Cheesy Spinach & Chicken"],
    "Vegan": ["Smoothie Bowl", "Chickpea Curry", "Fruit Salad", "Tofu Stir-fry"],
    "Diabetes_Friendly": ["Whole Grain Toast", "Lentil Soup", "Walnuts", "Roasted Cauliflower"]
}
CALORIES = {
    "Balanced": [400, 700, 200, 600],
    "Keto": [500, 800, 300, 700],
    "Vegan": [350, 600, 150, 500],
    "Diabetes_Friendly": [300, 500, 100, 400]
}
MACROS = {
    "Balanced": [25, 50, 25],
    "Keto": [20, 5, 75],
    "Vegan": [15, 65, 20],
    "Diabetes_Friendly": [30, 40, 30]
}
GROCERY = {
    "Balanced": ["Oats", "Berries", "Chicken", "Salmon", "Mixed Veggies"],
    "Keto": ["Eggs", "Avocado", "Butter", "Cheese", "Steak"],
    "Vegan": ["Tofu", "Chickpeas", "Fruits", "Soy Milk", "Lentils"],
    "Diabetes_Friendly": ["Whole Grains", "Lentils", "Walnuts", "Leafy Greens"]
}

# ===================== SIDEBAR INPUTS =====================
with st.sidebar:
    st.header("🧍 Personal & Health Details")
    age = st.number_input("Age", 10, 100, 25)
    weight = st.number_input("Weight (kg)", 10.0, 200.0, 70.0)
    height = st.number_input("Height (cm)", 100.0, 220.0, 170.0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    disease = st.selectbox("Disease", ["None", "Diabetes", "Hypertension", "Heart Disease", "PCOS", "Thyroid", "Obesity"])
    severity = st.selectbox("Severity", ["None", "Low", "Moderate", "High"])
    activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
    diet_pref = st.selectbox("Diet Preference", ["None", "Vegan", "Vegetarian", "Gluten-Free"])

# ===================== MAIN UI =====================
st.title("🥗 AI Diet Recommendation System")
st.markdown("---")

if st.button("🍽️ Generate Diet Plan"):
    # BMI Calculation
    bmi = round(weight / ((height/100)**2), 2)
    
    # Model Logic (Placeholder for joblib)
    # prediction = model.predict(user_df)[0]
    prediction = "Balanced" # Demo prediction
    if disease == "Diabetes": prediction = "Diabetes_Friendly"
    if diet_pref == "Vegan": prediction = "Vegan"

    # 1. Recommended Banner
    st.success(f"### Recommended Diet Type: {prediction}")
    
    # 2. BMI Info
    if bmi < 18.5:
        st.warning(f"📏 BMI: {bmi} | Underweight - High protein intake recommended.")
    elif bmi < 25:
        st.info(f"📏 BMI: {bmi} | Normal - Keep maintaining your lifestyle.")
    else:
        st.error(f"📏 BMI: {bmi} | Overweight - Calorie deficit recommended.")

    # 3. Charts Section
    st.markdown("---")
    col1, col2 = st.columns(2)
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]

    with col1:
        st.subheader("📊 Calories Distribution")
        fig = px.pie(values=CALORIES[prediction], names=meals, hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💪 Macro Nutrients (%)")
        df_macros = pd.DataFrame({"Macro": ["Protein", "Carbs", "Fat"], "Percent": MACROS[prediction]})
        fig2 = px.bar(df_macros, x="Macro", y="Percent", color="Macro", 
                     color_discrete_map={"Protein": "#00CC66", "Carbs": "#FFCC00", "Fat": "#FF4B4B"})
        st.plotly_chart(fig2, use_container_width=True)

    # 4. Daily Diet Plan (Horizontal Cards like Video)
    st.markdown("---")
    st.subheader("🍱 Daily Diet Plan")
    m_cols = st.columns(4)
    for i, (m, f) in enumerate(zip(meals, DIET_TEXT[prediction])):
        with m_cols[i]:
            st.markdown(f"""
                <div class="meal-card">
                    <div class="meal-title">{m}</div>
                    <div>{f}</div>
                </div>
            """, unsafe_allow_html=True)

    # 5. Weekly Plan & Grocery List
    st.markdown("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📅 Weekly Diet Plan")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekly_data = []
        for d in days:
            weekly_data.append(random.sample(DIET_TEXT[prediction], 4))
        
        weekly_df = pd.DataFrame(weekly_data, columns=meals, index=days)
        st.table(weekly_df)

    with col_right:
        st.subheader("🛒 Suggested Grocery List")
        for item in GROCERY[prediction]:
            st.markdown(f"- {item}")

    # 6. PDF Download
    def create_pdf():
        file = "diet_plan.pdf"
        doc = SimpleDocTemplate(file, pagesize=A4)
        styles = getSampleStyleSheet()
        content = []
        content.append(Paragraph("AI Diet Recommendation Report", styles["Title"]))
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"Diet Type: {prediction}", styles["Normal"]))
        content.append(Paragraph(f"BMI: {bmi}", styles["Normal"]))
        
        data = [["Meal", "Recommendation"]] + list(zip(meals, DIET_TEXT[prediction]))
        t = Table(data)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.green),('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)]))
        content.append(t)
        doc.build(content)
        return file

    pdf_path = create_pdf()
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Diet Report (PDF)", f, file_name="My_Diet_Plan.pdf")

    st.balloons()