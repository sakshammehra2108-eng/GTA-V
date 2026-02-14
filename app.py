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
    
    # Unique session timestamps
    dates = [start_date + timedelta(seconds=np.random.randint(0, 3888000)) for _ in range(n)]
    
    archetypes = ['Grinder', 'Griefer', 'Casual', 'Whale', 'Modder']
    platforms = ['PC', 'PS5', 'Xbox Series X']
    
    # Behavioral logs for Regex Mining
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
    
    # --- FORENSIC ANALYTICS ---
    # Z-Score for Toxicity (K/D and Citizen Kills)
    df['Toxicity_Z'] = stats.zscore(df['K/D_Ratio'] + df['Citizen_Kills'])
    
    # Benford's Law Lead Digit for Money Glitch Detection
    df['Lead_Digit'] = df['Bank_Balance_GTA$'].apply(lambda x: int(str(int(x))[0]) if x > 0 else 0)
    
    # Regex Sentiment/Risk Flagging
    risk_pattern = r"(Mod|Grief|Injection|Suspicious|Abuse)"
    df['Behavior_Flag'] = df['Action_Log'].apply(lambda x: 1 if re.search(risk_pattern, x, re.IGNORECASE) else 0)
    
    df['Hour'] = df['Timestamp'].dt.hour
    return df

df = generate_gta_telemetry()

# --- 2. THE WAR ROOM UI ---
st.set_page_config(page_title="GTA V Intelligence", layout="wide")
st.title("🎮 GTA V: Los Santos Player Intelligence Suite")
st.markdown("---")

# --- 3. SIDEBAR: THE BAN-HAMMER CONSOLE ---
st.sidebar.header("🛠️ Admin Controls")
with st.sidebar:
    selected_platform = st.multiselect("Platform", df['Platform'].unique(), default=df['Platform'].unique())
    selected_archetype = st.multiselect("Archetype", df['Archetype'].unique(), default=df['Archetype'].unique())
    
    st.divider()
    ban_sensitivity = st.slider("Toxicity Sensitivity (Z-Score Threshold)", 1.5, 5.0, 3.0)
    shark_card_min = st.number_input("Min Shark Card Spend ($)", 0, 1000, 0)

# Filter Data
mask = (df['Platform'].isin(selected_platform)) & \
       (df['Archetype'].isin(selected_archetype)) & \
       (df['Shark_Card_Spend'] >= shark_card_min)
f_df = df[mask]

# --- 4. TELEMETRY METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Sessions", len(f_df))
m2.metric("Avg K/D Ratio", round(f_df['K/D_Ratio'].mean(), 2))

flagged_toxic = f_df[f_df['Toxicity_Z'] > ban_sensitivity]
m3.metric("Flagged Griefers", len(flagged_toxic), delta="Z-Score Outliers", delta_color="inverse")

wealth_gini = f_df['Bank_Balance_GTA$'].sum() / 1e9
m4.metric("Economy Volume", f"GTA${wealth_gini:.2f}B")

st.markdown("---")

# --- 5. FORENSIC VISUALIZATIONS ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏦 Money Glitch Detection (Benford's Law)")
    st.info("Deviations from the logarithmic curve indicate non-organic currency injections (Modding).")
    # Benford Analysis
    benford_counts = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(benford_counts)
    

with col_b:
    st.subheader("🌙 Ghost Hour Activity (Modder Peak Time)")
    st.info("Server activity by hour. Spikes in late-night windows often correlate with mod-menu testing.")
    hourly_trends = f_df.groupby('Hour').size()
    st.line_chart(hourly_trends)

st.divider()

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("💰 Spending vs. Toxicity Index")
    st.write("Does high spending (Whales) reduce toxicity? Analyzing 'Pay-to-Win' behavior.")
    st.scatter_chart(data=f_df, x='Shark_Card_Spend', y='K/D_Ratio', color='Archetype')

with col_d:
    st.subheader("⚠️ Behavioral Risk Distribution")
    # Regex flag concentration by platform
    risk_dist = f_df.groupby('Platform')['Behavior_Flag'].sum()
    st.bar_chart(risk_dist)

# --- 6. THE "BAN-HAMMER" AUDIT TRAIL ---
st.divider()
st.subheader("🚨 High-Priority Enforcement List")
st.write("Players flagged by BOTH statistical outliers (Z-Score) and Behavioral Regex logs.")

# Forensic filter: High Z-Score OR High Risk Flag
audit_trail = f_df[(f_df['Toxicity_Z'] > ban_sensitivity) | (f_df['Behavior_Flag'] == 1)]
audit_trail = audit_trail.sort_values(by='Toxicity_Z', ascending=False)

st.dataframe(
    audit_trail[['Player_ID', 'Platform', 'Archetype', 'K/D_Ratio', 'Toxicity_Z', 'Action_Log']], 
    use_container_width=True
)
