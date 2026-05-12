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
            "upload_to_begin": "Envie um arquivo CSV, XLSX, TXT ou HTML para começar.",
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
            "upload_to_begin": "Sube un archivo CSV, XLSX, TXT o HTML para comenzar.",
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
 
 
FLAG_US_BASE64 = "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"
FLAG_BR_BASE64 = "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"
FLAG_ES_BASE64 = "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"
 
 
def language_options():
    return {
        "🇧🇷 Português": "Português",
        "🇺🇸 English": "English",
        "🇪🇸 Español": "Español",
    }
 
 
def language_display(language):
    reverse = {value: key for key, value in language_options().items()}
    return reverse.get(language, "🇺🇸 English")
 
 
def language_flag_image(language):
    if language == "Português":
        return FLAG_BR_BASE64, "Português"
    if language == "Español":
        return FLAG_ES_BASE64, "Español"
    return FLAG_US_BASE64, "English"
 
 
def language_flag_pill(language):
    flag_base64, label = language_flag_image(language)
    display_text = {
        "English": "English",
        "Português": "Português",
        "Español": "Español",
    }.get(language, label)
    return f"""
    <div class="language-flag-pill">
        <img class="language-flag-img" src="data:image/png;base64,{flag_base64}" />
        <span class="language-flag-text">{display_text}</span>
    </div>
    """
 
 
def upload_platform_label(language):
    if language == "Português":
        return "Plataforma / formato do relatório"
    if language == "Español":
        return "Plataforma / formato del reporte"
    return "Platform / report format"
 
 
def platform_options(language):
    if language == "Português":
        return {
            "Automático": "auto",
            "MetaTrader 5": "mt5",
            "MetaTrader 4": "mt4",
            "ProfitChart / Nelogica": "profitchart",
            "TradingView": "tradingview",
            "CSV Genérico": "generic_csv",
            "Excel Genérico": "generic_excel",
        }
    if language == "Español":
        return {
            "Automático": "auto",
            "MetaTrader 5": "mt5",
            "MetaTrader 4": "mt4",
            "ProfitChart / Nelogica": "profitchart",
            "TradingView": "tradingview",
            "CSV Genérico": "generic_csv",
            "Excel Genérico": "generic_excel",
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
    if language == "Português":
        return "Aceita CSV, XLSX, TXT e HTML. O RiskPilot tenta identificar automaticamente colunas de data, ativo, lado, quantidade e resultado."
    if language == "Español":
        return "Acepta CSV, XLSX, TXT y HTML. RiskPilot intenta identificar automáticamente columnas de fecha, activo, lado, cantidad y resultado."
    return "Supports CSV, XLSX, TXT and HTML. RiskPilot tries to identify date, symbol, side, quantity and result columns automatically."
 
 
def get_pricing_copy(language):
    if language == "Português":
        return {
            "title": "Planos para cada fase do trader",
            "subtitle": "Comece grátis, evolua com analytics profissional e desbloqueie inteligência comportamental premium.",
            "badge": "SaaS Trading Analytics",
            "free": "Free",
            "pro": "Pro",
            "premium": "Premium",
            "free_price": "R$ 0",
            "pro_price": "R$ 49/mês",
            "premium_price": "R$ 97/mês",
            "free_desc": "Para testar a plataforma e validar os primeiros relatórios.",
            "pro_desc": "Para traders que querem acompanhar performance, risco e evolução.",
            "premium_desc": "Para traders sérios que querem AI Coach, DNA e radar institucional.",
            "popular": "Mais recomendado",
            "cta_free": "Começar grátis",
            "cta_pro": "Plano profissional",
            "cta_premium": "Desbloquear Premium",
            "comparison_title": "Comparação de recursos",
            "faq_title": "Perguntas frequentes",
            "faq_1_q": "O RiskPilot opera por mim?",
            "faq_1_a": "Não. O RiskPilot analisa seus relatórios, performance, risco e comportamento operacional.",
            "faq_2_q": "Funciona para prop firm?",
            "faq_2_a": "Sim. O sistema calcula limites, drawdown, aprovação estimada e risco de violação.",
            "faq_3_q": "A IA já é real?",
            "faq_3_a": "A estrutura está pronta para OpenAI real. A versão atual usa regras inteligentes e análise comportamental baseada em métricas.",
            "features": {
                "Uploads": ["1 por dia", "Ilimitado", "Ilimitado"],
                "Dashboard": ["Básico", "Completo", "Institucional"],
                "Histórico": ["Limitado", "Completo", "Completo"],
                "PDF": ["Não", "Sim", "Sim Premium"],
                "AI Coach": ["Não", "Limitado", "Completo"],
                "Trader DNA": ["Não", "Sim", "Avançado"],
                "Radar Institucional": ["Não", "Sim", "Completo"],
                "Prop Firm Engine": ["Básico", "Completo", "Completo"],
            },
        }
    if language == "Español":
        return {
            "title": "Planes para cada etapa del trader",
            "subtitle": "Empieza gratis, evoluciona con analytics profesional y desbloquea inteligencia conductual premium.",
            "badge": "SaaS Trading Analytics",
            "free": "Free",
            "pro": "Pro",
            "premium": "Premium",
            "free_price": "$0",
            "pro_price": "$9/mes",
            "premium_price": "$19/mes",
            "free_desc": "Para probar la plataforma y validar los primeros reportes.",
            "pro_desc": "Para traders que quieren seguir rendimiento, riesgo y evolución.",
            "premium_desc": "Para traders serios que quieren AI Coach, DNA y radar institucional.",
            "popular": "Más recomendado",
            "cta_free": "Empezar gratis",
            "cta_pro": "Plan profesional",
            "cta_premium": "Desbloquear Premium",
            "comparison_title": "Comparación de recursos",
            "faq_title": "Preguntas frecuentes",
            "faq_1_q": "¿RiskPilot opera por mí?",
            "faq_1_a": "No. RiskPilot analiza tus reportes, rendimiento, riesgo y comportamiento operativo.",
            "faq_2_q": "¿Funciona para prop firms?",
            "faq_2_a": "Sí. El sistema calcula límites, drawdown, aprobación estimada y riesgo de violación.",
            "faq_3_q": "¿La IA ya es real?",
            "faq_3_a": "La estructura está lista para OpenAI real. La versión actual usa reglas inteligentes y análisis basado en métricas.",
            "features": {
                "Uploads": ["1 por día", "Ilimitado", "Ilimitado"],
                "Dashboard": ["Básico", "Completo", "Institucional"],
                "Historial": ["Limitado", "Completo", "Completo"],
                "PDF": ["No", "Sí", "Sí Premium"],
                "AI Coach": ["No", "Limitado", "Completo"],
                "Trader DNA": ["No", "Sí", "Avanzado"],
                "Radar Institucional": ["No", "Sí", "Completo"],
                "Prop Firm Engine": ["Básico", "Completo", "Completo"],
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
        "pro_price": "$9/mo",
        "premium_price": "$19/mo",
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
 
 
def _normalize_text(value):
    value = str(value).strip().lower()
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
    s = series.astype(str).str.strip()
    s = s.str.replace("R$", "", regex=False).str.replace("$", "", regex=False)
    s = s.str.replace(" ", "", regex=False)
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")
 
 
def _read_csv_safely(file_bytes):
    encodings = ["utf-8-sig", "utf-8", "latin1", "cp1252"]
    separators = [None, ";", ",", "\t", "|"]
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
                score = int(df.shape[1]) * 10 + int(df.shape[0] > 0)
                if df.shape[0] > 0 and df.shape[1] > 1 and score > best_score:
                    best_df = df
                    best_score = score
            except Exception as exc:
                last_error = exc
    if best_df is not None:
        return best_df
    raise ValueError(f"Could not read CSV/TXT file. Last error: {last_error}")
 
 
def load_universal_trading_file(uploaded_file, platform="auto"):
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()
 
    if file_name.endswith((".xlsx", ".xls")):
        try:
            return pd.read_excel(io.BytesIO(file_bytes))
        except Exception as exc:
            raise ValueError(f"Could not read Excel file. Save as .xlsx or CSV and try again. Details: {exc}")
 
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
 
 
def universal_normalize_trades(raw_df, platform="auto"):
    df = raw_df.copy()
    df = df.dropna(how="all")
    df.columns = [str(col).strip() for col in df.columns]
 
    date_col = _find_column(df, [
        "date", "time", "datetime", "open time", "close time", "data", "hora", "data/hora", "fecha", "fecha/hora",
        "open date", "close date", "entry time", "exit time", "abertura", "fechamento"
    ])
    asset_col = _find_column(df, [
        "asset", "symbol", "ticker", "ativo", "instrument", "instrumento", "mercado", "produto", "contrato", "scrip", "security"
    ])
    side_col = _find_column(df, [
        "side", "type", "operation", "operacao", "operação", "direcao", "direção", "buy/sell", "compra/venda", "action", "order type"
    ])
    qty_col = _find_column(df, [
        "quantity", "qty", "volume", "lots", "lot", "contracts", "contratos", "quantidade", "qtd", "size", "amount"
    ])
    entry_col = _find_column(df, [
        "entry_price", "entry price", "open price", "price", "preco", "preço", "preco entrada", "preço entrada", "entrada", "open", "avg price"
    ])
    exit_col = _find_column(df, [
        "exit_price", "exit price", "close price", "preco saida", "preço saída", "saida", "saída", "close", "closing price"
    ])
    fees_col = _find_column(df, [
        "fees", "fee", "commission", "commissions", "corretagem", "taxas", "custos", "costs", "swap", "charges"
    ])
    pnl_col = _find_column(df, [
        "net_pnl", "net pnl", "pnl", "p&l", "profit", "profit/loss", "profit loss", "lucro", "resultado", "resultado liquido",
        "resultado líquido", "net profit", "gross profit", "close profit", "profit currency", "pl", "gain", "realized p/l"
    ])
 
    if date_col is None:
        raise ValueError("Could not identify the date/time column. Please export a report with Date/Time, Open Time or Close Time.")
    if pnl_col is None:
        raise ValueError("Could not identify the result/P&L column. Please export a report with Profit, PnL, Resultado or Net Profit.")
 
    normalized = pd.DataFrame()
    normalized["date"] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
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
        st.markdown(language_flag_pill(st.session_state.landing_language), unsafe_allow_html=True)
 
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
 
    render_pricing_section(st.session_state.landing_language)
 
    st.stop()
 
 
# =========================================================
# LOGIN / REGISTER
# =========================================================
 
if not st.session_state.authenticated and st.session_state.show_login:
    t = ui_text(st.session_state.landing_language)
 
    st.title("🔐 RiskPilot")
    st.markdown(language_flag_pill(st.session_state.landing_language), unsafe_allow_html=True)
 
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
st.sidebar.markdown(language_flag_pill(language), unsafe_allow_html=True)
 
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
