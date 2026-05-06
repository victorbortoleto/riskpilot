import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from core.loader import load_trading_file
from core.normalizer import normalize_trades
from core.metrics import calculate_metrics, add_equity_curve
from core.risk_engine import generate_risk_alerts

st.set_page_config(
    page_title="RiskPilot MVP",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RiskPilot MVP")
st.caption("Trading Risk Dashboard — gerenciamento de risco, performance e consistência.")

with st.sidebar:
    st.header("Configurações")
    starting_balance = st.number_input(
        "Capital inicial",
        min_value=0.0,
        value=10000.0,
        step=100.0
    )

    daily_loss_limit = st.number_input(
        "Limite de perda diária",
        min_value=0.0,
        value=500.0,
        step=50.0
    )

    max_drawdown_limit = st.number_input(
        "Limite máximo de drawdown",
        min_value=0.0,
        value=2000.0,
        step=100.0
    )

    st.divider()
    st.caption("Suba um relatório CSV ou XLSX da sua plataforma.")

uploaded_file = st.file_uploader(
    "Upload do relatório de trades",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info("Envie um arquivo CSV ou XLSX para começar. Você pode testar com o `sample_trades.csv` incluso no projeto.")
    st.stop()

try:
    raw_df = load_trading_file(uploaded_file)
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

st.subheader("1. Dados Originais")
st.dataframe(raw_df, use_container_width=True)

try:
    trades = normalize_trades(raw_df)
except Exception as e:
    st.error(f"Não consegui normalizar esse arquivo automaticamente: {e}")
    st.warning("Esse MVP precisa encontrar ao menos uma coluna de data e uma coluna de resultado/lucro/prejuízo.")
    st.stop()

trades = add_equity_curve(trades, starting_balance)
metrics = calculate_metrics(trades, starting_balance)
alerts = generate_risk_alerts(
    trades,
    daily_loss_limit=daily_loss_limit,
    max_drawdown_limit=max_drawdown_limit
)

st.subheader("2. Resumo Geral")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Net P&L", f"${metrics['net_pnl']:,.2f}")
col2.metric("Winrate", f"{metrics['winrate']:.2f}%")
col3.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
col4.metric("Max Drawdown", f"${metrics['max_drawdown']:,.2f}")
col5.metric("Trades", f"{metrics['total_trades']}")

col6, col7, col8, col9 = st.columns(4)
col6.metric("Average Win", f"${metrics['average_win']:,.2f}")
col7.metric("Average Loss", f"${metrics['average_loss']:,.2f}")
col8.metric("Max Win Streak", f"{metrics['max_win_streak']}")
col9.metric("Max Loss Streak", f"{metrics['max_loss_streak']}")

st.subheader("3. Curva de Capital")
fig_equity = px.line(
    trades,
    x="date",
    y="equity",
    title="Equity Curve"
)
st.plotly_chart(fig_equity, use_container_width=True)

st.subheader("4. Drawdown")
fig_dd = px.area(
    trades,
    x="date",
    y="drawdown",
    title="Drawdown"
)
st.plotly_chart(fig_dd, use_container_width=True)

st.subheader("5. Resultado por Dia")
daily = trades.groupby(trades["date"].dt.date)["pnl"].sum().reset_index()
daily.columns = ["date", "pnl"]
fig_daily = px.bar(
    daily,
    x="date",
    y="pnl",
    title="Daily P&L"
)
st.plotly_chart(fig_daily, use_container_width=True)

if "asset" in trades.columns:
    st.subheader("6. Resultado por Ativo")
    by_asset = trades.groupby("asset")["pnl"].sum().sort_values(ascending=False).reset_index()
    fig_asset = px.bar(
        by_asset,
        x="asset",
        y="pnl",
        title="P&L by Asset"
    )
    st.plotly_chart(fig_asset, use_container_width=True)

st.subheader("7. Alertas de Risco")
if alerts:
    for alert in alerts:
        st.warning(alert)
else:
    st.success("Nenhum alerta crítico encontrado com os limites configurados.")

st.subheader("8. Dados Normalizados")
st.dataframe(trades, use_container_width=True)

csv = trades.to_csv(index=False).encode("utf-8")
st.download_button(
    "Baixar dados normalizados em CSV",
    csv,
    "normalized_trades.csv",
    "text/csv"
)
