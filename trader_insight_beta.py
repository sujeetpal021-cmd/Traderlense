# This is a ready-to-use beta version of the Trader Insight Tool
# Folder structure is embedded here. You can copy each file into the corresponding folder.

# 1️⃣ app.py (Streamlit main file)
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

# 2️⃣ utils/analytics.py
analytics_py = '''
import pandas as pd
import numpy as np

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
    }

    return results
'''

# 3️⃣ utils/recommendations.py
recommendations_py = '''
def generate_recommendations(results):
    hold = results['median_hold']
    dd = results['max_dd']
    win_rate = results['win_rate']

    if hold < 1:
        ttype = "Scalper"
    elif hold < 24:
        ttype = "Intraday Momentum Trader"
    elif hold < 168:
        ttype = "Swing Trader"
    else:
        ttype = "Position Trader"

    insights = []
    if dd > 20:
        insights.append("High drawdown detected – reduce position size or tighten stops.")
    if win_rate < 40:
        insights.append("Low win rate – focus on setups with higher accuracy.")
    if hold < 2:
        insights.append("Very short holding time – may indicate overtrading or lack of patience.")
    if hold > 100:
        insights.append("Long holding periods – review opportunity cost and capital rotation.")

    insights.append("Maintain consistent position sizing and review trade logs weekly.")

    return {'type': ttype, 'insights': insights}
'''

# 4️⃣ utils/visuals.py
visuals_py = '''
import plotly.graph_objects as go

def plot_equity_curve(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['pnl'].cumsum(), name="Equity Curve", line=dict(color="royalblue")))
    fig.update_layout(title="Equity Curve", xaxis_title="Trade #", yaxis_title="Cumulative P&L")
    return fig

def plot_pnl_distribution(df):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['pnl'], nbinsx=30, marker_color="seagreen"))
    fig.update_layout(title="Distribution of Trade P&L")
    return fig

def plot_holding_time(df):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['holding_hrs'], nbinsx=20, marker_color="darkorange"))
    fig.update_layout(title="Holding Time Distribution (hours)")
    return fig
'''

# 5️⃣ data/sample_trading_data.csv
sample_csv = '''symbol,entry_price,exit_price,qty,entry_date,exit_date
TCS,3500,3525,10,2024-05-01 10:00:00,2024-05-01 15:00:00
INFY,1450,1440,20,2024-05-02 09:30:00,2024-05-02 12:00:00
HDFCBANK,1600,1625,15,2024-05-03 09:30:00,2024-05-04 10:00:00
RELIANCE,2450,2480,10,2024-05-05 09:30:00,2024-05-07 10:00:00
SBIN,570,560,50,2024-05-07 09:30:00,2024-05-07 15:00:00
'''

# 6️⃣ requirements.txt
requirements_txt = '''streamlit
pandas
plotly
numpy
'''

# 7️⃣ README.md
readme_md = '''# Trader Insight Beta

This is a zero-cost beta version of the Trader Insight Tool built with Streamlit.

## How to Run
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Run Streamlit app:
```
streamlit run app.py
```
3. Upload your trading CSV file to see analysis, trader type, and recommendations.
'''


# Instructions for user
files = {
    'app.py': app_py,
    'utils/analytics.py': analytics_py,
    'utils/recommendations.py': recommendations_py,
    'utils/visuals.py': visuals_py,
    'data/sample_trading_data.csv': sample_csv,
    'requirements.txt': requirements_txt,
    'README.md': readme_md
}

# Saving files locally (if running this script locally)
import os

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("✅ All files created! You can now upload this folder to GitHub and deploy on Streamlit Cloud.")
