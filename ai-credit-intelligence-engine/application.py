import streamlit as st
import os
import pandas as pd
import pickle
import numpy as np
import hashlib


# Page Config
# -----------------------------------
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------------
# EARLY FONT & BASE STYLING (must run before show_auth)
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --gold-dim: rgba(201,168,76,0.15);
    --gold-glow: rgba(201,168,76,0.08);
    --bg-deep: #070B14;
    --bg-card: rgba(255,255,255,0.035);
    --border: rgba(201,168,76,0.2);
    --border-bright: rgba(201,168,76,0.5);
    --text-primary: #F0EBE0;
    --text-secondary: #9A9080;
    --text-muted: #5A5448;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'Montserrat', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--text-primary) !important;
}

/* Radio tab styling */
.stRadio > div {
    display: flex !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stRadio > div > label {
    flex: 1 !important;
    text-align: center !important;
    padding: 10px 20px !important;
    border-radius: 9px !important;
    cursor: pointer !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    transition: all 0.3s ease !important;
    border: none !important;
    background: transparent !important;
}
.stRadio > div > label[data-baseweb="radio"] > div:first-child { display: none !important; }

/* Input labels */
label, [data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    font-family: 'Montserrat', sans-serif !important;
    margin-bottom: 8px !important;
}

/* Text inputs */
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    font-family: 'Montserrat', sans-serif !important;
    padding: 14px 18px !important;
    transition: all 0.3s ease !important;
    height: 52px !important;
}
.stTextInput input::placeholder {
    color: var(--text-muted) !important;
    font-style: italic !important;
}
.stTextInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim), 0 0 20px rgba(201,168,76,0.1) !important;
    background: rgba(201,168,76,0.03) !important;
    outline: none !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #C9A84C 0%, #9B7A28 50%, #C9A84C 100%) !important;
    background-size: 200% 200% !important;
    color: #070B14 !important;
    border: none !important;
    border-radius: 12px !important;
    height: 54px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    font-family: 'Montserrat', sans-serif !important;
    box-shadow: 0 4px 30px rgba(201,168,76,0.3), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 40px rgba(201,168,76,0.5), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Alert boxes */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# USER DATABASE FUNCTIONS
# -----------------------------------
USER_FILE = "users.csv"

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    df = load_users()
    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)

def update_password(username, new_password):
    df = load_users()
    df.loc[df["username"] == username, "password"] = hash_password(new_password)
    df.to_csv(USER_FILE, index=False)

# -----------------------------------
# PASSWORD HASHING
# -----------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

import re

def is_valid_username(username):
    return re.match(r"^[a-zA-Z0-9_.]{4,20}$", username)

def is_valid_password(password):
    return (
        len(password) >= 6 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password)
    )

# ---------------- AUTH UI ----------------
def show_auth():
    st.markdown("""
    <style>
    /* Full-page auth background */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse 100% 60% at 50% 0%, rgba(201,168,76,0.07) 0%, transparent 55%),
            radial-gradient(ellipse 50% 30% at 10% 90%, rgba(201,168,76,0.04) 0%, transparent 50%),
            radial-gradient(ellipse 40% 25% at 90% 70%, rgba(201,168,76,0.03) 0%, transparent 50%),
            #070B14 !important;
    }

    /* Top gold accent line */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(201,168,76,0.4) 20%,
            rgba(232,201,122,0.9) 50%,
            rgba(201,168,76,0.4) 80%,
            transparent 100%);
        z-index: 999;
    }

    /* Auth card wrapper */
    .auth-card-wrap {
        display: flex;
        justify-content: center;
        padding: 60px 20px 40px;
    }

    .auth-card {
        width: 100%;
        max-width: 460px;
        background:
            radial-gradient(ellipse 90% 50% at 50% -5%, rgba(201,168,76,0.08) 0%, transparent 55%),
            linear-gradient(170deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.015) 100%);
        border: 1px solid rgba(201,168,76,0.22);
        border-radius: 28px;
        padding: 48px 44px 40px;
        backdrop-filter: blur(30px);
        box-shadow:
            0 0 0 1px rgba(201,168,76,0.06) inset,
            0 50px 100px rgba(0,0,0,0.7),
            0 0 80px rgba(201,168,76,0.04);
        position: relative;
        overflow: hidden;
    }

    /* Top shimmer on card */
    .auth-card::before {
        content: '';
        position: absolute;
        top: 0; left: 8%; right: 8%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(201,168,76,0.9), transparent);
    }

    /* Corner ornaments */
    .c-tl, .c-tr, .c-bl, .c-br {
        position: absolute;
        width: 18px; height: 18px;
        opacity: 0.5;
    }
    .c-tl { top: 14px; left: 14px;
        border-top: 1px solid #C9A84C; border-left: 1px solid #C9A84C; border-radius: 4px 0 0 0; }
    .c-tr { top: 14px; right: 14px;
        border-top: 1px solid #C9A84C; border-right: 1px solid #C9A84C; border-radius: 0 4px 0 0; }
    .c-bl { bottom: 14px; left: 14px;
        border-bottom: 1px solid #C9A84C; border-left: 1px solid #C9A84C; border-radius: 0 0 0 4px; }
    .c-br { bottom: 14px; right: 14px;
        border-bottom: 1px solid #C9A84C; border-right: 1px solid #C9A84C; border-radius: 0 0 4px 0; }

    /* Logo area */
    .auth-logo-wrap { text-align: center; margin-bottom: 30px; }

    .auth-emblem {
        width: 68px; height: 68px;
        border-radius: 20px;
        background: linear-gradient(145deg, rgba(201,168,76,0.18), rgba(201,168,76,0.05));
        border: 1px solid rgba(201,168,76,0.4);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        margin-bottom: 18px;
        box-shadow:
            0 8px 32px rgba(201,168,76,0.2),
            0 0 0 1px rgba(201,168,76,0.08) inset;
    }

    .auth-brand {
        font-family: 'Cormorant Garamond', serif;
        font-size: 36px;
        font-weight: 600;
        color: #F0EBE0;
        letter-spacing: 0.5px;
        line-height: 1;
        margin-bottom: 8px;
    }
    .auth-brand span { color: #C9A84C; }

    .auth-tagline {
        font-family: 'Montserrat', sans-serif;
        font-size: 10px;
        font-weight: 500;
        color: #4A4438;
        letter-spacing: 3.5px;
        text-transform: uppercase;
    }

    /* Divider */
    .auth-divider {
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 24px 0 20px;
    }
    .auth-div-line {
        flex: 1; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(201,168,76,0.25), transparent);
    }
    .auth-div-icon {
        color: rgba(201,168,76,0.45);
        font-size: 9px;
        letter-spacing: 5px;
    }

    /* Secure badge */
    .auth-secure {
        text-align: center;
        margin-top: 22px;
        font-family: 'Montserrat', sans-serif;
        font-size: 9px;
        color: #3A3428;
        letter-spacing: 2.5px;
        text-transform: uppercase;
    }

    /* Ambient orb */
    .auth-orb {
        position: fixed;
        width: 600px; height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(201,168,76,0.03) 0%, transparent 70%);
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        z-index: 0;
    }
    </style>

    <div class="auth-orb"></div>
    <div class="auth-card-wrap">
      <div class="auth-card">
        <div class="c-tl"></div><div class="c-tr"></div>
        <div class="c-bl"></div><div class="c-br"></div>
        <div class="auth-logo-wrap">
          <div class="auth-emblem">🏦</div>
          <div class="auth-brand">Loan<span>Sahayak</span></div>
          <div class="auth-tagline">Smart Loan Intelligence</div>
        </div>
        <div class="auth-divider">
          <div class="auth-div-line"></div>
          <div class="auth-div-icon">✦ ✦ ✦</div>
          <div class="auth-div-line"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Center column for Streamlit widgets
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        choice = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        users  = load_users()

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        if choice == "Login":
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Login", key="login_btn"):
                if username == "" or password == "":
                    st.warning("Please enter both fields.")
                else:
                    user = users[
                        (users["username"] == username) &
                        (users["password"] == hash_password(password))
                    ]
                    if not user.empty:
                        st.session_state.logged_in = True
                        st.session_state.username  = username
                        st.success("Access granted. Welcome back.")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")

        else:
            new_user     = st.text_input("Create Username", placeholder="Choose a username")
            new_pass     = st.text_input("Create Password", placeholder="Create a strong password", type="password")
            confirm_pass = st.text_input("Confirm Password", placeholder="Re-enter your password", type="password")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("Create Account", key="signup_btn"):
                if new_user == "" or new_pass == "":
                    st.warning("All fields are required.")
                elif not is_valid_username(new_user):
                    st.error("Username: 4–20 chars, letters/numbers/_ . only.")
                elif not is_valid_password(new_pass):
                    st.error("Password must include uppercase, lowercase & a number.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif new_user.lower() in users["username"].str.lower().values:
                    st.warning("Username already exists.")
                else:
                    save_user(new_user, hash_password(new_pass))
                    st.success("Account created. Please login.")

        st.markdown("""
        <div style="text-align:center; margin-top:20px;
                    font-family:'Montserrat',sans-serif; font-size:9px;
                    color:#3A3428; letter-spacing:2.5px; text-transform:uppercase;">
            ✦ &nbsp; Secured &amp; Encrypted &nbsp; ✦
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------
# LOGIN CHECK
# -----------------------------------
if not st.session_state.logged_in:
    show_auth()
    st.stop()

st.markdown(f"""
<div style="
    padding: 14px 20px;
    border-radius: 12px;
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.3);
    color: #E8C97A;
    font-size: 16px;
    margin-bottom: 18px;
">
    👋 Welcome !! <b>{st.session_state.username}</b> ..System status: Active. LoanSahayak is ready to transform your data into definitive financial insights
</div>
""", unsafe_allow_html=True)


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

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1200px !important;
}

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
.hero-title span { color: var(--gold); }

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

label, .stSelectbox label, .stNumberInput label,
.stSlider label, [data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
}

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

.stSlider > div > div > div { background: var(--gold) !important; }
.stSlider > div > div > div > div {
    background: var(--gold) !important;
    border: 2px solid var(--bg-deep) !important;
    box-shadow: 0 0 0 2px var(--gold) !important;
}
[data-testid="stSlider"] > div > div { background: rgba(255,255,255,0.07) !important; }

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
.stButton > button:active { transform: translateY(0) !important; }

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color 0.2s !important;
}
[data-testid="metric-container"]:hover { border-color: var(--border-bright) !important; }
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

.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 14px !important;
    border-left-width: 3px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 16px 20px !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
    border-radius: 100px !important;
}
.stProgress > div {
    background: rgba(255,255,255,0.07) !important;
    border-radius: 100px !important;
    height: 8px !important;
}

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

hr { border-color: var(--border) !important; margin: 28px 0 !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

.result-approved {
    padding: 32px 36px; border-radius: 20px;
    border: 1px solid rgba(46,204,113,0.3);
    background: radial-gradient(ellipse at top, rgba(46,204,113,0.06) 0%, transparent 70%), rgba(255,255,255,0.025);
    text-align: center;
}
.result-rejected {
    padding: 32px 36px; border-radius: 20px;
    border: 1px solid rgba(231,76,60,0.3);
    background: radial-gradient(ellipse at top, rgba(231,76,60,0.06) 0%, transparent 70%), rgba(255,255,255,0.025);
    text-align: center;
}
.result-icon { font-size: 48px; margin-bottom: 12px; }
.result-label { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; margin: 0 0 8px; }
.result-sub { font-size: 14px; color: var(--text-secondary); letter-spacing: 0.5px; }
.result-conf { display: inline-block; margin-top: 14px; padding: 6px 20px; border-radius: 100px; font-size: 13px; font-weight: 600; letter-spacing: 1px; }
.conf-approved { background: rgba(46,204,113,0.15); color: #2ECC71; border: 1px solid rgba(46,204,113,0.3); }
.conf-rejected { background: rgba(231,76,60,0.15); color: #E74C3C; border: 1px solid rgba(231,76,60,0.3); }

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

st.sidebar.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.sidebar.columns(3, gap="small")

with col1:
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <a href="https://www.linkedin.com/in/arnav-singh-a87847351" target="_blank">
            <div style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:rgba(78,161,255,0.08);border:1px solid rgba(78,161,255,0.2);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="#4EA1FF">
                <path d="M4.98 3.5C4.98 4.88 3.87 6 2.49 6C1.11 6 0 4.88 0 3.5C0 2.12 1.11 1 2.49 1C3.87 1 4.98 2.12 4.98 3.5ZM0.22 8.98H4.75V24H0.22V8.98ZM7.98 8.98H12.32V11.04H12.38C13.04 9.86 14.66 8.63 17.04 8.63C22.08 8.63 23 11.88 23 16.13V24H18.47V17.21C18.47 15.46 18.44 13.2 16.02 13.2C13.56 13.2 13.18 15.06 13.18 17.08V24H8.65V8.98H7.98Z"/>
                </svg>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <a href="mailto:itsarnav.singh80@gmail.com">
            <div style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:rgba(0,255,150,0.08);border:1px solid rgba(0,255,150,0.25);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="#00FFAA">
                <path d="M2 4C2 2.9 2.9 2 4 2H20C21.1 2 22 2.9 22 4V20C22 21.1 21.1 22 20 22H4C2.9 22 2 21.1 2 20V4ZM4 4V6L12 13L20 6V4L12 11L4 4ZM20 8L12 15L4 8V20H20V8Z"/>
                </svg>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <a href="https://github.com/Arnav-Singh-5080" target="_blank">
            <div style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);">
                <svg height="18" width="18" viewBox="0 0 16 16" fill="#4EA1FF">
                <path d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.6C5.87 15.67 6.02 15.43 6.02 15.23C6.02 15.05 6.01 14.5 6.01 13.88C4 14.26 3.48 12.92 3.32 12.41C3.23 12.16 2.84 11.36 2.5 11.18C2.22 11.03 1.82 10.68 2.49 10.67C3.12 10.66 3.58 11.25 3.73 11.5C4.45 12.71 5.59 12.36 6.05 12.14C6.12 11.62 6.33 11.25 6.56 11.04C4.78 10.84 2.91 10.15 2.91 7.13C2.91 6.27 3.22 5.55 3.73 4.98C3.65 4.78 3.36 3.95 3.81 2.81C3.81 2.81 4.49 2.59 6.01 3.58C6.65 3.4 7.33 3.31 8.01 3.31C8.69 3.31 9.37 3.4 10.01 3.58C11.53 2.58 12.21 2.81 12.21 2.81C12.66 3.95 12.37 4.78 12.29 4.98C12.8 5.55 13.11 6.27 13.11 7.13C13.11 10.16 11.23 10.84 9.45 11.04C9.74 11.29 10 11.77 10 12.54C10 13.64 9.99 14.93 9.99 15.23C9.99 15.43 10.14 15.68 10.54 15.6C13.71 14.53 16 11.54 16 8C16 3.58 12.42 0 8 0Z"/>
                </svg>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="font-size:12px; color:#5A5448; text-align:center;">
⭐ If you like this project, consider starring it on GitHub
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Load Model
# -----------------------------------
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "loan_model.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "..", "models", "scaler.pkl")

try:
    model  = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
except FileNotFoundError:
    st.error("### ⚠️ Model Files Not Found")
    st.info("""
    The required AI models (**loan_model.pkl** and **scaler.pkl**) are missing from the `models/` directory.
    
    **How to fix:**
    1. Place the `.pkl` files in the `models/` folder.
    2. Refer to `docs/setup.md` for detailed instructions.
    """)
    st.stop()

# -----------------------------------
# EMI Calculator
# -----------------------------------
def calculate_emi(principal: float, tenure_months: int, annual_rate: float) -> float:
    """
    Calculate monthly EMI using the standard reducing-balance formula.

    Args:
        principal      : Loan amount in ₹
        tenure_months  : Repayment period in months
        annual_rate    : Annual interest rate as a percentage (e.g. 10 for 10%)

    Returns:
        Monthly EMI in ₹ (0 if principal or tenure is zero)
    """
    if principal == 0 or tenure_months == 0:
        return 0.0
    monthly_rate = annual_rate / 12 / 100
    # Standard EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
          ((1 + monthly_rate) ** tenure_months - 1)
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
    applicant_income   = st.number_input("Applicant Income (₹)", min_value=0, step=1000)
    coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, step=1000)
    loan_amount        = st.number_input("Loan Amount (₹)", min_value=0, step=1000)
    savings            = st.number_input("Savings (₹)", min_value=0, step=1000)

with col2:
    collateral_value = st.number_input("Collateral Value (₹)", min_value=0, step=1000)
    dependents       = st.number_input("Number of Dependents", min_value=0)
    existing_loans   = st.number_input("Existing Active Loans", min_value=0)
    st.markdown('<div class="input-group-gap"></div>', unsafe_allow_html=True)

col3, col4 = st.columns(2, gap="large")
with col3:
    credit_score = st.slider("Credit Score", 300, 900, 650)
with col4:
    loan_term    = st.slider("Loan Term (Months)", 6, 360, 60)

col5, col6_rate = st.columns([1, 1], gap="large")
with col5:
    age = st.slider("Applicant Age", 18, 70, 30)
with col6_rate:
    # Dynamic annual interest rate — replaces all hardcoded 10% references
    annual_interest_rate = st.slider(
        "Annual Interest Rate (%)",
        min_value=5.0,
        max_value=24.0,
        value=10.0,
        step=0.5,
        help="Select the applicable annual interest rate for EMI calculation"
    )

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

bg_col1, bg_col2 = st.columns(2, gap="large")

with bg_col1:
    employment_dict   = {"Unemployed": 0, "Salaried": 1, "Self-Employed": 2}
    employment_status = employment_dict[st.selectbox("Employment Status", list(employment_dict.keys()))]

    property_dict = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
    property_area = property_dict[st.selectbox("Property Area", list(property_dict.keys()))]

    loan_purpose_dict = {"Home Loan": 0, "Car Loan": 1, "Education Loan": 2, "Personal Loan": 3}
    loan_purpose = loan_purpose_dict[st.selectbox("Loan Purpose", list(loan_purpose_dict.keys()))]

with bg_col2:
    education_dict  = {"Not Graduate": 0, "Graduate": 1}
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
    if applicant_income == 0 or loan_amount == 0:
        st.error("⚠ Income and Loan Amount must be greater than zero.")
        st.stop()

    import time
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.enums import TA_CENTER

    progress_bar = st.progress(0)
    status_text  = st.empty()

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

    total_income = applicant_income + coapplicant_income
    # Pass the user-selected annual interest rate — no hardcoded values
    emi       = calculate_emi(loan_amount, loan_term, annual_interest_rate)
    emi_ratio = emi / total_income if total_income > 0 else 0

    with st.expander("📋 Application Summary"):
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Household Income", f"₹{total_income:,}")
        s2.metric("Loan Amount Requested",  f"₹{loan_amount:,}")
        s3.metric("Credit Score", credit_score)

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

    scaled_data   = scaler.transform(input_data)
    prediction    = model.predict(scaled_data)
    probability   = model.predict_proba(scaled_data)
    approval_prob = probability[0][1] * 100

    st.markdown("---")

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">Financial Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    mA, mB, mC, mD = st.columns(4)
    mA.metric("Monthly EMI",          f"₹ {round(emi, 2):,}")
    mB.metric("Total Monthly Income", f"₹ {total_income:,}")
    mC.metric("EMI / Income Ratio",   f"{round(emi_ratio * 100, 2)} %")
    mD.metric("Annual Interest Rate", f"{annual_interest_rate} %")

    st.markdown("---")
    st.progress(int(approval_prob))
    st.markdown(f"**Approval Probability: {round(approval_prob,1)}%**")
    st.markdown("<br>", unsafe_allow_html=True)

    if emi_ratio > 0.5:
        st.warning("⚠ High EMI ratio")
    elif credit_score < 600:
        st.warning("⚠ Low credit score")
    else:
        st.info("✓ Stable profile")

    decision_text = "APPROVED" if prediction[0] == 1 else "REJECTED"

    if prediction[0] == 1:
        st.success(f"✓ Loan Approved (Confidence: {round(approval_prob,2)}%)")
    else:
        st.error(f"✕ Loan Rejected (Confidence: {round(100-approval_prob,2)}%)")

        reasons = []
        if total_income < 25000:
            reasons.append("Total household income is below the recommended threshold (Rs.25,000).")
        if emi_ratio > 0.5:
            reasons.append("EMI to income ratio is too high (greater than 50%).")
        if credit_score < 600:
            reasons.append("Credit score is below the acceptable limit (600).")
        if existing_loans > 3:
            reasons.append("Too many active loans already.")
        if collateral_value < loan_amount * 0.5:
            reasons.append("Collateral value is insufficient for the requested loan.")

        if len(reasons) > 0:
            st.markdown("""
    <div class="section-header">
        <div class="section-icon">⚠️</div>
        <div class="section-title">Possible Reasons for Rejection</div>
        <div class="section-desc">Key Risk Factors</div>
    </div>
    """, unsafe_allow_html=True)
            for reason in reasons:
                st.write(f"• {reason}")
        else:
            st.write("The application does not meet the Bank approval criteria.")

    # -----------------------------------
    # PREMIUM PDF REPORT
    # -----------------------------------
    import io
    pdf_buffer = io.BytesIO()
    doc    = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title', parent=styles['Title'],
        alignment=TA_CENTER, textColor=colors.HexColor("#C9A84C")
    )
    section_style = ParagraphStyle(
        name='Heading', parent=styles['Heading2'],
        textColor=colors.HexColor("#3B82F6")
    )

    content = []
    content.append(Paragraph("LoanSahayak", title_style))
    content.append(Spacer(1, 6))
    content.append(Paragraph("AI Loan Analysis Report", styles["Italic"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph("Financial Summary", section_style))
    content.append(Spacer(1, 10))

    table = Table([
        ["Metric",              "Value"],
        ["Total Income",        f"Rs. {total_income:,}"],
        ["Loan Amount",         f"Rs. {loan_amount:,}"],
        ["Loan Term",           f"{loan_term} months"],
        ["Annual Interest Rate", f"{annual_interest_rate} %"],
        ["Monthly EMI",         f"Rs. {round(emi, 2):,}"]
    ])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#C9A84C")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    content.append(table)
    content.append(Spacer(1, 20))
    content.append(Paragraph("Credit Profile", section_style))
    content.append(Spacer(1, 10))

    table2 = Table([
        ["Credit Score",   credit_score],
        ["Dependents",     dependents],
        ["Existing Loans", existing_loans]
    ])
    table2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    content.append(table2)
    content.append(Spacer(1, 20))

    color_dec = colors.green if prediction[0] == 1 else colors.red
    decision_style = ParagraphStyle(
        name='Decision', parent=styles['Heading1'],
        alignment=TA_CENTER, textColor=color_dec
    )
    content.append(Paragraph(decision_text, decision_style))
    content.append(Spacer(1, 10))

    confidence = round(approval_prob, 2) if prediction[0] == 1 else round(100 - approval_prob, 2)
    label      = "Approval Confidence" if prediction[0] == 1 else "Rejection Confidence"
    content.append(Paragraph(f"{label}: {confidence}%", styles["Normal"]))
    content.append(Spacer(1, 20))

    if prediction[0] == 0 and reasons:
        content.append(Paragraph("Reasons for Rejection", section_style))
        content.append(Spacer(1, 10))
        for r in reasons:
            content.append(Paragraph(f"• {r}", styles["Normal"]))
        content.append(Spacer(1, 20))

    content.append(Paragraph("Generated by LoanSahayak AI", styles["Italic"]))
    doc.build(content)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name="LoanSahayak_Report.pdf",
        mime="application/pdf"
    )


st.markdown("""
<style>

/* your old css */


/* =========================================
   TEXT VISIBILITY ENHANCEMENT
========================================= */

/* Section descriptions */
.section-desc {
    color: #B8AE9D !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 1.2px !important;
}

/* All labels */
label,
.stSelectbox label,
.stNumberInput label,
.stSlider label,
[data-testid="stWidgetLabel"] {
    color: #D8D2C5 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 1px !important;
}

/* Selectbox selected value */
.stSelectbox div[data-baseweb="select"] span {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* Dropdown text */
.stSelectbox div[data-baseweb="select"] {
    color: #FFFFFF !important;
}

/* Dropdown background */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
}

/* Section titles */
.section-title {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Footer visibility */
.footer-text {
    color: #9E9586 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* Footer gold text */
.footer-highlight {
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("""
<div style="
    margin-top: 100px;
    padding: 28px 32px;
    border-radius: 16px;
    border: 1px solid rgba(201,168,76,0.12);
    background: rgba(255,255,255,0.02);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    letter-spacing: 1px;
    color: #5A5448;">
    <div>© 2026 <span style='color:#C9A84C;'>LoanSahayak</span> — All Rights Reserved</div>
    <div style='text-transform:uppercase; letter-spacing:2px;'>AI · Credit · Intelligence</div>
</div>
""", unsafe_allow_html=True)
