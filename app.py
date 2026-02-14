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

# --- 2. ENHANCED GTA V AESTHETIC ---
st.set_page_config(page_title="LOS SANTOS INTEL", layout="wide")

# Multiple GTA V themed backgrounds for variety
BG_IMG = "https://images6.alphacoders.com/337/337346.jpg"  # Night city skyline

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pricedown&family=Bebas+Neue&family=Roboto+Condensed:wght@700&display=swap');
    
    /* Background with animated overlay */
    .stApp {{
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.75) 0%, rgba(20, 5, 0, 0.85) 50%, rgba(0, 0, 0, 0.9) 100%), 
                    url("{BG_IMG}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        animation: subtlePulse 10s ease-in-out infinite;
    }}
    
    @keyframes subtlePulse {{
        0%, 100% {{ background-position: center; }}
        50% {{ background-position: center top; }}
    }}
    
    /* GTA V Authentic Title Font */
    .gta-title {{
        font-family: 'Pricedown', 'Impact', sans-serif;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: -3px;
        font-size: 4.5rem;
        text-shadow: 
            4px 4px 0px #000000,
            8px 8px 0px rgba(0, 0, 0, 0.5),
            2px 2px 20px rgba(255, 157, 0, 0.6);
        border-left: 15px solid #4ECB71;
        border-bottom: 3px solid #4ECB71;
        padding-left: 25px;
        padding-bottom: 15px;
        margin-bottom: 40px;
        background: linear-gradient(90deg, rgba(78, 203, 113, 0.1) 0%, transparent 50%);
        animation: glowPulse 3s ease-in-out infinite;
    }}
    
    @keyframes glowPulse {{
        0%, 100% {{ 
            text-shadow: 
                4px 4px 0px #000000,
                8px 8px 0px rgba(0, 0, 0, 0.5),
                2px 2px 20px rgba(255, 157, 0, 0.6);
        }}
        50% {{ 
            text-shadow: 
                4px 4px 0px #000000,
                8px 8px 0px rgba(0, 0, 0, 0.5),
                2px 2px 30px rgba(255, 157, 0, 0.9),
                0px 0px 40px rgba(78, 203, 113, 0.5);
        }}
    }}
    
    .gta-serv {{
        color: #4ECB71;
        text-shadow: 
            4px 4px 0px #000000,
            8px 8px 0px rgba(0, 0, 0, 0.5),
            0px 0px 30px rgba(78, 203, 113, 0.8);
    }}

    /* Enhanced Sidebar - GTA Phone/Pause Menu Style */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, 
            rgba(10, 10, 15, 0.98) 0%, 
            rgba(15, 15, 20, 0.98) 50%, 
            rgba(20, 10, 5, 0.98) 100%) !important;
        border-right: 4px solid #4ECB71;
        box-shadow: 
            inset -2px 0 20px rgba(78, 203, 113, 0.3),
            0 0 50px rgba(0, 0, 0, 0.8);
    }}
    
    section[data-testid="stSidebar"] > div {{
        padding-top: 2rem;
    }}

    /* Sidebar Headers */
    section[data-testid="stSidebar"] h2 {{
        font-family: 'Bebas Neue', sans-serif;
        color: #4ECB71 !important;
        font-size: 1.8rem;
        letter-spacing: 3px;
        text-shadow: 2px 2px 0px #000000, 0 0 15px rgba(78, 203, 113, 0.6);
        border-bottom: 2px solid #4ECB71;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}
    
    /* Sidebar Labels */
    section[data-testid="stSidebar"] label {{
        font-family: 'Roboto Condensed', sans-serif;
        color: #FFD700 !important;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        text-shadow: 1px 1px 2px #000000;
    }}

    /* MultiSelect Pills - GTA Radio Wheel Style */
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
        background: linear-gradient(135deg, #FF6B35 0%, #FF9D00 100%) !important;
        color: #000000 !important;
        border: 2px solid #FFD700 !important;
        font-family: 'Roboto Condensed', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
        box-shadow: 
            0 2px 8px rgba(255, 157, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border-radius: 2px;
    }}

    /* Slider - Weapon Wheel Style */
    section[data-testid="stSidebar"] .stSlider {{
        padding: 15px 0;
    }}
    
    section[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {{
        background: radial-gradient(circle, #4ECB71 0%, #2A7F47 100%) !important;
        border: 3px solid #FFD700 !important;
        box-shadow: 
            0 0 15px rgba(78, 203, 113, 0.8),
            0 4px 10px rgba(0, 0, 0, 0.6);
        width: 24px !important;
        height: 24px !important;
    }}
    
    section[data-testid="stSidebar"] [data-baseweb="slider"] [data-testid="stTickBar"] > div {{
        background: linear-gradient(90deg, #FF6B35 0%, #4ECB71 100%) !important;
        height: 6px !important;
        border-radius: 3px;
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.5),
            0 0 10px rgba(78, 203, 113, 0.4);
    }}

    /* Metric Cards - Mission Complete Style */
    [data-testid="stMetricValue"] {{
        color: #4ECB71 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-weight: 700;
        font-size: 3rem !important;
        text-shadow: 
            3px 3px 0px #000000,
            0 0 20px rgba(78, 203, 113, 0.8);
        letter-spacing: 2px;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-family: 'Roboto Condensed', sans-serif !important;
        color: #FFD700 !important;
        font-weight: 700;
        font-size: 1rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px #000000;
    }}
    
    [data-testid="stMetricDelta"] {{
        font-family: 'Roboto Condensed', sans-serif !important;
        font-weight: 700;
        text-shadow: 1px 1px 2px #000000;
    }}

    /* Popover Buttons - GTA Menu Buttons */
    .stPopover button {{
        background: linear-gradient(135deg, #FF9D00 0%, #FF6B35 100%) !important;
        color: #000000 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-family: 'Roboto Condensed', sans-serif !important;
        letter-spacing: 1px;
        padding: 8px 16px !important;
        box-shadow: 
            0 4px 12px rgba(255, 157, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.2s ease;
    }}
    
    .stPopover button:hover {{
        background: linear-gradient(135deg, #FFB800 0%, #FF8C4B 100%) !important;
        box-shadow: 
            0 6px 16px rgba(255, 157, 0, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }}

    /* Section Headers */
    h3 {{
        font-family: 'Bebas Neue', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 2rem !important;
        letter-spacing: 3px;
        text-shadow: 
            3px 3px 0px #000000,
            0 0 20px rgba(78, 203, 113, 0.6);
        border-left: 8px solid #FF9D00;
        padding-left: 15px;
        margin-top: 20px;
        background: linear-gradient(90deg, rgba(255, 157, 0, 0.2) 0%, transparent 50%);
        padding-top: 10px;
        padding-bottom: 10px;
    }}

    /* Divider */
    hr {{
        border: none;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #4ECB71 20%, 
            #FFD700 50%, 
            #4ECB71 80%, 
            transparent 100%);
        box-shadow: 0 0 10px rgba(78, 203, 113, 0.5);
        margin: 30px 0;
    }}

    /* Chart Styling */
    [data-testid="stArrowVegaLiteChart"] {{
        background: rgba(0, 0, 0, 0.6) !important;
        border: 2px solid #4ECB71;
        border-radius: 4px;
        padding: 15px;
        box-shadow: 
            0 0 20px rgba(78, 203, 113, 0.3),
            inset 0 0 30px rgba(0, 0, 0, 0.5);
    }}

    /* Number Input */
    section[data-testid="stSidebar"] input[type="number"] {{
        background: rgba(20, 20, 30, 0.9) !important;
        color: #4ECB71 !important;
        border: 2px solid #4ECB71 !important;
        font-family: 'Roboto Condensed', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        border-radius: 2px;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
    }}
    
    /* Scanline Effect for Authentic Feel */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.05) 0px,
            transparent 1px,
            transparent 2px,
            rgba(0, 0, 0, 0.05) 3px
        );
        pointer-events: none;
        z-index: 999;
        opacity: 0.3;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR WITH WORKING LOGO ---
with st.sidebar:
    # Using a direct PNG link that works reliably
    try:
        st.image("https://logos-world.net/wp-content/uploads/2021/02/GTA-5-Logo.png", use_container_width=True)
    except:
        # Fallback if image fails to load
        st.markdown("""
            <div style='text-align: center; padding: 20px; background: rgba(78, 203, 113, 0.2); border: 3px solid #4ECB71; margin-bottom: 20px;'>
                <h1 style='color: #4ECB71; font-family: Impact; font-size: 3rem; margin: 0; text-shadow: 3px 3px 0px #000000;'>GTA V</h1>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #4ECB71;'>⚙️ ADMIN CONSOLE</h2>", unsafe_allow_html=True)
    
    selected_platform = st.multiselect("🖥️ NETWORK PLATFORM", df['Platform'].unique(), default=df['Platform'].unique())
    selected_archetype = st.multiselect("👤 BEHAVIORAL PROFILE", df['Archetype'].unique(), default=df['Archetype'].unique())
    
    st.divider()
    ban_sensitivity = st.slider("🎯 DETECTION SENSITIVITY", 1.5, 5.0, 3.0)
    shark_card_min = st.number_input("💳 MIN SHARK SPEND ($)", 0, 1000, 0)

# Filter Logic
f_df = df[(df['Platform'].isin(selected_platform)) & (df['Archetype'].isin(selected_archetype)) & (df['Shark_Card_Spend'] >= shark_card_min)]

# --- 4. MAIN INTERFACE ---
st.markdown('<div class="gta-title">SECURE <span class="gta-serv">SERV</span> TERMINAL</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("🎮 SESSIONS", f"{len(f_df):,}")
    st.popover("📊 HUD INFO").write("Live connection count across Los Santos servers.")
with m2:
    st.metric("⚔️ AVG K/D", round(f_df['K/D_Ratio'].mean(), 2))
    st.popover("🎯 COMBAT INFO").write("The average aggressiveness of the current lobby.")
with m3:
    flagged = f_df[f_df['Toxicity_Z'] > ban_sensitivity]
    st.metric("⚠️ THREATS", len(flagged), delta=f"{len(flagged)} Flagged", delta_color="inverse")
    st.popover("🛡️ SECURITY INFO").write("Users identified as Griefers or Modders based on Z-Score variance.")
with m4:
    vol = f_df['Bank_Balance_GTA$'].sum() / 1e9
    st.metric("💰 ECONOMY", f"${vol:.1f}B")
    st.popover("💵 CASH INFO").write("Total circulating GTA Dollars in this sector.")

st.markdown("---")

# Visuals
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("🏦 ANTI-CHEAT: MONEY DISTRO")
    st.popover("📈 METHODOLOGY").write("Detecting non-organic currency spikes using Benford's Law analysis. Leading digit distribution reveals glitching patterns.")
    benford = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(benford, color="#4ECB71")

with col_b:
    st.subheader("🌙 PEAK CRIME HOURS")
    st.popover("⏰ METHODOLOGY").write("Correlating time of day with mod-menu usage spikes. Shows when server activity and violations peak.")
    st.line_chart(f_df.groupby('Hour').size(), color="#FF9D00")

st.markdown("---")

# Additional Data Table Section
st.subheader("📋 RECENT THREAT ACTIVITY")
threat_df = f_df[f_df['Toxicity_Z'] > ban_sensitivity][['Player_ID', 'Platform', 'Archetype', 'K/D_Ratio', 'Action_Log']].head(10)
st.dataframe(
    threat_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("""
<div style='text-align: center; padding: 20px; margin-top: 40px; border-top: 2px solid #4ECB71;'>
    <p style='color: #FFD700; font-family: "Roboto Condensed", sans-serif; font-size: 0.9rem; letter-spacing: 2px;'>
        🎮 LOS SANTOS SECURE SERVER NETWORK | ROCKSTAR GAMES DIVISION | V2.0.26
    </p>
</div>
""", unsafe_allow_html=True)
