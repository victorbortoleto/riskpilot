import streamlit as st
import pandas as pd
import plotly.express as px

from core.loader import load_trading_file
from core.normalizer import normalize_trades
from core.metrics import calculate_metrics
from core.risk_engine import generate_risk_alerts


st.set_page_config(
    page_title="RiskPilot",
    page_icon="📊",
    layout="wide"
)


# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙️ Configurações")

initial_capital = st.sidebar.number_input(
    "Capital inicial",
    value=1000.0,
    step=100.0
)

max_daily_loss = st.sidebar.number_input(
    "Limite de perda diária",
    value=500.0,
    step=50.0
)

max_drawdown_limit = st.sidebar.number_input(
    "Limite máximo de drawdown",
    value=2000.0,
    step=100.0
)

profit_target = st.sidebar.number_input(
    "Meta da Prop Firm",
    value=3000.0,
    step=100.0
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Suba um relatório CSV ou XLSX da sua plataforma."
)


# =========================
# HEADER
# =========================

st.title("📊 RiskPilot")

st.markdown(
    "### Trading Risk Dashboard — gerenciamento de risco, performance e consistência"
)


# =========================
# UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload do relatório de trades",
    type=["csv", "xlsx"]
)


if uploaded_file:

    try:

        # =========================
        # LOAD
        # =========================

        raw_df = load_trading_file(uploaded_file)

        st.header("1. Dados Originais")
        st.dataframe(raw_df, use_container_width=True)


        # =========================
        # NORMALIZATION
        # =========================

        normalized_df = normalize_trades(raw_df)

        normalized_df["date"] = pd.to_datetime(normalized_df["date"])

        normalized_df["hour"] = normalized_df["date"].dt.hour
        normalized_df["day"] = normalized_df["date"].dt.date
        normalized_df["weekday"] = normalized_df["date"].dt.day_name()


        # =========================
        # EQUITY
        # =========================

        normalized_df["equity"] = (
            normalized_df["net_pnl"].cumsum() + initial_capital
        )

        normalized_df["equity_peak"] = (
            normalized_df["equity"].cummax()
        )

        normalized_df["
```
