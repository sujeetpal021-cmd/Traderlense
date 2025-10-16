# app.py
app_py = '''
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
'''


# -------------------------
# utils/analytics.py
analytics_py = '''
import pandas as pd


def analyze_trades(df):
df['pnl'] = (df['exit_price'] - df['entry_price']) * df['qty']
df['holding_hrs'] = (pd.to_datetime(df['exit_date']) - pd.to_datetime(df['entry_date'])).dt.total_seconds() / 3600


total_trades = len(df)
wins = df[df['pnl'] > 0]
win_rate = len(wins) / total_trades * 100
avg_pl = df['pnl'].mean()


df['equity'] = df['pnl'].cumsum()
df['peak'] = df['equity'].cummax()
df['drawdown'] = (df['equity'] - df['peak']) / df['peak']
max_dd = abs(df['drawdown'].min() * 100)


median_hold = df['holding_hrs'].median()


results = {
'total_trades': total_trades,
'win_rate': win_rate,
'avg_pl': avg_pl,
'max_dd': max_dd,
'median_hold': median_hold
'''
