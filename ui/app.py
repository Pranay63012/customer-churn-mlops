import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")
st.title("📊 Customer Churn Prediction System")

st.markdown("Enter customer details below to predict churn risk.")

gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", ["No", "Yes"])
partner = st.selectbox("Has Partner", ["Yes", "No"])
dependents = st.selectbox("Has Dependents", ["Yes", "No"])

tenure = st.slider("Customer Tenure (Months)", 0, 72, 12)

internet = st.selectbox(
    "Internet Service Type",
    ["DSL", "Fiber optic", "No"]
)

contract = st.selectbox(
    "Contract Type",
    ["Month-to-month", "One year", "Two year"]
)

payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ],
)

monthly = st.number_input("Monthly Charges (₹)", min_value=0.0, step=1.0)
total = st.number_input("Total Charges Paid (₹)", min_value=0.0, step=10.0)

if st.button("🔍 Predict Churn Risk"):
    payload = {
    "gender": gender,
    "SeniorCitizen": 1 if senior == "Yes" else 0,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,

    "PhoneService": "Yes",
    "MultipleLines": "No",

    "InternetService": internet,
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",

    "Contract": contract,
    "PaperlessBilling": "Yes",
    "PaymentMethod": payment,

    "MonthlyCharges": monthly,
    "TotalCharges": total,
}


    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        prob = result["churn_probability"]

        if prob >= 0.6:
            st.error("❌ Customer is likely to leave")
            st.markdown("### 🔴 Risk Level: HIGH")
            st.markdown(f"**Churn Probability:** {prob * 100:.1f}%")
            st.markdown("### 💡 Recommended Action")
            st.markdown("- Offer retention discount\n- Suggest long-term contract")

        elif prob >= 0.3:
            st.warning("⚠️ Customer may leave")
            st.markdown("### 🟡 Risk Level: MEDIUM")
            st.markdown(f"**Churn Probability:** {prob * 100:.1f}%")
            st.markdown("### 💡 Recommended Action")
            st.markdown("- Provide better support\n- Personalized offers")

        else:
            st.success("✅ Customer is likely to stay")
            st.markdown("### 🟢 Risk Level: LOW")
            st.markdown(f"**Churn Probability:** {prob * 100:.1f}%")
            st.markdown("### 💡 Recommended Action")
            st.markdown("- No immediate action required")

    else:
        st.error("API error. Please try again.")
