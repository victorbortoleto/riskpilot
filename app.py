import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import bcrypt
import time
 
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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
 
# =========================================================
# IDIOMAS
# =========================================================
 
def ui_text(language):
    texts = {
        "English": {
            "ai_coach": "AI Trading Coach",
"analyze_ai": "🧠 Analyze with AI",
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
            "select_upload": "Select an upload to view",
            "loaded_from_history": "Loaded from history. This analysis is read-only.",
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
            "download_csv": "⬇️ Download normalized CSV",
            "download_pdf": "📄 Download professional PDF report",
            
        },
        "Português": {
            "ai_coach": "AI Trading Coach",
"analyze_ai": "🧠 Analisar com IA",
"ai_score": "AI Score",
"executive_summary": "Resumo Executivo",
"action_plan": "Plano de Ação",
"risk_rules": "Regras de Risco",
"behavior_warnings": "Alertas Comportamentais",
            "institutional_radar": "Radar Institucional",
            "radar_discipline": "Disciplina",
            "radar_consistency": "Consistência",
            "radar_risk_control": "Controle de Risco",
            "radar_execution": "Execução",
            "radar_recovery": "Recuperação",
            "radar_prop_compatibility": "Compatibilidade Prop",
            "smart_prop_engine": "Motor Prop Firm Inteligente",
            "prop_rule_profile": "Perfil de Regras",
            "openai_ready": "OpenAI Ready",
            "openai_ready_sub": "Preparado para integração com IA real",
            "trader_dna": "Motor Trader DNA",
            "dna_score": "DNA Score",
            "trader_profile": "Perfil do Trader",
            "execution_style": "Estilo de Execução",
            "risk_behavior": "Comportamento de Risco",
            "prop_firm_fit": "Compatibilidade Prop Firm",
            "profile_confidence": "Confiança do Perfil",
            "profile_summary": "Resumo do Perfil",
            "strengths": "Pontos Fortes",
            "improvement_points": "Pontos de Melhoria",
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
            "select_upload": "Selecione um upload para visualizar",
            "loaded_from_history": "Carregado do histórico. Esta análise está em modo somente leitura.",
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
            "download_csv": "⬇️ Baixar CSV normalizado",
            "download_pdf": "📄 Baixar relatório profissional em PDF",
        },
        "Español": {
            "ai_coach": "AI Trading Coach",
"analyze_ai": "🧠 Analizar con IA",
"ai_score": "AI Score",
"executive_summary": "Resumen Ejecutivo",
"action_plan": "Plan de Acción",
"risk_rules": "Reglas de Riesgo",
"behavior_warnings": "Alertas Conductuales",
            "institutional_radar": "Radar Institucional",
            "radar_discipline": "Disciplina",
            "radar_consistency": "Consistencia",
            "radar_risk_control": "Control de Riesgo",
            "radar_execution": "Ejecución",
            "radar_recovery": "Recuperación",
            "radar_prop_compatibility": "Compatibilidad Prop",
            "smart_prop_engine": "Motor Prop Firm Inteligente",
            "prop_rule_profile": "Perfil de Reglas",
            "openai_ready": "OpenAI Ready",
            "openai_ready_sub": "Preparado para integración con IA real",
            "trader_dna": "Motor Trader DNA",
            "dna_score": "DNA Score",
            "trader_profile": "Perfil del Trader",
            "execution_style": "Estilo de Ejecución",
            "risk_behavior": "Comportamiento de Riesgo",
            "prop_firm_fit": "Compatibilidad Prop Firm",
            "profile_confidence": "Confianza del Perfil",
            "profile_summary": "Resumen del Perfil",
            "strengths": "Fortalezas",
            "improvement_points": "Puntos de Mejora",
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
            "select_upload": "Selecciona un upload para visualizar",
            "loaded_from_history": "Cargado desde historial. Este análisis está en modo solo lectura.",
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
            "download_csv": "⬇️ Descargar CSV normalizado",
            "download_pdf": "📄 Descargar informe profesional en PDF",
        },
    }
    return texts.get(language, texts["English"])
 
 
def language_options():
    return {
        "🇺🇸 English": "English",
        "🇧🇷 Português": "Português",
        "🇪🇸 Español": "Español",
    }
 
 
def language_display(language):
    reverse = {value: key for key, value in language_options().items()}
    return reverse.get(language, "🇺🇸 English")
 
 
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
        "FTMO": {"strictness": 1.00, "consistency_weight": 1.00, "drawdown_weight": 1.00, "style": "Balanced challenge / strict daily loss", "badge": "🏦"},
        "Apex": {"strictness": 1.18, "consistency_weight": 1.12, "drawdown_weight": 1.20, "style": "Futures profile / trailing drawdown sensitivity", "badge": "⚡"},
        "TopStep": {"strictness": 1.25, "consistency_weight": 1.15, "drawdown_weight": 1.25, "style": "Futures combine / very strict discipline", "badge": "🎯"},
        "FundingPips": {"strictness": 0.95, "consistency_weight": 1.05, "drawdown_weight": 0.95, "style": "Flexible challenge / consistency focus", "badge": "💎"},
        "MyFundedFX": {"strictness": 1.03, "consistency_weight": 1.05, "drawdown_weight": 1.02, "style": "Balanced FX challenge", "badge": "🌐"},
        "MyFundedFutures": {"strictness": 1.15, "consistency_weight": 1.10, "drawdown_weight": 1.18, "style": "Futures evaluation / drawdown sensitive", "badge": "📈"},
        "TakeProfit": {"strictness": 1.05, "consistency_weight": 1.08, "drawdown_weight": 1.05, "style": "Balanced target / consistency aware", "badge": "🚀"},
        "E8": {"strictness": 1.08, "consistency_weight": 1.10, "drawdown_weight": 1.08, "style": "Institutional evaluation profile", "badge": "🏛️"},
        "Custom": {"strictness": 1.00, "consistency_weight": 1.00, "drawdown_weight": 1.00, "style": "Custom rule profile", "badge": "⚙️"},
        "Personalizado": {"strictness": 1.00, "consistency_weight": 1.00, "drawdown_weight": 1.00, "style": "Perfil personalizado", "badge": "⚙️"},
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
 
    if language == "Português":
        if dna_score >= 80 and profit_factor >= 1.2 and behavior_score >= 75:
            profile = "Trader Institucional"
        elif total_trades >= 120 and loss_streak >= 4:
            profile = "Scalper Agressivo com Risco de Tilt"
        elif approval >= 70 and consistency_score >= 65:
            profile = "Prop Firm Ready"
        elif profit_factor < 1 and negative_days >= positive_days:
            profile = "Trader Defensivo em Recuperação"
        elif winrate >= 65 and profit_factor >= 1:
            profile = "Trader de Alta Assertividade"
        else:
            profile = "Trader em Desenvolvimento"
 
        execution_style = {
            "high": "Alta frequência operacional",
            "medium": "Frequência moderada",
            "low": "Baixa frequência / amostra pequena",
        }[execution_density]
 
        if behavior_score >= 75:
            risk_behavior = "Disciplina saudável"
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
            f"O melhor horário operacional foi {best_hour}h e o pior horário foi {worst_hour}h.",
            f"O melhor dia da semana foi {best_weekday}; o ponto de atenção foi {worst_weekday}.",
            f"A análise encontrou {positive_days} dias positivos e {negative_days} dias negativos.",
        ]
 
        strengths = []
        improvements = []
 
        if profit_factor >= 1:
            strengths.append("Existe vantagem operacional inicial pelo Profit Factor acima de 1.")
        else:
            improvements.append("Aumentar seletividade de entrada até o Profit Factor superar 1.20.")
 
        if consistency_score >= 65:
            strengths.append("A consistência diária está em nível aceitável para evolução.")
        else:
            improvements.append("Reduzir dispersão dos resultados diários e evitar dias muito negativos.")
 
        if behavior_score >= 70:
            strengths.append("O comportamento de risco está relativamente controlado.")
        else:
            improvements.append("Criar trava operacional após perdas consecutivas para reduzir tilt.")
 
        if approval >= 70:
            strengths.append("O perfil atual tem boa aderência ao ambiente de prop firm.")
        else:
            improvements.append("Melhorar controle de drawdown antes de buscar aprovação em prop firm.")
 
        if not strengths:
            strengths.append("Há dados suficientes para iniciar uma evolução guiada por métricas.")
        if not improvements:
            improvements.append("Manter o mesmo padrão de risco e evitar aumentar lote cedo demais.")
 
    elif language == "Español":
        if dna_score >= 80 and profit_factor >= 1.2 and behavior_score >= 75:
            profile = "Trader Institucional"
        elif total_trades >= 120 and loss_streak >= 4:
            profile = "Scalper Agresivo con Riesgo de Tilt"
        elif approval >= 70 and consistency_score >= 65:
            profile = "Prop Firm Ready"
        elif profit_factor < 1 and negative_days >= positive_days:
            profile = "Trader Defensivo en Recuperación"
        elif winrate >= 65 and profit_factor >= 1:
            profile = "Trader de Alta Asertividad"
        else:
            profile = "Trader en Desarrollo"
 
        execution_style = {
            "high": "Alta frecuencia operativa",
            "medium": "Frecuencia moderada",
            "low": "Baja frecuencia / muestra pequeña",
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
            f"El mejor día de la semana fue {best_weekday}; el punto de atención fue {worst_weekday}.",
            f"El análisis encontró {positive_days} días positivos y {negative_days} días negativos.",
        ]
 
        strengths = []
        improvements = []
 
        if profit_factor >= 1:
            strengths.append("Existe una ventaja operativa inicial por Profit Factor superior a 1.")
        else:
            improvements.append("Aumentar la selectividad de entrada hasta superar Profit Factor 1.20.")
 
        if consistency_score >= 65:
            strengths.append("La consistencia diaria está en un nivel aceptable para evolucionar.")
        else:
            improvements.append("Reducir dispersión de resultados diarios y evitar días muy negativos.")
 
        if behavior_score >= 70:
            strengths.append("El comportamiento de riesgo está relativamente controlado.")
        else:
            improvements.append("Crear bloqueo operativo después de pérdidas consecutivas para reducir tilt.")
 
        if approval >= 70:
            strengths.append("El perfil actual tiene buena compatibilidad con prop firms.")
        else:
            improvements.append("Mejorar control de drawdown antes de buscar aprobación en prop firm.")
 
        if not strengths:
            strengths.append("Hay datos suficientes para iniciar una evolución guiada por métricas.")
        if not improvements:
            improvements.append("Mantener el mismo patrón de riesgo y evitar aumentar lote demasiado pronto.")
 
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
            f'{prop_behavior.get("badge", "🏦")} {prop_mode}',
            f'{prop_description} · Strictness {prop_behavior.get("strictness", 1.0):.2f}x · Target {money(profit_target)} · Daily {money(max_daily_loss)} · Max DD {money(max_drawdown_limit)}',
        ),
        unsafe_allow_html=True,
    )
 
    section(t["equity_curve"])
    st.plotly_chart(make_equity_chart(normalized_df, t), use_container_width=True)
 
    section(t["drawdown"])
    st.plotly_chart(make_drawdown_chart(normalized_df, t), use_container_width=True)
 
    section(t["institutional_radar"])
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
 
    section(t["trader_dna"])
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
            st.markdown(f'<div class="diagnosis-box">🧬 {item}</div>', unsafe_allow_html=True)
    with dna_strength_col:
        st.markdown(f"## {t['strengths']}")
        for item in trader_dna["strengths"][:3]:
            st.markdown(f'<div class="diagnosis-box">✅ {item}</div>', unsafe_allow_html=True)
    with dna_improve_col:
        st.markdown(f"## {t['improvement_points']}")
        for item in trader_dna["improvements"][:3]:
            st.markdown(f'<div class="alert-box">📌 {item}</div>', unsafe_allow_html=True)
 
    section(t["ai_coach"])
    loading_texts = {
        "Português": [
            "Mapeando padrões comportamentais...",
            "Detectando risco de tilt e revenge trading...",
            "Avaliando consistência para prop firm...",
            "Calculando qualidade operacional...",
            "Gerando diagnóstico institucional...",
        ],
        "Español": [
            "Mapeando patrones conductuales...",
            "Detectando riesgo de tilt y revenge trading...",
            "Evaluando consistencia para prop firm...",
            "Calculando calidad operativa...",
            "Generando diagnóstico institucional...",
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
        "Português": "Gera uma análise comportamental premium com plano de ação.",
        "Español": "Genera un análisis conductual premium con plan de acción.",
        "English": "Generates a premium behavioral analysis with an action plan.",
    }.get(language, "Generates a premium behavioral analysis with an action plan.")
 
    if st.button(t["analyze_ai"], help=ai_button_help):
        loading_box = st.empty()
        progress_bar = st.progress(0)
        steps = loading_texts.get(language, loading_texts["English"])
 
        for index, message in enumerate(steps):
            percent_done = int(((index + 1) / len(steps)) * 100)
            loading_box.markdown(
                f'''<div class="diagnosis-box"><div class="diagnosis-title">AI TRADING COACH</div><div class="diagnosis-text">🧠 {message}</div></div>''',
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
                    st.markdown(f'<div class="alert-box">⚠️ {item}</div>', unsafe_allow_html=True)
            else:
                no_warning_text = {"Português": "Nenhum alerta comportamental crítico detectado.", "Español": "No se detectaron alertas conductuales críticos.", "English": "No critical behavioral warnings detected."}.get(language, "No critical behavioral warnings detected.")
                st.success(no_warning_text)
 
        with col_ai_2:
            st.markdown(f"## {t['action_plan']}")
            for item in ai_report["action_plan"][:5]:
                st.markdown(f'<div class="diagnosis-box">✅ {item}</div>', unsafe_allow_html=True)
            st.markdown(f"## {t['risk_rules']}")
            for item in ai_report["rules"][:5]:
                st.markdown(f'<div class="diagnosis-box">📌 {item}</div>', unsafe_allow_html=True)
 
    section(t["risk_alerts"])
    for alert in alerts:
        st.markdown(f'<div class="alert-box">⚠️ {alert}</div>', unsafe_allow_html=True)
 
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
 
    if read_only:
        st.info(t["loaded_from_history"])
    elif allow_save and st.session_state.authenticated:
        if st.button(t["save_analysis"]):
            save_upload(account_name=prop_mode, platform="Unknown", file_name=uploaded_file_name, trades_df=normalized_df, metrics=metrics, user_email=st.session_state.user_email)
            st.success(t["analysis_saved"])
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
 
    st.stop()
 
 
# =========================================================
# LOGIN / REGISTER
# =========================================================
 
if not st.session_state.authenticated and st.session_state.show_login:
    t = ui_text(st.session_state.landing_language)
 
    st.title("🔐 RiskPilot")
 
    auth_mode = st.radio(
        t["choose"],
        [t["login"].replace("🔐 ", ""), t["register"]],
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
 
t = ui_text(language)
 
st.sidebar.markdown(
    f'<div class="sidebar-brand"><div class="sidebar-logo">📊 RiskPilot</div><div class="sidebar-subtitle">{t["professional_analytics"]}</div></div>',
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
        f'<div class="terminal-header"><div class="terminal-title">📚 {t["history_title"]}</div><div class="terminal-subtitle">{t["loaded_from_history"]}</div><div class="terminal-pill">{prop_mode}</div></div>',
        unsafe_allow_html=True,
    )
 
    if not st.session_state.authenticated:
        st.info(t["history_account_required"])
        st.stop()
 
    history = load_upload_history(st.session_state.user_email)
 
    if history.empty:
        st.info(t["no_uploads"])
        st.stop()
 
    st.dataframe(history, use_container_width=True)
 
    history_options = history.apply(
        lambda row: f'{row["id"]} · {row["file_name"]} · {row["created_at"]}',
        axis=1,
    ).tolist()
 
    selected_label = st.selectbox(t["select_upload"], history_options)
    selected_id = int(selected_label.split(" · ")[0])
 
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
    f'<div class="terminal-header"><div class="terminal-title">{t["terminal_title"]}</div><div class="terminal-subtitle">{t["terminal_subtitle"]}</div><div class="terminal-pill">{t["live_engine"]} · {prop_mode}</div></div>',
    unsafe_allow_html=True,
)
 
if st.session_state.demo_mode and not st.session_state.authenticated:
    st.info(t["demo_info"])
    normalized_df = make_demo_dataframe()
    uploaded_file_name = "demo_data.csv"
else:
    uploaded_file = st.file_uploader(t["upload_report"], type=["csv", "xlsx"])
 
    if not uploaded_file:
        st.info(t["upload_to_begin"])
        st.stop()
 
    try:
        raw_df = load_trading_file(uploaded_file)
        normalized_df = normalize_trades(raw_df)
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
