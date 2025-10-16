# app.py
if win_rate < 40:
insights.append("Low win rate – focus on setups with higher accuracy.")
if hold < 2:
insights.append("Very short holding time – may indicate overtrading or lack of patience.")
if hold > 100:
insights.append("Long holding periods – review opportunity cost and capital rotation.")


insights.append("Maintain consistent position sizing and review trade logs weekly.")


return {'type': ttype, 'insights': insights}
'''


# -----------------------------------
# utils/visuals.py
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


# -----------------------------------
# data/sample_trading_data.csv
sample_csv = '''symbol,entry_price,exit_price,qty,entry_date,exit_date
TCS,3500,3525,10,2024-05-01 10:00:00,2024-05-01 15:00:00
INFY,1450,1440,20,2024-05-02 09:30:00,2024-05-02 12:00:00
HDFCBANK,1600,1625,15,2024-05-03 09:30:00,2024-05-04 10:00:00
RELIANCE,2450,2480,10,2024-05-05 09:30:00,2024-05-07 10:00:00
SBIN,570,560,50,2024-05-07 09:30:00,2024-05-07 15:00:00
'''


# -----------------------------------
# requirements.txt
requirements_txt = '''streamlit
pandas
plotly
numpy
'''


# -----------------------------------
# README.md
readme_md = '''# Trader Insight Beta


Zero-cost beta version of Trader Insight Tool built with Streamlit.


## Run Locally
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Run Streamlit app:
```
streamlit run app.py
```
3. Upload your trade CSV to see analysis, trader type, and recommendations.
'''
