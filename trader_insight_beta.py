import streamlit as st
import pandas as pd
from utils.analytics import analyze_trades
from utils.recommendations import generate_recommendations
from utils.visuals import plot_equity_curve, plot_pnl_distribution, plot_holding_time

st.set_page_config(page_title="Trader Insight Beta", layout="wide")
st.title("📊 Trader Insight Beta – Understand Your Trading DNA")
st.write("Upload your trading CSV to discover your trader type, performance metrics, and personalized improvement suggestions.")
st.write("Or use the default demo data below to explore the app.")

# Default demo CSV
DEFAULT_CSV = "data/demo_trading_data.csv"

# File uploader
uploaded_file = st.file_uploader("📤 Upload your trade CSV", type="csv")

# Load CSV
try:
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV loaded successfully!")
    else:
        df = pd.read_csv(DEFAULT_CSV)
        st.info("Using default demo CSV.")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Validate required columns
required_cols = ["symbol", "entry_price", "exit_price", "qty", "entry_date", "exit_date"]
if not all(col in df.columns for col in required_cols):
    st.error(f"CSV missing required columns. Must have: {required_cols}")
    st.stop()

# Show raw data
st.subheader("📄 Raw Data Preview")
st.dataframe(df.head())

# Analysis
try:
    results = analyze_trades(df)
except Exception as e:
    st.error(f"Error during trade analysis: {e}")
    st.stop()

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Win Rate", f"{results['win_rate']:.1f}%")
col2.metric("Avg P/L per Trade", f"{results['avg_pl']:.2f}")
col3.metric("Max Drawdown", f"{results['max_dd']:.1f}%")

# Charts
try:
    st.plotly_chart(plot_equity_curve(df), use_container_width=True)
    st.plotly_chart(plot_pnl_distribution(df), use_container_width=True)
    st.plotly_chart(plot_holding_time(df), use_container_width=True)
except Exception as e:
    st.error(f"Error generating charts: {e}")

# Trader type & recommendations
try:
    suggestions = generate_recommendations(results)
    st.subheader("🧠 Trader Profile & Suggestions")
    st.success(f"**Trader Type:** {suggestions['type']}")
    st.write("### Key Insights:")
    for i, s in enumerate(suggestions['insights'], 1):
        st.write(f"{i}. {s}")
except Exception as e:
    st.error(f"Error generating recommendations: {e}")
