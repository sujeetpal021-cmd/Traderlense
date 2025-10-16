import streamlit as st
import pandas as pd
from utils.analytics import analyze_trades
from utils.recommendations import generate_recommendations
from utils.visuals import plot_equity_curve, plot_pnl_distribution, plot_holding_time

st.set_page_config(page_title="Trader Insight Beta", layout="wide")
st.title("📊 Trader Insight Beta – Understand Your Trading DNA")
st.write("Upload your trading CSV to discover your trader type, performance metrics, and personalized improvement suggestions.")

uploaded_file = st.file_uploader("📤 Upload your trade CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Performance Analysis")
    results = analyze_trades(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Win Rate", f"{results['win_rate']:.1f}%")
    col2.metric("Avg P/L per Trade", f"{results['avg_pl']:.2f}")
    col3.metric("Max Drawdown", f"{results['max_dd']:.1f}%")

    st.plotly_chart(plot_equity_curve(df), use_container_width=True)
    st.plotly_chart(plot_pnl_distribution(df), use_container_width=True)
    st.plotly_chart(plot_holding_time(df), use_container_width=True)

    st.subheader("🧠 Trader Profile & Suggestions")
    suggestions = generate_recommendations(results)
    st.success(f"**Trader Type:** {suggestions['type']}")
    st.write("### Key Insights:")
    for i, s in enumerate(suggestions['insights'], 1):
        st.write(f"{i}. {s}")
else:
    st.info("Please upload a trade CSV file to begin.")
