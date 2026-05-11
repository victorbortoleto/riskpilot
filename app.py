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
# INIT DB
# =========================

init_db()


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="RiskPilot",
    page_icon="📊",
    layout="wide"
)


# =========================
# CSS
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

    .alert-box {
        background: #1f2937;
        border-left: 5px solid #f59e0b;
        padding: 16px 18px;
        border-radius: 12px;
        color: #f9fafb;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# HELPERS
# =========================

def money(value):
    return f"${float(value):,.2f}"


def percent(value):
    return f"{float(value):.2f}%"


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def metric_card(label, value, help_text="", status="neutral"):

    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {status}">{value}</div>
        <div class="metric-help">{help_text}</div>
    </div>
    """


def prepare_dataframe(df, initial_capital):

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(subset=["date"])

    df["net_pnl"] = pd.to_numeric(
        df["net_pnl"],
        errors="coerce"
    ).fillna(0)

    df["hour"] = df["date"].dt.hour
    df["day"] = df["date"].dt.date
    df["weekday"] = df["date"].dt.day_name()

    df = df.sort_values("date").reset_index(drop=True)

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
# AUTH
# =========================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None


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
# LANGUAGE
# =========================

language = st.sidebar.selectbox(
    "Language / Idioma",
    ["Português", "English", "Español"]
)

t = get_translations(language)


# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    f"⚙️ {t['risk_settings']}"
)

st.sidebar.write(
    f"👤 {st.session_state.user_email}"
)

if st.sidebar.button("Logout"):

    st.session_state.authenticated = False
    st.session_state.user_email = None

    st.rerun()

initial_capital = st.sidebar.number_input(
    t["initial_capital"],
    value=1000.0
)

max_daily_loss = st.sidebar.number_input(
    t["daily_loss_limit"],
    value=500.0
)

max_drawdown_limit = st.sidebar.number_input(
    t["max_drawdown_limit"],
    value=2000.0
)

profit_target = st.sidebar.number_input(
    t["profit_target"],
    value=3000.0
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    t["navigation"],
    [t["dashboard"], t["history"]]
)


# =========================
# HEADER
# =========================

st.markdown("# 📊 RiskPilot")

st.markdown(
    f'<div class="subtitle">{t["subtitle"]}</div>',
    unsafe_allow_html=True
)


# =========================
# HISTORY
# =========================

if page == t["history"]:

    section(t["history_uploads"])

    history = load_upload_history(
        st.session_state.user_email
    )

    if history.empty:
        st.info(t["no_saved_uploads"])
        st.stop()

    st.dataframe(
        history,
        use_container_width=True
    )

    selected_id = st.selectbox(
        t["select_upload"],
        history["id"].tolist()
    )

    if selected_id:

        selected_df = load_upload_by_id(
            selected_id
        )

        if not selected_df.empty:

            selected_df = prepare_dataframe(
                selected_df,
                initial_capital
            )

            fig = px.line(
                selected_df,
                x="date",
                y="equity",
                title="Equity Curve"
            )

            fig.update_layout(
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                selected_df,
                use_container_width=True
            )

    st.stop()


# =========================
# DASHBOARD
# =========================

uploaded_file = st.file_uploader(
    t["upload_report"],
    type=["csv", "xlsx"]
)

if uploaded_file:

    try:

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

        section(t["summary"])

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                metric_card(
                    t["net_pnl"],
                    money(metrics["net_pnl"]),
                    t["total_result"],
                    "positive"
                ),
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                metric_card(
                    t["winrate"],
                    percent(metrics["winrate"]),
                    t["winning_percent"]
                ),
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                metric_card(
                    t["profit_factor"],
                    metrics["profit_factor"],
                    t["above_one_positive"]
                ),
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                metric_card(
                    t["max_drawdown"],
                    money(metrics["max_drawdown"]),
                    t["biggest_curve_drop"],
                    "negative"
                ),
                unsafe_allow_html=True
            )

        section(t["equity_curve"])

        fig_equity = px.line(
            normalized_df,
            x="date",
            y="equity",
            title="Equity Curve"
        )

        fig_equity.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig_equity,
            use_container_width=True
        )

        section(t["risk_alerts"])

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

        if st.button(t["save_analysis"]):

            save_upload(
                account_name="Main Account",
                platform="Unknown",
                file_name=uploaded_file.name,
                trades_df=normalized_df,
                metrics=metrics,
                user_email=st.session_state.user_email
            )

            st.success(
                t["saved_success"]
            )

        section(t["normalized_data"])

        st.dataframe(
            normalized_df,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f'{t["file_error"]}: {e}'
        )

else:

    st.info(
        t["send_file_to_start"]
    )
