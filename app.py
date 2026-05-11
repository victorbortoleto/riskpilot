import streamlit as st
import pandas as pd
import plotly.express as px
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
    layout="wide"
)


# =========================
# CSS — FORCE DARK PREMIUM THEME
# =========================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #050816 !important;
    color: #ffffff !important;
}

[data-testid="stHeader"] {
    background: rgba(5,8,22,0.95) !important;
}

[data-testid="stSidebar"] {
    background: #0b1020 !important;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: inherit;
}

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

.hero-title span {
    color: #38bdf8 !important;
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

.auth-box {
    max-width: 620px;
    margin: 30px auto;
    background: linear-gradient(135deg,#101827 0%,#172033 100%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 26px;
    padding: 35px;
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


def metric_card(title, value):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


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

st.sidebar.title("⚙️ RiskPilot")

if st.session_state.authenticated:
    st.sidebar.write(f"👤 {st.session_state.user_email}")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.show_login = False
        st.session_state.demo_mode = False
        st.session_state.user_email = None
        st.rerun()
else:
    st.sidebar.write("📊 Demo Mode")

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

st.title("📊 RiskPilot Dashboard")

if st.session_state.demo_mode and not st.session_state.authenticated:
    st.info("Demo mode: sample data loaded. Create a free account to upload and save your own trading reports.")
    normalized_df = prepare_dataframe(make_demo_dataframe(), initial_capital)
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
    except Exception as e:
        st.error(f'{t.get("file_error", "Error reading file")}: {e}')
        st.stop()

metrics = calculate_metrics(normalized_df, initial_capital)

section("Performance Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(metric_card("Net P&L", money(metrics["net_pnl"])), unsafe_allow_html=True)

with c2:
    st.markdown(metric_card("Winrate", percent(metrics["winrate"])), unsafe_allow_html=True)

with c3:
    st.markdown(metric_card("Profit Factor", f"{metrics['profit_factor']:.2f}"), unsafe_allow_html=True)

with c4:
    st.markdown(metric_card("Max Drawdown", money(metrics["max_drawdown"])), unsafe_allow_html=True)

section("Equity Curve")

fig = px.line(
    normalized_df,
    x="date",
    y="equity",
    title="Equity Curve"
)
fig.update_layout(template="plotly_dark", height=500)
st.plotly_chart(fig, use_container_width=True)

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

if st.session_state.authenticated:
    if st.button("💾 Save Analysis"):
        save_upload(
            account_name="Main Account",
            platform="Unknown",
            file_name="demo_data.csv" if st.session_state.demo_mode else uploaded_file.name,
            trades_df=normalized_df,
            metrics=metrics,
            user_email=st.session_state.user_email
        )
        st.success("Analysis saved.")
else:
    st.warning("Create a free account to save your analysis history.")

section("Trades")
st.dataframe(normalized_df, use_container_width=True)
