import streamlit as st
import pandas as pd
import numpy as np
import re
from scipy import stats
from datetime import datetime, timedelta

# --- 1. LOS SANTOS DATA ENGINE ---
@st.cache_data
def generate_gta_telemetry(n=10000):
    np.random.seed(42)
    start_date = datetime(2026, 1, 1)
    dates = [start_date + timedelta(seconds=np.random.randint(0, 3888000)) for _ in range(n)]
    archetypes = ['Grinder', 'Griefer', 'Casual', 'Whale', 'Modder']
    platforms = ['PC', 'PS5', 'Xbox Series X']
    logs = ["Successful Cayo Perico Heist", "Purchased Oppressor MKII", "Suspicious Mod-Menu Activity", "Shark Card Bundle Purchased"]
    
    df = pd.DataFrame({
        'Player_ID': [f"USER_{i:06d}" for i in range(n)],
        'Timestamp': dates,
        'Platform': np.random.choice(platforms, n),
        'Archetype': np.random.choice(archetypes, n, p=[0.4, 0.15, 0.3, 0.1, 0.05]),
        'K/D_Ratio': np.random.lognormal(mean=0.2, sigma=0.8, size=n),
        'Citizen_Kills': np.random.poisson(lam=5, size=n),
        'Bank_Balance_GTA$': np.random.lognormal(mean=14, sigma=2.5, size=n),
        'Shark_Card_Spend': np.random.exponential(scale=50, size=n),
        'Action_Log': np.random.choice(logs, n)
    })
    df['Toxicity_Z'] = stats.zscore(df['K/D_Ratio'] + df['Citizen_Kills'])
    df['Lead_Digit'] = df['Bank_Balance_GTA$'].apply(lambda x: int(str(int(x))[0]) if x > 0 else 0)
    df['Behavior_Flag'] = df['Action_Log'].apply(lambda x: 1 if "Mod" in x else 0)
    df['Hour'] = df['Timestamp'].dt.hour
    return df

df = generate_gta_telemetry()

# --- 2. THE ULTIMATE GTA AESTHETIC ---
st.set_page_config(page_title="LOS SANTOS INTEL", layout="wide")

# Using a high-quality GTA V themed background with a dark overlay
BG_IMG = "https://images.alphacoders.com/463/463838.jpg" 

st.markdown(f"""
    <style>
    /* Background Image with Dark Overlay */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("{BG_IMG}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* GTA Title Font Style */
    .gta-title {{
        font-family: 'Arial Black', sans-serif;
        color: white;
        text-transform: uppercase;
        letter-spacing: -2px;
        font-size: 3.5rem;
        text-shadow: 3px 3px #000000;
        border-left: 10px solid #FF9D00;
        padding-left: 20px;
        margin-bottom: 30px;
    }}

    /* Styling the Sidebar to look like a HUD menu */
    section[data-testid="stSidebar"] {{
        background-color: rgba(15, 15, 15, 0.95) !important;
        border-right: 2px solid #FF9D00;
    }}

    /* Metric Cards */
    [data-testid="stMetricValue"] {{
        color: #FF9D00 !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }}
    
    /* Custom Info Button Style */
    .stPopover button {{
        background-color: #FF9D00 !important;
        color: black !important;
        border-radius: 0px !important;
        font-weight: bold !important;
        text-transform: uppercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR WITH LOGO FIX ---
with st.sidebar:
    # Reliable logo link (PNG instead of SVG for better compatibility)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Grand_Theft_Auto_V_logo.svg/1200px-Grand_Theft_Auto_V_logo.svg.png", use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #FF9D00;'>ADMIN CONSOLE</h2>", unsafe_allow_html=True)
    
    selected_platform = st.multiselect("NETWORK PLATFORM", df['Platform'].unique(), default=df['Platform'].unique())
    selected_archetype = st.multiselect("BEHAVIORAL PROFILE", df['Archetype'].unique(), default=df['Archetype'].unique())
    
    st.divider()
    ban_sensitivity = st.slider("DETECTION SENSITIVITY", 1.5, 5.0, 3.0)
    shark_card_min = st.number_input("MIN SHARK SPEND ($)", 0, 1000, 0)

# Filter Logic
f_df = df[(df['Platform'].isin(selected_platform)) & (df['Archetype'].isin(selected_archetype)) & (df['Shark_Card_Spend'] >= shark_card_min)]

# --- 4. THE INTERFACE ---
st.markdown('<div class="gta-title">SECURE <span style="color:#FF9D00">SERV</span> TERMINAL</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("SESSIONS", len(f_df))
    st.popover("HUD Info").write("Live connection count across Los Santos servers.")
with m2:
    st.metric("AVG K/D", round(f_df['K/D_Ratio'].mean(), 2))
    st.popover("Combat Info").write("The average aggressiveness of the current lobby.")
with m3:
    flagged = f_df[f_df['Toxicity_Z'] > ban_sensitivity]
    st.metric("THREATS", len(flagged), delta=f"{len(flagged)} Flagged", delta_color="inverse")
    st.popover("Security Info").write("Users identified as Griefers or Modders based on Z-Score variance.")
with m4:
    vol = f_df['Bank_Balance_GTA$'].sum() / 1e9
    st.metric("ECONOMY", f"${vol:.1f}B")
    st.popover("Cash Info").write("Total circulating GTA Dollars in this sector.")

st.markdown("---")

# Visuals
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("🏦 ANTI-CHEAT: MONEY DISTRO")
    st.popover("Methodology").write("Detecting non-organic currency spikes (Glitching).")
    benford = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(benford, color="#FF9D00")

with col_b:
    st.subheader("🌙 PEAK CRIME HOURS")
    st.popover("Methodology").write("Correlating time of day with mod-menu usage spikes.")
    st.line_chart(f_df.groupby('Hour').size(), color="#FFFFFF")
