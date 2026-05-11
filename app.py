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
# CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #050816;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

h1,h2,h3,h4 {
    color: white;
}

.hero-title {
    font-size: 4rem;
    font-weight: 900;
    line-height: 1.0;
    color: white;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #94a3b8;
    margin-top: 20px;
    margin-bottom: 40px;
}

.feature-card {
    background: linear-gradient(135deg,#111827 0%,#1f2937 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 30px;
    min-height: 220px;
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-4px);
}

.metric-card {
    background: linear-gradient(135deg,#111827 0%,#1f2937 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 24px;
}

.metric-title {
    color: #9ca3af;
    font-size: 0.9rem;
}

.metric-value {
    color: white;
    font-size: 2rem;
    font-weight: 800;
}

.section-title {
    font-size: 2rem;
    font-weight: 800;
    color: white;
    margin-top: 60px;
    margin-bottom: 25px;
}

.alert-box {
    background: #1f2937;
    border-left: 5px solid orange;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: white;
}

.stButton > button {
    border-radius: 12px;
    height: 52px;
    font-weight: 700;
    font-size: 1rem;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HELPERS
# =========================

def money(v):
    return f"${float(v):,.2f}"


def percent(v):
    return f"{float(v):.2f}%"


def metric_card(title, value):

    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def prepare_dataframe(df, initial_capital):

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["net_pnl"] = pd.to_numeric(
        df["net_pnl"],
        errors="coerce"
    ).fillna(0)

    df["hour"] = df["date"].dt.hour
    df["day"] = df["date"].dt.date

    df["equity"] = (
        df["net_pnl"].cumsum()
        + initial_capital
    )

    df["equity_peak"] = df["equity"].cummax()

    df["drawdown"] = (
        df["equity"]
        - df["equity_peak"]
    )

    return df


# =========================
# SESSION
# =========================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None


# =========================
# HOMEPAGE
# =========================

if not st.session_state.authenticated and not st.session_state.show_login:

    col1, col2 = st.columns([1.3,1])

    with col1:

        st.markdown("""
        <div class="hero-title">
        Institutional<br>
        Trading Analytics
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-subtitle">
        Professional-grade trading analytics platform focused on risk,
        performance, consistency and prop firm approval.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            if st.button("🚀 Start Free"):
                st.session_state.show_login = True
                st.rerun()

        with c2:
            if st.button("📊 Demo"):
                st.session_state.show_login = True
                st.rerun()

    with col2:

        st.image(
            "https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1200&auto=format&fit=crop",
            use_container_width=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Why RiskPilot?</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="feature-card">
        <h3>📉 Risk Intelligence</h3>
        <p>
        Detect revenge trading, overtrading,
        dangerous drawdowns and loss streaks automatically.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature-card">
        <h3>🏆 Prop Firm Ready</h3>
        <p>
        Track consistency, daily drawdown,
        max drawdown and passing probability.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature-card">
        <h3>🤖 AI Trading Insights</h3>
        <p>
        Discover your best hours, worst behaviors
        and operational weaknesses automatically.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# =========================
# LOGIN
# =========================

if not st.session_state.authenticated:

    st.title("🔐 RiskPilot")

    mode = st.radio(
        "Choose",
        ["Login", "Register"]
    )

    if mode == "Register":

        name = st.text_input("Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Create Account"):

            existing = get_user_by_email(email)

            if existing:
                st.error("User already exists.")

            else:

                hashed = bcrypt.hashpw(
                    password.encode(),
                    bcrypt.gensalt()
                ).decode()

                create_user(
                    name,
                    email,
                    hashed
                )

                st.success(
                    "Account created successfully."
                )

    else:

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = get_user_by_email(email)

            if not user:
                st.error("Invalid credentials.")

            else:

                valid = bcrypt.checkpw(
                    password.encode(),
                    user["password"].encode()
                )

                if valid:

                    st.session_state.authenticated = True
                    st.session_state.user_email = user["email"]

                    st.rerun()

                else:
                    st.error("Invalid credentials.")

    st.stop()


# =========================
# SIDEBAR
# =========================

language = st.sidebar.selectbox(
    "Language",
    ["English", "Português", "Español"]
)

t = get_translations(language)

st.sidebar.title("⚙️ RiskPilot")

st.sidebar.write(
    f"👤 {st.session_state.user_email}"
)

if st.sidebar.button("Logout"):

    st.session_state.authenticated = False
    st.session_state.show_login = False
    st.session_state.user_email = None

    st.rerun()

initial_capital = st.sidebar.number_input(
    "Initial Capital",
    value=1000.0
)

max_daily_loss = st.sidebar.number_input(
    "Daily Loss Limit",
    value=500.0
)

max_drawdown_limit = st.sidebar.number_input(
    "Max Drawdown",
    value=2000.0
)

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "History"]
)


# =========================
# HISTORY
# =========================

if page == "History":

    st.title("📚 Upload History")

    history = load_upload_history(
        st.session_state.user_email
    )

    if history.empty:
        st.info("No uploads yet.")
        st.stop()

    st.dataframe(
        history,
        use_container_width=True
    )

    st.stop()


# =========================
# DASHBOARD
# =========================

st.title("📊 RiskPilot Dashboard")

uploaded_file = st.file_uploader(
    "Upload trading report",
    type=["csv", "xlsx"]
)

if uploaded_file:

    raw_df = load_trading_file(
        uploaded_file
    )

    normalized_df = normalize_trades(
        raw_df
    )

    normalized_df = prepare_dataframe(
        normalized_df,
        initial_capital
    )

    metrics = calculate_metrics(
        normalized_df,
        initial_capital
    )

    st.markdown(
        '<div class="section-title">Performance Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            metric_card(
                "Net P&L",
                money(metrics["net_pnl"])
            ),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            metric_card(
                "Winrate",
                percent(metrics["winrate"])
            ),
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            metric_card(
                "Profit Factor",
                metrics["profit_factor"]
            ),
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            metric_card(
                "Max Drawdown",
                money(metrics["max_drawdown"])
            ),
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Equity Curve</div>',
        unsafe_allow_html=True
    )

    fig = px.line(
        normalized_df,
        x="date",
        y="equity",
        title="Equity Curve"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-title">Risk Alerts</div>',
        unsafe_allow_html=True
    )

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

    if st.button("💾 Save Analysis"):

        save_upload(
            account_name="Main Account",
            platform="Unknown",
            file_name=uploaded_file.name,
            trades_df=normalized_df,
            metrics=metrics,
            user_email=st.session_state.user_email
        )

        st.success("Analysis saved.")

    st.markdown(
        '<div class="section-title">Trades</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        normalized_df,
        use_container_width=True
    )

else:

    st.info(
        "Upload a CSV or XLSX report to begin."
    )
