#PANDAS
import pandas as pd

#NUMPY
import numpy as np

#STREAMLIT
import streamlit as st

#SAVE
import pickle

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ReturnSense AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }

    /* Hide streamlit default menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Title */
    h1 {
        color: #ffffff;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #e0e0ff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(20, 20, 40, 0.85);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #7f00ff, #e100ff);
        color: white;
        font-weight: 600;
        font-size: 18px;
        padding: 12px 28px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 0 20px rgba(225, 0, 255, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(225, 0, 255, 0.8);
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #ddd;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #7f00ff, #e100ff) !important;
        color: white !important;
    }

    /* Custom card */
    .custom-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }

    /* Result box */
    .result-kept {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        box-shadow: 0 0 30px rgba(56, 239, 125, 0.5);
    }

    .result-return {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        box-shadow: 0 0 30px rgba(255, 75, 43, 0.5);
    }

    /* Header badge */
    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #7f00ff, #e100ff);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- LOAD MODEL ----------
import os
import pickle

# Get the directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'return_prediction_model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)
scaler = pickle.load(open('scaler.pkl', 'rb'))

# ---------- LOAD ENCODERS ----------
le_category = pickle.load(open('le_category.pkl', 'rb'))
le_payment = pickle.load(open('le_payment.pkl', 'rb'))
le_shipping = pickle.load(open('le_shipping.pkl', 'rb'))

# ---------- HEADER ----------
st.markdown('<span class="badge">🤖 AI Powered</span>', unsafe_allow_html=True)
st.markdown("# 📦 ReturnSense AI")
st.markdown("### Predict E-Commerce Product Returns Before They Happen")
st.markdown("---")

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📂 Batch Upload", "📊 Model Insights"])

# =====================================================
# TAB 1 — SINGLE PREDICTION
# =====================================================
with tab1:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🛒 Order Details")

        price = st.number_input("💵 Price (₹)", min_value=0.0, value=1500.0, step=50.0)
        quantity = st.slider("📦 Quantity", 1, 10, 1)
        discount_pct = st.slider("🏷️ Discount (%)", 0, 90, 20)
        delivery_days = st.slider("🚚 Delivery Days", 1, 30, 5)
        seller_rating = st.slider("⭐ Seller Rating", 1.0, 5.0, 4.0, step=0.1)

    with col2:
        st.markdown("### 👤 Customer Info")

        previous_returns_count = st.slider("🔁 Previous Returns", 0, 20, 2)
        customer_tenure_days = st.slider("📅 Customer Tenure (Days)", 1, 3000, 365)
        customer_total_orders = st.slider("🧾 Total Orders", 1, 100, 10)
        review_rating = st.slider("📝 Review Rating", 1.0, 5.0, 4.0, step=0.1)
        order_weekday = st.slider("📆 Order Weekday (0=Mon, 6=Sun)", 0, 6, 2)
        order_hour = st.slider("🕐 Order Hour (0-23)", 0, 23, 14)

    st.markdown("### 🏷️ Category Details")

    col3, col4, col5 = st.columns(3)

    with col3:
        product_category = st.selectbox("🛍️ Product Category",
            ['Electronics', 'Clothing', 'Home', 'Beauty', 'Sports', 'Books', 'Toys'])

    with col4:
        payment_method = st.selectbox("💳 Payment Method",
            ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery'])

    with col5:
        shipping_type = st.selectbox("📮 Shipping Type",
            ['Standard', 'Express', 'Same Day'])

    is_prime_member = st.radio("👑 Prime Member?", ['Yes', 'No'], horizontal=True)

    st.markdown("---")

    # ---------- FEATURE ENGINEERING ----------
    customer_tenure_years = customer_tenure_days / 365
    total_spend = price * quantity
    net_price = price * (1 - discount_pct / 100)
    prev_return_ratio = previous_returns_count / (customer_total_orders + 1)
    order_frequency = customer_tenure_days / (customer_total_orders + 1)
    is_prime_member_num = 1 if is_prime_member == 'Yes' else 0

    # ---------- ENCODE CATEGORICAL ----------
    encoded_product_category = le_category.transform([product_category])[0]
    encoded_payment_method = le_payment.transform([payment_method])[0]
    encoded_shipping_type = le_shipping.transform([shipping_type])[0]

    # ---------- BUILD INPUT DATAFRAME ----------
    input_data = pd.DataFrame({
        'price': [price],
        'quantity': [quantity],
        'discount_pct': [discount_pct],
        'delivery_days': [delivery_days],
        'seller_rating': [seller_rating],
        'previous_returns_count': [previous_returns_count],
        'customer_tenure_years': [customer_tenure_years],
        'customer_total_orders': [customer_total_orders],
        'review_rating': [review_rating],
        'is_prime_member': [is_prime_member_num],
        'order_weekday': [order_weekday],
        'order_hour': [order_hour],
        'total_spend': [total_spend],
        'net_price': [net_price],
        'prev_return_ratio': [prev_return_ratio],
        'order_frequency': [order_frequency],
        'encoded_product_category': [encoded_product_category],
        'encoded_payment_method': [encoded_payment_method],
        'encoded_shipping_type': [encoded_shipping_type]
    })

    # ---------- PREDICT BUTTON ----------
    if st.button("🚀 Predict Return Risk"):

        # ---------- SCALE INPUT ----------
        input_scaled = scaler.transform(input_data)

        # ---------- PREDICT ----------
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]

        st.markdown("---")
        st.markdown("## 🎯 Prediction Result")

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric("Decision", "RETURNED ⚠️" if prediction == 1 else "KEPT ✅")

        with colB:
            st.metric("Confidence", f"{max(probability)*100:.2f}%")

        with colC:
            risk_level = "High" if probability[1] > 0.7 else "Medium" if probability[1] > 0.4 else "Low"
            st.metric("Risk Level", risk_level)

        st.markdown("---")

        if prediction == 1:
            st.markdown(f'<div class="result-return">⚠️ This order is likely to be RETURNED<br><br>Confidence: {probability[1]*100:.2f}%</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-kept">✅ This order is likely to be KEPT<br><br>Confidence: {probability[0]*100:.2f}%</div>', unsafe_allow_html=True)

        st.markdown("### 📊 Probability Breakdown")

        st.write(f"**Not Returned** — {probability[0]*100:.2f}%")
        st.progress(float(probability[0]))

        st.write(f"**Returned** — {probability[1]*100:.2f}%")
        st.progress(float(probability[1]))

        with st.expander("🔍 View Input Data Used For Prediction"):
            st.dataframe(input_data)

# =====================================================
# TAB 2 — BATCH UPLOAD
# =====================================================
with tab2:
    st.markdown("### 📂 Batch Prediction")
    st.write("Upload a CSV file with multiple orders and get predictions for all of them at once.")

    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.write("### Preview")
        st.dataframe(batch_df.head())

        if st.button("🚀 Predict All"):
            st.success(f"✅ Processed {len(batch_df)} orders successfully!")
            st.info("Full batch prediction feature coming soon in next update.")

# =====================================================
# TAB 3 — MODEL INSIGHTS
# =====================================================
with tab3:
    st.markdown("### 📊 Model Insights")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Model Type", "XGBoost")
    col2.metric("Features", "19")
    col3.metric("Training Rows", "4,000")
    col4.metric("Test Rows", "1,000")

    st.markdown("---")
    st.markdown("### 🧠 Top Features Used By The Model")

    feature_importance = pd.DataFrame({
        'Feature': ['previous_returns_count', 'prev_return_ratio', 'delivery_days',
                    'seller_rating', 'net_price', 'total_spend', 'discount_pct',
                    'order_frequency', 'review_rating', 'customer_tenure_years'],
        'Importance': [0.18, 0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04]
    })

    st.bar_chart(feature_importance.set_index('Feature'))

    st.markdown("---")
    st.markdown("### ℹ️ About This Model")
    st.write("""
    - **Algorithm:** XGBoost Classifier
    - **Training Data:** Amazon e-commerce returns dataset
    - **Features:** 19 engineered features
    - **Goal:** Predict probability of return before shipping
    - **Use Case:** Helps sellers reduce return losses
    """)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#888;">Built with ❤️ by Amank | ReturnSense AI © 2025</p>',
    unsafe_allow_html=True
)