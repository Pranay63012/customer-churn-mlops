import streamlit as st
import requests

API_URL = "https://customer-churn-mlops.onrender.com/predict"

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

st.title("📉 Customer Churn Risk Predictor")
st.write(
    "This tool helps predict whether a customer is **likely to leave the service**, "
    "based on their subscription and usage details."
)

st.divider()

with st.form("churn_form"):

    st.subheader("👤 Customer Profile")

    gender = st.radio("Customer Gender", ["Male", "Female"], horizontal=True)

    senior = st.radio(
        "Is the customer a senior citizen (60+)?",
        ["No", "Yes"],
        horizontal=True
    )

    partner = st.radio(
        "Does the customer have a partner?",
        ["No", "Yes"],
        horizontal=True
    )

    dependents = st.radio(
        "Does the customer have dependents?",
        ["No", "Yes"],
        horizontal=True
    )

    tenure = st.slider(
        "How long has the customer been using the service? (months)",
        min_value=0,
        max_value=72,
        value=12
    )

    st.divider()
    st.subheader("📞 Services Used")

    phone = st.radio("Phone Service", ["Yes", "No"], horizontal=True)

    multiple = st.selectbox(
        "Multiple phone lines",
        ["No", "Yes", "No phone service"]
    )

    internet = st.selectbox(
        "Internet Service Type",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Online Security Add-on",
        ["No", "Yes", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup Service",
        ["No", "Yes", "No internet service"]
    )

    device_protection = st.selectbox(
        "Device Protection Plan",
        ["No", "Yes", "No internet service"]
    )

    tech_support = st.selectbox(
        "Technical Support",
        ["No", "Yes", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["No", "Yes", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["No", "Yes", "No internet service"]
    )

    st.divider()
    st.subheader("💳 Billing Information")

    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless = st.radio(
        "Paperless Billing",
        ["Yes", "No"],
        horizontal=True
    )

    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly = st.slider(
        "Monthly Charges (₹)",
        min_value=0.0,
        max_value=10000.0,
        value=89.0,
        step=10.0
    )

    total = st.slider(
        "Total Charges Paid (₹)",
        min_value=0.0,
        max_value=200000.0,
        value=7500.0,
        step=100.0
    )

    submit = st.form_submit_button("🔍 Predict Churn Risk")

if submit:
    payload = {
        "gender": gender,
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    with st.spinner("Analyzing customer risk..."):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            result = response.json()

            churn_label = result["churn_prediction"]
            churn_prob = round(result["churn_probability"] * 100, 2)

            st.divider()
            st.subheader("📊 Prediction Result")

            if churn_label == 1:
                st.error(f"🚨 High Churn Risk ({churn_prob}%)")
                st.write("⚠️ This customer is **likely to leave** the service.")
            else:
                st.success(f"✅ Low Churn Risk ({churn_prob}%)")
                st.write("👍 This customer is **likely to stay**.")

        except Exception:
            st.error("❌ Unable to connect to prediction service. Please try again later.")
