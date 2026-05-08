import streamlit as st
import pandas as pd
import plotly.express as px

from core.loader import load_trading_file
from core.normalizer import normalize_trades
from core.metrics import calculate_metrics
from core.risk_engine import generate_risk_alerts
from core.db import save_upload, load_upload_history, load_upload_by_id

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
    .main { background-color: #0b0f19; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }
    h1, h2, h3 { color: #ffffff; letter-spacing: -0.03em; }
    .subtitle { color: #9ca3af; font-size: 1.05rem; margin-top: -10px; margin-bottom: 30px; }
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
    .metric-label { color: #9ca3af; font-size: 0.9rem; font-weight: 600; margin-bottom: 8px; }
    .metric-value { color: #ffffff; font-size: 2rem; font-weight: 800; line-height: 1.1; }
    .metric-help { color: #6b7280; font-size: 0.78rem; margin-top: 8px; }
    .positive { color: #22c55e; }
    .negative { color: #ef4444; }
    .neutral { color: #38bdf8; }
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
    .insight-box {
        background: linear-gradient(135deg, #111827 0%, #172554 100%);
        border: 1px solid rgba(96,165,250,0.25);
        border-radius: 16px;
        padding: 18px;
        color: #f9fafb;
        min-height: 105px;
    }
    .footer-note { color: #6b7280; font-size: 0.85rem; margin-top: 40px; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HELPERS
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


def safe_idx_value(series, mode="max"):
    if series.empty:
        return "N/A", 0
    if mode == "max":
        idx = series.idxmax()
        return idx, series.max()
    idx = series.idxmin()
    return idx, series.min()


def prepare_dataframe(df, initial_capital):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour
    df["day"] = df["date"].dt.date
    df["weekday"] = df["date"].dt.day_name()
    df = df.sort_values("date").reset_index(drop=True)
    df["equity"] = df["net_pnl"].cumsum() + initial_capital
    df["equity_peak"] = df["equity"].cummax()
    df["drawdown"] = df["equity"] - df["equity_peak"]
    return df

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙️ Risk Settings")

initial_capital = st.sidebar.number_input("Capital inicial", value=1000.0, step=100.0)
max_daily_loss = st.sidebar.number_input("Limite de perda diária", value=500.0, step=50.0)
max_drawdown_limit = st.sidebar.number_input("Limite máximo de drawdown", value=2000.0, step=100.0)
profit_target = st.sidebar.number_input("Meta da Prop Firm", value=3000.0, step=100.0)

st.sidebar.markdown("---")
page = st.sidebar.radio("Navegação", ["Dashboard", "Histórico"])
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
# HISTORY PAGE
# =========================

if page == "Histórico":
    section("Histórico de Uploads")

    history = load_upload_history()

    if history.empty:
        st.info("Ainda não há uploads salvos.")
        st.stop()

    st.dataframe(history, use_container_width=True)

    selected_id = st.selectbox(
        "Selecione um upload para visualizar",
        options=history["id"].tolist()
    )

    if selected_id:
        selected_df = load_upload_by_id(selected_id)

        if selected_df.empty:
            st.warning("Não encontrei dados desse upload.")
        else:
            selected_df = prepare_dataframe(selected_df, initial_capital)
            metrics = calculate_metrics(selected_df, initial_capital)

            section("Resumo do Upload Selecionado")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(metric_card("💰 Net P&L", money(metrics["net_pnl"]), "Resultado líquido", "positive" if metrics["net_pnl"] >= 0 else "negative"), unsafe_allow_html=True)
            with c2:
                st.markdown(metric_card("🎯 Winrate", percent(metrics["winrate"]), "Trades vencedores", "neutral"), unsafe_allow_html=True)
            with c3:
                st.markdown(metric_card("📈 Profit Factor", f"{metrics['profit_factor']:.2f}", "Acima de 1 é positivo", "positive" if metrics["profit_factor"] >= 1 else "negative"), unsafe_allow_html=True)
            with c4:
                st.markdown(metric_card("⚠️ Max DD", money(metrics["max_drawdown"]), "Maior drawdown", "neutral"), unsafe_allow_html=True)

            fig = px.line(selected_df, x="date", y="equity", title="Equity Curve — Upload Salvo")
            fig.update_layout(template="plotly_dark", height=450)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(selected_df, use_container_width=True)

    st.stop()

# =========================
# DASHBOARD PAGE
# =========================

uploaded_file = st.file_uploader("Upload do relatório de trades", type=["csv", "xlsx"])

if uploaded_file:
    try:
        raw_df = load_trading_file(uploaded_file)

        section("1. Dados Originais")
        st.dataframe(raw_df, use_container_width=True)

        normalized_df = normalize_trades(raw_df)
        normalized_df = prepare_dataframe(normalized_df, initial_capital)

        section("2. Informações do Upload")

        u1, u2, u3 = st.columns(3)
        with u1:
            account_name = st.text_input("Nome da conta", value="Conta Principal")
        with u2:
            platform_name = st.selectbox("Plataforma", ["MT5", "Profit", "TradingView", "NinjaTrader", "Outro"])
        with u3:
            st.write("")
            st.write("")
            save_clicked = st.button("💾 Salvar análise no histórico")

        # =========================
        # FILTERS
        # =========================

        section("3. Filtros")

        f1, f2, f3 = st.columns(3)

        min_date = normalized_df["date"].dt.date.min()
        max_date = normalized_df["date"].dt.date.max()

        with f1:
            date_range = st.date_input("Período", value=(min_date, max_date), min_value=min_date, max_value=max_date)

        assets = sorted(normalized_df["asset"].dropna().astype(str).unique().tolist())
        sides = sorted(normalized_df["side"].dropna().astype(str).unique().tolist())

        with f2:
            selected_assets = st.multiselect("Ativos", options=assets, default=assets)

        with f3:
            selected_sides = st.multiselect("Lado", options=sides, default=sides)

        filtered_df = normalized_df.copy()

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df["date"].dt.date >= start_date) &
                (filtered_df["date"].dt.date <= end_date)
            ]

        filtered_df = filtered_df[filtered_df["asset"].astype(str).isin(selected_assets)]
        filtered_df = filtered_df[filtered_df["side"].astype(str).isin(selected_sides)]

        if filtered_df.empty:
            st.warning("Nenhum trade encontrado com os filtros selecionados.")
            st.stop()

        filtered_df = prepare_dataframe(filtered_df, initial_capital)
        metrics = calculate_metrics(filtered_df, initial_capital)

        if save_clicked:
            save_upload(
                account_name=account_name,
                platform=platform_name,
                file_name=uploaded_file.name,
                trades_df=normalized_df,
                metrics=calculate_metrics(normalized_df, initial_capital)
            )
            st.success("Análise salva no histórico com sucesso.")

        expectancy = metrics.get("expectancy", 0)
        recovery_factor = metrics.get("recovery_factor", 0)
        payoff_ratio = metrics.get("payoff_ratio", 0)

        net_status = "positive" if metrics["net_pnl"] >= 0 else "negative"
        pf_status = "positive" if metrics["profit_factor"] >= 1 else "negative"
        dd_status = "negative" if metrics["max_drawdown"] >= max_drawdown_limit else "neutral"

        section("4. Resumo Geral")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(metric_card("💰 Net P&L", money(metrics["net_pnl"]), "Resultado líquido total", net_status), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("🎯 Winrate", percent(metrics["winrate"]), "Percentual de trades vencedores", "neutral"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("📈 Profit Factor", f"{metrics['profit_factor']:.2f}", "Acima de 1 é positivo", pf_status), unsafe_allow_html=True)
        with c4:
            st.markdown(metric_card("⚠️ Max Drawdown", money(metrics["max_drawdown"]), "Maior queda da curva", dd_status), unsafe_allow_html=True)

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

        section("5. Insights Automáticos")

        hourly_sum = filtered_df.groupby("hour")["net_pnl"].sum()
        best_hour, best_hour_pnl = safe_idx_value(hourly_sum, "max")
        worst_hour, worst_hour_pnl = safe_idx_value(hourly_sum, "min")

        weekday_sum = filtered_df.groupby("weekday")["net_pnl"].sum()
        best_day, best_day_pnl = safe_idx_value(weekday_sum, "max")
        worst_day, worst_day_pnl = safe_idx_value(weekday_sum, "min")

        i1, i2, i3, i4 = st.columns(4)
        with i1:
            st.markdown(f'<div class="insight-box"><div class="metric-label">Melhor horário</div><div class="metric-value positive">{best_hour}h</div><div class="metric-help">Resultado: {money(best_hour_pnl)}</div></div>', unsafe_allow_html=True)
        with i2:
            st.markdown(f'<div class="insight-box"><div class="metric-label">Pior horário</div><div class="metric-value negative">{worst_hour}h</div><div class="metric-help">Resultado: {money(worst_hour_pnl)}</div></div>', unsafe_allow_html=True)
        with i3:
            st.markdown(f'<div class="insight-box"><div class="metric-label">Melhor dia</div><div class="metric-value positive">{best_day}</div><div class="metric-help">Resultado: {money(best_day_pnl)}</div></div>', unsafe_allow_html=True)
        with i4:
            st.markdown(f'<div class="insight-box"><div class="metric-label">Pior dia</div><div class="metric-value negative">{worst_day}</div><div class="metric-help">Resultado: {money(worst_day_pnl)}</div></div>', unsafe_allow_html=True)

        section("6. Painel Prop Firm")

        remaining_target = profit_target - metrics["net_pnl"]
        daily_worst = filtered_df.groupby("day")["net_pnl"].sum().min()
        daily_remaining = max_daily_loss - abs(daily_worst)
        max_dd_remaining = max_drawdown_limit - abs(metrics["max_drawdown"])

        prop1, prop2, prop3 = st.columns(3)
        with prop1:
            st.markdown(f'<div class="prop-card"><div class="metric-label">🎯 Distância da Meta</div><div class="metric-value neutral">{money(remaining_target)}</div><div class="metric-help">Faltam para atingir o objetivo configurado</div></div>', unsafe_allow_html=True)
        with prop2:
            st.markdown(f'<div class="prop-card"><div class="metric-label">⚠️ Daily DD Restante</div><div class="metric-value {"negative" if daily_remaining < 0 else "neutral"}">{money(daily_remaining)}</div><div class="metric-help">Margem restante até o limite diário</div></div>', unsafe_allow_html=True)
        with prop3:
            st.markdown(f'<div class="prop-card"><div class="metric-label">🛑 Max DD Restante</div><div class="metric-value {"negative" if max_dd_remaining < 0 else "neutral"}">{money(max_dd_remaining)}</div><div class="metric-help">Margem restante até o drawdown máximo</div></div>', unsafe_allow_html=True)

        section("7. Curva de Capital")
        fig_equity = px.line(filtered_df, x="date", y="equity", title="Equity Curve")
        fig_equity.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_equity, use_container_width=True)

        section("8. Drawdown")
        fig_dd = px.area(filtered_df, x="date", y="drawdown", title="Drawdown")
        fig_dd.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_dd, use_container_width=True)

        section("9. Resultado por Dia")
        daily_pnl = filtered_df.groupby("day")["net_pnl"].sum().reset_index()
        fig_daily = px.bar(daily_pnl, x="day", y="net_pnl", title="Daily P&L")
        fig_daily.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_daily, use_container_width=True)

        section("10. Resultado por Hora")
        hourly = filtered_df.groupby("hour")["net_pnl"].sum().reset_index()
        fig_hour = px.bar(hourly, x="hour", y="net_pnl", title="Resultado por Hora")
        fig_hour.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_hour, use_container_width=True)

        section("11. Resultado por Dia da Semana")
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = filtered_df.groupby("weekday")["net_pnl"].sum().reset_index()
        weekday["weekday"] = pd.Categorical(weekday["weekday"], categories=weekday_order, ordered=True)
        weekday = weekday.sort_values("weekday")
        fig_weekday = px.bar(weekday, x="weekday", y="net_pnl", title="Resultado por Dia da Semana")
        fig_weekday.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_weekday, use_container_width=True)

        section("12. Resultado por Ativo")
        asset = filtered_df.groupby("asset")["net_pnl"].sum().reset_index()
        fig_asset = px.bar(asset, x="asset", y="net_pnl", title="P&L por Ativo")
        fig_asset.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_asset, use_container_width=True)

        section("13. Alertas de Risco")
        alerts = generate_risk_alerts(filtered_df, max_daily_loss, max_drawdown_limit)
        for alert in alerts:
            st.markdown(f'<div class="alert-box">⚠️ {alert}</div>', unsafe_allow_html=True)

        if metrics["profit_factor"] < 1:
            st.error("Profit Factor abaixo de 1. Você está perdendo mais do que ganha.")

        if payoff_ratio < 1:
            st.warning("Seu payoff está abaixo de 1. Seus losses estão maiores que seus gains.")

        section("14. Dados Normalizados")
        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Baixar dados filtrados normalizados",
            csv,
            "riskpilot_filtered_trades.csv",
            "text/csv"
        )

        st.markdown('<div class="footer-note">RiskPilot MVP — Trading risk analytics for serious traders.</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

else:
    st.info("Envie um arquivo CSV ou XLSX para começar.")
