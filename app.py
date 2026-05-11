import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import bcrypt

from core.loader import load_trading_file
from core.normalizer import normalize_trades
from core.metrics import calculate_metrics
from core.risk_engine import generate_risk_alerts

from core.db import (
    init_db,
    save_upload,
    load_upload_history,
    load_upload_by_id,
    create_user,
    get_user_by_email
)

from core.i18n import get_translations


# =========================
# INIT
# =========================

init_db()

st.set_page_config(
    page_title="RiskPilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# CSS — INSTITUTIONAL TERMINAL
# =========================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #050816 !important;
    color: #ffffff !important;
}

[data-testid="stHeader"] {
    background: rgba(5,8,22,0.98) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060b18 0%, #0b1020 100%) !important;
    border-right: 1px solid rgba(148,163,184,0.12);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: inherit;
}

/* Sidebar premium cards */
.sidebar-brand {
    background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(15,23,42,0.9));
    border: 1px solid rgba(56,189,248,0.30);
    border-radius: 22px;
    padding: 20px 18px;
    margin-bottom: 18px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.24);
}

.sidebar-logo {
    font-size: 1.55rem;
    font-weight: 950;
    letter-spacing: -0.04em;
    color: #ffffff !important;
}

.sidebar-subtitle {
    color: #93c5fd !important;
    font-size: 0.82rem;
    margin-top: 4px;
    line-height: 1.35;
}

.sidebar-user-card {
    background: #0f172a;
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 18px;
    padding: 16px;
    margin: 14px 0 18px 0;
}

.sidebar-user-label {
    color: #94a3b8 !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
}

.sidebar-user-value {
    color: #ffffff !important;
    font-size: 0.92rem;
    margin-top: 5px;
    word-break: break-word;
}

.sidebar-kpi {
    background: rgba(15,23,42,0.88);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 15px;
    padding: 13px 14px;
    margin-bottom: 10px;
}

.sidebar-kpi-title {
    color: #94a3b8 !important;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.sidebar-kpi-value {
    color: #ffffff !important;
    font-size: 1.15rem;
    font-weight: 900;
    margin-top: 4px;
}

.sidebar-note {
    color: #64748b !important;
    font-size: 0.78rem;
    line-height: 1.45;
    margin-top: 12px;
}

/* Homepage */
.hero-wrap {
    padding-top: 25px;
    padding-bottom: 30px;
}

.hero-title {
    font-size: clamp(3.2rem, 6vw, 5.8rem);
    font-weight: 950;
    line-height: 1.08;
    letter-spacing: -0.06em;
    color: #ffffff !important;
    margin-bottom: 26px;
    max-width: 820px;
}

.hero-subtitle {
    font-size: 1.25rem;
    line-height: 1.75;
    color: #b6c2d2 !important;
    margin-top: 18px;
    margin-bottom: 34px;
    max-width: 780px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.35);
    color: #7dd3fc !important;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 20px;
}

.hero-image-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,41,59,0.45));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 26px;
    padding: 14px;
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}

.feature-card {
    background: linear-gradient(135deg,#101827 0%,#172033 100%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 30px;
    min-height: 230px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.23);
}

.feature-card h3 {
    color: #ffffff !important;
    font-size: 1.45rem;
    margin-bottom: 15px;
}

.feature-card p {
    color: #b6c2d2 !important;
    font-size: 1rem;
    line-height: 1.65;
}

/* App components */
.metric-card {
    background: linear-gradient(135deg,#111827 0%,#1f2937 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 24px;
    min-height: 125px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.metric-title {
    color: #9ca3af !important;
    font-size: 0.9rem;
    font-weight: 700;
}

.metric-value {
    color: #ffffff !important;
    font-size: 2rem;
    font-weight: 850;
    margin-top: 6px;
}

.metric-sub {
    color: #64748b !important;
    font-size: 0.82rem;
    margin-top: 6px;
}

.section-title {
    font-size: 2rem;
    font-weight: 850;
    color: #ffffff !important;
    margin-top: 60px;
    margin-bottom: 24px;
    letter-spacing: -0.035em;
}

.alert-box {
    background: #1f2937;
    border-left: 5px solid #f59e0b;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #ffffff !important;
}

.insight-card {
    background: linear-gradient(135deg,#0f172a 0%,#172554 100%);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 18px;
    padding: 22px;
    min-height: 126px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.insight-title {
    color: #94a3b8 !important;
    font-size: 0.88rem;
    font-weight: 750;
}

.insight-value {
    color: #ffffff !important;
    font-size: 1.65rem;
    font-weight: 850;
    margin-top: 8px;
}

.insight-sub {
    color: #7dd3fc !important;
    font-size: 0.85rem;
    margin-top: 8px;
}

.auth-box {
    max-width: 620px;
    margin: 30px auto;
    background: linear-gradient(135deg,#101827 0%,#172033 100%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 26px;
    padding: 35px;
}

.chart-card {
    background: #0b1020;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 22px;
    padding: 12px 12px 2px 12px;
    margin-bottom: 22px;
}

.terminal-header {
    background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(2,6,23,0.78));
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 26px;
    padding: 26px 30px;
    margin-bottom: 30px;
    box-shadow: 0 20px 70px rgba(0,0,0,0.28);
}

.terminal-title {
    color: #ffffff !important;
    font-size: 2.65rem;
    font-weight: 950;
    letter-spacing: -0.055em;
    line-height: 1.05;
}

.terminal-subtitle {
    color: #94a3b8 !important;
    font-size: 1rem;
    margin-top: 8px;
}

.terminal-pill {
    display: inline-block;
    background: rgba(34,197,94,0.12);
    color: #86efac !important;
    border: 1px solid rgba(34,197,94,0.28);
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 0.78rem;
    font-weight: 800;
    margin-top: 12px;
}

.stButton > button {
    border-radius: 14px;
    min-height: 52px;
    font-weight: 800;
    font-size: 1rem;
    border: 1px solid rgba(255,255,255,0.15);
    background: #0f172a !important;
    color: #ffffff !important;
}

.stButton > button:hover {
    border-color: #38bdf8 !important;
    color: #7dd3fc !important;
}

input, textarea, select {
    color: #ffffff !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div,
[data-testid="stDateInput"] input {
    background: #111827 !important;
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HELPERS
# =========================

def money(v):
    try:
        return f"${float(v):,.2f}"
    except Exception:
        return "$0.00"


def percent(v):
    try:
        return f"{float(v):.2f}%"
    except Exception:
        return "0.00%"


def metric_card(title, value, sub=""):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """


def insight_card(title, value, sub=""):
    return f"""
    <div class="insight-card">
        <div class="insight-title">{title}</div>
        <div class="insight-value">{value}</div>
        <div class="insight-sub">{sub}</div>
    </div>
    """


def sidebar_kpi(title, value):
    return f"""
    <div class="sidebar-kpi">
        <div class="sidebar-kpi-title">{title}</div>
        <div class="sidebar-kpi-value">{value}</div>
    </div>
    """


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def chart_wrap_start():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)


def chart_wrap_end():
    st.markdown('</div>', unsafe_allow_html=True)


def prepare_dataframe(df, initial_capital):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["net_pnl"] = pd.to_numeric(df["net_pnl"], errors="coerce").fillna(0)

    df["hour"] = df["date"].dt.hour
    df["day"] = df["date"].dt.date
    df["weekday"] = df["date"].dt.day_name()

    df = df.sort_values("date").reset_index(drop=True)

    df["equity"] = df["net_pnl"].cumsum() + initial_capital
    df["equity_peak"] = df["equity"].cummax()
    df["drawdown"] = df["equity"] - df["equity_peak"]

    return df


def smooth_series(series, window=5):
    if len(series) < window:
        return series
    return series.rolling(window=window, min_periods=1).mean()


def base_chart_layout(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=20, r=20, t=55, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title=dict(font=dict(size=18, color="#ffffff")),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color="#cbd5e1")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.16)", zeroline=False, color="#cbd5e1")
    return fig


def make_equity_chart(df):
    chart_df = df.copy()
    chart_df["equity_smooth"] = smooth_series(chart_df["equity"], window=6)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["date"],
            y=chart_df["equity"],
            mode="lines",
            name="Equity",
            line=dict(width=1.4, color="rgba(56,189,248,0.28)"),
            hovertemplate="%{y:.2f}<extra>Equity</extra>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_df["date"],
            y=chart_df["equity_smooth"],
            mode="lines",
            name="Smoothed Equity",
            line=dict(width=3.2, color="#38bdf8", shape="spline", smoothing=1.2),
            hovertemplate="%{y:.2f}<extra>Smoothed</extra>"
        )
    )

    return base_chart_layout(fig, height=430)


def make_drawdown_chart(df):
    chart_df = df.copy()
    chart_df["drawdown_smooth"] = smooth_series(chart_df["drawdown"], window=6)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["date"],
            y=chart_df["drawdown_smooth"],
            mode="lines",
            name="Drawdown",
            line=dict(width=3, color="#fb7185", shape="spline", smoothing=1.1),
            fill="tozeroy",
            fillcolor="rgba(251,113,133,0.18)",
            hovertemplate="%{y:.2f}<extra>Drawdown</extra>"
        )
    )

    return base_chart_layout(fig, height=360)


def make_bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_traces(marker_color="#38bdf8", marker_line_width=0)
    return base_chart_layout(fig, height=340)


def make_demo_dataframe():
    data = [
        {"date": "2026-03-17 09:31:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 182565, "exit_price": 182565, "pnl": 12, "fees": 0, "net_pnl": 12},
        {"date": "2026-03-17 09:52:00", "asset": "WIN", "side": "sell", "quantity": 1, "entry_price": 182135, "exit_price": 182135, "pnl": -35, "fees": 0, "net_pnl": -35},
        {"date": "2026-03-17 10:45:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 184115, "exit_price": 184115, "pnl": -40, "fees": 0, "net_pnl": -40},
        {"date": "2026-03-18 09:43:00", "asset": "WIN", "side": "sell", "quantity": 1, "entry_price": 181690, "exit_price": 181690, "pnl": 19, "fees": 0, "net_pnl": 19},
        {"date": "2026-03-18 10:10:00", "asset": "WIN", "side": "sell", "quantity": 2, "entry_price": 181350, "exit_price": 181350, "pnl": -74, "fees": 0, "net_pnl": -74},
        {"date": "2026-03-19 09:20:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 183400, "exit_price": 183400, "pnl": 83, "fees": 0, "net_pnl": 83},
        {"date": "2026-03-20 11:20:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 184200, "exit_price": 184200, "pnl": -71, "fees": 0, "net_pnl": -71},
        {"date": "2026-03-24 09:10:00", "asset": "WIN", "side": "sell", "quantity": 1, "entry_price": 185000, "exit_price": 185000, "pnl": 92, "fees": 0, "net_pnl": 92},
        {"date": "2026-03-25 10:50:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 185300, "exit_price": 185300, "pnl": -76, "fees": 0, "net_pnl": -76},
        {"date": "2026-03-27 09:25:00", "asset": "WIN", "side": "sell", "quantity": 1, "entry_price": 186100, "exit_price": 186100, "pnl": 94, "fees": 0, "net_pnl": 94},
        {"date": "2026-04-01 10:15:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 187200, "exit_price": 187200, "pnl": -70, "fees": 0, "net_pnl": -70},
        {"date": "2026-04-02 09:55:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 187900, "exit_price": 187900, "pnl": 22, "fees": 0, "net_pnl": 22},
        {"date": "2026-04-07 09:40:00", "asset": "WIN", "side": "sell", "quantity": 1, "entry_price": 188200, "exit_price": 188200, "pnl": 78, "fees": 0, "net_pnl": 78},
        {"date": "2026-04-08 10:35:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 188550, "exit_price": 188550, "pnl": -76, "fees": 0, "net_pnl": -76},
        {"date": "2026-04-14 09:15:00", "asset": "WIN", "side": "sell", "quantity": 1, "entry_price": 189000, "exit_price": 189000, "pnl": 89, "fees": 0, "net_pnl": 89},
        {"date": "2026-04-15 10:45:00", "asset": "WIN", "side": "buy", "quantity": 1, "entry_price": 189300, "exit_price": 189300, "pnl": -12, "fees": 0, "net_pnl": -12},
    ]
    return pd.DataFrame(data)


# =========================
# SESSION STATE
# =========================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

if "landing_language" not in st.session_state:
    st.session_state.landing_language = "English"


# =========================
# HOMEPAGE
# =========================

if not st.session_state.authenticated and not st.session_state.show_login and not st.session_state.demo_mode:
    top1, top2, top3 = st.columns([1, 4, 1])

    with top1:
        selected_language = st.selectbox(
            "Language",
            ["English", "Português", "Español"],
            index=["English", "Português", "Español"].index(st.session_state.landing_language)
        )
        st.session_state.landing_language = selected_language

    if st.session_state.landing_language == "Português":
        hero_title = "Analytics institucional para traders"
        hero_subtitle = "Plataforma profissional de análise operacional focada em risco, consistência, performance e aprovação em prop firms."
        badge = "Infraestrutura de risco para traders sérios"
        start_text = "🚀 Criar conta grátis"
        login_text = "🔐 Entrar"
        demo_text = "📊 Ver demo"
        why_title = "Por que RiskPilot?"
        f1_title = "📉 Inteligência de Risco"
        f1_text = "Detecte drawdowns perigosos, overtrading, revenge trading e sequências ruins automaticamente."
        f2_title = "🏆 Pronto para Prop Firms"
        f2_text = "Acompanhe perda diária, drawdown máximo, consistência e distância até a meta."
        f3_title = "🤖 Insights Operacionais"
        f3_text = "Descubra seus melhores horários, piores padrões e fraquezas operacionais."
    elif st.session_state.landing_language == "Español":
        hero_title = "Analytics institucional para traders"
        hero_subtitle = "Plataforma profesional de análisis operativo enfocada en riesgo, consistencia, rendimiento y aprobación en prop firms."
        badge = "Infraestructura de riesgo para traders serios"
        start_text = "🚀 Crear cuenta gratis"
        login_text = "🔐 Entrar"
        demo_text = "📊 Ver demo"
        why_title = "¿Por qué RiskPilot?"
        f1_title = "📉 Inteligencia de Riesgo"
        f1_text = "Detecta drawdowns peligrosos, overtrading, revenge trading y secuencias negativas automáticamente."
        f2_title = "🏆 Listo para Prop Firms"
        f2_text = "Monitorea pérdida diaria, drawdown máximo, consistencia y distancia a la meta."
        f3_title = "🤖 Insights Operativos"
        f3_text = "Descubre tus mejores horarios, peores patrones y debilidades operativas."
    else:
        hero_title = "Institutional trading analytics"
        hero_subtitle = "Professional-grade trading analytics platform focused on risk, consistency, performance and prop firm approval."
        badge = "Risk infrastructure for serious traders"
        start_text = "🚀 Start free"
        login_text = "🔐 Login"
        demo_text = "📊 View demo"
        why_title = "Why RiskPilot?"
        f1_title = "📉 Risk Intelligence"
        f1_text = "Detect dangerous drawdowns, overtrading, revenge trading and losing streaks automatically."
        f2_title = "🏆 Prop Firm Ready"
        f2_text = "Track daily loss, max drawdown, consistency and target distance."
        f3_title = "🤖 Operational Insights"
        f3_text = "Discover your best hours, worst patterns and operational weaknesses."

    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.25, 1])

    with col1:
        st.markdown(f'<div class="hero-badge">⚡ {badge}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-title">{hero_title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{hero_subtitle}</div>', unsafe_allow_html=True)

        b1, b2, b3 = st.columns([1, 1, 1])

        with b1:
            if st.button(start_text):
                st.session_state.auth_mode = "Register"
                st.session_state.show_login = True
                st.rerun()

        with b2:
            if st.button(login_text):
                st.session_state.auth_mode = "Login"
                st.session_state.show_login = True
                st.rerun()

        with b3:
            if st.button(demo_text):
                st.session_state.demo_mode = True
                st.rerun()

    with col2:
        st.markdown('<div class="hero-image-card">', unsafe_allow_html=True)
        st.image(
            "https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1200&auto=format&fit=crop",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">{why_title}</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown(
            f"""
            <div class="feature-card">
                <h3>{f1_title}</h3>
                <p>{f1_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            f"""
            <div class="feature-card">
                <h3>{f2_title}</h3>
                <p>{f2_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            f"""
            <div class="feature-card">
                <h3>{f3_title}</h3>
                <p>{f3_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.stop()


# =========================
# LOGIN / REGISTER
# =========================

if not st.session_state.authenticated and st.session_state.show_login:
    st.markdown('<div class="auth-box">', unsafe_allow_html=True)
    st.title("🔐 RiskPilot")

    auth_mode = st.radio(
        "Choose",
        ["Login", "Register"],
        index=0 if st.session_state.auth_mode == "Login" else 1
    )

    if auth_mode == "Register":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            existing = get_user_by_email(email)

            if existing:
                st.error("User already exists.")
            else:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                create_user(name, email, hashed)
                st.success("Account created successfully. You can now login.")

    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = get_user_by_email(email)

            if not user:
                st.error("Invalid credentials.")
            else:
                valid = bcrypt.checkpw(password.encode(), user["password"].encode())

                if valid:
                    st.session_state.authenticated = True
                    st.session_state.user_email = user["email"]
                    st.session_state.show_login = False
                    st.session_state.demo_mode = False
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

    if st.button("← Back to homepage"):
        st.session_state.show_login = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# =========================
# SIDEBAR APP
# =========================

language = st.sidebar.selectbox(
    "Language / Idioma",
    ["English", "Português", "Español"],
    index=["English", "Português", "Español"].index(st.session_state.landing_language)
)

st.session_state.landing_language = language
t = get_translations(language)

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-logo">📊 RiskPilot</div>
        <div class="sidebar-subtitle">Professional Trading Analytics</div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.authenticated:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-user-card">
            <div class="sidebar-user-label">Authenticated user</div>
            <div class="sidebar-user-value">{st.session_state.user_email}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.show_login = False
        st.session_state.demo_mode = False
        st.session_state.user_email = None
        st.rerun()
else:
    st.sidebar.markdown(
        """
        <div class="sidebar-user-card">
            <div class="sidebar-user-label">Current mode</div>
            <div class="sidebar-user-value">Demo Mode</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("Create free account"):
        st.session_state.demo_mode = False
        st.session_state.auth_mode = "Register"
        st.session_state.show_login = True
        st.rerun()

initial_capital = st.sidebar.number_input(
    t.get("initial_capital", "Initial Capital"),
    value=1000.0
)

max_daily_loss = st.sidebar.number_input(
    t.get("daily_loss_limit", "Daily Loss Limit"),
    value=500.0
)

max_drawdown_limit = st.sidebar.number_input(
    t.get("max_drawdown_limit", "Max Drawdown"),
    value=2000.0
)

page = st.sidebar.radio(
    t.get("navigation", "Navigation"),
    [t.get("dashboard", "Dashboard"), t.get("history", "History")]
)

st.sidebar.markdown("---")
st.sidebar.markdown(sidebar_kpi("Account status", "Active"), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_kpi("Risk mode", "Prop firm"), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_kpi("Analytics", "Enabled"), unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-note">RiskPilot monitors performance, drawdown, behavior and operational consistency.</div>',
    unsafe_allow_html=True
)


# =========================
# HISTORY
# =========================

if page == t.get("history", "History"):
    st.title("📚 " + t.get("history_uploads", "Upload History"))

    if not st.session_state.authenticated:
        st.info("History is available after creating a free account.")
        st.stop()

    history = load_upload_history(st.session_state.user_email)

    if history.empty:
        st.info(t.get("no_saved_uploads", "No uploads yet."))
        st.stop()

    st.dataframe(history, use_container_width=True)
    st.stop()


# =========================
# DASHBOARD
# =========================

st.markdown(
    """
    <div class="terminal-header">
        <div class="terminal-title">RiskPilot Terminal</div>
        <div class="terminal-subtitle">Institutional-grade trading risk intelligence and performance analytics.</div>
        <div class="terminal-pill">LIVE ANALYTICS ENGINE</div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.demo_mode and not st.session_state.authenticated:
    st.info("Demo mode: sample data loaded. Create a free account to upload and save your own trading reports.")
    normalized_df = prepare_dataframe(make_demo_dataframe(), initial_capital)
    uploaded_file_name = "demo_data.csv"
else:
    uploaded_file = st.file_uploader(
        t.get("upload_report", "Upload trading report"),
        type=["csv", "xlsx"]
    )

    if not uploaded_file:
        st.info(t.get("send_file_to_start", "Upload a CSV or XLSX report to begin."))
        st.stop()

    try:
        raw_df = load_trading_file(uploaded_file)
        normalized_df = normalize_trades(raw_df)
        normalized_df = prepare_dataframe(normalized_df, initial_capital)
        uploaded_file_name = uploaded_file.name
    except Exception as e:
        st.error(f'{t.get("file_error", "Error reading file")}: {e}')
        st.stop()

metrics = calculate_metrics(normalized_df, initial_capital)

# =========================
# PERFORMANCE OVERVIEW
# =========================

section("Performance Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(metric_card("Net P&L", money(metrics["net_pnl"]), "Total net result"), unsafe_allow_html=True)

with c2:
    st.markdown(metric_card("Winrate", percent(metrics["winrate"]), "Winning trades"), unsafe_allow_html=True)

with c3:
    st.markdown(metric_card("Profit Factor", f"{metrics['profit_factor']:.2f}", "Gross profit / gross loss"), unsafe_allow_html=True)

with c4:
    st.markdown(metric_card("Max Drawdown", money(metrics["max_drawdown"]), "Largest equity decline"), unsafe_allow_html=True)

# =========================
# ADVANCED INSIGHTS
# =========================

section("Automatic Insights")

hourly = normalized_df.groupby("hour")["net_pnl"].sum()
daily = normalized_df.groupby("day")["net_pnl"].sum()
weekday = normalized_df.groupby("weekday")["net_pnl"].sum()

best_hour = hourly.idxmax() if not hourly.empty else "N/A"
best_hour_pnl = hourly.max() if not hourly.empty else 0
worst_hour = hourly.idxmin() if not hourly.empty else "N/A"
worst_hour_pnl = hourly.min() if not hourly.empty else 0

best_day = daily.idxmax() if not daily.empty else "N/A"
best_day_pnl = daily.max() if not daily.empty else 0
worst_day = daily.idxmin() if not daily.empty else "N/A"
worst_day_pnl = daily.min() if not daily.empty else 0

best_weekday = weekday.idxmax() if not weekday.empty else "N/A"
best_weekday_pnl = weekday.max() if not weekday.empty else 0
worst_weekday = weekday.idxmin() if not weekday.empty else "N/A"
worst_weekday_pnl = weekday.min() if not weekday.empty else 0

ic1, ic2, ic3, ic4 = st.columns(4)

with ic1:
    st.markdown(insight_card("Best Hour", f"{best_hour}h", money(best_hour_pnl)), unsafe_allow_html=True)

with ic2:
    st.markdown(insight_card("Worst Hour", f"{worst_hour}h", money(worst_hour_pnl)), unsafe_allow_html=True)

with ic3:
    st.markdown(insight_card("Best Day", str(best_day), money(best_day_pnl)), unsafe_allow_html=True)

with ic4:
    st.markdown(insight_card("Worst Day", str(worst_day), money(worst_day_pnl)), unsafe_allow_html=True)

ic5, ic6, ic7, ic8 = st.columns(4)

with ic5:
    st.markdown(insight_card("Best Weekday", str(best_weekday), money(best_weekday_pnl)), unsafe_allow_html=True)

with ic6:
    st.markdown(insight_card("Worst Weekday", str(worst_weekday), money(worst_weekday_pnl)), unsafe_allow_html=True)

with ic7:
    positive_days = int((daily > 0).sum()) if not daily.empty else 0
    st.markdown(insight_card("Positive Days", positive_days, "Days above zero"), unsafe_allow_html=True)

with ic8:
    negative_days = int((daily < 0).sum()) if not daily.empty else 0
    st.markdown(insight_card("Negative Days", negative_days, "Days below zero"), unsafe_allow_html=True)

# =========================
# CHARTS
# =========================

section("Equity Curve")
chart_wrap_start()
st.plotly_chart(make_equity_chart(normalized_df), use_container_width=True)
chart_wrap_end()

section("Drawdown")
chart_wrap_start()
st.plotly_chart(make_drawdown_chart(normalized_df), use_container_width=True)
chart_wrap_end()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    section("Daily P&L")
    daily_df = daily.reset_index()
    daily_df.columns = ["day", "net_pnl"]
    chart_wrap_start()
    st.plotly_chart(make_bar_chart(daily_df, "day", "net_pnl", "Daily P&L"), use_container_width=True)
    chart_wrap_end()

with chart_col2:
    section("P&L by Hour")
    hourly_df = hourly.reset_index()
    hourly_df.columns = ["hour", "net_pnl"]
    chart_wrap_start()
    st.plotly_chart(make_bar_chart(hourly_df, "hour", "net_pnl", "P&L by Hour"), use_container_width=True)
    chart_wrap_end()

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    section("P&L by Weekday")
    weekday_df = weekday.reset_index()
    weekday_df.columns = ["weekday", "net_pnl"]
    chart_wrap_start()
    st.plotly_chart(make_bar_chart(weekday_df, "weekday", "net_pnl", "P&L by Weekday"), use_container_width=True)
    chart_wrap_end()

with chart_col4:
    section("P&L by Asset")
    asset_df = normalized_df.groupby("asset")["net_pnl"].sum().reset_index()
    chart_wrap_start()
    st.plotly_chart(make_bar_chart(asset_df, "asset", "net_pnl", "P&L by Asset"), use_container_width=True)
    chart_wrap_end()

# =========================
# ALERTS
# =========================

section("Risk Alerts")

alerts = generate_risk_alerts(
    normalized_df,
    max_daily_loss,
    max_drawdown_limit,
    language=language
)

for alert in alerts:
    st.markdown(
        f'''
        <div class="alert-box">
            ⚠️ {alert}
        </div>
        ''',
        unsafe_allow_html=True
    )

# =========================
# SAVE
# =========================

if st.session_state.authenticated:
    if st.button("💾 Save Analysis"):
        save_upload(
            account_name="Main Account",
            platform="Unknown",
            file_name=uploaded_file_name,
            trades_df=normalized_df,
            metrics=metrics,
            user_email=st.session_state.user_email
        )
        st.success("Analysis saved.")
else:
    st.warning("Create a free account to save your analysis history.")

# =========================
# DATA
# =========================

section("Trades")
st.dataframe(normalized_df, use_container_width=True)
