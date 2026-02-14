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
    logs = [
        "Successful Cayo Perico Heist", "Purchased Oppressor MKII", 
        "Player Reported for Griefing", "Unexpected Currency Injection",
        "Excellent Heist Leader", "Suspicious Mod-Menu Activity",
        "Shark Card Bundle Purchased", "Passive Mode Abused"
    ]
    
    df = pd.DataFrame({
        'Player_ID': [f"USER_{i:06d}" for i in range(n)],
        'Timestamp': dates,
        'Platform': np.random.choice(platforms, n),
        'Archetype': np.random.choice(archetypes, n, p=[0.4, 0.15, 0.3, 0.1, 0.05]),
        'K/D_Ratio': np.random.lognormal(mean=0.2, sigma=0.8, size=n),
        'Citizen_Kills': np.random.poisson(lam=5, size=n) * np.random.randint(1, 5, n),
        'Bank_Balance_GTA$': np.random.lognormal(mean=14, sigma=2.5, size=n),
        'Shark_Card_Spend': np.random.exponential(scale=50, size=n),
        'Action_Log': np.random.choice(logs, n)
    })
    
    df['Toxicity_Z'] = stats.zscore(df['K/D_Ratio'] + df['Citizen_Kills'])
    df['Lead_Digit'] = df['Bank_Balance_GTA$'].apply(lambda x: int(str(int(x))[0]) if x > 0 else 0)
    risk_pattern = r"(Mod|Grief|Injection|Suspicious|Abuse)"
    df['Behavior_Flag'] = df['Action_Log'].apply(lambda x: 1 if re.search(risk_pattern, x, re.IGNORECASE) else 0)
    df['Hour'] = df['Timestamp'].dt.hour
    return df

df = generate_gta_telemetry()

# --- 2. GTA V AESTHETIC INJECTION ---
st.set_page_config(page_title="LOS SANTOS INTEL", layout="wide")

st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* GTA Header Style */
    .gta-title {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: -2px;
        font-size: 3rem;
        border-bottom: 5px solid #FF9D00;
        margin-bottom: 20px;
    }
    /* Highlight Orange */
    .highlight { color: #FF9D00; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        color: #FF9D00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="gta-title">SECURE <span class="highlight">SERV</span> INTEL SYSTEM</h1>', unsafe_allow_html=True)

# --- 3. SIDEBAR: THE BAN-HAMMER CONSOLE ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e1/Grand_Theft_Auto_V_logo.svg", width=100)
    st.header("ADMIN CONSOLE")
    selected_platform = st.multiselect("PLATFORM NETWORK", df['Platform'].unique(), default=df['Platform'].unique())
    selected_archetype = st.multiselect("BEHAVIORAL TYPE", df['Archetype'].unique(), default=df['Archetype'].unique())
    
    st.divider()
    ban_sensitivity = st.slider("DETECTION SENSITIVITY", 1.5, 5.0, 3.0)
    shark_card_min = st.number_input("MIN SHARK SPEND ($)", 0, 1000, 0)

# Filter Data
mask = (df['Platform'].isin(selected_platform)) & \
       (df['Archetype'].isin(selected_archetype)) & \
       (df['Shark_Card_Spend'] >= shark_card_min)
f_df = df[mask]

# --- 4. TELEMETRY METRICS ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("SESSIONS", len(f_df))
    with st.popover("ℹ️ Info"):
        st.write("Total active player connections currently being monitored in the Los Santos grid.")

with m2:
    st.metric("AVG K/D", round(f_df['K/D_Ratio'].mean(), 2))
    with st.popover("ℹ️ Info"):
        st.write("Average Kill/Death ratio. Extreme spikes often correlate with 'Griefing' behavior.")

with m3:
    flagged_toxic = f_df[f_df['Toxicity_Z'] > ban_sensitivity]
    st.metric("FLAGGED", len(flagged_toxic), delta=f"{len(flagged_toxic)} Threat", delta_color="inverse")
    with st.popover("ℹ️ Info"):
        st.write("Players exceeding the Toxicity Z-Score threshold. Candidates for the Ban-Hammer.")

with m4:
    wealth_gini = f_df['Bank_Balance_GTA$'].sum() / 1e9
    st.metric("CASH FLOW", f"${wealth_gini:.1f}B")
    with st.popover("ℹ️ Info"):
        st.write("Total liquid GTA$ circulating in the selected archetype economy.")

st.markdown("---")

# --- 5. FORENSIC VISUALIZATIONS ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏦 MONEY GLITCH DETECTION")
    with st.popover("Analysis Method"):
        st.markdown("**Benford's Law Analysis**")
        st.write("Organic numbers follow a specific distribution. Spikes in the chart suggest manually injected currency (modding/glitching).")
    
    benford_counts = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(benford_counts, color="#FF9D00")

with col_b:
    st.subheader("🌙 GHOST HOUR ACTIVITY")
    with st.popover("Analysis Method"):
        st.write("Monitoring server load by hour. The 'Ghost Hour' (2 AM - 5 AM) is typically when mod-menu developers test new exploits.")
    
    hourly_trends = f_df.groupby('Hour').size()
    st.line_chart(hourly_trends, color="#FFFFFF")

st.divider()

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("💰 SPEND VS. TOXICITY")
    with st.popover("Analysis Method"):
        st.write("Scatter plot correlating real-world Shark Card spending with in-game aggression (K/D). Helps identify 'Aggressive Whales'.")
    st.scatter_chart(data=f_df, x='Shark_Card_Spend', y='K/D_Ratio', color='Archetype')

with col_d:
    st.subheader("⚠️ REGEX RISK FLAGS")
    with st.popover("Analysis Method"):
        st.write("Real-time log scanning for keywords like 'Injection', 'Mod', or 'Abuse' across platforms.")
    risk_dist = f_df.groupby('Platform')['Behavior_Flag'].sum()
    st.bar_chart(risk_dist, color="#FF0000")

# --- 6. THE "BAN-HAMMER" AUDIT TRAIL ---
st.markdown('<h2 style="color:#FF0000;">🚨 HIGH-PRIORITY ENFORCEMENT LIST</h2>', unsafe_allow_html=True)
audit_trail = f_df[(f_df['Toxicity_Z'] > ban_sensitivity) | (f_df['Behavior_Flag'] == 1)]
audit_trail = audit_trail.sort_values(by='Toxicity_Z', ascending=False)

st.dataframe(
    audit_trail[['Player_ID', 'Platform', 'Archetype', 'K/D_Ratio', 'Toxicity_Z', 'Action_Log']], 
    use_container_width=True
)
