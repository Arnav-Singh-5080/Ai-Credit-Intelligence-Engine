import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------------
# Premium UI Styling — Luxury Finance Aesthetic
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --gold-dim: rgba(201,168,76,0.15);
    --bg-deep: #070B14;
    --bg-card: rgba(255,255,255,0.035);
    --bg-card-hover: rgba(255,255,255,0.06);
    --border: rgba(201,168,76,0.2);
    --border-bright: rgba(201,168,76,0.5);
    --text-primary: #F0EBE0;
    --text-secondary: #9A9080;
    --text-muted: #5A5448;
    --success: #2ECC71;
    --danger: #E74C3C;
    --blue-accent: #3B82F6;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Noise texture overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* Main content wrapper */
.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1200px !important;
}

/* ── Hero ── */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 72px 40px 60px;
    border-radius: 24px;
    border: 1px solid var(--border);
    background:
        radial-gradient(ellipse 80% 60% at 50% 0%, rgba(201,168,76,0.08) 0%, transparent 70%),
        linear-gradient(180deg, #0C1525 0%, #070B14 100%);
    overflow: hidden;
    margin-bottom: 8px;
}

.hero-wrap::after {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

.hero-badge {
    display: inline-block;
    padding: 6px 18px;
    border: 1px solid var(--border-bright);
    border-radius: 100px;
    font-size: 11px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--gold);
    background: var(--gold-dim);
    margin-bottom: 24px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}

.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 56px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 0 16px !important;
    line-height: 1.1 !important;
    letter-spacing: -0.5px;
}

.hero-title span {
    color: var(--gold);
}

.hero-sub {
    font-size: 17px;
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.3px;
    max-width: 520px;
    margin: 0 auto 28px;
    line-height: 1.7;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin-top: 36px;
    padding-top: 28px;
    border-top: 1px solid var(--border);
}

.hero-stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 600;
    color: var(--gold-light);
}

.hero-stat-label {
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 36px 0 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
}

.section-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: var(--gold-dim);
    border: 1px solid var(--border-bright);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}

.section-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}

.section-desc {
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-left: auto;
}

/* ── Input labels ── */
label, .stSelectbox label, .stNumberInput label,
.stSlider label, [data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
}

/* ── Text inputs & number inputs ── */
input[type="number"], .stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 10px 14px !important;
    font-size: 15px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}

input[type="number"]:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
    outline: none !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}

/* ── Sliders ── */
.stSlider > div > div > div {
    background: var(--gold) !important;
}

.stSlider > div > div > div > div {
    background: var(--gold) !important;
    border: 2px solid var(--bg-deep) !important;
    box-shadow: 0 0 0 2px var(--gold) !important;
}

/* slider track bg */
[data-testid="stSlider"] > div > div {
    background: rgba(255,255,255,0.07) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%) !important;
    color: #070B14 !important;
    border: none !important;
    border-radius: 12px !important;
    height: 54px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(201,168,76,0.25) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(201,168,76,0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color 0.2s !important;
}

[data-testid="metric-container"]:hover {
    border-color: var(--border-bright) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 26px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
}

.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── Alert boxes ── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 14px !important;
    border-left-width: 3px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 16px 20px !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
    border-radius: 100px !important;
}

.stProgress > div {
    background: rgba(255,255,255,0.07) !important;
    border-radius: 100px !important;
    height: 8px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #070B14 !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
    font-family: 'Playfair Display', serif !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 28px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ── Result card ── */
.result-approved {
    padding: 32px 36px;
    border-radius: 20px;
    border: 1px solid rgba(46,204,113,0.3);
    background: radial-gradient(ellipse at top, rgba(46,204,113,0.06) 0%, transparent 70%),
                rgba(255,255,255,0.025);
    text-align: center;
}

.result-rejected {
    padding: 32px 36px;
    border-radius: 20px;
    border: 1px solid rgba(231,76,60,0.3);
    background: radial-gradient(ellipse at top, rgba(231,76,60,0.06) 0%, transparent 70%),
                rgba(255,255,255,0.025);
    text-align: center;
}

.result-icon { font-size: 48px; margin-bottom: 12px; }
.result-label {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 700;
    margin: 0 0 8px;
}
.result-sub { font-size: 14px; color: var(--text-secondary); letter-spacing: 0.5px; }
.result-conf {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 20px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
}
.conf-approved { background: rgba(46,204,113,0.15); color: #2ECC71; border: 1px solid rgba(46,204,113,0.3); }
.conf-rejected { background: rgba(231,76,60,0.15); color: #E74C3C; border: 1px solid rgba(231,76,60,0.3); }

/* ── Input group divider ── */
.input-group-gap { margin-top: 8px; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HERO HEADER
# -----------------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">✦ AI-Powered Lending Intelligence</div>
    <div class="hero-title">Loan<span>Sahayak</span></div>
    <div class="hero-sub">
        Sophisticated credit analysis and risk assessment — engineered for modern lending decisions.
    </div>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">83.4%</div>
            <div class="hero-stat-label">Accuracy</div>
        </div>
        <div>
            <div class="hero-stat-val">&lt; 2s</div>
            <div class="hero-stat-label">Decision Time</div>
        </div>
        <div>
            <div class="hero-stat-val">16+</div>
            <div class="hero-stat-label">Risk Factors</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Sidebar
# -----------------------------------
# -----------------------------------
# Sidebar (Premium – Same Font Style)
# -----------------------------------
st.sidebar.markdown("""
<div style="padding: 8px 0 20px; border-bottom: 1px solid rgba(201,168,76,0.2); margin-bottom: 20px;">
    <div style="font-family: 'Playfair Display', serif; font-size: 22px; color: #F0EBE0; font-weight: 700;">
        LoanSahayak
    </div>
    <div style="font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #9A9080; margin-top: 4px;">
        Smart Loan Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# System Info (Improved readability)
st.sidebar.markdown("""
<div style="
    padding:16px;
    border-radius:14px;
    background: rgba(59,130,246,0.08);
    border:1px solid rgba(59,130,246,0.2);
    color:#9CCBFF;
    font-size:14px;
    line-height:1.6;
">
AI-powered system that evaluates loan applications using:<br>
• Financial indicators<br>
• Credit score analysis<br>
• Multi-factor risk assessment
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Trust Indicators (NEW 🔥)
st.sidebar.markdown("""
<div style="font-size:12px; color:#9A9080; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px;">
System Stats
</div>
<div style="font-size:14px; color:#F0EBE0; line-height:1.8;">
✔ Accuracy: <span style="color:#C9A84C;">83.4%</span><br>
✔ Decision Time: <span style="color:#C9A84C;">&lt; 2s</span><br>
✔ Risk Factors: <span style="color:#C9A84C;">16+</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Author Section (Refined)
st.sidebar.markdown("""
<div style="font-family:'Playfair Display', serif; font-size:20px; color:#F0EBE0; font-weight:600;">
👤 Project Author
</div>

<div style="margin-top:10px; font-size:16px; color:#F0EBE0; font-weight:500;">
Arnav Singh
</div>

<div style="font-size:13px; color:#9A9080; margin-top:4px;">
Machine Learning Enthusiast | Aspiring Data Scientist
</div>
""", unsafe_allow_html=True)

# Clean Links (Same Font – No Buttons ❌)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.sidebar.columns(3, gap="small")

# LinkedIn
with col1:
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <a href="https://www.linkedin.com/in/arnav-singh-a87847351" target="_blank">
            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                width:40px;
                height:40px;
                border-radius:12px;
                background:rgba(78,161,255,0.08);
                border:1px solid rgba(78,161,255,0.2);
            ">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="#4EA1FF">
                <path d="M4.98 3.5C4.98 4.88 3.87 6 2.49 6C1.11 6 0 4.88 0 3.5C0 2.12 1.11 1 2.49 1C3.87 1 4.98 2.12 4.98 3.5ZM0.22 8.98H4.75V24H0.22V8.98ZM7.98 8.98H12.32V11.04H12.38C13.04 9.86 14.66 8.63 17.04 8.63C22.08 8.63 23 11.88 23 16.13V24H18.47V17.21C18.47 15.46 18.44 13.2 16.02 13.2C13.56 13.2 13.18 15.06 13.18 17.08V24H8.65V8.98H7.98Z"/>
                </svg>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Email (CENTER)
with col2:
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <a href="mailto:itsarnav.singh80@gmail.com">
            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                width:40px;
                height:40px;
                border-radius:12px;
                background:rgba(0,255,150,0.08);
                border:1px solid rgba(0,255,150,0.25);
            ">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="#00FFAA">
                <path d="M2 4C2 2.9 2.9 2 4 2H20C21.1 2 22 2.9 22 4V20C22 21.1 21.1 22 20 22H4C2.9 22 2 21.1 2 20V4ZM4 4V6L12 13L20 6V4L12 11L4 4ZM20 8L12 15L4 8V20H20V8Z"/>
                </svg>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# GitHub
with col3:
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <a href="https://github.com/Arnav-Singh-5080" target="_blank">
            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                width:40px;
                height:40px;
                border-radius:12px;
                background:rgba(255,255,255,0.05);
                border:1px solid rgba(255,255,255,0.15);
            ">
                <svg height="18" width="18" viewBox="0 0 16 16" fill="#4EA1FF">
                <path d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.6C5.87 15.67 6.02 15.43 6.02 15.23C6.02 15.05 6.01 14.5 6.01 13.88C4 14.26 3.48 12.92 3.32 12.41C3.23 12.16 2.84 11.36 2.5 11.18C2.22 11.03 1.82 10.68 2.49 10.67C3.12 10.66 3.58 11.25 3.73 11.5C4.45 12.71 5.59 12.36 6.05 12.14C6.12 11.62 6.33 11.25 6.56 11.04C4.78 10.84 2.91 10.15 2.91 7.13C2.91 6.27 3.22 5.55 3.73 4.98C3.65 4.78 3.36 3.95 3.81 2.81C3.81 2.81 4.49 2.59 6.01 3.58C6.65 3.4 7.33 3.31 8.01 3.31C8.69 3.31 9.37 3.4 10.01 3.58C11.53 2.58 12.21 2.81 12.21 2.81C12.66 3.95 12.37 4.78 12.29 4.98C12.8 5.55 13.11 6.27 13.11 7.13C13.11 10.16 11.23 10.84 9.45 11.04C9.74 11.29 10 11.77 10 12.54C10 13.64 9.99 14.93 9.99 15.23C9.99 15.43 10.14 15.68 10.54 15.6C13.71 14.53 16 11.54 16 8C16 3.58 12.42 0 8 0Z"/>
                </svg>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Optional CTA
st.sidebar.markdown("""
<div style="font-size:12px; color:#5A5448; text-align:center;">
⭐ If you like this project, consider starring it on GitHub
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Load Model
# -----------------------------------
model = pickle.load(open("models/loan_model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# -----------------------------------
# EMI Calculator
# -----------------------------------
def calculate_emi(principal, tenure_months, annual_rate=10):
    if principal == 0 or tenure_months == 0:
        return 0
    monthly_rate = annual_rate / 12 / 100
    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / \
          ((1 + monthly_rate)**tenure_months - 1)
    return emi

# -----------------------------------
# Section: Financial Details
# -----------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-icon">💼</div>
    <div class="section-title">Financial Profile</div>
    <div class="section-desc">Income & Loan Details</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    applicant_income    = st.number_input("Applicant Income (₹)", min_value=0, step=1000)
    coapplicant_income  = st.number_input("Coapplicant Income (₹)", min_value=0, step=1000)
    loan_amount         = st.number_input("Loan Amount (₹)", min_value=0, step=1000)
    savings             = st.number_input("Savings (₹)", min_value=0, step=1000)

with col2:
    collateral_value    = st.number_input("Collateral Value (₹)", min_value=0, step=1000)
    dependents          = st.number_input("Number of Dependents", min_value=0)
    existing_loans      = st.number_input("Existing Active Loans", min_value=0)
    st.markdown('<div class="input-group-gap"></div>', unsafe_allow_html=True)

col3, col4 = st.columns(2, gap="large")
with col3:
    credit_score = st.slider("Credit Score", 300, 900, 650)
with col4:
    loan_term    = st.slider("Loan Term (Months)", 6, 360, 60)

col5, _ = st.columns([1, 1], gap="large")
with col5:
    age = st.slider("Applicant Age", 18, 70, 30)

# -----------------------------------
# Section: Background Details
# -----------------------------------
st.markdown("""
<div class="section-header" style="margin-top: 44px;">
    <div class="section-icon">👤</div>
    <div class="section-title">Applicant Background</div>
    <div class="section-desc">Demographic & Employment</div>
</div>
""", unsafe_allow_html=True)

col6, col7 = st.columns(2, gap="large")

with col6:
    employment_dict = {"Unemployed": 0, "Salaried": 1, "Self-Employed": 2}
    employment_status = employment_dict[st.selectbox("Employment Status", list(employment_dict.keys()))]

    property_dict = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
    property_area = property_dict[st.selectbox("Property Area", list(property_dict.keys()))]

    loan_purpose_dict = {"Home Loan": 0, "Car Loan": 1, "Education Loan": 2, "Personal Loan": 3}
    loan_purpose = loan_purpose_dict[st.selectbox("Loan Purpose", list(loan_purpose_dict.keys()))]

with col7:
    education_dict = {"Not Graduate": 0, "Graduate": 1}
    education_level = education_dict[st.selectbox("Education Level", list(education_dict.keys()))]

    gender_dict = {"Female": 0, "Male": 1}
    gender = gender_dict[st.selectbox("Gender", list(gender_dict.keys()))]

    employer_category_dict = {"Private Sector": 0, "Government": 1, "Business Owner": 2}
    employer_category = employer_category_dict[st.selectbox("Employer Category", list(employer_category_dict.keys()))]

# -----------------------------------
# Analyse Button
# -----------------------------------
st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
col_btn, _, _ = st.columns([1.2, 1, 1])
with col_btn:
    run = st.button("⬡  Analyse Loan Application")

# -----------------------------------
# Prediction
# -----------------------------------
if run:
    import time
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.enums import TA_CENTER

    progress_bar = st.progress(0)
    status_text = st.empty()

    # AI processing animation
    steps = [
        "🔍 Collecting financial data...",
        "📊 Analyzing income & liabilities...",
        "🧠 Running ML model inference...",
        "⚖️ Evaluating risk parameters...",
        "✅ Finalizing decision..."
    ]

    for i, step in enumerate(steps):
        status_text.markdown(f"<span style='color:#C9A84C;'>{step}</span>", unsafe_allow_html=True)
        progress_bar.progress((i + 1) * 20)
        time.sleep(0.4)

    status_text.empty()
    progress_bar.empty()

    # ---------------- MAIN LOGIC ----------------
    total_income = applicant_income + coapplicant_income
    emi = calculate_emi(loan_amount, loan_term)
    emi_ratio = emi / total_income if total_income > 0 else 0

    # Summary
    with st.expander("📋 Application Summary"):
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Household Income", f"₹{total_income:,}")
        s2.metric("Loan Amount Requested", f"₹{loan_amount:,}")
        s3.metric("Credit Score", credit_score)

    # Prediction
    input_data = pd.DataFrame([[
        applicant_income, coapplicant_income, loan_amount, credit_score,
        age, dependents, existing_loans, savings, collateral_value,
        loan_term, employment_status, property_area, loan_purpose,
        education_level, gender, employer_category
    ]], columns=[
        'Applicant_Income','Coapplicant_Income','Loan_Amount','Credit_Score',
        'Age','Dependents','Existing_Loans','Savings','Collateral_Value',
        'Loan_Term','Employment_Status','Property_Area','Loan_Purpose',
        'Education_Level','Gender','Employer_Category'
    ])

    scaled_data  = scaler.transform(input_data)
    prediction   = model.predict(scaled_data)
    probability  = model.predict_proba(scaled_data)
    approval_prob = probability[0][1] * 100

    # Divider
    st.markdown("---")

    # Financial Analysis
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">Financial Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    mA, mB, mC = st.columns(3)
    mA.metric("Monthly EMI", f"₹ {round(emi, 2):,}")
    mB.metric("Total Monthly Income", f"₹ {total_income:,}")
    mC.metric("EMI / Income Ratio", f"{round(emi_ratio * 100, 2)} %")

    # AI Confidence
    st.markdown("---")
    st.progress(int(approval_prob))
    st.markdown(f"**Approval Probability: {round(approval_prob,1)}%**")

    st.markdown("<br>", unsafe_allow_html=True)

    # Decision UI
    decision_text = "APPROVED" if prediction[0] == 1 else "REJECTED"

    if prediction[0] == 1:
        st.success(f"✓ Loan Approved (Confidence: {round(approval_prob,2)}%)")
    else:
        st.error(f"✕ Loan Rejected (Confidence: {round(100-approval_prob,2)}%)")

    # Risk
    if emi_ratio > 0.5:
        st.warning("⚠ High EMI ratio")
    elif credit_score < 600:
        st.warning("⚠ Low credit score")
    else:
        st.info("✓ Stable profile")

    # -----------------------------------
    # PREMIUM PDF REPORT
    # -----------------------------------
    pdf_path = "loan_report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#C9A84C")
    )

    section_style = ParagraphStyle(
        name='Heading',
        parent=styles['Heading2'],
        textColor=colors.HexColor("#3B82F6")
    )

    content = []

    # Header
    content.append(Paragraph("LoanSahayak", title_style))
    content.append(Spacer(1, 6))
    content.append(Paragraph("AI Loan Analysis Report", styles["Italic"]))
    content.append(Spacer(1, 20))

    # Financial Table
    content.append(Paragraph("Financial Summary", section_style))
    content.append(Spacer(1, 10))

    table = Table([
        ["Metric", "Value"],
        ["Total Income", f"₹ {total_income:,}"],
        ["Loan Amount", f"₹ {loan_amount:,}"],
        ["Loan Term", f"{loan_term} months"],
        ["EMI", f"₹ {round(emi,2)}"]
    ])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#C9A84C")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    # Credit Table
    content.append(Paragraph("Credit Profile", section_style))
    content.append(Spacer(1, 10))

    table2 = Table([
        ["Credit Score", credit_score],
        ["Dependents", dependents],
        ["Existing Loans", existing_loans]
    ])

    table2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))

    content.append(table2)
    content.append(Spacer(1, 20))

    # Decision
    color = colors.green if prediction[0] == 1 else colors.red
    decision_style = ParagraphStyle(
        name='Decision',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        textColor=color
    )

    content.append(Paragraph(decision_text, decision_style))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Confidence: {round(approval_prob,2)}%", styles["Normal"]))

    content.append(Spacer(1, 20))
    content.append(Paragraph("Generated by LoanSahayak AI", styles["Italic"]))

    doc.build(content)

    # Download Button
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Download Premium PDF Report",
            data=f,
            file_name="LoanSahayak_Report.pdf",
            mime="application/pdf"
        )

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
.footer-container {
    margin-top: 100px;
    padding: 40px 32px;
    border-radius: 16px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-primary);
    font-family: 'DM Sans', sans-serif;
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 40px;
}

.footer-section {
    flex: 1;
    min-width: 200px;
}

.footer-section h4 {
    color: var(--gold);
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-links li {
    margin-bottom: 8px;
}

.footer-links a {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 14px;
    transition: all 0.3s ease;
}

.footer-links a:hover {
    color: var(--gold);
    transform: translateX(5px);
}

.social-icons {
    display: flex;
    gap: 16px;
}

.social-icons a {
    color: var(--text-secondary);
    font-size: 24px;
    transition: all 0.3s ease;
}

.social-icons a:hover {
    color: var(--gold);
    transform: scale(1.1);
}

.author-section {
    text-align: center;
}

.author-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 2px solid var(--gold);
    margin-bottom: 12px;
}

.author-name {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.author-role {
    color: var(--text-secondary);
    font-size: 14px;
}

.copyright {
    text-align: center;
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 12px;
}

.copyright span {
    color: var(--gold);
}
</style>

<div class="footer-container">
    <div class="footer-content">
        <div class="footer-section">
            <h4>Quick Links</h4>
            <ul class="footer-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="https://github.com/Arnav-Singh-5080/Ai-Credit-Intelligence-Engine" target="_blank">GitHub</a></li>
            </ul>
        </div>
        <div class="footer-section">
            <h4>Connect</h4>
            <div class="social-icons">
                <a href="https://github.com/Arnav-Singh-5080" target="_blank"><i class="fab fa-github"></i></a>
                <a href="#" target="_blank"><i class="fab fa-linkedin"></i></a>
                <a href="#" target="_blank"><i class="fab fa-twitter"></i></a>
            </div>
        </div>
        <div class="footer-section author-section">
            <h4>Project Author</h4>
            <img src="https://via.placeholder.com/60" alt="Author Avatar" class="author-avatar">
            <div class="author-name">Arnav Singh</div>
            <div class="author-role">AI Developer & Data Scientist</div>
        </div>
    </div>
    <div class="copyright">
        © 2026 <span>LoanSahayak</span> — All Rights Reserved | AI · Credit · Intelligence
    </div>
</div>
""", unsafe_allow_html=True)
