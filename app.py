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
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>
    .main {
        background-color: #0b0f19;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    h1, h2, h3 {
        color: #ffffff;
        letter-spacing: -0.03em;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 35px;
        margin-bottom: 16px;
        border-left: 4px solid #38bdf8;
        padding-left: 12px;
    }

    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        min-height: 125px;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-help {
        color: #6b7280;
        font-size: 0.78rem;
        margin-top: 8px;
    }

    .positive {
        color: #22c55e;
    }

    .negative {
        color: #ef4444;
    }

    .neutral {
        color: #38bdf8;
    }

    .prop-card {
        background: linear-gradient(135deg, #082f49 0%, #111827 100%);
        border: 1px solid rgba(56,189,248,0.35);
        border-radius: 18px;
        padding: 22px;
        min-height: 120px;
    }

    .alert-box {
        background: #1f2937;
        border-left: 5px solid #f59e0b;
        padding: 16px 18px;
        border-radius: 12px;
        color: #f9fafb;
        margin-bottom: 12px;
    }

    .footer-note {
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 40px;
        text-align: center;
    }

    div[data-testid="stMetric"] {
        background: #111827;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HELPER FUNCTIONS
# =========================

def money(value):
    return f"${value:,.2f}"


def percent(value):
    return f"{value:.2f}%"


def metric_card(label, value, help_text="", status="neutral"):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {status}">{value}</div>
        <div class="metric-help">{help_text}</div>
    </div>
    """


def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙️ Risk Settings")

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

st.markdown("# 📊 RiskPilot")
st.markdown(
    '<div class="subtitle">Trading Risk Dashboard — gerenciamento de risco, performance e consistência operacional.</div>',
    unsafe_allow_html=True
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
        raw_df = load_trading_file(uploaded_file)

        section("1. Dados Originais")
        st.dataframe(raw_df, use_container_width=True)

        normalized_df = normalize_trades(raw_df)

        normalized_df["date"] = pd.to_datetime(normalized_df["date"])
        normalized_df["hour"] = normalized_df["date"].dt.hour
        normalized_df["day"] = normalized_df["date"].dt.date
        normalized_df["weekday"] = normalized_df["date"].dt.day_name()

        normalized_df["equity"] = normalized_df["net_pnl"].cumsum() + initial_capital
        normalized_df["equity_peak"] = normalized_df["equity"].cummax()
        normalized_df["drawdown"] = normalized_df["equity"] - normalized_df["equity_peak"]

        metrics = calculate_metrics(normalized_df, initial_capital)

        expectancy = metrics.get("expectancy", 0)
        recovery_factor = metrics.get("recovery_factor", 0)
        payoff_ratio = metrics.get("payoff_ratio", 0)

        net_status = "positive" if metrics["net_pnl"] >= 0 else "negative"
        pf_status = "positive" if metrics["profit_factor"] >= 1 else "negative"
        dd_status = "negative" if metrics["max_drawdown"] >= max_drawdown_limit else "neutral"

        # =========================
        # SUMMARY
        # =========================

        section("2. Resumo Geral")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                metric_card(
                    "💰 Net P&L",
                    money(metrics["net_pnl"]),
                    "Resultado líquido total",
                    net_status
                ),
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                metric_card(
                    "🎯 Winrate",
                    percent(metrics["winrate"]),
                    "Percentual de trades vencedores",
                    "neutral"
                ),
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                metric_card(
                    "📈 Profit Factor",
                    f"{metrics['profit_factor']:.2f}",
                    "Acima de 1 é positivo",
                    pf_status
                ),
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                metric_card(
                    "⚠️ Max Drawdown",
                    money(metrics["max_drawdown"]),
                    "Maior queda da curva",
                    dd_status
                ),
                unsafe_allow_html=True
            )

        c5, c6, c7, c8 = st.columns(4)

        with c5:
            st.markdown(metric_card("🏆 Avg Win", money(metrics["average_win"]), "Média dos ganhos", "positive"), unsafe_allow_html=True)

        with c6:
            st.markdown(metric_card("❌ Avg Loss", money(metrics["average_loss"]), "Média das perdas", "negative"), unsafe_allow_html=True)

        with c7:
            st.markdown(metric_card("🔥 Win Streak", metrics["max_win_streak"], "Maior sequência vencedora", "positive"), unsafe_allow_html=True)

        with c8:
            st.markdown(metric_card("🥶 Loss Streak", metrics["max_loss_streak"], "Maior sequência perdedora", "negative"), unsafe_allow_html=True)

        c9, c10, c11, c12 = st.columns(4)

        with c9:
            st.markdown(metric_card("🧠 Expectancy", money(expectancy), "Resultado esperado por trade", "neutral"), unsafe_allow_html=True)

        with c10:
            st.markdown(metric_card("🛡 Recovery", f"{recovery_factor:.2f}", "Recuperação vs drawdown", "neutral"), unsafe_allow_html=True)

        with c11:
            st.markdown(metric_card("⚖️ Payoff", f"{payoff_ratio:.2f}", "Avg win / Avg loss", "neutral"), unsafe_allow_html=True)

        with c12:
            st.markdown(metric_card("📊 Trades", metrics["total_trades"], "Total analisado", "neutral"), unsafe_allow_html=True)

        # =========================
        # PROP FIRM PANEL
        # =========================

        section("3. Painel Prop Firm")

        remaining_target = profit_target - metrics["net_pnl"]
        daily_worst = normalized_df.groupby("day")["net_pnl"].sum().min()
        daily_remaining = max_daily_loss - abs(daily_worst)
        max_dd_remaining = max_drawdown_limit - abs(metrics["max_drawdown"])

        prop1, prop2, prop3 = st.columns(3)

        with prop1:
            st.markdown(
                f"""
                <div class="prop-card">
                    <div class="metric-label">🎯 Distância da Meta</div>
                    <div class="metric-value neutral">{money(remaining_target)}</div>
                    <div class="metric-help">Faltam para atingir o objetivo configurado</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with prop2:
            st.markdown(
                f"""
                <div class="prop-card">
                    <div class="metric-label">⚠️ Daily DD Restante</div>
                    <div class="metric-value {'negative' if daily_remaining < 0 else 'neutral'}">{money(daily_remaining)}</div>
                    <div class="metric-help">Margem restante até o limite diário</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with prop3:
            st.markdown(
                f"""
                <div class="prop-card">
                    <div class="metric-label">🛑 Max DD Restante</div>
                    <div class="metric-value {'negative' if max_dd_remaining < 0 else 'neutral'}">{money(max_dd_remaining)}</div>
                    <div class="metric-help">Margem restante até o drawdown máximo</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =========================
        # CHARTS
        # =========================

        section("4. Curva de Capital")
        fig_equity = px.line(normalized_df, x="date", y="equity", title="Equity Curve")
        fig_equity.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_equity, use_container_width=True)

        section("5. Drawdown")
        fig_dd = px.area(normalized_df, x="date", y="drawdown", title="Drawdown")
        fig_dd.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_dd, use_container_width=True)

        section("6. Resultado por Dia")
        daily_pnl = normalized_df.groupby("day")["net_pnl"].sum().reset_index()
        fig_daily = px.bar(daily_pnl, x="day", y="net_pnl", title="Daily P&L")
        fig_daily.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_daily, use_container_width=True)

        section("7. Resultado por Hora")
        hourly = normalized_df.groupby("hour")["net_pnl"].sum().reset_index()
        fig_hour = px.bar(hourly, x="hour", y="net_pnl", title="Resultado por Hora")
        fig_hour.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_hour, use_container_width=True)

        section("8. Resultado por Dia da Semana")
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = normalized_df.groupby("weekday")["net_pnl"].sum().reset_index()
        weekday["weekday"] = pd.Categorical(weekday["weekday"], categories=weekday_order, ordered=True)
        weekday = weekday.sort_values("weekday")
        fig_weekday = px.bar(weekday, x="weekday", y="net_pnl", title="Resultado por Dia da Semana")
        fig_weekday.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_weekday, use_container_width=True)

        section("9. Resultado por Ativo")
        asset = normalized_df.groupby("asset")["net_pnl"].sum().reset_index()
        fig_asset = px.bar(asset, x="asset", y="net_pnl", title="P&L por Ativo")
        fig_asset.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_asset, use_container_width=True)

        # =========================
        # ALERTS
        # =========================

        section("10. Alertas de Risco")

        alerts = generate_risk_alerts(normalized_df, max_daily_loss, max_drawdown_limit)

        for alert in alerts:
            st.markdown(
                f'<div class="alert-box">⚠️ {alert}</div>',
                unsafe_allow_html=True
            )

        if metrics["profit_factor"] < 1:
            st.error("Profit Factor abaixo de 1. Você está perdendo mais do que ganha.")

        if payoff_ratio < 1:
            st.warning("Seu payoff está abaixo de 1. Seus losses estão maiores que seus gains.")

        # =========================
        # NORMALIZED DATA
        # =========================

        section("11. Dados Normalizados")
        st.dataframe(normalized_df, use_container_width=True)

        csv = normalized_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Baixar dados normalizados",
            csv,
            "riskpilot_normalized_trades.csv",
            "text/csv"
        )

        st.markdown(
            '<div class="footer-note">RiskPilot MVP — Trading risk analytics for serious traders.</div>',
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

else:
    st.info("Envie um arquivo CSV ou XLSX para começar.")
2. Render → Manual Deploy → Deploy latest commit
3. Teste novamente com o XLSX.
