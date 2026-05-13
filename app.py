import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import bcrypt
import time
import io
import unicodedata
 
 
from core.loader import load_trading_file
from core.normalizer import normalize_trades
from core.metrics import calculate_metrics
from core.risk_engine import generate_risk_alerts
from core.pdf_report import build_pdf_report
from core.ai_coach import build_ai_coach_report
 
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
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
 
# =========================================================
# ADMIN / BILLING READY
# =========================================================
 
ADMIN_EMAILS = [
    "victorbortoleto@yahoo.com.br",
]
 
 
def is_admin_user():
    email = st.session_state.get("user_email")
    return bool(email and email.lower() in [admin.lower() for admin in ADMIN_EMAILS])
 
 
def effective_user_plan():
    if is_admin_user():
        return "Premium"
    return st.session_state.get("user_plan", "Free")
 
 
# =========================================================
# IDIOMAS
# =========================================================
 
def ui_text(language):
    texts = {
        "English": {
            "ai_coach": "AI Trading Coach",
"analyze_ai": "\U0001f9e0 Analyze with AI",
"ai_score": "AI Score",
"executive_summary": "Executive Summary",
"action_plan": "Action Plan",
"risk_rules": "Risk Rules",
"behavior_warnings": "Behavior Warnings",
            "institutional_radar": "Institutional Radar",
            "radar_discipline": "Discipline",
            "radar_consistency": "Consistency",
            "radar_risk_control": "Risk Control",
            "radar_execution": "Execution",
            "radar_recovery": "Recovery",
            "radar_prop_compatibility": "Prop Compatibility",
            "smart_prop_engine": "Smart Prop Firm Engine",
            "prop_rule_profile": "Rule Profile",
            "openai_ready": "OpenAI Ready",
            "openai_ready_sub": "Prepared for real AI integration",
            "trader_dna": "Trader DNA Engine",
            "dna_score": "DNA Score",
            "trader_profile": "Trader Profile",
            "execution_style": "Execution Style",
            "risk_behavior": "Risk Behavior",
            "prop_firm_fit": "Prop Firm Fit",
            "profile_confidence": "Profile Confidence",
            "profile_summary": "Profile Summary",
            "strengths": "Strengths",
            "improvement_points": "Improvement Points",
            "language": "Language",
            "hero_title": "Institutional trading analytics",
            "hero_subtitle": "Professional-grade trading analytics platform focused on risk, consistency, performance and prop firm approval.",
            "hero_badge": "Risk infrastructure for serious traders",
            "start_free": "\U0001f680 Start free",
            "login": "\U0001f510 Login",
            "view_demo": "\U0001f4ca View demo",
            "why": "Why RiskPilot?",
            "feature_1_title": "\U0001f4c9 Risk Intelligence",
            "feature_1_text": "Detect dangerous drawdowns, overtrading, revenge trading and losing streaks automatically.",
            "feature_2_title": "\U0001f3c6 Prop Firm Ready",
            "feature_2_text": "Track daily loss, maximum drawdown, consistency and target distance.",
            "feature_3_title": "\U0001f916 Operational Insights",
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
            "back_home": "\u2190 Back to homepage",
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
            "select_upload": "Select an upload to view",
            "loaded_from_history": "Loaded from history. This analysis is read-only.",
            "terminal_title": "RiskPilot Terminal",
            "terminal_subtitle": "Institutional-grade trading risk intelligence and performance analytics.",
            "live_engine": "LIVE ANALYTICS ENGINE",
            "demo_info": "Demo mode: sample data loaded. Create a free account to upload and save your own trading reports.",
            "upload_report": "Upload trading report",
            "upload_to_begin": "Upload a CSV, XLSX, TXT or HTML report to begin.",
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
            "save_analysis": "\U0001f4be Save Analysis",
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
            "download_csv": "\u2b07\ufe0f Download normalized CSV",
            "download_pdf": "\U0001f4c4 Download professional PDF report",
            
        },
        "Portugu\u00eas": {
            "ai_coach": "AI Trading Coach",
"analyze_ai": "\U0001f9e0 Analisar com IA",
"ai_score": "AI Score",
"executive_summary": "Resumo Executivo",
"action_plan": "Plano de A\u00e7\u00e3o",
"risk_rules": "Regras de Risco",
"behavior_warnings": "Alertas Comportamentais",
            "institutional_radar": "Radar Institucional",
            "radar_discipline": "Disciplina",
            "radar_consistency": "Consist\u00eancia",
            "radar_risk_control": "Controle de Risco",
            "radar_execution": "Execu\u00e7\u00e3o",
            "radar_recovery": "Recupera\u00e7\u00e3o",
            "radar_prop_compatibility": "Compatibilidade Prop",
            "smart_prop_engine": "Motor Prop Firm Inteligente",
            "prop_rule_profile": "Perfil de Regras",
            "openai_ready": "OpenAI Ready",
            "openai_ready_sub": "Preparado para integra\u00e7\u00e3o com IA real",
            "trader_dna": "Motor Trader DNA",
            "dna_score": "DNA Score",
            "trader_profile": "Perfil do Trader",
            "execution_style": "Estilo de Execu\u00e7\u00e3o",
            "risk_behavior": "Comportamento de Risco",
            "prop_firm_fit": "Compatibilidade Prop Firm",
            "profile_confidence": "Confian\u00e7a do Perfil",
            "profile_summary": "Resumo do Perfil",
            "strengths": "Pontos Fortes",
            "improvement_points": "Pontos de Melhoria",
            "language": "Idioma",
            "hero_title": "Analytics institucional para traders",
            "hero_subtitle": "Plataforma profissional de an\u00e1lise operacional focada em risco, consist\u00eancia, performance e aprova\u00e7\u00e3o em prop firms.",
            "hero_badge": "Infraestrutura de risco para traders s\u00e9rios",
            "start_free": "\U0001f680 Criar conta gr\u00e1tis",
            "login": "\U0001f510 Entrar",
            "view_demo": "\U0001f4ca Ver demo",
            "why": "Por que RiskPilot?",
            "feature_1_title": "\U0001f4c9 Intelig\u00eancia de Risco",
            "feature_1_text": "Detecte drawdowns perigosos, overtrading, revenge trading e sequ\u00eancias ruins automaticamente.",
            "feature_2_title": "\U0001f3c6 Pronto para Prop Firms",
            "feature_2_text": "Acompanhe perda di\u00e1ria, drawdown m\u00e1ximo, consist\u00eancia e dist\u00e2ncia at\u00e9 a meta.",
            "feature_3_title": "\U0001f916 Insights Operacionais",
            "feature_3_text": "Descubra seus melhores hor\u00e1rios, piores padr\u00f5es e fraquezas operacionais.",
            "choose": "Escolha",
            "register": "Cadastrar",
            "name": "Nome",
            "email": "E-mail",
            "password": "Senha",
            "create_account": "Criar conta",
            "user_exists": "Usu\u00e1rio j\u00e1 existe.",
            "account_created": "Conta criada com sucesso. Agora voc\u00ea j\u00e1 pode entrar.",
            "invalid_credentials": "Credenciais inv\u00e1lidas.",
            "back_home": "\u2190 Voltar para a p\u00e1gina inicial",
            "professional_analytics": "Analytics Profissional de Trading",
            "authenticated_user": "Usu\u00e1rio autenticado",
            "current_mode": "Modo atual",
            "demo_mode": "Modo Demo",
            "create_free_account": "Criar conta gr\u00e1tis",
            "initial_capital": "Capital Inicial",
            "prop_firm_mode": "Modo Prop Firm",
            "account_size": "Tamanho da Conta",
            "daily_loss_limit": "Limite de Perda Di\u00e1ria",
            "max_drawdown_limit": "Limite M\u00e1ximo de Drawdown",
            "profit_target": "Meta de Lucro",
            "navigation": "Navega\u00e7\u00e3o",
            "dashboard": "Dashboard",
            "history": "Hist\u00f3rico",
            "logout": "Sair",
            "account_status": "Status da Conta",
            "active": "Ativa",
            "risk_mode": "Modo de Risco",
            "analytics": "Analytics",
            "enabled": "Ativado",
            "sidebar_note": "O RiskPilot monitora performance, drawdown, comportamento e consist\u00eancia operacional.",
            "history_title": "Hist\u00f3rico de Uploads",
            "history_account_required": "O hist\u00f3rico fica dispon\u00edvel ap\u00f3s criar uma conta gr\u00e1tis.",
            "no_uploads": "Ainda n\u00e3o h\u00e1 uploads salvos.",
            "select_upload": "Selecione um upload para visualizar",
            "loaded_from_history": "Carregado do hist\u00f3rico. Esta an\u00e1lise est\u00e1 em modo somente leitura.",
            "terminal_title": "Terminal RiskPilot",
            "terminal_subtitle": "Intelig\u00eancia institucional de risco e performance para traders.",
            "live_engine": "MOTOR DE AN\u00c1LISE ATIVO",
            "demo_info": "Modo demo: dados de exemplo carregados. Crie uma conta gr\u00e1tis para enviar e salvar seus pr\u00f3prios relat\u00f3rios.",
            "upload_report": "Upload do relat\u00f3rio de trades",
            "upload_to_begin": "Envie um arquivo CSV, XLSX, TXT ou HTML para come\u00e7ar.",
            "file_error": "Erro ao ler o arquivo",
            "performance": "Resumo de Performance",
            "net_pnl": "Resultado L\u00edquido",
            "total_net_result": "Resultado l\u00edquido total",
            "winrate": "Taxa de Acerto",
            "winning_trades": "Trades vencedores",
            "profit_factor": "Fator de Lucro",
            "gross_ratio": "Lucro bruto / perda bruta",
            "max_drawdown": "Drawdown M\u00e1ximo",
            "largest_decline": "Maior queda da curva",
            "risk_score": "Score de Risco",
            "risk_score_sub": "Qualidade do risco operacional",
            "consistency_score": "Score de Consist\u00eancia",
            "consistency_score_sub": "Estabilidade dia a dia",
            "account_health": "Sa\u00fade da Conta",
            "account_health_sub": "Prontid\u00e3o para prop firm",
            "behavior_score": "Score Comportamental",
            "behavior_score_sub": "Proxy de tilt e disciplina",
            "prop_firm_panel": "Painel de Controle Prop Firm",
            "approval_probability": "Probabilidade de Aprova\u00e7\u00e3o",
            "approval_probability_sub": "Estimativa de aprova\u00e7\u00e3o",
            "daily_remaining": "Perda Di\u00e1ria Restante",
            "daily_remaining_sub": "Margem antes da viola\u00e7\u00e3o di\u00e1ria",
            "drawdown_remaining": "Drawdown Restante",
            "drawdown_remaining_sub": "Margem antes da viola\u00e7\u00e3o da conta",
            "target_distance": "Dist\u00e2ncia da Meta",
            "target_distance_sub": "Faltante para a meta de lucro",
            "violation_risk": "Risco de Viola\u00e7\u00e3o",
            "violation_risk_sub": "Risco de reprova\u00e7\u00e3o operacional",
            "automatic_insights": "Insights Autom\u00e1ticos",
            "best_hour": "Melhor Hor\u00e1rio",
            "worst_hour": "Pior Hor\u00e1rio",
            "best_day": "Melhor Dia",
            "worst_day": "Pior Dia",
            "best_weekday": "Melhor Dia da Semana",
            "worst_weekday": "Pior Dia da Semana",
            "positive_days": "Dias Positivos",
            "negative_days": "Dias Negativos",
            "days_above_zero": "Dias acima de zero",
            "days_below_zero": "Dias abaixo de zero",
            "ai_diagnosis": "Diagn\u00f3stico Operacional",
            "equity_curve": "Curva de Capital",
            "drawdown": "Drawdown",
            "daily_pnl": "Resultado por Dia",
            "pnl_by_hour": "Resultado por Hor\u00e1rio",
            "pnl_by_weekday": "Resultado por Dia da Semana",
            "pnl_by_asset": "Resultado por Ativo",
            "risk_alerts": "Alertas de Risco",
            "save_analysis": "\U0001f4be Salvar An\u00e1lise",
            "analysis_saved": "An\u00e1lise salva.",
            "save_warning": "Crie uma conta gr\u00e1tis para salvar seu hist\u00f3rico de an\u00e1lises.",
            "trades": "Trades",
            "excellent": "Excelente",
            "healthy": "Saud\u00e1vel",
            "attention": "Aten\u00e7\u00e3o",
            "critical": "Cr\u00edtico",
            "low": "Baixo",
            "medium": "M\u00e9dio",
            "high": "Alto",
            "download_csv": "\u2b07\ufe0f Baixar CSV normalizado",
            "download_pdf": "\U0001f4c4 Baixar relat\u00f3rio profissional em PDF",
        },
        "Espa\u00f1ol": {
            "ai_coach": "AI Trading Coach",
"analyze_ai": "\U0001f9e0 Analizar con IA",
"ai_score": "AI Score",
"executive_summary": "Resumen Ejecutivo",
"action_plan": "Plan de Acci\u00f3n",
"risk_rules": "Reglas de Riesgo",
"behavior_warnings": "Alertas Conductuales",
            "institutional_radar": "Radar Institucional",
            "radar_discipline": "Disciplina",
            "radar_consistency": "Consistencia",
            "radar_risk_control": "Control de Riesgo",
            "radar_execution": "Ejecuci\u00f3n",
            "radar_recovery": "Recuperaci\u00f3n",
            "radar_prop_compatibility": "Compatibilidad Prop",
            "smart_prop_engine": "Motor Prop Firm Inteligente",
            "prop_rule_profile": "Perfil de Reglas",
            "openai_ready": "OpenAI Ready",
            "openai_ready_sub": "Preparado para integraci\u00f3n con IA real",
            "trader_dna": "Motor Trader DNA",
            "dna_score": "DNA Score",
            "trader_profile": "Perfil del Trader",
            "execution_style": "Estilo de Ejecuci\u00f3n",
            "risk_behavior": "Comportamiento de Riesgo",
            "prop_firm_fit": "Compatibilidad Prop Firm",
            "profile_confidence": "Confianza del Perfil",
            "profile_summary": "Resumen del Perfil",
            "strengths": "Fortalezas",
            "improvement_points": "Puntos de Mejora",
            "language": "Idioma",
            "hero_title": "Analytics institucional para traders",
            "hero_subtitle": "Plataforma profesional de an\u00e1lisis operativo enfocada en riesgo, consistencia, rendimiento y aprobaci\u00f3n en prop firms.",
            "hero_badge": "Infraestructura de riesgo para traders serios",
            "start_free": "\U0001f680 Crear cuenta gratis",
            "login": "\U0001f510 Entrar",
            "view_demo": "\U0001f4ca Ver demo",
            "why": "\u00bfPor qu\u00e9 RiskPilot?",
            "feature_1_title": "\U0001f4c9 Inteligencia de Riesgo",
            "feature_1_text": "Detecta drawdowns peligrosos, overtrading, revenge trading y secuencias negativas autom\u00e1ticamente.",
            "feature_2_title": "\U0001f3c6 Listo para Prop Firms",
            "feature_2_text": "Monitorea p\u00e9rdida diaria, drawdown m\u00e1ximo, consistencia y distancia a la meta.",
            "feature_3_title": "\U0001f916 Insights Operativos",
            "feature_3_text": "Descubre tus mejores horarios, peores patrones y debilidades operativas.",
            "choose": "Elige",
            "register": "Registrar",
            "name": "Nombre",
            "email": "Email",
            "password": "Contrase\u00f1a",
            "create_account": "Crear cuenta",
            "user_exists": "El usuario ya existe.",
            "account_created": "Cuenta creada con \u00e9xito. Ahora puedes entrar.",
            "invalid_credentials": "Credenciales inv\u00e1lidas.",
            "back_home": "\u2190 Volver al inicio",
            "professional_analytics": "Analytics Profesional de Trading",
            "authenticated_user": "Usuario autenticado",
            "current_mode": "Modo actual",
            "demo_mode": "Modo Demo",
            "create_free_account": "Crear cuenta gratis",
            "initial_capital": "Capital Inicial",
            "prop_firm_mode": "Modo Prop Firm",
            "account_size": "Tama\u00f1o de la Cuenta",
            "daily_loss_limit": "L\u00edmite de P\u00e9rdida Diaria",
            "max_drawdown_limit": "L\u00edmite M\u00e1ximo de Drawdown",
            "profit_target": "Meta de Lucro",
            "navigation": "Navegaci\u00f3n",
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
            "history_account_required": "El historial est\u00e1 disponible despu\u00e9s de crear una cuenta gratis.",
            "no_uploads": "A\u00fan no hay uploads guardados.",
            "select_upload": "Selecciona un upload para visualizar",
            "loaded_from_history": "Cargado desde historial. Este an\u00e1lisis est\u00e1 en modo solo lectura.",
            "terminal_title": "Terminal RiskPilot",
            "terminal_subtitle": "Inteligencia institucional de riesgo y rendimiento para traders.",
            "live_engine": "MOTOR DE AN\u00c1LISIS ACTIVO",
            "demo_info": "Modo demo: datos de ejemplo cargados. Crea una cuenta gratis para subir y guardar tus propios reportes.",
            "upload_report": "Subir reporte de trading",
            "upload_to_begin": "Sube un archivo CSV, XLSX, TXT o HTML para comenzar.",
            "file_error": "Error al leer el archivo",
            "performance": "Resumen de Rendimiento",
            "net_pnl": "Resultado Neto",
            "total_net_result": "Resultado neto total",
            "winrate": "Tasa de Acierto",
            "winning_trades": "Trades ganadores",
            "profit_factor": "Factor de Lucro",
            "gross_ratio": "Lucro bruto / p\u00e9rdida bruta",
            "max_drawdown": "Drawdown M\u00e1ximo",
            "largest_decline": "Mayor ca\u00edda de la curva",
            "risk_score": "Score de Riesgo",
            "risk_score_sub": "Calidad del riesgo operativo",
            "consistency_score": "Score de Consistencia",
            "consistency_score_sub": "Estabilidad d\u00eda a d\u00eda",
            "account_health": "Salud de la Cuenta",
            "account_health_sub": "Preparaci\u00f3n para prop firm",
            "behavior_score": "Score Conductual",
            "behavior_score_sub": "Proxy de tilt y disciplina",
            "prop_firm_panel": "Panel de Control Prop Firm",
            "approval_probability": "Probabilidad de Aprobaci\u00f3n",
            "approval_probability_sub": "Estimaci\u00f3n de aprobaci\u00f3n",
            "daily_remaining": "P\u00e9rdida Diaria Restante",
            "daily_remaining_sub": "Margen antes de violaci\u00f3n diaria",
            "drawdown_remaining": "Drawdown Restante",
            "drawdown_remaining_sub": "Margen antes de violaci\u00f3n de cuenta",
            "target_distance": "Distancia a la Meta",
            "target_distance_sub": "Faltante para la meta de lucro",
            "violation_risk": "Riesgo de Violaci\u00f3n",
            "violation_risk_sub": "Riesgo de reprobaci\u00f3n operativa",
            "automatic_insights": "Insights Autom\u00e1ticos",
            "best_hour": "Mejor Horario",
            "worst_hour": "Peor Horario",
            "best_day": "Mejor D\u00eda",
            "worst_day": "Peor D\u00eda",
            "best_weekday": "Mejor D\u00eda de la Semana",
            "worst_weekday": "Peor D\u00eda de la Semana",
            "positive_days": "D\u00edas Positivos",
            "negative_days": "D\u00edas Negativos",
            "days_above_zero": "D\u00edas sobre cero",
            "days_below_zero": "D\u00edas bajo cero",
            "ai_diagnosis": "Diagn\u00f3stico Operativo",
            "equity_curve": "Curva de Capital",
            "drawdown": "Drawdown",
            "daily_pnl": "Resultado Diario",
            "pnl_by_hour": "Resultado por Horario",
            "pnl_by_weekday": "Resultado por D\u00eda de la Semana",
            "pnl_by_asset": "Resultado por Activo",
            "risk_alerts": "Alertas de Riesgo",
            "save_analysis": "\U0001f4be Guardar An\u00e1lisis",
            "analysis_saved": "An\u00e1lisis guardado.",
            "save_warning": "Crea una cuenta gratis para guardar tu historial de an\u00e1lisis.",
            "trades": "Trades",
            "excellent": "Excelente",
            "healthy": "Saludable",
            "attention": "Atenci\u00f3n",
            "critical": "Cr\u00edtico",
            "low": "Bajo",
            "medium": "Medio",
            "high": "Alto",
            "download_csv": "\u2b07\ufe0f Descargar CSV normalizado",
            "download_pdf": "\U0001f4c4 Descargar informe profesional en PDF",
        },
    }
    return texts.get(language, texts["English"])
 
 
def language_options():
    return {
        "English - EN": "English",
        "Spanish - ES": "Espa\u00f1ol",
        "Portuguese - BR": "Portugu\u00eas",
    }
 
 
def language_display(language):
    reverse = {value: key for key, value in language_options().items()}
    return reverse.get(language, "English - EN")
 
 
def language_flag_pill(language):
    return ""
 
 
def upload_platform_label(language):
    if language == "Portugu\u00eas":
        return "Plataforma / formato do relat\u00f3rio"
    if language == "Espa\u00f1ol":
        return "Plataforma / formato del reporte"
    return "Platform / report format"
 
 
def platform_options(language):
    if language == "Portugu\u00eas":
        return {
            "Autom\u00e1tico": "auto",
            "MetaTrader 5": "mt5",
            "MetaTrader 4": "mt4",
            "ProfitChart / Nelogica": "profitchart",
            "TradingView": "tradingview",
            "CSV Gen\u00e9rico": "generic_csv",
            "Excel Gen\u00e9rico": "generic_excel",
        }
    if language == "Espa\u00f1ol":
        return {
            "Autom\u00e1tico": "auto",
            "MetaTrader 5": "mt5",
            "MetaTrader 4": "mt4",
            "ProfitChart / Nelogica": "profitchart",
            "TradingView": "tradingview",
            "CSV Gen\u00e9rico": "generic_csv",
            "Excel Gen\u00e9rico": "generic_excel",
        }
    return {
        "Automatic": "auto",
        "MetaTrader 5": "mt5",
        "MetaTrader 4": "mt4",
        "ProfitChart / Nelogica": "profitchart",
        "TradingView": "tradingview",
        "Generic CSV": "generic_csv",
        "Generic Excel": "generic_excel",
    }
 
 
def platform_help_text(language):
    if language == "Portugu\u00eas":
        return "Aceita CSV, XLSX, TXT e HTML. O RiskPilot tenta identificar automaticamente colunas de data, ativo, lado, quantidade e resultado."
    if language == "Espa\u00f1ol":
        return "Acepta CSV, XLSX, TXT y HTML. RiskPilot intenta identificar autom\u00e1ticamente columnas de fecha, activo, lado, cantidad y resultado."
    return "Supports CSV, XLSX, TXT and HTML. RiskPilot tries to identify date, symbol, side, quantity and result columns automatically."
 
 
 
 
# =========================================================
# MONETIZATION / PLAN GATES
# =========================================================
 
def plan_text(language):
    if language == "Portugu\u00eas":
        return {
            "current_plan": "Plano atual",
            "free": "Free",
            "pro": "Pro",
            "premium": "Premium",
            "upgrade_title": "Recurso bloqueado",
            "upgrade_pro": "Este recurso est\u00e1 dispon\u00edvel a partir do plano Pro.",
            "upgrade_premium": "Este recurso est\u00e1 dispon\u00edvel no plano Premium.",
            "upgrade_cta": "Atualizar plano",
            "free_limit": "Plano Free: limite de 1 upload por sess\u00e3o nesta vers\u00e3o de testes.",
            "pricing_note": "Checkout ainda n\u00e3o integrado. Esta tela j\u00e1 prepara a estrutura para Stripe ou Mercado Pago.",
        }
    if language == "Espa\u00f1ol":
        return {
            "current_plan": "Plan actual",
            "free": "Free",
            "pro": "Pro",
            "premium": "Premium",
            "upgrade_title": "Recurso bloqueado",
            "upgrade_pro": "Este recurso est\u00e1 disponible desde el plan Pro.",
            "upgrade_premium": "Este recurso est\u00e1 disponible en el plan Premium.",
            "upgrade_cta": "Actualizar plan",
            "free_limit": "Plan Free: l\u00edmite de 1 upload por sesi\u00f3n en esta versi\u00f3n de prueba.",
            "pricing_note": "Checkout a\u00fan no integrado. Esta pantalla ya prepara la estructura para Stripe o Mercado Pago.",
        }
    return {
        "current_plan": "Current plan",
        "free": "Free",
        "pro": "Pro",
        "premium": "Premium",
        "upgrade_title": "Feature locked",
        "upgrade_pro": "This feature is available from the Pro plan.",
        "upgrade_premium": "This feature is available on the Premium plan.",
        "upgrade_cta": "Upgrade plan",
        "free_limit": "Free plan: limited to 1 upload per session in this test version.",
        "pricing_note": "Checkout is not integrated yet. This screen is ready for Stripe or Mercado Pago.",
    }
 
 
def plan_options(language):
    txt = plan_text(language)
    return {txt["free"]: "Free", txt["pro"]: "Pro", txt["premium"]: "Premium"}
 
 
def plan_rank(plan):
    return {"Free": 0, "Pro": 1, "Premium": 2}.get(plan, 0)
 
 
def has_plan(required_plan):
    if is_admin_user():
        return True
    return plan_rank(st.session_state.get("user_plan", "Free")) >= plan_rank(required_plan)
 
 
def locked_feature_box(language, required_plan="Premium"):
    txt = plan_text(language)
    message = txt["upgrade_premium"] if required_plan == "Premium" else txt["upgrade_pro"]
    return (
        f'<div class="diagnosis-box">'
        f'<div class="diagnosis-title">\U0001f512 {txt["upgrade_title"]}</div>'
        f'<div class="diagnosis-text">{message}</div>'
        f'<div style="margin-top:14px;display:inline-block;background:linear-gradient(135deg,#0284c7,#0ea5e9);padding:10px 14px;border-radius:12px;color:white;font-weight:900;">{txt["upgrade_cta"]}</div>'
        f'</div>'
    )
 
 
def enforce_free_upload_limit(language, uploaded_file_name):
    if is_admin_user():
        return True
    if st.session_state.get("user_plan", "Free") != "Free":
        return True
    if "free_upload_count" not in st.session_state:
        st.session_state.free_upload_count = 0
    if "last_counted_upload" not in st.session_state:
        st.session_state.last_counted_upload = None
    if st.session_state.last_counted_upload != uploaded_file_name:
        st.session_state.free_upload_count += 1
        st.session_state.last_counted_upload = uploaded_file_name
    if st.session_state.free_upload_count > 1:
        st.warning(plan_text(language)["free_limit"])
        st.markdown(locked_feature_box(language, required_plan="Pro"), unsafe_allow_html=True)
        return False
    return True
 
def get_pricing_copy(language):
    if language == "Portugu\u00eas":
        return {
            "title": "Planos para cada fase do trader",
            "subtitle": "Comece gr\u00e1tis, evolua com analytics profissional e desbloqueie intelig\u00eancia comportamental premium.",
            "badge": "SaaS Trading Analytics",
            "free": "Free",
            "pro": "Pro",
            "premium": "Premium",
            "free_price": "R$ 0",
            "pro_price": "R$ 149,90/m\u00eas",
            "premium_price": "R$ 249,90/m\u00eas",
            "free_desc": "Para testar a plataforma e validar os primeiros relat\u00f3rios.",
            "pro_desc": "Para traders que querem acompanhar performance, risco e evolu\u00e7\u00e3o.",
            "premium_desc": "Para traders s\u00e9rios que querem AI Coach, DNA e radar institucional.",
            "popular": "Mais recomendado",
            "cta_free": "Come\u00e7ar gr\u00e1tis",
            "cta_pro": "Plano profissional",
            "cta_premium": "Desbloquear Premium",
            "comparison_title": "Compara\u00e7\u00e3o de recursos",
            "faq_title": "Perguntas frequentes",
            "faq_1_q": "O RiskPilot opera por mim?",
            "faq_1_a": "N\u00e3o. O RiskPilot analisa seus relat\u00f3rios, performance, risco e comportamento operacional.",
            "faq_2_q": "Funciona para prop firm?",
            "faq_2_a": "Sim. O sistema calcula limites, drawdown, aprova\u00e7\u00e3o estimada e risco de viola\u00e7\u00e3o.",
            "faq_3_q": "A IA j\u00e1 \u00e9 real?",
            "faq_3_a": "A estrutura est\u00e1 pronta para OpenAI real. A vers\u00e3o atual usa regras inteligentes e an\u00e1lise comportamental baseada em m\u00e9tricas.",
            "features": {
                "Uploads": ["1 por dia", "Ilimitado", "Ilimitado"],
                "Dashboard": ["B\u00e1sico", "Completo", "Institucional"],
                "Hist\u00f3rico": ["Limitado", "Completo", "Completo"],
                "PDF": ["N\u00e3o", "Sim", "Sim Premium"],
                "AI Coach": ["N\u00e3o", "Limitado", "Completo"],
                "Trader DNA": ["N\u00e3o", "Sim", "Avan\u00e7ado"],
                "Radar Institucional": ["N\u00e3o", "Sim", "Completo"],
                "Prop Firm Engine": ["B\u00e1sico", "Completo", "Completo"],
            },
        }
    if language == "Espa\u00f1ol":
        return {
            "title": "Planes para cada etapa del trader",
            "subtitle": "Empieza gratis, evoluciona con analytics profesional y desbloquea inteligencia conductual premium.",
            "badge": "SaaS Trading Analytics",
            "free": "Free",
            "pro": "Pro",
            "premium": "Premium",
            "free_price": "$0",
            "pro_price": "\u20ac29,90/m\u00eas",
            "premium_price": "\u20ac49,90/m\u00eas",
            "free_desc": "Para probar la plataforma y validar los primeros reportes.",
            "pro_desc": "Para traders que quieren seguir rendimiento, riesgo y evoluci\u00f3n.",
            "premium_desc": "Para traders serios que quieren AI Coach, DNA y radar institucional.",
            "popular": "M\u00e1s recomendado",
            "cta_free": "Empezar gratis",
            "cta_pro": "Plan profesional",
            "cta_premium": "Desbloquear Premium",
            "comparison_title": "Comparaci\u00f3n de recursos",
            "faq_title": "Preguntas frecuentes",
            "faq_1_q": "\u00bfRiskPilot opera por m\u00ed?",
            "faq_1_a": "No. RiskPilot analiza tus reportes, rendimiento, riesgo y comportamiento operativo.",
            "faq_2_q": "\u00bfFunciona para prop firms?",
            "faq_2_a": "S\u00ed. El sistema calcula l\u00edmites, drawdown, aprobaci\u00f3n estimada y riesgo de violaci\u00f3n.",
            "faq_3_q": "\u00bfLa IA ya es real?",
            "faq_3_a": "La estructura est\u00e1 lista para OpenAI real. La versi\u00f3n actual usa reglas inteligentes y an\u00e1lisis basado en m\u00e9tricas.",
            "features": {
                "Uploads": ["1 por d\u00eda", "Ilimitado", "Ilimitado"],
                "Dashboard": ["B\u00e1sico", "Completo", "Institucional"],
                "Historial": ["Limitado", "Completo", "Completo"],
                "PDF": ["No", "S\u00ed", "S\u00ed Premium"],
                "AI Coach": ["No", "Limitado", "Completo"],
                "Trader DNA": ["No", "S\u00ed", "Avanzado"],
                "Radar Institucional": ["No", "S\u00ed", "Completo"],
                "Prop Firm Engine": ["B\u00e1sico", "Completo", "Completo"],
            },
        }
    return {
        "title": "Plans for every trader stage",
        "subtitle": "Start free, evolve with professional analytics and unlock premium behavioral intelligence.",
        "badge": "SaaS Trading Analytics",
        "free": "Free",
        "pro": "Pro",
        "premium": "Premium",
        "free_price": "$0",
        "pro_price": "US$29.90/mo",
        "premium_price": "US$49.90/mo",
        "free_desc": "For testing the platform and validating your first reports.",
        "pro_desc": "For traders who want to track performance, risk and evolution.",
        "premium_desc": "For serious traders who want AI Coach, DNA and institutional radar.",
        "popular": "Most recommended",
        "cta_free": "Start free",
        "cta_pro": "Go Pro",
        "cta_premium": "Unlock Premium",
        "comparison_title": "Feature comparison",
        "faq_title": "Frequently asked questions",
        "faq_1_q": "Does RiskPilot trade for me?",
        "faq_1_a": "No. RiskPilot analyzes your reports, performance, risk and operational behavior.",
        "faq_2_q": "Does it work for prop firms?",
        "faq_2_a": "Yes. The system calculates limits, drawdown, estimated approval and violation risk.",
        "faq_3_q": "Is the AI already real?",
        "faq_3_a": "The structure is ready for real OpenAI integration. The current version uses intelligent rules and metric-based behavior analysis.",
        "features": {
            "Uploads": ["1 per day", "Unlimited", "Unlimited"],
            "Dashboard": ["Basic", "Full", "Institutional"],
            "History": ["Limited", "Full", "Full"],
            "PDF": ["No", "Yes", "Premium PDF"],
            "AI Coach": ["No", "Limited", "Full"],
            "Trader DNA": ["No", "Yes", "Advanced"],
            "Institutional Radar": ["No", "Yes", "Full"],
            "Prop Firm Engine": ["Basic", "Full", "Full"],
        },
    }
 
 
def render_pricing_section(language):
    copy = get_pricing_copy(language)
    st.markdown(
        f"""
        <div class="pricing-wrapper">
            <div class="pricing-badge">{copy["badge"]}</div>
            <div class="pricing-title">{copy["title"]}</div>
            <div class="pricing-subtitle">{copy["subtitle"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    plan_cols = st.columns(3, gap="large")
    plans = [
        (copy["free"], copy["free_price"], copy["free_desc"], copy["cta_free"], ""),
        (copy["pro"], copy["pro_price"], copy["pro_desc"], copy["cta_pro"], copy["popular"]),
        (copy["premium"], copy["premium_price"], copy["premium_desc"], copy["cta_premium"], "AI"),
    ]
 
    for col, plan in zip(plan_cols, plans):
        name, price, desc, cta, tag = plan
        with col:
            tag_html = f'<div class="plan-tag">{tag}</div>' if tag else '<div class="plan-tag plan-tag-muted">Starter</div>'
            st.markdown(
                f"""
                <div class="pricing-card">
                    {tag_html}
                    <div class="plan-name">{name}</div>
                    <div class="plan-price">{price}</div>
                    <div class="plan-desc">{desc}</div>
                    <div class="plan-cta">{cta}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
 
    st.markdown(f'<div class="section-title">{copy["comparison_title"]}</div>', unsafe_allow_html=True)
    rows = []
    for feature, values in copy["features"].items():
        rows.append({"Feature": feature, copy["free"]: values[0], copy["pro"]: values[1], copy["premium"]: values[2]})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.info(plan_text(language)["pricing_note"])
 
    st.markdown(f'<div class="section-title">{copy["faq_title"]}</div>', unsafe_allow_html=True)
    faq1, faq2, faq3 = st.columns(3, gap="large")
    faqs = [(copy["faq_1_q"], copy["faq_1_a"]), (copy["faq_2_q"], copy["faq_2_a"]), (copy["faq_3_q"], copy["faq_3_a"])]
    for col, (q, a) in zip([faq1, faq2, faq3], faqs):
        with col:
            st.markdown(
                f"""
                <div class="faq-card">
                    <div class="faq-question">{q}</div>
                    <div class="faq-answer">{a}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
 
 
# =========================================================
# CSS
# =========================================================
 
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
.metric-card{margin-bottom:18px;background:linear-gradient(135deg,#111827 0%,#1f2937 100%);border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:24px;min-height:125px;box-shadow:0 10px 30px rgba(0,0,0,.25)}.metric-title{color:#9ca3af!important;font-size:.9rem;font-weight:700}.metric-value{font-size:2rem;font-weight:850;margin-top:6px}.metric-sub{color:#64748b!important;font-size:.82rem;margin-top:6px}.value-positive{color:#22c55e!important}.value-negative{color:#fb7185!important}.value-neutral{color:#38bdf8!important}.value-warning{color:#f59e0b!important}
.section-title{font-size:2rem;font-weight:850;color:#fff!important;margin-top:60px;margin-bottom:24px;letter-spacing:-.035em}.alert-box{background:#1f2937;border-left:5px solid #f59e0b;padding:16px;border-radius:12px;margin-bottom:12px;color:#fff!important}.diagnosis-box{margin-bottom:18px;background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(30,41,59,.78));border:1px solid rgba(56,189,248,.18);border-radius:22px;padding:22px 24px;margin-bottom:14px}.diagnosis-title{color:#7dd3fc!important;font-size:.85rem;font-weight:850;text-transform:uppercase;letter-spacing:.08em}.diagnosis-text{color:#e5e7eb!important;font-size:1rem;line-height:1.6;margin-top:8px}
.insight-card{margin-bottom:18px;background:linear-gradient(135deg,#0f172a 0%,#172554 100%);border:1px solid rgba(56,189,248,.22);border-radius:18px;padding:24px;min-height:148px;margin-bottom:24px;box-shadow:0 10px 30px rgba(0,0,0,.20)}.insight-title{color:#94a3b8!important;font-size:.88rem;font-weight:750}.insight-value{font-size:1.65rem;font-weight:850;margin-top:8px}.insight-sub{color:#7dd3fc!important;font-size:.85rem;margin-top:8px}
.auth-box{max-width:620px;margin:30px auto;background:linear-gradient(135deg,#101827 0%,#172033 100%);border:1px solid rgba(255,255,255,.09);border-radius:26px;padding:35px}.terminal-header{background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(2,6,23,.78));border:1px solid rgba(148,163,184,.14);border-radius:26px;padding:26px 30px;margin-bottom:30px;box-shadow:0 20px 70px rgba(0,0,0,.28)}.terminal-title{color:#fff!important;font-size:2.65rem;font-weight:950;letter-spacing:-.055em;line-height:1.05}.terminal-subtitle{color:#94a3b8!important;font-size:1rem;margin-top:8px}.terminal-pill{display:inline-block;background:rgba(34,197,94,.12);color:#86efac!important;border:1px solid rgba(34,197,94,.28);border-radius:999px;padding:7px 12px;font-size:.78rem;font-weight:800;margin-top:12px}
.stButton>button{border-radius:14px;min-height:52px;font-weight:800;font-size:1rem;border:1px solid rgba(255,255,255,.15);background:#0f172a!important;color:#fff!important}.stButton>button:hover{border-color:#38bdf8!important;color:#7dd3fc!important}input,textarea,select{color:#fff!important}[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stSelectbox"] div,[data-testid="stDateInput"] input{background:#111827!important;color:#fff!important}
 
.radar-card{background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(30,41,59,.70));border:1px solid rgba(56,189,248,.22);border-radius:24px;padding:20px;margin-bottom:18px;box-shadow:0 18px 50px rgba(0,0,0,.28)}
.premium-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(56,189,248,.55),transparent);margin:24px 0}
 
.metric-card{display:flex;flex-direction:column;justify-content:center;gap:6px;min-height:158px;overflow:hidden;margin-bottom:22px;}
.metric-value{font-size:clamp(1.35rem,1.7vw,2rem)!important;line-height:1.12!important;overflow-wrap:normal!important;word-break:normal!important;hyphens:none!important;}
.metric-title,.metric-sub{line-height:1.25!important;overflow-wrap:normal!important;word-break:normal!important;}
.diagnosis-box,.alert-box,.insight-card{overflow-wrap:normal!important;word-break:normal!important;hyphens:none!important;}
@media (max-width: 1100px){.metric-card{min-height:135px;padding:18px!important}.metric-value{font-size:1.45rem!important}.section-title{font-size:1.65rem!important}}
 
.score-ring-card{background:linear-gradient(135deg,#101827 0%,#1e293b 100%);border:1px solid rgba(56,189,248,.24);border-radius:26px;padding:30px;display:flex;align-items:center;gap:28px;min-height:230px;margin-bottom:26px;box-shadow:0 22px 70px rgba(0,0,0,.28)}
.score-ring{width:168px;height:168px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--ring-color) calc(var(--score)*1%),rgba(30,41,59,.80) 0);position:relative;box-shadow:0 0 38px rgba(56,189,248,.18)}
.score-ring::before{content:"";position:absolute;width:118px;height:118px;border-radius:50%;background:#0b1220;border:1px solid rgba(148,163,184,.18)}
.score-ring-value{position:relative;z-index:1;font-size:2.05rem;font-weight:950;color:#fff!important;letter-spacing:-.05em}.score-ring-label{position:relative;z-index:1;font-size:.72rem;color:#94a3b8!important;margin-top:-4px}
.score-ring-content{flex:1}.score-ring-title{color:#93c5fd!important;font-size:.82rem;text-transform:uppercase;letter-spacing:.12em;font-weight:900;margin-bottom:8px}.score-ring-status{font-size:2.25rem;font-weight:950;letter-spacing:-.05em;margin-bottom:8px}.score-ring-text{color:#cbd5e1!important;font-size:1rem;line-height:1.55}.score-ring-hint{color:#64748b!important;font-size:.82rem;margin-top:8px}
[data-testid="column"]{padding-left:.48rem!important;padding-right:.48rem!important}.stColumn{gap:1.2rem!important}
@media (max-width: 900px){.score-ring-card{flex-direction:column;text-align:center}.score-ring{width:140px;height:140px}.score-ring::before{width:98px;height:98px}}
 
 
 
.language-flag-pill{display:inline-flex;align-items:center;gap:8px;background:rgba(15,23,42,.92);border:1px solid rgba(56,189,248,.28);border-radius:999px;padding:8px 12px;margin:8px 0 4px 0;box-shadow:0 8px 24px rgba(0,0,0,.22)}
.language-flag-img{width:22px!important;height:22px!important;min-width:22px!important;max-width:22px!important;object-fit:cover!important;border-radius:50%!important;display:inline-block!important}.language-flag-icon{font-size:1.45rem;line-height:1}.language-flag-text{font-size:.86rem;font-weight:800;color:#e5e7eb!important;white-space:nowrap!important}
.pricing-wrapper{margin-top:70px;text-align:center;padding:32px 20px;border-radius:28px;background:linear-gradient(135deg,rgba(15,23,42,.62),rgba(2,6,23,.2));border:1px solid rgba(56,189,248,.14)}
.pricing-badge{display:inline-flex;padding:7px 12px;border-radius:999px;background:rgba(34,197,94,.11);border:1px solid rgba(34,197,94,.26);color:#86efac!important;font-size:.82rem;font-weight:900;text-transform:uppercase;letter-spacing:.08em;margin-bottom:16px}.pricing-title{font-size:2.55rem;font-weight:950;letter-spacing:-.055em;color:#fff!important}.pricing-subtitle{max-width:760px;margin:14px auto 0 auto;color:#94a3b8!important;font-size:1.08rem;line-height:1.65}
.pricing-card{position:relative;min-height:255px;margin-top:24px;border-radius:26px;padding:28px;background:linear-gradient(135deg,#101827 0%,#172033 100%);border:1px solid rgba(56,189,248,.18);box-shadow:0 20px 55px rgba(0,0,0,.28)}.pricing-card:hover{border-color:rgba(56,189,248,.55);box-shadow:0 25px 70px rgba(14,165,233,.15)}.plan-tag{display:inline-flex;padding:6px 10px;border-radius:999px;background:rgba(14,165,233,.16);border:1px solid rgba(14,165,233,.35);color:#7dd3fc!important;font-size:.72rem;font-weight:900;text-transform:uppercase;letter-spacing:.08em}.plan-tag-muted{background:rgba(148,163,184,.10);border-color:rgba(148,163,184,.20);color:#cbd5e1!important}.plan-name{font-size:1.55rem;font-weight:950;color:#fff!important;margin-top:18px}.plan-price{font-size:2.15rem;font-weight:950;color:#22c55e!important;margin-top:10px}.plan-desc{color:#94a3b8!important;font-size:.95rem;line-height:1.55;margin-top:10px;min-height:52px}.plan-cta{margin-top:20px;background:linear-gradient(135deg,#0284c7,#0ea5e9);color:#fff!important;border-radius:14px;padding:13px 16px;text-align:center;font-weight:900;box-shadow:0 12px 35px rgba(14,165,233,.18)}
.faq-card{min-height:170px;border-radius:22px;padding:24px;background:rgba(15,23,42,.84);border:1px solid rgba(148,163,184,.14);box-shadow:0 14px 40px rgba(0,0,0,.20);margin-bottom:20px}.faq-question{font-size:1.05rem;font-weight:900;color:#fff!important;line-height:1.35}.faq-answer{font-size:.92rem;color:#94a3b8!important;line-height:1.6;margin-top:12px}
 
</style>
""", unsafe_allow_html=True)
 
 
# =========================================================
# HELPERS
# =========================================================
 
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
 
 
def score_ring_card(title, score, status, profile, hint=""):
    try:
        score_int = int(float(score))
    except Exception:
        score_int = 0
    score_int = max(0, min(100, score_int))
    if score_int >= 80:
        ring_color = "#22c55e"
        status_class = "value-positive"
    elif score_int >= 60:
        ring_color = "#f59e0b"
        status_class = "value-warning"
    else:
        ring_color = "#fb7185"
        status_class = "value-negative"
    return f"""
    <div class="score-ring-card">
        <div class="score-ring" style="--score:{score_int};--ring-color:{ring_color};">
            <div>
                <div class="score-ring-value">{score_int}</div>
                <div class="score-ring-label">/100</div>
            </div>
        </div>
        <div class="score-ring-content">
            <div class="score-ring-title">{title}</div>
            <div class="score-ring-status {status_class}">{status}</div>
            <div class="score-ring-text">{profile}</div>
            <div class="score-ring-hint">{hint}</div>
        </div>
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
 
 
 
def clamp_score(value):
    try:
        value = float(value)
    except Exception:
        value = 0
    return max(0, min(100, round(value)))
 
 
def build_radar_scores(risk_score, consistency_score, behavior_score, approval, metrics, daily):
    profit_factor = float(metrics.get("profit_factor", 0))
    net_pnl = float(metrics.get("net_pnl", 0))
    loss_streak = float(metrics.get("max_loss_streak", 0))
 
    risk_control = clamp_score(risk_score)
    consistency = clamp_score(consistency_score)
    discipline = clamp_score(behavior_score)
    prop_compatibility = clamp_score(approval)
    execution = clamp_score(min(max(profit_factor / 1.8, 0), 1) * 100)
 
    if daily.empty:
        recovery = 50
    else:
        positive_days = int((daily > 0).sum())
        negative_days = int((daily < 0).sum())
        recovery = clamp_score(55 + (positive_days - negative_days) * 7 + (10 if net_pnl > 0 else -10) - loss_streak * 4)
 
    return {
        "Discipline": discipline,
        "Consistency": consistency,
        "Risk Control": risk_control,
        "Execution": execution,
        "Recovery": recovery,
        "Prop Compatibility": prop_compatibility,
    }
 
 
def make_radar_chart(radar_scores, t):
    labels = [
        t["radar_discipline"],
        t["radar_consistency"],
        t["radar_risk_control"],
        t["radar_execution"],
        t["radar_recovery"],
        t["radar_prop_compatibility"],
    ]
    values = [
        radar_scores["Discipline"],
        radar_scores["Consistency"],
        radar_scores["Risk Control"],
        radar_scores["Execution"],
        radar_scores["Recovery"],
        radar_scores["Prop Compatibility"],
    ]
 
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name="RiskPilot Radar",
            line=dict(color="#38bdf8", width=3),
            fillcolor="rgba(56,189,248,0.22)",
        )
    )
    fig.update_layout(
        template="plotly_dark",
        height=470,
        margin=dict(l=30, r=30, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(148,163,184,0.22)"),
            angularaxis=dict(gridcolor="rgba(148,163,184,0.18)"),
        ),
        showlegend=False,
    )
    return fig
 
 
def prop_firm_behavior(prop_mode):
    """Controls how strict each prop firm profile is in the scoring layer."""
    behaviors = {
        "FTMO": {"strictness": 1.00, "consistency_weight": 1.00, "drawdown_weight": 1.00, "style": "Balanced challenge / strict daily loss", "badge": "\U0001f3e6"},
        "Apex": {"strictness": 1.18, "consistency_weight": 1.12, "drawdown_weight": 1.20, "style": "Futures profile / trailing drawdown sensitivity", "badge": "\u26a1"},
        "TopStep": {"strictness": 1.25, "consistency_weight": 1.15, "drawdown_weight": 1.25, "style": "Futures combine / very strict discipline", "badge": "\U0001f3af"},
        "FundingPips": {"strictness": 0.95, "consistency_weight": 1.05, "drawdown_weight": 0.95, "style": "Flexible challenge / consistency focus", "badge": "\U0001f48e"},
        "MyFundedFX": {"strictness": 1.03, "consistency_weight": 1.05, "drawdown_weight": 1.02, "style": "Balanced FX challenge", "badge": "\U0001f310"},
        "MyFundedFutures": {"strictness": 1.15, "consistency_weight": 1.10, "drawdown_weight": 1.18, "style": "Futures evaluation / drawdown sensitive", "badge": "\U0001f4c8"},
        "TakeProfit": {"strictness": 1.05, "consistency_weight": 1.08, "drawdown_weight": 1.05, "style": "Balanced target / consistency aware", "badge": "\U0001f680"},
        "E8": {"strictness": 1.08, "consistency_weight": 1.10, "drawdown_weight": 1.08, "style": "Institutional evaluation profile", "badge": "\U0001f3db\ufe0f"},
        "Custom": {"strictness": 1.00, "consistency_weight": 1.00, "drawdown_weight": 1.00, "style": "Custom rule profile", "badge": "\u2699\ufe0f"},
        "Personalizado": {"strictness": 1.00, "consistency_weight": 1.00, "drawdown_weight": 1.00, "style": "Perfil personalizado", "badge": "\u2699\ufe0f"},
    }
    return behaviors.get(prop_mode, behaviors["Custom"])
 
 
def prop_profiles(account_size):
    """Smart Prop Firm Engine - rule presets used for risk dashboards."""
    return {
        "Custom": {"target": account_size * 0.10, "daily": account_size * 0.05, "drawdown": account_size * 0.10, "label": "Custom rule profile"},
        "Personalizado": {"target": account_size * 0.10, "daily": account_size * 0.05, "drawdown": account_size * 0.10, "label": "Perfil personalizado"},
        "FTMO": {"target": account_size * 0.10, "daily": account_size * 0.05, "drawdown": account_size * 0.10, "label": "FTMO style: 10% target / 5% daily / 10% max"},
        "Apex": {"target": account_size * 0.06, "daily": account_size * 0.03, "drawdown": account_size * 0.05, "label": "Apex style: futures evaluation profile"},
        "MyFundedFX": {"target": account_size * 0.08, "daily": account_size * 0.05, "drawdown": account_size * 0.08, "label": "MyFundedFX style: balanced evaluation"},
        "MyFundedFutures": {"target": account_size * 0.06, "daily": account_size * 0.03, "drawdown": account_size * 0.05, "label": "MyFundedFutures style: futures risk profile"},
        "TopStep": {"target": account_size * 0.06, "daily": account_size * 0.03, "drawdown": account_size * 0.04, "label": "TopStep style: strict drawdown control"},
        "TakeProfit": {"target": account_size * 0.08, "daily": account_size * 0.04, "drawdown": account_size * 0.08, "label": "TakeProfit style: balanced target and drawdown"},
        "FundingPips": {"target": account_size * 0.08, "daily": account_size * 0.05, "drawdown": account_size * 0.10, "label": "FundingPips style: target with 10% max drawdown"},
        "E8": {"target": account_size * 0.08, "daily": account_size * 0.05, "drawdown": account_size * 0.08, "label": "E8 style: institutional evaluation profile"},
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
 
 
def calculate_prop_status(metrics, daily, profit_target, max_daily_loss, max_drawdown_limit, risk_score, consistency_score, behavior_score, prop_mode="Custom"):
    net_pnl = float(metrics.get("net_pnl", 0))
    max_dd = float(metrics.get("max_drawdown", 0))
    profit_factor = float(metrics.get("profit_factor", 0))
    worst_day = abs(float(daily.min())) if not daily.empty else 0
 
    behavior = prop_firm_behavior(prop_mode)
    strictness = float(behavior.get("strictness", 1.0))
    consistency_weight = float(behavior.get("consistency_weight", 1.0))
    drawdown_weight = float(behavior.get("drawdown_weight", 1.0))
 
    target_distance = profit_target - net_pnl
    daily_remaining = max_daily_loss - worst_day
    dd_remaining = max_drawdown_limit - max_dd
 
    daily_ratio = max(0, min(1, daily_remaining / max(max_daily_loss, 1)))
    dd_ratio = max(0, min(1, dd_remaining / max(max_drawdown_limit, 1)))
    target_ratio = max(0, min(1, net_pnl / max(profit_target, 1)))
    pf_bonus = max(0, min(1, (profit_factor - 1.0) / 1.0))
 
    strictness_penalty = (strictness - 1.0) * 12
    consistency_adjusted = max(0, min(100, consistency_score / max(consistency_weight, 0.01)))
    drawdown_adjusted = max(0, min(100, (dd_ratio * 100) / max(drawdown_weight, 0.01)))
 
    approval = round(
        (risk_score * 0.30)
        + (consistency_adjusted * 0.22)
        + (behavior_score * 0.18)
        + (daily_ratio * 10)
        + (drawdown_adjusted * 0.10)
        + (target_ratio * 6)
        + (pf_bonus * 4)
        - strictness_penalty
    )
 
    approval = max(0, min(100, approval))
    violation_score = max(0, min(100, 100 - approval + round(strictness_penalty)))
 
    if daily_remaining < 0 or dd_remaining < 0:
        approval = min(approval, 12)
        violation_score = max(violation_score, 92)
 
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
 
    if language == "Portugu\u00eas":
        items = []
        items.append("O Profit Factor est\u00e1 abaixo de 1, indicando que o operacional ainda perde mais do que ganha." if profit_factor < 1 else "O Profit Factor est\u00e1 acima de 1, indicando vantagem operacional inicial.")
        if net_pnl < 0:
            items.append("O resultado l\u00edquido est\u00e1 negativo. A prioridade agora \u00e9 reduzir drawdown e filtrar hor\u00e1rios ruins.")
        if worst_hour != "N/A":
            items.append(f"O pior hor\u00e1rio foi {worst_hour}h, com resultado de {money(worst_hour_value)}. Esse per\u00edodo merece bloqueio, redu\u00e7\u00e3o de lote ou revis\u00e3o de setup.")
        if best_hour != "N/A":
            items.append(f"O melhor hor\u00e1rio foi {best_hour}h, com resultado de {money(best_hour_value)}. Esse pode ser seu principal per\u00edodo operacional.")
        if loss_streak >= 4:
            items.append(f"Foi detectada sequ\u00eancia de {loss_streak} perdas. Isso pode indicar tilt, insist\u00eancia ou condi\u00e7\u00e3o ruim de mercado.")
        items.append(f"Probabilidade estimada de aprova\u00e7\u00e3o: {approval}/100. Faltam {money(target_distance)} para a meta, {money(daily_remaining)} de margem di\u00e1ria e {money(dd_remaining)} de margem no drawdown m\u00e1ximo.")
        items.append(f"Score de risco: {risk_score}/100. Score de consist\u00eancia: {consistency_score}/100. Score comportamental: {behavior_score}/100. Foram encontrados {negative_days} dias negativos.")
        return items
 
    if language == "Espa\u00f1ol":
        items = []
        items.append("El Profit Factor est\u00e1 por debajo de 1, indicando que el sistema a\u00fan pierde m\u00e1s de lo que gana." if profit_factor < 1 else "El Profit Factor est\u00e1 por encima de 1, indicando una ventaja operativa inicial.")
        if net_pnl < 0:
            items.append("El resultado neto est\u00e1 negativo. La prioridad ahora es reducir drawdown y filtrar horarios d\u00e9biles.")
        if worst_hour != "N/A":
            items.append(f"El peor horario fue {worst_hour}h, con resultado de {money(worst_hour_value)}. Ese periodo merece bloqueo, reducci\u00f3n de lote o revisi\u00f3n de setup.")
        if best_hour != "N/A":
            items.append(f"El mejor horario fue {best_hour}h, con resultado de {money(best_hour_value)}. Puede ser tu principal ventana operativa.")
        if loss_streak >= 4:
            items.append(f"Se detect\u00f3 una secuencia de {loss_streak} p\u00e9rdidas. Esto puede indicar tilt, insistencia o malas condiciones de mercado.")
        items.append(f"Probabilidad estimada de aprobaci\u00f3n: {approval}/100. Faltan {money(target_distance)} para la meta, {money(daily_remaining)} de margen diario y {money(dd_remaining)} de margen en drawdown m\u00e1ximo.")
        items.append(f"Score de riesgo: {risk_score}/100. Score de consistencia: {consistency_score}/100. Score conductual: {behavior_score}/100. Se encontraron {negative_days} d\u00edas negativos.")
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
 
 
 
def build_trader_dna(
    language,
    metrics,
    daily,
    hourly,
    weekday,
    risk_score,
    consistency_score,
    behavior_score,
    approval,
):
    """Rule-based Trader DNA profile engine."""
 
    net_pnl = float(metrics.get("net_pnl", 0))
    profit_factor = float(metrics.get("profit_factor", 0))
    winrate = float(metrics.get("winrate", 0))
    max_drawdown = float(metrics.get("max_drawdown", 0))
    total_trades = int(metrics.get("total_trades", 0))
    loss_streak = int(metrics.get("max_loss_streak", 0))
 
    positive_days = int((daily > 0).sum()) if not daily.empty else 0
    negative_days = int((daily < 0).sum()) if not daily.empty else 0
 
    best_hour = hourly.idxmax() if not hourly.empty else "N/A"
    worst_hour = hourly.idxmin() if not hourly.empty else "N/A"
 
    best_weekday = weekday.idxmax() if not weekday.empty else "N/A"
    worst_weekday = weekday.idxmin() if not weekday.empty else "N/A"
 
    dna_score = round(
        risk_score * 0.28
        + consistency_score * 0.27
        + behavior_score * 0.25
        + approval * 0.20
    )
    dna_score = max(0, min(100, dna_score))
 
    if total_trades >= 120:
        execution_density = "high"
    elif total_trades >= 50:
        execution_density = "medium"
    else:
        execution_density = "low"
 
    if language == "Portugu\u00eas":
        if dna_score >= 80 and profit_factor >= 1.2 and behavior_score >= 75:
            profile = "Trader Institucional"
        elif total_trades >= 120 and loss_streak >= 4:
            profile = "Scalper Agressivo com Risco de Tilt"
        elif approval >= 70 and consistency_score >= 65:
            profile = "Prop Firm Ready"
        elif profit_factor < 1 and negative_days >= positive_days:
            profile = "Trader Defensivo em Recupera\u00e7\u00e3o"
        elif winrate >= 65 and profit_factor >= 1:
            profile = "Trader de Alta Assertividade"
        else:
            profile = "Trader em Desenvolvimento"
 
        execution_style = {
            "high": "Alta frequ\u00eancia operacional",
            "medium": "Frequ\u00eancia moderada",
            "low": "Baixa frequ\u00eancia / amostra pequena",
        }[execution_density]
 
        if behavior_score >= 75:
            risk_behavior = "Disciplina saud\u00e1vel"
        elif behavior_score >= 50:
            risk_behavior = "Risco comportamental moderado"
        else:
            risk_behavior = "Risco elevado de tilt ou overtrading"
 
        if approval >= 75:
            prop_fit = "Alta compatibilidade"
        elif approval >= 50:
            prop_fit = "Compatibilidade moderada"
        else:
            prop_fit = "Baixa compatibilidade"
 
        summary = [
            f"O perfil dominante identificado foi: {profile}.",
            f"O melhor hor\u00e1rio operacional foi {best_hour}h e o pior hor\u00e1rio foi {worst_hour}h.",
            f"O melhor dia da semana foi {best_weekday}; o ponto de aten\u00e7\u00e3o foi {worst_weekday}.",
            f"A an\u00e1lise encontrou {positive_days} dias positivos e {negative_days} dias negativos.",
        ]
 
        strengths = []
        improvements = []
 
        if profit_factor >= 1:
            strengths.append("Existe vantagem operacional inicial pelo Profit Factor acima de 1.")
        else:
            improvements.append("Aumentar seletividade de entrada at\u00e9 o Profit Factor superar 1.20.")
 
        if consistency_score >= 65:
            strengths.append("A consist\u00eancia di\u00e1ria est\u00e1 em n\u00edvel aceit\u00e1vel para evolu\u00e7\u00e3o.")
        else:
            improvements.append("Reduzir dispers\u00e3o dos resultados di\u00e1rios e evitar dias muito negativos.")
 
        if behavior_score >= 70:
            strengths.append("O comportamento de risco est\u00e1 relativamente controlado.")
        else:
            improvements.append("Criar trava operacional ap\u00f3s perdas consecutivas para reduzir tilt.")
 
        if approval >= 70:
            strengths.append("O perfil atual tem boa ader\u00eancia ao ambiente de prop firm.")
        else:
            improvements.append("Melhorar controle de drawdown antes de buscar aprova\u00e7\u00e3o em prop firm.")
 
        if not strengths:
            strengths.append("H\u00e1 dados suficientes para iniciar uma evolu\u00e7\u00e3o guiada por m\u00e9tricas.")
        if not improvements:
            improvements.append("Manter o mesmo padr\u00e3o de risco e evitar aumentar lote cedo demais.")
 
    elif language == "Espa\u00f1ol":
        if dna_score >= 80 and profit_factor >= 1.2 and behavior_score >= 75:
            profile = "Trader Institucional"
        elif total_trades >= 120 and loss_streak >= 4:
            profile = "Scalper Agresivo con Riesgo de Tilt"
        elif approval >= 70 and consistency_score >= 65:
            profile = "Prop Firm Ready"
        elif profit_factor < 1 and negative_days >= positive_days:
            profile = "Trader Defensivo en Recuperaci\u00f3n"
        elif winrate >= 65 and profit_factor >= 1:
            profile = "Trader de Alta Asertividad"
        else:
            profile = "Trader en Desarrollo"
 
        execution_style = {
            "high": "Alta frecuencia operativa",
            "medium": "Frecuencia moderada",
            "low": "Baja frecuencia / muestra peque\u00f1a",
        }[execution_density]
 
        if behavior_score >= 75:
            risk_behavior = "Disciplina saludable"
        elif behavior_score >= 50:
            risk_behavior = "Riesgo conductual moderado"
        else:
            risk_behavior = "Riesgo elevado de tilt u overtrading"
 
        if approval >= 75:
            prop_fit = "Alta compatibilidad"
        elif approval >= 50:
            prop_fit = "Compatibilidad moderada"
        else:
            prop_fit = "Baja compatibilidad"
 
        summary = [
            f"El perfil dominante identificado fue: {profile}.",
            f"El mejor horario operativo fue {best_hour}h y el peor horario fue {worst_hour}h.",
            f"El mejor d\u00eda de la semana fue {best_weekday}; el punto de atenci\u00f3n fue {worst_weekday}.",
            f"El an\u00e1lisis encontr\u00f3 {positive_days} d\u00edas positivos y {negative_days} d\u00edas negativos.",
        ]
 
        strengths = []
        improvements = []
 
        if profit_factor >= 1:
            strengths.append("Existe una ventaja operativa inicial por Profit Factor superior a 1.")
        else:
            improvements.append("Aumentar la selectividad de entrada hasta superar Profit Factor 1.20.")
 
        if consistency_score >= 65:
            strengths.append("La consistencia diaria est\u00e1 en un nivel aceptable para evolucionar.")
        else:
            improvements.append("Reducir dispersi\u00f3n de resultados diarios y evitar d\u00edas muy negativos.")
 
        if behavior_score >= 70:
            strengths.append("El comportamiento de riesgo est\u00e1 relativamente controlado.")
        else:
            improvements.append("Crear bloqueo operativo despu\u00e9s de p\u00e9rdidas consecutivas para reducir tilt.")
 
        if approval >= 70:
            strengths.append("El perfil actual tiene buena compatibilidad con prop firms.")
        else:
            improvements.append("Mejorar control de drawdown antes de buscar aprobaci\u00f3n en prop firm.")
 
        if not strengths:
            strengths.append("Hay datos suficientes para iniciar una evoluci\u00f3n guiada por m\u00e9tricas.")
        if not improvements:
            improvements.append("Mantener el mismo patr\u00f3n de riesgo y evitar aumentar lote demasiado pronto.")
 
    else:
        if dna_score >= 80 and profit_factor >= 1.2 and behavior_score >= 75:
            profile = "Institutional Trader"
        elif total_trades >= 120 and loss_streak >= 4:
            profile = "Aggressive Scalper with Tilt Risk"
        elif approval >= 70 and consistency_score >= 65:
            profile = "Prop Firm Ready"
        elif profit_factor < 1 and negative_days >= positive_days:
            profile = "Defensive Recovery Trader"
        elif winrate >= 65 and profit_factor >= 1:
            profile = "High Accuracy Trader"
        else:
            profile = "Developing Trader"
 
        execution_style = {
            "high": "High-frequency execution",
            "medium": "Moderate execution frequency",
            "low": "Low frequency / small sample",
        }[execution_density]
 
        if behavior_score >= 75:
            risk_behavior = "Healthy discipline"
        elif behavior_score >= 50:
            risk_behavior = "Moderate behavioral risk"
        else:
            risk_behavior = "Elevated tilt or overtrading risk"
 
        if approval >= 75:
            prop_fit = "High compatibility"
        elif approval >= 50:
            prop_fit = "Moderate compatibility"
        else:
            prop_fit = "Low compatibility"
 
        summary = [
            f"The dominant profile identified was: {profile}.",
            f"Best trading hour was {best_hour}h and weakest trading hour was {worst_hour}h.",
            f"Best weekday was {best_weekday}; key attention point was {worst_weekday}.",
            f"The analysis found {positive_days} positive days and {negative_days} negative days.",
        ]
 
        strengths = []
        improvements = []
 
        if profit_factor >= 1:
            strengths.append("There is an initial operational edge with Profit Factor above 1.")
        else:
            improvements.append("Increase entry selectivity until Profit Factor rises above 1.20.")
 
        if consistency_score >= 65:
            strengths.append("Daily consistency is at an acceptable level for development.")
        else:
            improvements.append("Reduce daily result dispersion and avoid very negative days.")
 
        if behavior_score >= 70:
            strengths.append("Risk behavior appears relatively controlled.")
        else:
            improvements.append("Create a hard stop after consecutive losses to reduce tilt risk.")
 
        if approval >= 70:
            strengths.append("Current profile has good prop firm compatibility.")
        else:
            improvements.append("Improve drawdown control before pursuing prop firm approval.")
 
        if not strengths:
            strengths.append("There is enough data to start metric-driven improvement.")
        if not improvements:
            improvements.append("Maintain current risk behavior and avoid increasing size too early.")
 
    return {
        "dna_score": dna_score,
        "profile": profile,
        "execution_style": execution_style,
        "risk_behavior": risk_behavior,
        "prop_fit": prop_fit,
        "confidence": f"{min(95, max(45, total_trades // 2 + 45))}%",
        "summary": summary,
        "strengths": strengths[:4],
        "improvements": improvements[:4],
    }
 
 
def _normalize_text(value):
    value = str(value).strip().lower()
    value = value.replace("\ufeff", "").replace("\x00", "")
    value = value.replace("<", "").replace(">", "")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.replace("\n", " ").replace("\r", " ")
    value = " ".join(value.split())
    return value
 
 
def _find_column(df, candidates):
    normalized_columns = {_normalize_text(col): col for col in df.columns}
    for candidate in candidates:
        candidate_norm = _normalize_text(candidate)
        if candidate_norm in normalized_columns:
            return normalized_columns[candidate_norm]
    for candidate in candidates:
        candidate_norm = _normalize_text(candidate)
        for norm_col, original_col in normalized_columns.items():
            if candidate_norm in norm_col or norm_col in candidate_norm:
                return original_col
    return None
 
 
def _to_number(series):
    if series is None:
        return None
 
    def convert_one(value):
        if pd.isna(value):
            return None
        text = str(value).strip()
        text = text.replace("\ufeff", "").replace("\x00", "")
        text = text.replace("R$", "").replace("$", "").replace("\u20ac", "")
        text = text.replace(" ", "").replace("\u00a0", "")
        text = text.replace("%", "")
        text = text.replace("+", "")
 
        if text in ["", "-", "--", "nan", "None"]:
            return None
 
        # Brazilian format: 1.234,56
        if "," in text and "." in text:
            if text.rfind(",") > text.rfind("."):
                text = text.replace(".", "").replace(",", ".")
            else:
                text = text.replace(",", "")
 
        # Decimal comma only: 1234,56
        elif "," in text and "." not in text:
            text = text.replace(",", ".")
 
        try:
            return float(text)
        except Exception:
            return None
 
    return pd.to_numeric(series.apply(convert_one), errors="coerce")
 
 
def _clean_imported_columns(df):
    df = df.copy()
    cleaned = []
    for col in df.columns:
        col_text = str(col).replace("\ufeff", "").replace("\x00", "").strip()
        col_text = col_text.replace("<", "").replace(">", "").strip()
        cleaned.append(col_text)
    df.columns = cleaned
    return df
 
 
def _read_csv_safely(file_bytes):
    encodings = ["utf-16", "utf-16-le", "utf-16-be", "utf-8-sig", "utf-8", "latin1", "cp1252"]
    separators = ["\t", ";", ",", "|", None]
    best_df = None
    best_score = -1
    last_error = None
 
    for encoding in encodings:
        for separator in separators:
            try:
                buffer = io.BytesIO(file_bytes)
                if separator is None:
                    df = pd.read_csv(buffer, sep=None, engine="python", encoding=encoding)
                else:
                    df = pd.read_csv(buffer, sep=separator, engine="python", encoding=encoding)
 
                df = _clean_imported_columns(df)
                df = df.dropna(how="all")
 
                score = int(df.shape[1]) * 10 + int(df.shape[0] > 0)
                recognizable = sum(1 for col in df.columns if _normalize_text(col) in ["date", "time", "datetime", "balance", "equity", "profit", "pnl", "net pnl"])
                score += recognizable * 25
 
                if df.shape[0] > 0 and df.shape[1] > 1 and score > best_score:
                    best_df = df
                    best_score = score
            except Exception as exc:
                last_error = exc
 
    if best_df is not None:
        return best_df
 
    raise ValueError(f"Could not read CSV/TXT file. Last error: {last_error}")
 
 
def _read_excel_safely(file_bytes):
    """Read Excel reports from MetaTrader/ProfitChart/TradingView and generic XLSX files.
 
    Some MetaTrader Strategy Tester exports are not simple tables: they contain
    many metadata rows before the real deal table. This function scans every
    sheet, detects the most likely header row, and returns a clean DataFrame.
    """
    excel_buffer = io.BytesIO(file_bytes)
 
    try:
        excel_file = pd.ExcelFile(excel_buffer)
    except Exception as exc:
        raise ValueError(f"Could not open Excel workbook. Details: {exc}")
 
    best_df = None
    best_score = -1
 
    date_terms = {
        "date", "time", "datetime", "date time", "open time", "close time",
        "data", "hora", "horario", "data hora", "data/hora", "fecha",
        "fecha hora", "fecha/hora", "tempo", "abertura", "fechamento"
    }
    pnl_terms = {
        "profit", "pnl", "p&l", "lucro", "resultado", "net profit",
        "gross profit", "profit loss", "profit/loss", "realized p/l",
        "ganho", "pl"
    }
    trade_terms = {
        "symbol", "asset", "ativo", "type", "tipo", "direcao", "dire\u00e7\u00e3o",
        "volume", "preco", "pre\u00e7o", "price", "ordem", "order", "deal",
        "oferta", "commission", "comissao", "comiss\u00e3o", "swap", "saldo",
        "balance"
    }
 
    for sheet_name in excel_file.sheet_names:
        try:
            raw = pd.read_excel(
                io.BytesIO(file_bytes),
                sheet_name=sheet_name,
                header=None,
                dtype=object,
            )
        except Exception:
            continue
 
        raw = raw.dropna(how="all")
        if raw.empty:
            continue
 
        # Try the first row as a normal table header.
        try:
            normal_df = pd.read_excel(
                io.BytesIO(file_bytes),
                sheet_name=sheet_name,
                dtype=object,
            )
            normal_df = _clean_imported_columns(normal_df).dropna(how="all")
            normal_cols = {_normalize_text(col) for col in normal_df.columns}
            normal_score = len(normal_df) + 10 * len(normal_df.columns)
            if normal_cols & date_terms:
                normal_score += 200
            if normal_cols & pnl_terms:
                normal_score += 200
            if normal_cols & trade_terms:
                normal_score += 60
            if normal_df.shape[0] > 0 and normal_df.shape[1] > 1 and normal_score > best_score:
                best_df = normal_df
                best_score = normal_score
        except Exception:
            pass
 
        # Scan rows to find embedded table headers, common in MetaTrader reports.
        for row_idx in range(len(raw)):
            row_values = raw.iloc[row_idx].tolist()
            headers = [str(value).replace("\x00", "").strip() if pd.notna(value) else "" for value in row_values]
            normalized_headers = [_normalize_text(value) for value in headers]
            non_empty = [value for value in normalized_headers if value]
 
            if len(non_empty) < 3:
                continue
 
            has_date = any(value in date_terms for value in non_empty)
            has_pnl = any(value in pnl_terms for value in non_empty)
            trade_hits = sum(1 for value in non_empty if value in trade_terms)
 
            score = 0
            if has_date:
                score += 300
            if has_pnl:
                score += 10000
            score += trade_hits * 40
            score += len(non_empty) * 5
            score += max(0, len(raw) - row_idx)
 
            # Require either date+pnl or a strong row with many known trade columns.
            if not ((has_date and has_pnl) or (has_date and trade_hits >= 4)):
                continue
 
            candidate = raw.iloc[row_idx + 1:].copy()
            if candidate.empty:
                continue
 
            # Make duplicate/blank headers safe.
            safe_headers = []
            seen = {}
            for pos, header in enumerate(headers):
                name = header if header else f"column_{pos}"
                count = seen.get(name, 0)
                seen[name] = count + 1
                if count:
                    name = f"{name}_{count}"
                safe_headers.append(name)
 
            candidate.columns = safe_headers[:candidate.shape[1]]
            candidate = _clean_imported_columns(candidate).dropna(how="all")
 
            if candidate.shape[0] > 0 and candidate.shape[1] > 1 and score > best_score:
                best_df = candidate
                best_score = score
 
    if best_df is not None:
        return best_df.reset_index(drop=True)
 
    raise ValueError("Could not identify a valid table inside the Excel file. Export the report as XLSX or CSV with Date/Time and Profit columns.")
 
 
def load_universal_trading_file(uploaded_file, platform="auto"):
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()
 
    if file_name.endswith((".xlsx", ".xls")):
        return _read_excel_safely(file_bytes)
 
    if file_name.endswith((".html", ".htm")):
        try:
            tables = pd.read_html(io.BytesIO(file_bytes))
            tables = [tbl for tbl in tables if tbl.shape[0] > 0 and tbl.shape[1] > 1]
            if tables:
                return max(tables, key=lambda tbl: tbl.shape[0] * tbl.shape[1])
        except Exception:
            pass
        return _read_csv_safely(file_bytes)
 
    return _read_csv_safely(file_bytes)
 
 
def _parse_datetime_series(series):
    raw = series.astype(str).str.replace("\x00", "", regex=False).str.strip()
 
    # First try ISO / yyyy-mm-dd / yyyy.mm.dd formats.
    parsed = pd.to_datetime(raw, errors="coerce")
 
    # Then try Brazilian/European day-first formats only where needed.
    missing = parsed.isna()
    if missing.any():
        parsed_alt = pd.to_datetime(raw[missing], errors="coerce", dayfirst=True)
        parsed.loc[missing] = parsed_alt
 
    return parsed
 
 
def universal_normalize_trades(raw_df, platform="auto"):
    df = raw_df.copy()
    df = df.dropna(how="all")
    df = _clean_imported_columns(df)
    df.columns = [str(col).strip() for col in df.columns]
 
    date_col = _find_column(df, [
        "date", "time", "datetime", "date time", "open time", "close time", "data", "hora", "horario", "hor\u00e1rio", "tempo", "data/hora", "data hora", "fecha", "fecha/hora",
        "open date", "close date", "entry time", "exit time", "abertura", "fechamento"
    ])
    asset_col = _find_column(df, [
        "asset", "symbol", "ticker", "ativo", "instrument", "instrumento", "mercado", "produto", "contrato", "scrip", "security"
    ])
    side_col = _find_column(df, [
        "side", "type", "operation", "operacao", "opera\u00e7\u00e3o", "direcao", "dire\u00e7\u00e3o", "buy/sell", "compra/venda", "action", "order type"
    ])
    qty_col = _find_column(df, [
        "quantity", "qty", "volume", "lots", "lot", "contracts", "contratos", "quantidade", "qtd", "size", "amount"
    ])
    entry_col = _find_column(df, [
        "entry_price", "entry price", "open price", "price", "preco", "pre\u00e7o", "preco entrada", "pre\u00e7o entrada", "entrada", "open", "avg price"
    ])
    exit_col = _find_column(df, [
        "exit_price", "exit price", "close price", "preco saida", "pre\u00e7o sa\u00edda", "saida", "sa\u00edda", "close", "closing price"
    ])
    fees_col = _find_column(df, [
        "fees", "fee", "commission", "commissions", "corretagem", "taxas", "custos", "costs", "swap", "charges"
    ])
    pnl_col = _find_column(df, [
        "net_pnl", "net pnl", "pnl", "p&l", "profit", "profit/loss", "profit loss", "lucro", "resultado", "resultado liquido",
        "resultado l\u00edquido", "net profit", "gross profit", "close profit", "profit currency", "pl", "gain", "realized p/l"
    ])
 
    balance_col = _find_column(df, [
        "balance", "saldo", "saldo conta", "account balance", "balanco", "balan\u00e7o"
    ])
    equity_col = _find_column(df, [
        "equity", "patrimonio", "patrim\u00f4nio", "saldo liquido", "saldo l\u00edquido", "account equity"
    ])
 
    if date_col is None:
        raise ValueError("Could not identify the date/time column. Please export a report with Date/Time, Open Time or Close Time.")
 
    parsed_dates = _parse_datetime_series(df[date_col])
 
    # TesterGraph / strategy tester equity reports often do not have trade rows.
    # They usually contain DATE, BALANCE, EQUITY and DEPOSIT LOAD. In this case,
    # RiskPilot reconstructs closed-result events from BALANCE changes.
    if pnl_col is None and (balance_col is not None or equity_col is not None):
        source_col = balance_col if balance_col is not None else equity_col
        source_values = _to_number(df[source_col])
        pnl_values = source_values.diff().fillna(0)
 
        normalized = pd.DataFrame()
        normalized["date"] = parsed_dates
        normalized["asset"] = "TesterGraph"
        normalized["side"] = "balance_change" if balance_col is not None else "equity_change"
        normalized["quantity"] = 1
        normalized["entry_price"] = source_values.shift(1).fillna(source_values)
        normalized["exit_price"] = source_values
        normalized["fees"] = 0
        normalized["pnl"] = pnl_values
        normalized["net_pnl"] = pnl_values
 
        normalized = normalized.dropna(subset=["date"])
        normalized = normalized[normalized["net_pnl"].notna()]
        normalized = normalized[normalized["net_pnl"].abs() > 0.0000001]
 
        if normalized.empty:
            raise ValueError("The file was read as an equity/balance report, but no balance/equity changes were found.")
 
        return normalized.reset_index(drop=True)
 
    if pnl_col is None:
        raise ValueError("Could not identify the result/P&L column. Please export a report with Profit, PnL, Resultado, Net Profit, Balance or Equity.")
 
    normalized = pd.DataFrame()
    normalized["date"] = parsed_dates
    normalized["asset"] = df[asset_col].astype(str) if asset_col else "UNKNOWN"
    normalized["side"] = df[side_col].astype(str).str.lower() if side_col else "unknown"
    normalized["quantity"] = _to_number(df[qty_col]).fillna(1) if qty_col else 1
    normalized["entry_price"] = _to_number(df[entry_col]).fillna(0) if entry_col else 0
    normalized["exit_price"] = _to_number(df[exit_col]).fillna(0) if exit_col else 0
    normalized["fees"] = _to_number(df[fees_col]).fillna(0) if fees_col else 0
    pnl_values = _to_number(df[pnl_col]).fillna(0)
    normalized["pnl"] = pnl_values
    normalized["net_pnl"] = pnl_values - normalized["fees"].abs()
 
    normalized = normalized.dropna(subset=["date"])
    normalized = normalized[normalized["net_pnl"].notna()]
 
    # MetaTrader deal tables usually include the initial balance row and entry rows
    # with zero profit. These rows are useful in the platform report, but they
    # distort RiskPilot metrics if counted as trades.
    asset_clean = normalized["asset"].astype(str).str.lower().str.strip()
    normalized = normalized[~asset_clean.isin(["", "nan", "none", "balance"])]
 
    side_clean = normalized["side"].astype(str).str.lower().str.strip()
    if side_clean.isin(["in", "entrada"]).any() and side_clean.isin(["out", "saida", "sa\u00edda"]).any():
        normalized = normalized[~side_clean.isin(["in", "entrada"])]
 
    # Remove zero-result operational rows generated by order/open-position exports.
    normalized = normalized[normalized["net_pnl"].abs() > 0.0000001]
 
    if normalized.empty:
        raise ValueError("The file was read, but no valid trades were found after normalization.")
 
    return normalized.reset_index(drop=True)
 
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
 
 
# =========================================================
# RENDER DO DASHBOARD COMPLETO
# =========================================================
 
def render_full_dashboard(
    normalized_df,
    t,
    language,
    initial_capital,
    max_daily_loss,
    max_drawdown_limit,
    profit_target,
    prop_mode,
    account_size,
    uploaded_file_name,
    allow_save=True,
    read_only=False,
):
    normalized_df = prepare_dataframe(normalized_df, initial_capital)
    metrics = calculate_metrics(normalized_df, initial_capital)
 
    hourly = normalized_df.groupby("hour")["net_pnl"].sum()
    daily = normalized_df.groupby("day")["net_pnl"].sum()
    weekday = normalized_df.groupby("weekday")["net_pnl"].sum()
 
    risk_score, consistency_score, account_health, behavior_score = calculate_scores(
        metrics,
        daily,
        max_daily_loss,
        max_drawdown_limit,
    )
 
    approval, daily_remaining, dd_remaining, target_distance, violation_score = calculate_prop_status(
        metrics,
        daily,
        profit_target,
        max_daily_loss,
        max_drawdown_limit,
        risk_score,
        consistency_score,
        behavior_score,
        prop_mode,
    )
 
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
    positive_days = int((daily > 0).sum()) if not daily.empty else 0
    negative_days = int((daily < 0).sum()) if not daily.empty else 0
 
    diagnosis_items = generate_diagnosis(
        language,
        metrics,
        daily,
        hourly,
        risk_score,
        consistency_score,
        behavior_score,
        approval,
        target_distance,
        daily_remaining,
        dd_remaining,
    )
 
    alerts = generate_risk_alerts(
        normalized_df,
        max_daily_loss,
        max_drawdown_limit,
        language=language,
    )
 
    ai_report_preview = build_ai_coach_report(
        language=language,
        metrics=metrics,
        daily=daily,
        hourly=hourly,
        risk_score=risk_score,
        consistency_score=consistency_score,
        behavior_score=behavior_score,
        approval_probability=approval,
        target_distance=target_distance,
        daily_remaining=daily_remaining,
        dd_remaining=dd_remaining,
    )
 
    ai_score = ai_report_preview["score"]
    prop_behavior = prop_firm_behavior(prop_mode)
    prop_description = prop_behavior.get("label", prop_behavior.get("style", prop_mode))
 
    st.markdown(
        score_ring_card(
            t["ai_score"],
            ai_score,
            ai_report_preview["status"],
            ai_report_preview["profile"],
            ai_report_preview["headline"],
        ),
        unsafe_allow_html=True,
    )
 
    hero_1, hero_2, hero_3 = st.columns(3, gap="large")
    with hero_1:
        st.markdown(metric_card(t["net_pnl"], money(metrics["net_pnl"]), t["total_net_result"], value_class(metrics["net_pnl"])), unsafe_allow_html=True)
    with hero_2:
        st.markdown(metric_card(t["approval_probability"], f"{approval}/100", prop_mode, score_class(approval)), unsafe_allow_html=True)
    with hero_3:
        st.markdown(metric_card(t["violation_risk"], violation_label(violation_score, t), t["violation_risk_sub"], score_class(100 - violation_score)), unsafe_allow_html=True)
 
    st.markdown(
        diagnosis_box(
            f'{prop_behavior.get("badge", "\U0001f3e6")} {prop_mode}',
            f'{prop_description} \u00b7 Strictness {prop_behavior.get("strictness", 1.0):.2f}x \u00b7 Target {money(profit_target)} \u00b7 Daily {money(max_daily_loss)} \u00b7 Max DD {money(max_drawdown_limit)}',
        ),
        unsafe_allow_html=True,
    )
 
    section(t["equity_curve"])
    st.plotly_chart(make_equity_chart(normalized_df, t), use_container_width=True)
 
    section(t["drawdown"])
    st.plotly_chart(make_drawdown_chart(normalized_df, t), use_container_width=True)
 
    section(t["institutional_radar"])
    if not has_plan("Premium"):
        st.markdown(locked_feature_box(language, required_plan="Premium"), unsafe_allow_html=True)
    else:
        radar_scores = build_radar_scores(
            risk_score=risk_score,
            consistency_score=consistency_score,
            behavior_score=behavior_score,
            approval=approval,
            metrics=metrics,
            daily=daily,
        )
 
        radar_col, radar_metrics_col = st.columns([1.35, 1], gap="large")
        with radar_col:
            st.plotly_chart(make_radar_chart(radar_scores, t), use_container_width=True)
 
        with radar_metrics_col:
            st.markdown(metric_card(t["radar_risk_control"], f'{radar_scores["Risk Control"]}/100', t["max_drawdown_limit"], score_class(radar_scores["Risk Control"])), unsafe_allow_html=True)
            st.markdown(metric_card(t["radar_consistency"], f'{radar_scores["Consistency"]}/100', t["consistency_score_sub"], score_class(radar_scores["Consistency"])), unsafe_allow_html=True)
            st.markdown(metric_card(t["radar_prop_compatibility"], f'{radar_scores["Prop Compatibility"]}/100', t["approval_probability"], score_class(radar_scores["Prop Compatibility"])), unsafe_allow_html=True)
 
    section(t["performance"])
    perf_1, perf_2, perf_3, perf_4 = st.columns(4, gap="large")
    with perf_1:
        st.markdown(metric_card(t["winrate"], percent(metrics["winrate"]), t["winning_trades"], value_class(metrics["winrate"], warning_threshold=50)), unsafe_allow_html=True)
    with perf_2:
        st.markdown(metric_card(t["profit_factor"], f"{metrics['profit_factor']:.2f}", t["gross_ratio"], value_class(metrics["profit_factor"], warning_threshold=1)), unsafe_allow_html=True)
    with perf_3:
        st.markdown(metric_card(t["max_drawdown"], money(metrics["max_drawdown"]), t["largest_decline"], value_class(metrics["max_drawdown"], higher_is_better=False)), unsafe_allow_html=True)
    with perf_4:
        st.markdown(metric_card(t["target_distance"], money(target_distance), t["target_distance_sub"], "value-neutral" if target_distance > 0 else "value-positive"), unsafe_allow_html=True)
 
    risk_1, risk_2, risk_3 = st.columns(3, gap="large")
    with risk_1:
        st.markdown(metric_card(t["daily_remaining"], money(daily_remaining), t["daily_remaining_sub"], value_class(daily_remaining)), unsafe_allow_html=True)
    with risk_2:
        st.markdown(metric_card(t["drawdown_remaining"], money(dd_remaining), t["drawdown_remaining_sub"], value_class(dd_remaining)), unsafe_allow_html=True)
    with risk_3:
        st.markdown(metric_card(t["risk_score"], f"{risk_score}/100", t["risk_score_sub"], score_class(risk_score)), unsafe_allow_html=True)
 
    section(t["automatic_insights"])
    insight_1, insight_2, insight_3, insight_4 = st.columns(4, gap="large")
    with insight_1:
        st.markdown(insight_card(t["best_hour"], f"{best_hour}h", money(best_hour_pnl), value_class(best_hour_pnl)), unsafe_allow_html=True)
    with insight_2:
        st.markdown(insight_card(t["worst_hour"], f"{worst_hour}h", money(worst_hour_pnl), value_class(worst_hour_pnl)), unsafe_allow_html=True)
    with insight_3:
        st.markdown(insight_card(t["positive_days"], positive_days, t["days_above_zero"], "value-positive"), unsafe_allow_html=True)
    with insight_4:
        st.markdown(insight_card(t["negative_days"], negative_days, t["days_below_zero"], "value-negative"), unsafe_allow_html=True)
 
    insight_5, insight_6 = st.columns(2, gap="large")
    with insight_5:
        st.markdown(insight_card(t["best_day"], str(best_day), money(best_day_pnl), value_class(best_day_pnl)), unsafe_allow_html=True)
    with insight_6:
        st.markdown(insight_card(t["worst_day"], str(worst_day), money(worst_day_pnl), value_class(worst_day_pnl)), unsafe_allow_html=True)
 
    section(t["trader_dna"])
    if not has_plan("Premium"):
        st.markdown(locked_feature_box(language, required_plan="Premium"), unsafe_allow_html=True)
    else:
        trader_dna = build_trader_dna(
            language=language,
            metrics=metrics,
            daily=daily,
            hourly=hourly,
            weekday=weekday,
            risk_score=risk_score,
            consistency_score=consistency_score,
            behavior_score=behavior_score,
            approval=approval,
        )
 
        dna_color = score_class(trader_dna["dna_score"])
 
        dna_col1, dna_col2, dna_col3 = st.columns(3, gap="large")
        with dna_col1:
            st.markdown(metric_card(t["trader_profile"], trader_dna["profile"], t["profile_summary"], dna_color), unsafe_allow_html=True)
        with dna_col2:
            st.markdown(metric_card(t["dna_score"], f'{trader_dna["dna_score"]}/100', t["profile_confidence"] + ": " + trader_dna["confidence"], dna_color), unsafe_allow_html=True)
        with dna_col3:
            st.markdown(metric_card(t["prop_firm_fit"], trader_dna["prop_fit"], t["prop_firm_panel"], dna_color), unsafe_allow_html=True)
 
        dna_summary_col, dna_strength_col, dna_improve_col = st.columns(3, gap="large")
        with dna_summary_col:
            st.markdown(f"## {t['profile_summary']}")
            for item in trader_dna["summary"][:3]:
                st.markdown(f'<div class="diagnosis-box">\U0001f9ec {item}</div>', unsafe_allow_html=True)
        with dna_strength_col:
            st.markdown(f"## {t['strengths']}")
            for item in trader_dna["strengths"][:3]:
                st.markdown(f'<div class="diagnosis-box">\u2705 {item}</div>', unsafe_allow_html=True)
        with dna_improve_col:
            st.markdown(f"## {t['improvement_points']}")
            for item in trader_dna["improvements"][:3]:
                st.markdown(f'<div class="alert-box">\U0001f4cc {item}</div>', unsafe_allow_html=True)
 
    section(t["ai_coach"])
    if not has_plan("Premium"):
        st.markdown(locked_feature_box(language, required_plan="Premium"), unsafe_allow_html=True)
    else:
        loading_texts = {
            "Portugu\u00eas": [
                "Mapeando padr\u00f5es comportamentais...",
                "Detectando risco de tilt e revenge trading...",
                "Avaliando consist\u00eancia para prop firm...",
                "Calculando qualidade operacional...",
                "Gerando diagn\u00f3stico institucional...",
            ],
            "Espa\u00f1ol": [
                "Mapeando patrones conductuales...",
                "Detectando riesgo de tilt y revenge trading...",
                "Evaluando consistencia para prop firm...",
                "Calculando calidad operativa...",
                "Generando diagn\u00f3stico institucional...",
            ],
            "English": [
                "Mapping behavioral patterns...",
                "Detecting tilt and revenge trading risk...",
                "Evaluating prop firm consistency...",
                "Calculating execution quality...",
                "Generating institutional diagnosis...",
            ],
        }
 
        ai_button_help = {
            "Portugu\u00eas": "Gera uma an\u00e1lise comportamental premium com plano de a\u00e7\u00e3o.",
            "Espa\u00f1ol": "Genera un an\u00e1lisis conductual premium con plan de acci\u00f3n.",
            "English": "Generates a premium behavioral analysis with an action plan.",
        }.get(language, "Generates a premium behavioral analysis with an action plan.")
 
        if st.button(t["analyze_ai"], help=ai_button_help):
            loading_box = st.empty()
            progress_bar = st.progress(0)
            steps = loading_texts.get(language, loading_texts["English"])
 
            for index, message in enumerate(steps):
                percent_done = int(((index + 1) / len(steps)) * 100)
                loading_box.markdown(
                    f'<div class="diagnosis-box"><div class="diagnosis-title">AI TRADING COACH</div><div class="diagnosis-text">\U0001f9e0 {message}</div></div>',
                    unsafe_allow_html=True,
                )
                progress_bar.progress(percent_done)
                time.sleep(0.35)
 
            loading_box.empty()
            progress_bar.empty()
 
            ai_report = build_ai_coach_report(
                language=language,
                metrics=metrics,
                daily=daily,
                hourly=hourly,
                risk_score=risk_score,
                consistency_score=consistency_score,
                behavior_score=behavior_score,
                approval_probability=approval,
                target_distance=target_distance,
                daily_remaining=daily_remaining,
                dd_remaining=dd_remaining,
            )
 
            st.markdown(score_ring_card(t["ai_score"], ai_report["score"], ai_report["status"], ai_report["profile"], ai_report["headline"]), unsafe_allow_html=True)
 
            col_ai_1, col_ai_2 = st.columns(2, gap="large")
            with col_ai_1:
                st.markdown(f"## {t['executive_summary']}")
                for item in ai_report["executive_summary"][:4]:
                    st.markdown(f'<div class="diagnosis-box">{item}</div>', unsafe_allow_html=True)
                st.markdown(f"## {t['behavior_warnings']}")
                if ai_report["warnings"]:
                    for item in ai_report["warnings"]:
                        st.markdown(f'<div class="alert-box">\u26a0\ufe0f {item}</div>', unsafe_allow_html=True)
                else:
                    no_warning_text = {"Portugu\u00eas": "Nenhum alerta comportamental cr\u00edtico detectado.", "Espa\u00f1ol": "No se detectaron alertas conductuales cr\u00edticos.", "English": "No critical behavioral warnings detected."}.get(language, "No critical behavioral warnings detected.")
                    st.success(no_warning_text)
 
            with col_ai_2:
                st.markdown(f"## {t['action_plan']}")
                for item in ai_report["action_plan"][:5]:
                    st.markdown(f'<div class="diagnosis-box">\u2705 {item}</div>', unsafe_allow_html=True)
                st.markdown(f"## {t['risk_rules']}")
                for item in ai_report["rules"][:5]:
                    st.markdown(f'<div class="diagnosis-box">\U0001f4cc {item}</div>', unsafe_allow_html=True)
 
    section(t["risk_alerts"])
    for alert in alerts:
        st.markdown(f'<div class="alert-box">\u26a0\ufe0f {alert}</div>', unsafe_allow_html=True)
 
    csv = normalized_df.to_csv(index=False).encode("utf-8")
    st.download_button(t["download_csv"], csv, f"riskpilot_{uploaded_file_name.replace(' ', '_')}.csv", "text/csv")
 
    insights_for_pdf = [
        {"label": t["best_hour"], "value": f"{best_hour}h", "result": money(best_hour_pnl)},
        {"label": t["worst_hour"], "value": f"{worst_hour}h", "result": money(worst_hour_pnl)},
        {"label": t["best_day"], "value": str(best_day), "result": money(best_day_pnl)},
        {"label": t["worst_day"], "value": str(worst_day), "result": money(worst_day_pnl)},
        {"label": t["best_weekday"], "value": str(best_weekday), "result": money(best_weekday_pnl)},
        {"label": t["worst_weekday"], "value": str(worst_weekday), "result": money(worst_weekday_pnl)},
        {"label": t["positive_days"], "value": str(positive_days), "result": t["days_above_zero"]},
        {"label": t["negative_days"], "value": str(negative_days), "result": t["days_below_zero"]},
    ]
 
    if has_plan("Pro"):
        pdf_bytes = build_pdf_report(
            language=language,
            title=t["terminal_title"],
            subtitle=t["terminal_subtitle"],
            file_name=uploaded_file_name,
            prop_mode=prop_mode,
            account_size=account_size,
            metrics=metrics,
            scores=(risk_score, consistency_score, account_health, behavior_score),
            prop_status=(approval, daily_remaining, dd_remaining, target_distance, violation_score),
            insights=insights_for_pdf,
            diagnosis_items=diagnosis_items,
            alerts=alerts,
            trades_df=normalized_df,
        )
 
        st.download_button(t["download_pdf"], pdf_bytes, f"riskpilot_report_{uploaded_file_name.replace(' ', '_')}.pdf", "application/pdf")
    else:
        st.markdown(locked_feature_box(language, required_plan="Pro"), unsafe_allow_html=True)
 
    if read_only:
        st.info(t["loaded_from_history"])
    elif allow_save and st.session_state.authenticated and has_plan("Pro"):
        if st.button(t["save_analysis"]):
            save_upload(account_name=prop_mode, platform="Unknown", file_name=uploaded_file_name, trades_df=normalized_df, metrics=metrics, user_email=st.session_state.user_email)
            st.success(t["analysis_saved"])
    elif allow_save and st.session_state.authenticated:
        st.markdown(locked_feature_box(language, required_plan="Pro"), unsafe_allow_html=True)
    elif allow_save:
        st.warning(t["save_warning"])
 
    with st.expander(t["trades"]):
        st.dataframe(normalized_df, use_container_width=True)
 
# =========================================================
# SESSION STATE
# =========================================================
 
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
if "user_plan" not in st.session_state:
    st.session_state.user_plan = "Free"
 
 
# =========================================================
# HOMEPAGE
# =========================================================
 
if not st.session_state.authenticated and not st.session_state.show_login and not st.session_state.demo_mode:
    top1, top2, top3 = st.columns([1, 4, 1])
    with top1:
        language_map = language_options()
        selected_language_label = st.selectbox(
            "Language / Idioma",
            list(language_map.keys()),
            index=list(language_map.values()).index(st.session_state.landing_language),
        )
        st.session_state.landing_language = language_map[selected_language_label]
        st.markdown(language_flag_pill(st.session_state.landing_language), unsafe_allow_html=True)
 
    t = ui_text(st.session_state.landing_language)
 
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.25, 1])
 
    with col1:
        st.markdown(f'<div class="hero-badge">\u26a1 {t["hero_badge"]}</div>', unsafe_allow_html=True)
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
        st.image(
            "https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1200&auto=format&fit=crop",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
 
    st.markdown("</div>", unsafe_allow_html=True)
 
    st.markdown(f'<div class="section-title">{t["why"]}</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(f'<div class="feature-card"><h3>{t["feature_1_title"]}</h3><p>{t["feature_1_text"]}</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown(f'<div class="feature-card"><h3>{t["feature_2_title"]}</h3><p>{t["feature_2_text"]}</p></div>', unsafe_allow_html=True)
    with f3:
        st.markdown(f'<div class="feature-card"><h3>{t["feature_3_title"]}</h3><p>{t["feature_3_text"]}</p></div>', unsafe_allow_html=True)
 
    render_pricing_section(st.session_state.landing_language)
 
    st.stop()
 
 
# =========================================================
# LOGIN / REGISTER
# =========================================================
 
if not st.session_state.authenticated and st.session_state.show_login:
    t = ui_text(st.session_state.landing_language)
 
    st.title("\U0001f510 RiskPilot")
    st.markdown(language_flag_pill(st.session_state.landing_language), unsafe_allow_html=True)
 
    auth_mode = st.radio(
        t["choose"],
        [t["login"].replace("\U0001f510 ", ""), t["register"]],
        index=0 if st.session_state.auth_mode == "Login" else 1,
    )
 
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
                    if is_admin_user():
                        st.session_state.user_plan = "Premium"
                    st.rerun()
                else:
                    st.error(t["invalid_credentials"])
 
    if st.button(t["back_home"]):
        st.session_state.show_login = False
        st.rerun()
 
    st.stop()
 
 
# =========================================================
# SIDEBAR APP
# =========================================================
 
language_map = language_options()
language_label = st.sidebar.selectbox(
    "Language / Idioma",
    list(language_map.keys()),
    index=list(language_map.values()).index(st.session_state.landing_language),
)
language = language_map[language_label]
st.session_state.landing_language = language
st.sidebar.markdown(language_flag_pill(language), unsafe_allow_html=True)
 
t = ui_text(language)
 
st.sidebar.markdown(
    f'<div class="sidebar-brand"><div class="sidebar-logo">\U0001f4ca RiskPilot</div><div class="sidebar-subtitle">{t["professional_analytics"]}</div></div>',
    unsafe_allow_html=True,
)
 
if st.session_state.authenticated:
    st.sidebar.markdown(
        f'<div class="sidebar-user-card"><div class="sidebar-user-label">{t["authenticated_user"]}</div><div class="sidebar-user-value">{st.session_state.user_email}</div></div>',
        unsafe_allow_html=True,
    )
 
    if st.sidebar.button(t["logout"]):
        st.session_state.authenticated = False
        st.session_state.show_login = False
        st.session_state.demo_mode = False
        st.session_state.user_email = None
        st.session_state.user_plan = "Free"
        st.rerun()
else:
    st.sidebar.markdown(
        f'<div class="sidebar-user-card"><div class="sidebar-user-label">{t["current_mode"]}</div><div class="sidebar-user-value">{t["demo_mode"]}</div></div>',
        unsafe_allow_html=True,
    )
 
    if st.sidebar.button(t["create_free_account"]):
        st.session_state.demo_mode = False
        st.session_state.auth_mode = "Register"
        st.session_state.show_login = True
        st.rerun()
 
plan_map = plan_options(language)
plan_labels = list(plan_map.keys())
 
if is_admin_user():
    st.session_state.user_plan = "Premium"
    st.sidebar.markdown(sidebar_kpi(plan_text(language)["current_plan"], "Admin / Premium"), unsafe_allow_html=True)
else:
    current_plan_label = next((label for label, value in plan_map.items() if value == st.session_state.get("user_plan", "Free")), plan_labels[0])
    selected_plan_label = st.sidebar.selectbox(
        plan_text(language)["current_plan"],
        plan_labels,
        index=plan_labels.index(current_plan_label),
    )
    st.session_state.user_plan = plan_map[selected_plan_label]
    st.sidebar.markdown(sidebar_kpi(plan_text(language)["current_plan"], st.session_state.user_plan), unsafe_allow_html=True)
 
account_size = st.sidebar.number_input(t["account_size"], value=50000.0, step=5000.0)
prop_mode = st.sidebar.selectbox(t["prop_firm_mode"], ["FTMO", "Apex", "TopStep", "MyFundedFX", "MyFundedFutures", "FundingPips", "TakeProfit", "E8", "Custom", "Personalizado"])
 
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
 
 
# =========================================================
# HISTORY COM DASHBOARD COMPLETO
# =========================================================
 
if page == t["history"]:
    st.markdown(
        f'<div class="terminal-header"><div class="terminal-title">\U0001f4da {t["history_title"]}</div><div class="terminal-subtitle">{t["loaded_from_history"]}</div><div class="terminal-pill">{prop_mode}</div></div>',
        unsafe_allow_html=True,
    )
 
    if not st.session_state.authenticated:
        st.info(t["history_account_required"])
        st.stop()
 
    if not has_plan("Pro"):
        st.markdown(locked_feature_box(language, required_plan="Pro"), unsafe_allow_html=True)
        st.stop()
 
    history = load_upload_history(st.session_state.user_email)
 
    if history.empty:
        st.info(t["no_uploads"])
        st.stop()
 
    st.dataframe(history, use_container_width=True)
 
    history_options = history.apply(
        lambda row: f'{row["id"]} \u00b7 {row["file_name"]} \u00b7 {row["created_at"]}',
        axis=1,
    ).tolist()
 
    selected_label = st.selectbox(t["select_upload"], history_options)
    selected_id = int(selected_label.split(" \u00b7 ")[0])
 
    selected_df = load_upload_by_id(selected_id)
 
    if selected_df.empty:
        st.info(t["no_uploads"])
        st.stop()
 
    render_full_dashboard(
        selected_df,
        t,
        language,
        initial_capital,
        max_daily_loss,
        max_drawdown_limit,
        profit_target,
        prop_mode,
        account_size,
        uploaded_file_name=f"upload_{selected_id}",
        allow_save=False,
        read_only=True,
    )
 
    st.stop()
 
 
# =========================================================
# DASHBOARD NORMAL
# =========================================================
 
st.markdown(
    f'<div class="terminal-header"><div class="terminal-title">{t["terminal_title"]}</div><div class="terminal-subtitle">{t["terminal_subtitle"]}</div><div class="terminal-pill">{t["live_engine"]} \u00b7 {prop_mode}</div></div>',
    unsafe_allow_html=True,
)
 
if st.session_state.demo_mode and not st.session_state.authenticated:
    st.info(t["demo_info"])
    normalized_df = make_demo_dataframe()
    uploaded_file_name = "demo_data.csv"
else:
    platform_map = platform_options(language)
    selected_platform_label = st.selectbox(
        upload_platform_label(language),
        list(platform_map.keys()),
        help=platform_help_text(language),
    )
    selected_import_platform = platform_map[selected_platform_label]
 
    uploaded_file = st.file_uploader(
        t["upload_report"],
        type=["csv", "xlsx", "xls", "txt", "html", "htm"],
        help=platform_help_text(language),
    )
 
    if not uploaded_file:
        st.info(t["upload_to_begin"])
        st.stop()
 
    if not enforce_free_upload_limit(language, uploaded_file.name):
        st.stop()
 
    try:
        raw_df = load_universal_trading_file(uploaded_file, selected_import_platform)
        normalized_df = universal_normalize_trades(raw_df, selected_import_platform)
        uploaded_file_name = uploaded_file.name
    except Exception as e:
        st.error(f'{t["file_error"]}: {e}')
        st.stop()
 
render_full_dashboard(
    normalized_df,
    t,
    language,
    initial_capital,
    max_daily_loss,
    max_drawdown_limit,
    profit_target,
    prop_mode,
    account_size,
    uploaded_file_name=uploaded_file_name,
    allow_save=True,
    read_only=False,
)
