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
    get_user_by_email,
)


init_db()

st.set_page_config(
    page_title="RiskPilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# TEXTOS / IDIOMAS
# =========================

def ui_text(language):
    texts = {
        "English": {
            "language": "Language",
            "hero_title": "Institutional trading analytics",
            "hero_subtitle": "Professional-grade trading analytics platform focused on risk, consistency, performance and prop firm approval.",
            "hero_badge": "Risk infrastructure for serious traders",
            "start_free": "🚀 Start free",
            "login": "🔐 Login",
            "view_demo": "📊 View demo",
            "why": "Why RiskPilot?",
            "feature_1_title": "📉 Risk Intelligence",
            "feature_1_text": "Detect dangerous drawdowns, overtrading, revenge trading and losing streaks automatically.",
            "feature_2_title": "🏆 Prop Firm Ready",
            "feature_2_text": "Track daily loss, maximum drawdown, consistency and target distance.",
            "feature_3_title": "🤖 Operational Insights",
            "feature_3_text": "Discover your best hours, worst patterns and operational weaknesses.",
            "choose": "Choose",
            "register": "Register",
            "name": "Name",
            "email": "Email",
            "password": "Password",
            "create_account": "Create Account",
            "user_exists": "User already exists.",
            "account_created": "Account created successfully. You can now login.",
            "invalid_credentials": "Invalid credentials.",
            "back_home": "← Back to homepage",
            "professional_analytics": "Professional Trading Analytics",
            "authenticated_user": "Authenticated user",
            "current_mode": "Current mode",
            "demo_mode": "Demo Mode",
            "create_free_account": "Create free account",
            "initial_capital": "Initial Capital",
            "prop_firm_mode": "Prop Firm Mode",
            "account_size": "Account Size",
            "daily_loss_limit": "Daily Loss Limit",
            "max_drawdown_limit": "Max Drawdown Limit",
            "profit_target": "Profit Target",
            "navigation": "Navigation",
            "dashboard": "Dashboard",
            "history": "History",
            "logout": "Logout",
            "account_status": "Account Status",
            "active": "Active",
            "risk_mode": "Risk Mode",
            "analytics": "Analytics",
            "enabled": "Enabled",
            "sidebar_note": "RiskPilot monitors performance, drawdown, behavior and operational consistency.",
            "history_title": "Upload History",
            "history_account_required": "History is available after creating a free account.",
            "no_uploads": "No uploads yet.",
            "terminal_title": "RiskPilot Terminal",
            "terminal_subtitle": "Institutional-grade trading risk intelligence and performance analytics.",
            "live_engine": "LIVE ANALYTICS ENGINE",
            "demo_info": "Demo mode: sample data loaded. Create a free account to upload and save your own trading reports.",
            "upload_report": "Upload trading report",
            "upload_to_begin": "Upload a CSV or XLSX report to begin.",
            "file_error": "Error reading file",
            "performance": "Performance Overview",
            "net_pnl": "Net P&L",
            "total_net_result": "Total net result",
            "winrate": "Winrate",
            "winning_trades": "Winning trades",
            "profit_factor": "Profit Factor",
            "gross_ratio": "Gross profit / gross loss",
            "max_drawdown": "Max Drawdown",
            "largest_decline": "Largest equity decline",
            "risk_score": "Risk Score",
            "risk_score_sub": "Operational risk quality",
            "consistency_score": "Consistency Score",
            "consistency_score_sub": "Day-to-day stability",
            "account_health": "Account Health",
            "account_health_sub": "Prop firm readiness",
            "behavior_score": "Behavior Score",
            "behavior_score_sub": "Tilt and discipline proxy",
            "prop_firm_panel": "Prop Firm Control Panel",
            "approval_probability": "Approval Probability",
            "approval_probability_sub": "Estimated passing probability",
            "daily_remaining": "Daily Loss Remaining",
            "daily_remaining_sub": "Margin before daily violation",
            "drawdown_remaining": "Max Drawdown Remaining",
            "drawdown_remaining_sub": "Margin before account violation",
            "target_distance": "Target Distance",
            "target_distance_sub": "Remaining to profit target",
            "violation_risk": "Violation Risk",
            "violation_risk_sub": "Operational failure risk",
            "automatic_insights": "Automatic Insights",
            "best_hour": "Best Hour",
            "worst_hour": "Worst Hour",
            "best_day": "Best Day",
            "worst_day": "Worst Day",
            "best_weekday": "Best Weekday",
            "worst_weekday": "Worst Weekday",
            "positive_days": "Positive Days",
            "negative_days": "Negative Days",
            "days_above_zero": "Days above zero",
            "days_below_zero": "Days below zero",
            "ai_diagnosis": "Operational Diagnosis",
            "equity_curve": "Equity Curve",
            "drawdown": "Drawdown",
            "daily_pnl": "Daily P&L",
            "pnl_by_hour": "P&L by Hour",
            "pnl_by_weekday": "P&L by Weekday",
            "pnl_by_asset": "P&L by Asset",
            "risk_alerts": "Risk Alerts",
            "save_analysis": "💾 Save Analysis",
            "analysis_saved": "Analysis saved.",
            "save_warning": "Create a free account to save your analysis history.",
            "trades": "Trades",
            "excellent": "Excellent",
            "healthy": "Healthy",
            "attention": "Attention",
            "critical": "Critical",
            "low": "Low",
            "medium": "Medium",
            "high": "High",
        },
        "Português": {
            "language": "Idioma",
            "hero_title": "Analytics institucional para traders",
            "hero_subtitle": "Plataforma profissional de análise operacional focada em risco, consistência, performance e aprovação em prop firms.",
            "hero_badge": "Infraestrutura de risco para traders sérios",
            "start_free": "🚀 Criar conta grátis",
            "login": "🔐 Entrar",
            "view_demo": "📊 Ver demo",
            "why": "Por que RiskPilot?",
            "feature_1_title": "📉 Inteligência de Risco",
            "feature_1_text": "Detecte drawdowns perigosos, overtrading, revenge trading e sequências ruins automaticamente.",
            "feature_2_title": "🏆 Pronto para Prop Firms",
            "feature_2_text": "Acompanhe perda diária, drawdown máximo, consistência e distância até a meta.",
            "feature_3_title": "🤖 Insights Operacionais",
            "feature_3_text": "Descubra seus melhores horários, piores padrões e fraquezas operacionais.",
            "choose": "Escolha",
            "register": "Cadastrar",
            "name": "Nome",
            "email": "E-mail",
            "password": "Senha",
            "create_account": "Criar conta",
            "user_exists": "Usuário já existe.",
            "account_created": "Conta criada com sucesso. Agora você já pode entrar.",
            "invalid_credentials": "Credenciais inválidas.",
            "back_home": "← Voltar para a página inicial",
            "professional_analytics": "Analytics Profissional de Trading",
            "authenticated_user": "Usuário autenticado",
            "current_mode": "Modo atual",
            "demo_mode": "Modo Demo",
            "create_free_account": "Criar conta grátis",
            "initial_capital": "Capital Inicial",
            "prop_firm_mode": "Modo Prop Firm",
            "account_size": "Tamanho da Conta",
            "daily_loss_limit": "Limite de Perda Diária",
            "max_drawdown_limit": "Limite Máximo de Drawdown",
            "profit_target": "Meta de Lucro",
            "navigation": "Navegação",
            "dashboard": "Dashboard",
            "history": "Histórico",
            "logout": "Sair",
            "account_status": "Status da Conta",
            "active": "Ativa",
            "risk_mode": "Modo de Risco",
            "analytics": "Analytics",
            "enabled": "Ativado",
            "sidebar_note": "O RiskPilot monitora performance, drawdown, comportamento e consistência operacional.",
            "history_title": "Histórico de Uploads",
            "history_account_required": "O histórico fica disponível após criar uma conta grátis.",
            "no_uploads": "Ainda não há uploads salvos.",
            "terminal_title": "Terminal RiskPilot",
            "terminal_subtitle": "Inteligência institucional de risco e performance para traders.",
            "live_engine": "MOTOR DE ANÁLISE ATIVO",
            "demo_info": "Modo demo: dados de exemplo carregados. Crie uma conta grátis para enviar e salvar seus próprios relatórios.",
            "upload_report": "Upload do relatório de trades",
            "upload_to_begin": "Envie um arquivo CSV ou XLSX para começar.",
            "file_error": "Erro ao ler o arquivo",
            "performance": "Resumo de Performance",
            "net_pnl": "Resultado Líquido",
            "total_net_result": "Resultado líquido total",
            "winrate": "Taxa de Acerto",
            "winning_trades": "Trades vencedores",
            "profit_factor": "Fator de Lucro",
            "gross_ratio": "Lucro bruto / perda bruta",
            "max_drawdown": "Drawdown Máximo",
            "largest_decline": "Maior queda da curva",
            "risk_score": "Score de Risco",
            "risk_score_sub": "Qualidade do risco operacional",
            "consistency_score": "Score de Consistência",
            "consistency_score_sub": "Estabilidade dia a dia",
            "account_health": "Saúde da Conta",
            "account_health_sub": "Prontidão para prop firm",
            "behavior_score": "Score Comportamental",
            "behavior_score_sub": "Proxy de tilt e disciplina",
            "prop_firm_panel": "Painel de Controle Prop Firm",
            "approval_probability": "Probabilidade de Aprovação",
            "approval_probability_sub": "Estimativa de aprovação",
            "daily_remaining": "Perda Diária Restante",
            "daily_remaining_sub": "Margem antes da violação diária",
            "drawdown_remaining": "Drawdown Restante",
            "drawdown_remaining_sub": "Margem antes da violação da conta",
            "target_distance": "Distância da Meta",
            "target_distance_sub": "Faltante para a meta de lucro",
            "violation_risk": "Risco de Violação",
            "violation_risk_sub": "Risco de reprovação operacional",
            "automatic_insights": "Insights Automáticos",
            "best_hour": "Melhor Horário",
            "worst_hour": "Pior Horário",
            "best_day": "Melhor Dia",
            "worst_day": "Pior Dia",
            "best_weekday": "Melhor Dia da Semana",
            "worst_weekday": "Pior Dia da Semana",
            "positive_days": "Dias Positivos",
            "negative_days": "Dias Negativos",
            "days_above_zero": "Dias acima de zero",
            "days_below_zero": "Dias abaixo de zero",
            "ai_diagnosis": "Diagnóstico Operacional",
            "equity_curve": "Curva de Capital",
            "drawdown": "Drawdown",
            "daily_pnl": "Resultado por Dia",
            "pnl_by_hour": "Resultado por Horário",
            "pnl_by_weekday": "Resultado por Dia da Semana",
            "pnl_by_asset": "Resultado por Ativo",
            "risk_alerts": "Alertas de Risco",
            "save_analysis": "💾 Salvar Análise",
            "analysis_saved": "Análise salva.",
            "save_warning": "Crie uma conta grátis para salvar seu histórico de análises.",
            "trades": "Trades",
            "excellent": "Excelente",
            "healthy": "Saudável",
            "attention": "Atenção",
            "critical": "Crítico",
            "low": "Baixo",
            "medium": "Médio",
            "high": "Alto",
        },
        "Español": {
            "language": "Idioma",
            "hero_title": "Analytics institucional para traders",
            "hero_subtitle": "Plataforma profesional de análisis operativo enfocada en riesgo, consistencia, rendimiento y aprobación en prop firms.",
            "hero_badge": "Infraestructura de riesgo para traders serios",
            "start_free": "🚀 Crear cuenta gratis",
            "login": "🔐 Entrar",
            "view_demo": "📊 Ver demo",
            "why": "¿Por qué RiskPilot?",
            "feature_1_title": "📉 Inteligencia de Riesgo",
            "feature_1_text": "Detecta drawdowns peligrosos, overtrading, revenge trading y secuencias negativas automáticamente.",
            "feature_2_title": "🏆 Listo para Prop Firms",
            "feature_2_text": "Monitorea pérdida diaria, drawdown máximo, consistencia y distancia a la meta.",
            "feature_3_title": "🤖 Insights Operativos",
            "feature_3_text": "Descubre tus mejores horarios, peores patrones y debilidades operativas.",
            "choose": "Elige",
            "register": "Registrar",
            "name": "Nombre",
            "email": "Email",
            "password": "Contraseña",
            "create_account": "Crear cuenta",
            "user_exists": "El usuario ya existe.",
            "account_created": "Cuenta creada con éxito. Ahora puedes entrar.",
            "invalid_credentials": "Credenciales inválidas.",
            "back_home": "← Volver al inicio",
            "professional_analytics": "Analytics Profesional de Trading",
            "authenticated_user": "Usuario autenticado",
            "current_mode": "Modo actual",
            "demo_mode": "Modo Demo",
            "create_free_account": "Crear cuenta gratis",
            "initial_capital": "Capital Inicial",
            "prop_firm_mode": "Modo Prop Firm",
            "account_size": "Tamaño de la Cuenta",
            "daily_loss_limit": "Límite de Pérdida Diaria",
            "max_drawdown_limit": "Límite Máximo de Drawdown",
            "profit_target": "Meta de Lucro",
            "navigation": "Navegación",
            "dashboard": "Dashboard",
            "history": "Historial",
            "logout": "Salir",
            "account_status": "Estado de la Cuenta",
            "active": "Activa",
            "risk_mode": "Modo de Riesgo",
            "analytics": "Analytics",
            "enabled": "Activado",
            "sidebar_note": "RiskPilot monitorea rendimiento, drawdown, comportamiento y consistencia operativa.",
            "history_title": "Historial de Uploads",
            "history_account_required": "El historial está disponible después de crear una cuenta gratis.",
            "no_uploads": "Aún no hay uploads guardados.",
            "terminal_title": "Terminal RiskPilot",
            "terminal_subtitle": "Inteligencia institucional de riesgo y rendimiento para traders.",
            "live_engine": "MOTOR DE ANÁLISIS ACTIVO",
            "demo_info": "Modo demo: datos de ejemplo cargados. Crea una cuenta gratis para subir y guardar tus propios reportes.",
            "upload_report": "Subir reporte de trading",
            "upload_to_begin": "Sube un archivo CSV o XLSX para comenzar.",
            "file_error": "Error al leer el archivo",
            "performance": "Resumen de Rendimiento",
            "net_pnl": "Resultado Neto",
            "total_net_result": "Resultado neto total",
            "winrate": "Tasa de Acierto",
            "winning_trades": "Trades ganadores",
            "profit_factor": "Factor de Lucro",
            "gross_ratio": "Lucro bruto / pérdida bruta",
            "max_drawdown": "Drawdown Máximo",
            "largest_decline": "Mayor caída de la curva",
            "risk_score": "Score de Riesgo",
            "risk_score_sub": "Calidad del riesgo operativo",
            "consistency_score": "Score de Consistencia",
            "consistency_score_sub": "Estabilidad día a día",
            "account_health": "Salud de la Cuenta",
            "account_health_sub": "Preparación para prop firm",
            "behavior_score": "Score Conductual",
            "behavior_score_sub": "Proxy de tilt y disciplina",
            "prop_firm_panel": "Panel de Control Prop Firm",
            "approval_probability": "Probabilidad de Aprobación",
            "approval_probability_sub": "Estimación de aprobación",
            "daily_remaining": "Pérdida Diaria Restante",
            "daily_remaining_sub": "Margen antes de violación diaria",
            "drawdown_remaining": "Drawdown Restante",
            "drawdown_remaining_sub": "Margen antes de violación de cuenta",
            "target_distance": "Distancia a la Meta",
            "target_distance_sub": "Faltante para la meta de lucro",
            "violation_risk": "Riesgo de Violación",
            "violation_risk_sub": "Riesgo de reprobación operativa",
            "automatic_insights": "Insights Automáticos",
            "best_hour": "Mejor Horario",
            "worst_hour": "Peor Horario",
            "best_day": "Mejor Día",
            "worst_day": "Peor Día",
            "best_weekday": "Mejor Día de la Semana",
            "worst_weekday": "Peor Día de la Semana",
            "positive_days": "Días Positivos",
            "negative_days": "Días Negativos",
            "days_above_zero": "Días sobre cero",
            "days_below_zero": "Días bajo cero",
            "ai_diagnosis": "Diagnóstico Operativo",
            "equity_curve": "Curva de Capital",
            "drawdown": "Drawdown",
            "daily_pnl": "Resultado Diario",
            "pnl_by_hour": "Resultado por Horario",
            "pnl_by_weekday": "Resultado por Día de la Semana",
            "pnl_by_asset": "Resultado por Activo",
            "risk_alerts": "Alertas de Riesgo",
            "save_analysis": "💾 Guardar Análisis",
            "analysis_saved": "Análisis guardado.",
            "save_warning": "Crea una cuenta gratis para guardar tu historial de análisis.",
            "trades": "Trades",
            "excellent": "Excelente",
            "healthy": "Saludable",
            "attention": "Atención",
            "critical": "Crítico",
            "low": "Bajo",
            "medium": "Medio",
            "high": "Alto",
        },
    }
    return texts.get(language, texts["English"])


# =========================
# CSS
# =========================

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {background:#050816!important;color:#fff!important;}
[data-testid="stHeader"] {background:rgba(5,8,22,.98)!important;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#060b18 0%,#0b1020 100%)!important;border-right:1px solid rgba(148,163,184,.12);}
[data-testid="stSidebar"] * {color:#fff!important;}
.block-container {max-width:1500px;padding-top:1.6rem;padding-bottom:4rem;}
#MainMenu, footer, header {visibility:hidden;}
.sidebar-brand{background:linear-gradient(135deg,rgba(56,189,248,.15),rgba(15,23,42,.9));border:1px solid rgba(56,189,248,.30);border-radius:22px;padding:20px 18px;margin-bottom:18px;box-shadow:0 14px 40px rgba(0,0,0,.24)}
.sidebar-logo{font-size:1.55rem;font-weight:950;letter-spacing:-.04em;color:#fff!important}.sidebar-subtitle{color:#93c5fd!important;font-size:.82rem;margin-top:4px;line-height:1.35}
.sidebar-user-card{background:#0f172a;border:1px solid rgba(148,163,184,.14);border-radius:18px;padding:16px;margin:14px 0 18px 0}.sidebar-user-label{color:#94a3b8!important;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;font-weight:800}.sidebar-user-value{color:#fff!important;font-size:.92rem;margin-top:5px;word-break:break-word}
.sidebar-kpi{background:rgba(15,23,42,.88);border:1px solid rgba(148,163,184,.12);border-radius:15px;padding:13px 14px;margin-bottom:10px}.sidebar-kpi-title{color:#94a3b8!important;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em}.sidebar-kpi-value{color:#fff!important;font-size:1.15rem;font-weight:900;margin-top:4px}.sidebar-note{color:#64748b!important;font-size:.78rem;line-height:1.45;margin-top:12px}
.hero-wrap{padding-top:25px;padding-bottom:30px}.hero-title{font-size:clamp(3.2rem,6vw,5.8rem);font-weight:950;line-height:1.08;letter-spacing:-.06em;color:#fff!important;margin-bottom:26px;max-width:820px}.hero-subtitle{font-size:1.25rem;line-height:1.75;color:#b6c2d2!important;margin-top:18px;margin-bottom:34px;max-width:780px}.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:rgba(56,189,248,.12);border:1px solid rgba(56,189,248,.35);color:#7dd3fc!important;font-size:.9rem;font-weight:700;margin-bottom:20px}.hero-image-card{background:linear-gradient(135deg,rgba(15,23,42,.9),rgba(30,41,59,.45));border:1px solid rgba(255,255,255,.08);border-radius:26px;padding:14px;box-shadow:0 25px 80px rgba(0,0,0,.35)}
.feature-card{background:linear-gradient(135deg,#101827 0%,#172033 100%);border:1px solid rgba(255,255,255,.09);border-radius:22px;padding:30px;min-height:230px;box-shadow:0 14px 40px rgba(0,0,0,.23)}.feature-card h3{color:#fff!important;font-size:1.45rem;margin-bottom:15px}.feature-card p{color:#b6c2d2!important;font-size:1rem;line-height:1.65}
.metric-card{background:linear-gradient(135deg,#111827 0%,#1f2937 100%);border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:24px;min-height:125px;box-shadow:0 10px 30px rgba(0,0,0,.25)}.metric-title{color:#9ca3af!important;font-size:.9rem;font-weight:700}.metric-value{font-size:2rem;font-weight:850;margin-top:6px}.metric-sub{color:#64748b!important;font-size:.82rem;margin-top:6px}.value-positive{color:#22c55e!important}.value-negative{color:#fb7185!important}.value-neutral{color:#38bdf8!important}.value-warning{color:#f59e0b!important}
.section-title{font-size:2rem;font-weight:850;color:#fff!important;margin-top:60px;margin-bottom:24px;letter-spacing:-.035em}.alert-box{background:#1f2937;border-left:5px solid #f59e0b;padding:16px;border-radius:12px;margin-bottom:12px;color:#fff!important}.diagnosis-box{background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(30,41,59,.78));border:1px solid rgba(56,189,248,.18);border-radius:22px;padding:22px 24px;margin-bottom:14px}.diagnosis-title{color:#7dd3fc!important;font-size:.85rem;font-weight:850;text-transform:uppercase;letter-spacing:.08em}.diagnosis-text{color:#e5e7eb!important;font-size:1rem;line-height:1.6;margin-top:8px}
.insight-card{background:linear-gradient(135deg,#0f172a 0%,#172554 100%);border:1px solid rgba(56,189,248,.22);border-radius:18px;padding:22px;min-height:126px;box-shadow:0 10px 30px rgba(0,0,0,.20)}.insight-title{color:#94a3b8!important;font-size:.88rem;font-weight:750}.insight-value{font-size:1.65rem;font-weight:850;margin-top:8px}.insight-sub{color:#7dd3fc!important;font-size:.85rem;margin-top:8px}
.auth-box{max-width:620px;margin:30px auto;background:linear-gradient(135deg,#101827 0%,#172033 100%);border:1px solid rgba(255,255,255,.09);border-radius:26px;padding:35px}.terminal-header{background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(2,6,23,.78));border:1px solid rgba(148,163,184,.14);border-radius:26px;padding:26px 30px;margin-bottom:30px;box-shadow:0 20px 70px rgba(0,0,0,.28)}.terminal-title{color:#fff!important;font-size:2.65rem;font-weight:950;letter-spacing:-.055em;line-height:1.05}.terminal-subtitle{color:#94a3b8!important;font-size:1rem;margin-top:8px}.terminal-pill{display:inline-block;background:rgba(34,197,94,.12);color:#86efac!important;border:1px solid rgba(34,197,94,.28);border-radius:999px;padding:7px 12px;font-size:.78rem;font-weight:800;margin-top:12px}
.stButton>button{border-radius:14px;min-height:52px;font-weight:800;font-size:1rem;border:1px solid rgba(255,255,255,.15);background:#0f172a!important;color:#fff!important}.stButton>button:hover{border-color:#38bdf8!important;color:#7dd3fc!important}input,textarea,select{color:#fff!important}[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stSelectbox"] div,[data-testid="stDateInput"] input{background:#111827!important;color:#fff!important}
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


def value_class(value, higher_is_better=True, warning_threshold=None):
    try:
        value = float(value)
    except Exception:
        return "value-neutral"
    if warning_threshold is not None:
        if value >= warning_threshold:
            return "value-positive" if higher_is_better else "value-negative"
        return "value-warning"
    if value > 0:
        return "value-positive" if higher_is_better else "value-negative"
    if value < 0:
        return "value-negative" if higher_is_better else "value-positive"
    return "value-neutral"


def metric_card(title, value, sub="", css_class="value-neutral"):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value {css_class}">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """


def insight_card(title, value, sub="", css_class="value-neutral"):
    return f"""
    <div class="insight-card">
        <div class="insight-title">{title}</div>
        <div class="insight-value {css_class}">{value}</div>
        <div class="insight-sub">{sub}</div>
    </div>
    """


def diagnosis_box(title, text):
    return f"""
    <div class="diagnosis-box">
        <div class="diagnosis-title">{title}</div>
        <div class="diagnosis-text">{text}</div>
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
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color="#cbd5e1")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.16)", zeroline=False, color="#cbd5e1")
    return fig


def make_equity_chart(df, t):
    chart_df = df.copy()
    chart_df["equity_smooth"] = smooth_series(chart_df["equity"], window=6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_df["date"], y=chart_df["equity"], mode="lines", name=t["equity_curve"], line=dict(width=1.4, color="rgba(56,189,248,0.28)")))
    fig.add_trace(go.Scatter(x=chart_df["date"], y=chart_df["equity_smooth"], mode="lines", name="Smooth", line=dict(width=3.2, color="#38bdf8", shape="spline", smoothing=1.2)))
    return base_chart_layout(fig, height=430)


def make_drawdown_chart(df, t):
    chart_df = df.copy()
    chart_df["drawdown_smooth"] = smooth_series(chart_df["drawdown"], window=6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_df["date"], y=chart_df["drawdown_smooth"], mode="lines", name=t["drawdown"], line=dict(width=3, color="#fb7185", shape="spline", smoothing=1.1), fill="tozeroy", fillcolor="rgba(251,113,133,0.18)"))
    return base_chart_layout(fig, height=360)


def make_bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title)
    colors = ["#22c55e" if value >= 0 else "#fb7185" for value in df[y]]
    fig.update_traces(marker_color=colors, marker_line_width=0)
    return base_chart_layout(fig, height=340)


def prop_profiles(account_size):
    return {
        "Custom": {"target": account_size * 0.10, "daily": account_size * 0.05, "drawdown": account_size * 0.10},
        "FTMO": {"target": account_size * 0.10, "daily": account_size * 0.05, "drawdown": account_size * 0.10},
        "Apex": {"target": account_size * 0.06, "daily": account_size * 0.03, "drawdown": account_size * 0.05},
        "MyFundedFX": {"target": account_size * 0.08, "daily": account_size * 0.05, "drawdown": account_size * 0.08},
        "TopStep": {"target": account_size * 0.06, "daily": account_size * 0.03, "drawdown": account_size * 0.04},
        "Personalizado": {"target": account_size * 0.10, "daily": account_size * 0.05, "drawdown": account_size * 0.10},
    }


def calculate_scores(metrics, daily, max_daily_loss, max_drawdown_limit):
    net_pnl = float(metrics.get("net_pnl", 0))
    profit_factor = float(metrics.get("profit_factor", 0))
    max_drawdown = float(metrics.get("max_drawdown", 0))
    winrate = float(metrics.get("winrate", 0))
    loss_streak = float(metrics.get("max_loss_streak", 0))
    pf_score = min(max(profit_factor / 2.0, 0), 1) * 25
    dd_score = max(0, 1 - (max_drawdown / max(max_drawdown_limit, 1))) * 25
    win_score = min(max(winrate / 70, 0), 1) * 20
    pnl_score = 15 if net_pnl > 0 else 5
    streak_score = max(0, 1 - (loss_streak / 8)) * 15
    risk_score = round(pf_score + dd_score + win_score + pnl_score + streak_score)
    if daily.empty or len(daily) <= 1:
        consistency_score = 50
    else:
        daily_std = daily.std()
        avg_abs = max(abs(daily).mean(), 1)
        consistency_score = round(max(0, 100 - (daily_std / avg_abs * 35)))
        consistency_score = min(100, max(0, consistency_score))
    account_health = round((risk_score * 0.65) + (consistency_score * 0.35))
    behavior_score = 100
    behavior_score -= min(loss_streak * 8, 40)
    if not daily.empty and daily.min() < -abs(max_daily_loss):
        behavior_score -= 25
    if profit_factor < 1:
        behavior_score -= 20
    behavior_score = round(max(0, min(100, behavior_score)))
    return risk_score, consistency_score, account_health, behavior_score


def calculate_prop_status(metrics, daily, profit_target, max_daily_loss, max_drawdown_limit, risk_score, consistency_score, behavior_score):
    net_pnl = float(metrics.get("net_pnl", 0))
    max_dd = float(metrics.get("max_drawdown", 0))
    worst_day = abs(float(daily.min())) if not daily.empty else 0
    target_distance = profit_target - net_pnl
    daily_remaining = max_daily_loss - worst_day
    dd_remaining = max_drawdown_limit - max_dd
    daily_ratio = max(0, min(1, daily_remaining / max(max_daily_loss, 1)))
    dd_ratio = max(0, min(1, dd_remaining / max(max_drawdown_limit, 1)))
    target_ratio = max(0, min(1, net_pnl / max(profit_target, 1)))
    approval = round((risk_score * 0.35) + (consistency_score * 0.20) + (behavior_score * 0.20) + (daily_ratio * 10) + (dd_ratio * 10) + (target_ratio * 5))
    violation_score = 100 - approval
    if daily_remaining < 0 or dd_remaining < 0:
        approval = min(approval, 15)
        violation_score = max(violation_score, 90)
    return approval, daily_remaining, dd_remaining, target_distance, violation_score


def score_class(score):
    if score >= 75:
        return "value-positive"
    if score >= 50:
        return "value-warning"
    return "value-negative"


def score_label(score, t):
    if score >= 80:
        return t["excellent"]
    if score >= 65:
        return t["healthy"]
    if score >= 45:
        return t["attention"]
    return t["critical"]


def violation_label(value, t):
    if value >= 75:
        return t["high"]
    if value >= 40:
        return t["medium"]
    return t["low"]


def generate_diagnosis(language, metrics, daily, hourly, risk_score, consistency_score, behavior_score, approval, target_distance, daily_remaining, dd_remaining):
    net_pnl = float(metrics.get("net_pnl", 0))
    profit_factor = float(metrics.get("profit_factor", 0))
    loss_streak = int(metrics.get("max_loss_streak", 0))
    worst_hour = hourly.idxmin() if not hourly.empty else "N/A"
    worst_hour_value = hourly.min() if not hourly.empty else 0
    best_hour = hourly.idxmax() if not hourly.empty else "N/A"
    best_hour_value = hourly.max() if not hourly.empty else 0
    negative_days = int((daily < 0).sum()) if not daily.empty else 0

    if language == "Português":
        items = []
        items.append("O Profit Factor está abaixo de 1, indicando que o operacional ainda perde mais do que ganha." if profit_factor < 1 else "O Profit Factor está acima de 1, indicando vantagem operacional inicial.")
        if net_pnl < 0:
            items.append("O resultado líquido está negativo. A prioridade agora é reduzir drawdown e filtrar horários ruins.")
        if worst_hour != "N/A":
            items.append(f"O pior horário foi {worst_hour}h, com resultado de {money(worst_hour_value)}. Esse período merece bloqueio, redução de lote ou revisão de setup.")
        if best_hour != "N/A":
            items.append(f"O melhor horário foi {best_hour}h, com resultado de {money(best_hour_value)}. Esse pode ser seu principal período operacional.")
        if loss_streak >= 4:
            items.append(f"Foi detectada sequência de {loss_streak} perdas. Isso pode indicar tilt, insistência ou condição ruim de mercado.")
        items.append(f"Probabilidade estimada de aprovação: {approval}/100. Faltam {money(target_distance)} para a meta, {money(daily_remaining)} de margem diária e {money(dd_remaining)} de margem no drawdown máximo.")
        items.append(f"Score de risco: {risk_score}/100. Score de consistência: {consistency_score}/100. Score comportamental: {behavior_score}/100. Foram encontrados {negative_days} dias negativos.")
        return items

    if language == "Español":
        items = []
        items.append("El Profit Factor está por debajo de 1, indicando que el sistema aún pierde más de lo que gana." if profit_factor < 1 else "El Profit Factor está por encima de 1, indicando una ventaja operativa inicial.")
        if net_pnl < 0:
            items.append("El resultado neto está negativo. La prioridad ahora es reducir drawdown y filtrar horarios débiles.")
        if worst_hour != "N/A":
            items.append(f"El peor horario fue {worst_hour}h, con resultado de {money(worst_hour_value)}. Ese periodo merece bloqueo, reducción de lote o revisión de setup.")
        if best_hour != "N/A":
            items.append(f"El mejor horario fue {best_hour}h, con resultado de {money(best_hour_value)}. Puede ser tu principal ventana operativa.")
        if loss_streak >= 4:
            items.append(f"Se detectó una secuencia de {loss_streak} pérdidas. Esto puede indicar tilt, insistencia o malas condiciones de mercado.")
        items.append(f"Probabilidad estimada de aprobación: {approval}/100. Faltan {money(target_distance)} para la meta, {money(daily_remaining)} de margen diario y {money(dd_remaining)} de margen en drawdown máximo.")
        items.append(f"Score de riesgo: {risk_score}/100. Score de consistencia: {consistency_score}/100. Score conductual: {behavior_score}/100. Se encontraron {negative_days} días negativos.")
        return items

    items = []
    items.append("Profit Factor is below 1, which means the system is still losing more than it wins." if profit_factor < 1 else "Profit Factor is above 1, indicating an initial operational edge.")
    if net_pnl < 0:
        items.append("Net result is negative. The priority now is to reduce drawdown and filter weak trading windows.")
    if worst_hour != "N/A":
        items.append(f"Worst hour was {worst_hour}h, with a result of {money(worst_hour_value)}. This window should be blocked, reduced or reviewed.")
    if best_hour != "N/A":
        items.append(f"Best hour was {best_hour}h, with a result of {money(best_hour_value)}. This may be your main trading window.")
    if loss_streak >= 4:
        items.append(f"A sequence of {loss_streak} losses was detected. This may indicate tilt, overtrading or poor market conditions.")
    items.append(f"Estimated approval probability: {approval}/100. Remaining target: {money(target_distance)}, daily margin: {money(daily_remaining)}, max drawdown margin: {money(dd_remaining)}.")
    items.append(f"Risk Score: {risk_score}/100. Consistency Score: {consistency_score}/100. Behavior Score: {behavior_score}/100. There were {negative_days} negative days.")
    return items


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
        selected_language = st.selectbox("Language / Idioma", ["English", "Português", "Español"], index=["English", "Português", "Español"].index(st.session_state.landing_language))
        st.session_state.landing_language = selected_language
    t = ui_text(st.session_state.landing_language)
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.25, 1])
    with col1:
        st.markdown(f'<div class="hero-badge">⚡ {t["hero_badge"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-title">{t["hero_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{t["hero_subtitle"]}</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns([1, 1, 1])
        with b1:
            if st.button(t["start_free"]):
                st.session_state.auth_mode = "Register"
                st.session_state.show_login = True
                st.rerun()
        with b2:
            if st.button(t["login"]):
                st.session_state.auth_mode = "Login"
                st.session_state.show_login = True
                st.rerun()
        with b3:
            if st.button(t["view_demo"]):
                st.session_state.demo_mode = True
                st.rerun()
    with col2:
        st.markdown('<div class="hero-image-card">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1200&auto=format&fit=crop", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{t["why"]}</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(f'<div class="feature-card"><h3>{t["feature_1_title"]}</h3><p>{t["feature_1_text"]}</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown(f'<div class="feature-card"><h3>{t["feature_2_title"]}</h3><p>{t["feature_2_text"]}</p></div>', unsafe_allow_html=True)
    with f3:
        st.markdown(f'<div class="feature-card"><h3>{t["feature_3_title"]}</h3><p>{t["feature_3_text"]}</p></div>', unsafe_allow_html=True)
    st.stop()


# =========================
# LOGIN / REGISTER
# =========================

if not st.session_state.authenticated and st.session_state.show_login:
    t = ui_text(st.session_state.landing_language)
    st.markdown('<div class="auth-box">', unsafe_allow_html=True)
    st.title("🔐 RiskPilot")
    auth_mode = st.radio(t["choose"], [t["login"].replace("🔐 ", ""), t["register"]], index=0 if st.session_state.auth_mode == "Login" else 1)
    if auth_mode == t["register"]:
        name = st.text_input(t["name"])
        email = st.text_input(t["email"])
        password = st.text_input(t["password"], type="password")
        if st.button(t["create_account"]):
            existing = get_user_by_email(email)
            if existing:
                st.error(t["user_exists"])
            else:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                create_user(name, email, hashed)
                st.success(t["account_created"])
    else:
        email = st.text_input(t["email"])
        password = st.text_input(t["password"], type="password")
        if st.button(t["login"]):
            user = get_user_by_email(email)
            if not user:
                st.error(t["invalid_credentials"])
            else:
                valid = bcrypt.checkpw(password.encode(), user["password"].encode())
                if valid:
                    st.session_state.authenticated = True
                    st.session_state.user_email = user["email"]
                    st.session_state.show_login = False
                    st.session_state.demo_mode = False
                    st.rerun()
                else:
                    st.error(t["invalid_credentials"])
    if st.button(t["back_home"]):
        st.session_state.show_login = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# =========================
# SIDEBAR APP
# =========================

language = st.sidebar.selectbox("Language / Idioma", ["English", "Português", "Español"], index=["English", "Português", "Español"].index(st.session_state.landing_language))
st.session_state.landing_language = language
t = ui_text(language)

st.sidebar.markdown(f'<div class="sidebar-brand"><div class="sidebar-logo">📊 RiskPilot</div><div class="sidebar-subtitle">{t["professional_analytics"]}</div></div>', unsafe_allow_html=True)

if st.session_state.authenticated:
    st.sidebar.markdown(f'<div class="sidebar-user-card"><div class="sidebar-user-label">{t["authenticated_user"]}</div><div class="sidebar-user-value">{st.session_state.user_email}</div></div>', unsafe_allow_html=True)
    if st.sidebar.button(t["logout"]):
        st.session_state.authenticated = False
        st.session_state.show_login = False
        st.session_state.demo_mode = False
        st.session_state.user_email = None
        st.rerun()
else:
    st.sidebar.markdown(f'<div class="sidebar-user-card"><div class="sidebar-user-label">{t["current_mode"]}</div><div class="sidebar-user-value">{t["demo_mode"]}</div></div>', unsafe_allow_html=True)
    if st.sidebar.button(t["create_free_account"]):
        st.session_state.demo_mode = False
        st.session_state.auth_mode = "Register"
        st.session_state.show_login = True
        st.rerun()

account_size = st.sidebar.number_input(t["account_size"], value=50000.0, step=5000.0)
prop_mode = st.sidebar.selectbox(t["prop_firm_mode"], ["FTMO", "Apex", "MyFundedFX", "TopStep", "Custom", "Personalizado"])
profiles = prop_profiles(account_size)
profile = profiles.get(prop_mode, profiles["Custom"])

initial_capital = st.sidebar.number_input(t["initial_capital"], value=1000.0)

if prop_mode in ["Custom", "Personalizado"]:
    max_daily_loss = st.sidebar.number_input(t["daily_loss_limit"], value=float(profile["daily"]))
    max_drawdown_limit = st.sidebar.number_input(t["max_drawdown_limit"], value=float(profile["drawdown"]))
    profit_target = st.sidebar.number_input(t["profit_target"], value=float(profile["target"]))
else:
    max_daily_loss = float(profile["daily"])
    max_drawdown_limit = float(profile["drawdown"])
    profit_target = float(profile["target"])
    st.sidebar.markdown(sidebar_kpi(t["daily_loss_limit"], money(max_daily_loss)), unsafe_allow_html=True)
    st.sidebar.markdown(sidebar_kpi(t["max_drawdown_limit"], money(max_drawdown_limit)), unsafe_allow_html=True)
    st.sidebar.markdown(sidebar_kpi(t["profit_target"], money(profit_target)), unsafe_allow_html=True)

page = st.sidebar.radio(t["navigation"], [t["dashboard"], t["history"]])

st.sidebar.markdown("---")
st.sidebar.markdown(sidebar_kpi(t["account_status"], t["active"]), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_kpi(t["risk_mode"], prop_mode), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_kpi(t["analytics"], t["enabled"]), unsafe_allow_html=True)
st.sidebar.markdown(f'<div class="sidebar-note">{t["sidebar_note"]}</div>', unsafe_allow_html=True)


# =========================
# HISTORY
# =========================

if page == t["history"]:
    st.title("📚 " + t["history_title"])
    if not st.session_state.authenticated:
        st.info(t["history_account_required"])
        st.stop()
    history = load_upload_history(st.session_state.user_email)
    if history.empty:
        st.info(t["no_uploads"])
        st.stop()
    st.dataframe(history, use_container_width=True)
    st.stop()


# =========================
# DASHBOARD
# =========================

st.markdown(f'<div class="terminal-header"><div class="terminal-title">{t["terminal_title"]}</div><div class="terminal-subtitle">{t["terminal_subtitle"]}</div><div class="terminal-pill">{t["live_engine"]} · {prop_mode}</div></div>', unsafe_allow_html=True)

if st.session_state.demo_mode and not st.session_state.authenticated:
    st.info(t["demo_info"])
    normalized_df = prepare_dataframe(make_demo_dataframe(), initial_capital)
    uploaded_file_name = "demo_data.csv"
else:
    uploaded_file = st.file_uploader(t["upload_report"], type=["csv", "xlsx"])
    if not uploaded_file:
        st.info(t["upload_to_begin"])
        st.stop()
    try:
        raw_df = load_trading_file(uploaded_file)
        normalized_df = normalize_trades(raw_df)
        normalized_df = prepare_dataframe(normalized_df, initial_capital)
        uploaded_file_name = uploaded_file.name
    except Exception as e:
        st.error(f'{t["file_error"]}: {e}')
        st.stop()

metrics = calculate_metrics(normalized_df, initial_capital)
hourly = normalized_df.groupby("hour")["net_pnl"].sum()
daily = normalized_df.groupby("day")["net_pnl"].sum()
weekday = normalized_df.groupby("weekday")["net_pnl"].sum()

risk_score, consistency_score, account_health, behavior_score = calculate_scores(metrics, daily, max_daily_loss, max_drawdown_limit)
approval, daily_remaining, dd_remaining, target_distance, violation_score = calculate_prop_status(metrics, daily, profit_target, max_daily_loss, max_drawdown_limit, risk_score, consistency_score, behavior_score)

section(t["performance"])
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_card(t["net_pnl"], money(metrics["net_pnl"]), t["total_net_result"], value_class(metrics["net_pnl"])), unsafe_allow_html=True)
with c2:
    st.markdown(metric_card(t["winrate"], percent(metrics["winrate"]), t["winning_trades"], value_class(metrics["winrate"], warning_threshold=50)), unsafe_allow_html=True)
with c3:
    st.markdown(metric_card(t["profit_factor"], f"{metrics['profit_factor']:.2f}", t["gross_ratio"], value_class(metrics["profit_factor"], warning_threshold=1)), unsafe_allow_html=True)
with c4:
    st.markdown(metric_card(t["max_drawdown"], money(metrics["max_drawdown"]), t["largest_decline"], value_class(metrics["max_drawdown"], higher_is_better=False)), unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(metric_card(t["risk_score"], f"{risk_score}/100", t["risk_score_sub"], score_class(risk_score)), unsafe_allow_html=True)
with s2:
    st.markdown(metric_card(t["consistency_score"], f"{consistency_score}/100", t["consistency_score_sub"], score_class(consistency_score)), unsafe_allow_html=True)
with s3:
    st.markdown(metric_card(t["account_health"], score_label(account_health, t), t["account_health_sub"], score_class(account_health)), unsafe_allow_html=True)
with s4:
    st.markdown(metric_card(t["behavior_score"], f"{behavior_score}/100", t["behavior_score_sub"], score_class(behavior_score)), unsafe_allow_html=True)

section(t["prop_firm_panel"])
p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    st.markdown(metric_card(t["approval_probability"], f"{approval}/100", t["approval_probability_sub"], score_class(approval)), unsafe_allow_html=True)
with p2:
    st.markdown(metric_card(t["daily_remaining"], money(daily_remaining), t["daily_remaining_sub"], value_class(daily_remaining)), unsafe_allow_html=True)
with p3:
    st.markdown(metric_card(t["drawdown_remaining"], money(dd_remaining), t["drawdown_remaining_sub"], value_class(dd_remaining)), unsafe_allow_html=True)
with p4:
    st.markdown(metric_card(t["target_distance"], money(target_distance), t["target_distance_sub"], "value-neutral" if target_distance > 0 else "value-positive"), unsafe_allow_html=True)
with p5:
    st.markdown(metric_card(t["violation_risk"], violation_label(violation_score, t), t["violation_risk_sub"], score_class(100 - violation_score)), unsafe_allow_html=True)

section(t["automatic_insights"])
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
    st.markdown(insight_card(t["best_hour"], f"{best_hour}h", money(best_hour_pnl), value_class(best_hour_pnl)), unsafe_allow_html=True)
with ic2:
    st.markdown(insight_card(t["worst_hour"], f"{worst_hour}h", money(worst_hour_pnl), value_class(worst_hour_pnl)), unsafe_allow_html=True)
with ic3:
    st.markdown(insight_card(t["best_day"], str(best_day), money(best_day_pnl), value_class(best_day_pnl)), unsafe_allow_html=True)
with ic4:
    st.markdown(insight_card(t["worst_day"], str(worst_day), money(worst_day_pnl), value_class(worst_day_pnl)), unsafe_allow_html=True)

ic5, ic6, ic7, ic8 = st.columns(4)
with ic5:
    st.markdown(insight_card(t["best_weekday"], str(best_weekday), money(best_weekday_pnl), value_class(best_weekday_pnl)), unsafe_allow_html=True)
with ic6:
    st.markdown(insight_card(t["worst_weekday"], str(worst_weekday), money(worst_weekday_pnl), value_class(worst_weekday_pnl)), unsafe_allow_html=True)
with ic7:
    positive_days = int((daily > 0).sum()) if not daily.empty else 0
    st.markdown(insight_card(t["positive_days"], positive_days, t["days_above_zero"], "value-positive"), unsafe_allow_html=True)
with ic8:
    negative_days = int((daily < 0).sum()) if not daily.empty else 0
    st.markdown(insight_card(t["negative_days"], negative_days, t["days_below_zero"], "value-negative"), unsafe_allow_html=True)

section(t["ai_diagnosis"])
for item in generate_diagnosis(language, metrics, daily, hourly, risk_score, consistency_score, behavior_score, approval, target_distance, daily_remaining, dd_remaining):
    st.markdown(diagnosis_box(t["ai_diagnosis"], item), unsafe_allow_html=True)

section(t["equity_curve"])
st.plotly_chart(make_equity_chart(normalized_df, t), use_container_width=True)

section(t["drawdown"])
st.plotly_chart(make_drawdown_chart(normalized_df, t), use_container_width=True)

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    section(t["daily_pnl"])
    daily_df = daily.reset_index()
    daily_df.columns = ["day", "net_pnl"]
    st.plotly_chart(make_bar_chart(daily_df, "day", "net_pnl", t["daily_pnl"]), use_container_width=True)
with chart_col2:
    section(t["pnl_by_hour"])
    hourly_df = hourly.reset_index()
    hourly_df.columns = ["hour", "net_pnl"]
    st.plotly_chart(make_bar_chart(hourly_df, "hour", "net_pnl", t["pnl_by_hour"]), use_container_width=True)
chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    section(t["pnl_by_weekday"])
    weekday_df = weekday.reset_index()
    weekday_df.columns = ["weekday", "net_pnl"]
    st.plotly_chart(make_bar_chart(weekday_df, "weekday", "net_pnl", t["pnl_by_weekday"]), use_container_width=True)
with chart_col4:
    section(t["pnl_by_asset"])
    asset_df = normalized_df.groupby("asset")["net_pnl"].sum().reset_index()
    st.plotly_chart(make_bar_chart(asset_df, "asset", "net_pnl", t["pnl_by_asset"]), use_container_width=True)

section(t["risk_alerts"])
alerts = generate_risk_alerts(normalized_df, max_daily_loss, max_drawdown_limit, language=language)
for alert in alerts:
    st.markdown(f'<div class="alert-box">⚠️ {alert}</div>', unsafe_allow_html=True)

if st.session_state.authenticated:
    if st.button(t["save_analysis"]):
        save_upload(account_name=prop_mode, platform="Unknown", file_name=uploaded_file_name, trades_df=normalized_df, metrics=metrics, user_email=st.session_state.user_email)
        st.success(t["analysis_saved"])
else:
    st.warning(t["save_warning"])

section(t["trades"])
st.dataframe(normalized_df, use_container_width=True)
