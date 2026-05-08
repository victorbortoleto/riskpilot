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
st.sidebar.info("Suba um relatório CSV ou XLSX da sua plataforma.")

# =========================
# HEADER
# =========================

st.title("📊 RiskPilot")
st.markdown("### Trading Risk Dashboard — gerenciamento de risco, performance e consistência")

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
        # EQUITY / DRAWDOWN
        # =========================

        normalized_df["equity"] = normalized_df["net_pnl"].cumsum() + initial_capital
        normalized_df["equity_peak"] = normalized_df["equity"].cummax()
        normalized_df["drawdown"] = normalized_df["equity"] - normalized_df["equity_peak"]

        # =========================
        # METRICS
        # =========================

        metrics = calculate_metrics(normalized_df, initial_capital)

        expectancy = metrics.get("expectancy", 0)
        recovery_factor = metrics.get("recovery_factor", 0)
        payoff_ratio = metrics.get("payoff_ratio", 0)

        if "expectancy" not in metrics:
            expectancy = (
                (metrics["winrate"] / 100) * metrics["average_win"]
            ) - (
                (1 - metrics["winrate"] / 100) * abs(metrics["average_loss"])
            )

        if "recovery_factor" not in metrics:
            recovery_factor = (
                metrics["net_pnl"] / abs(metrics["max_drawdown"])
                if metrics["max_drawdown"] != 0
                else 0
            )

        if "payoff_ratio" not in metrics:
            payoff_ratio = (
                abs(metrics["average_win"] / metrics["average_loss"])
                if metrics["average_loss"] != 0
                else 0
            )

        # =========================
        # SUMMARY
        # =========================

        st.header("2. Resumo Geral")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💰 Net P&L", f"${metrics['net_pnl']:.2f}")

        with col2:
            st.metric("🎯 Winrate", f"{metrics['winrate']:.2f}%")

        with col3:
            st.metric("📈 Profit Factor", f"{metrics['profit_factor']:.2f}")

        with col4:
            st.metric("⚠️ Max Drawdown", f"${metrics['max_drawdown']:.2f}")

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("🏆 Avg Win", f"${metrics['average_win']:.2f}")

        with col6:
            st.metric("❌ Avg Loss", f"${metrics['average_loss']:.2f}")

        with col7:
            st.metric("🔥 Max Win Streak", metrics["max_win_streak"])

        with col8:
            st.metric("🥶 Max Loss Streak", metrics["max_loss_streak"])

        col9, col10, col11, col12 = st.columns(4)

        with col9:
            st.metric("🧠 Expectancy", f"${expectancy:.2f}")

        with col10:
            st.metric("🛡 Recovery Factor", f"{recovery_factor:.2f}")

        with col11:
            st.metric("⚖️ Payoff Ratio", f"{payoff_ratio:.2f}")

        with col12:
            st.metric("📊 Trades", metrics["total_trades"])

        # =========================
        # PROP FIRM PANEL
        # =========================

        st.header("3. Painel Prop Firm")

        remaining_target = profit_target - metrics["net_pnl"]

        daily_worst = normalized_df.groupby("day")["net_pnl"].sum().min()
        daily_remaining = max_daily_loss - abs(daily_worst)

        max_dd_remaining = max_drawdown_limit - abs(metrics["max_drawdown"])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info(f"🎯 Faltam ${remaining_target:.2f} para atingir a meta")

        with c2:
            st.warning(f"⚠️ Daily DD restante: ${daily_remaining:.2f}")

        with c3:
            st.error(f"🛑 Max DD restante: ${max_dd_remaining:.2f}")

        # =========================
        # EQUITY CURVE
        # =========================

        st.header("4. Curva de Capital")

        fig_equity = px.line(
            normalized_df,
            x="date",
            y="equity",
            title="Equity Curve"
        )
        st.plotly_chart(fig_equity, use_container_width=True)

        # =========================
        # DRAWDOWN
        # =========================

        st.header("5. Drawdown")

        fig_dd = px.area(
            normalized_df,
            x="date",
            y="drawdown",
            title="Drawdown"
        )
        st.plotly_chart(fig_dd, use_container_width=True)

        # =========================
        # DAILY RESULT
        # =========================

        st.header("6. Resultado por Dia")

        daily_pnl = normalized_df.groupby("day")["net_pnl"].sum().reset_index()

        fig_daily = px.bar(
            daily_pnl,
            x="day",
            y="net_pnl",
            title="Daily P&L"
        )
        st.plotly_chart(fig_daily, use_container_width=True)

        # =========================
        # RESULT BY HOUR
        # =========================

        st.header("7. Resultado por Hora")

        hourly = normalized_df.groupby("hour")["net_pnl"].sum().reset_index()

        fig_hour = px.bar(
            hourly,
            x="hour",
            y="net_pnl",
            title="Resultado por Hora"
        )
        st.plotly_chart(fig_hour, use_container_width=True)

        # =========================
        # RESULT BY WEEKDAY
        # =========================

        st.header("8. Resultado por Dia da Semana")

        weekday_order = [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ]

        weekday = normalized_df.groupby("weekday")["net_pnl"].sum().reset_index()
        weekday["weekday"] = pd.Categorical(
            weekday["weekday"],
            categories=weekday_order,
            ordered=True
        )
        weekday = weekday.sort_values("weekday")

        fig_weekday = px.bar(
            weekday,
            x="weekday",
            y="net_pnl",
            title="Resultado por Dia da Semana"
        )
        st.plotly_chart(fig_weekday, use_container_width=True)

        # =========================
        # RESULT BY ASSET
        # =========================

        st.header("9. Resultado por Ativo")

        asset = normalized_df.groupby("asset")["net_pnl"].sum().reset_index()

        fig_asset = px.bar(
            asset,
            x="asset",
            y="net_pnl",
            title="P&L por Ativo"
        )
        st.plotly_chart(fig_asset, use_container_width=True)

        # =========================
        # ALERTS
        # =========================

        st.header("10. Alertas de Risco")

        alerts = generate_risk_alerts(
            normalized_df,
            max_daily_loss,
            max_drawdown_limit
        )

        for alert in alerts:
            st.warning(f"⚠️ {alert}")

        if metrics["profit_factor"] < 1:
            st.error("Profit Factor abaixo de 1. Você está perdendo mais do que ganha.")

        if payoff_ratio < 1:
            st.warning("Seu payoff está abaixo de 1. Seus losses estão maiores que seus gains.")

        # =========================
        # NORMALIZED DATA
        # =========================

        st.header("11. Dados Normalizados")
        st.dataframe(normalized_df, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

else:
    st.info("Envie um arquivo CSV ou XLSX para começar.")
```
