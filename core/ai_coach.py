import pandas as pd
 
 
def money(value):
    try:
        return f"${float(value):,.2f}"
    except:
        return "$0.00"
 
 
 
def build_ai_coach_report(
    language,
    metrics,
    daily,
    hourly,
    risk_score,
    consistency_score,
    behavior_score,
    approval_probability,
    target_distance,
    daily_remaining,
    dd_remaining,
):
 
    net_pnl = float(metrics.get("net_pnl", 0))
    profit_factor = float(metrics.get("profit_factor", 0))
    winrate = float(metrics.get("winrate", 0))
    max_drawdown = float(metrics.get("max_drawdown", 0))
    total_trades = int(metrics.get("total_trades", 0))
 
    ai_score = int(
        (
            risk_score * 0.30
            + consistency_score * 0.25
            + behavior_score * 0.25
            + approval_probability * 0.20
        )
    )
 
    ai_score = max(0, min(100, ai_score))
 
    best_hour = "N/A"
    worst_hour = "N/A"
 
    if not hourly.empty:
        best_hour = hourly.idxmax()
        worst_hour = hourly.idxmin()
 
    positive_days = 0
    negative_days = 0
 
    if not daily.empty:
        positive_days = int((daily > 0).sum())
        negative_days = int((daily < 0).sum())
 
    if language == "Português":
 
        if ai_score >= 80:
            status = "Excelente"
            profile = "Trader consistente com perfil institucional"
        elif ai_score >= 60:
            status = "Saudável"
            profile = "Trader em evolução com boa consistência"
        elif ai_score >= 40:
            status = "Atenção"
            profile = "Trader inconsistente com risco elevado"
        else:
            status = "Crítico"
            profile = "Trader em fase crítica de risco"
 
        executive_summary = [
            f"Resultado líquido atual: {money(net_pnl)}.",
            f"Profit Factor atual: {profit_factor:.2f}.",
            f"Winrate operacional: {winrate:.2f}%.",
            f"Maior drawdown registrado: {money(max_drawdown)}.",
        ]
 
        action_plan = [
            f"Priorizar operações no horário de {best_hour}h.",
            f"Evitar operações no horário de {worst_hour}h.",
            "Reduzir exposição após sequência de perdas.",
            "Manter controle rígido de drawdown.",
            "Evitar overtrading em dias negativos.",
        ]
 
        rules = [
            "Parar após 2 perdas consecutivas.",
            "Não aumentar lote após loss.",
            "Encerrar o dia ao atingir limite diário.",
            "Operar apenas horários validados.",
            "Evitar operar emocionalmente.",
        ]
 
        warnings = []
 
        if profit_factor < 1:
            warnings.append("Profit Factor abaixo de 1.0.")
 
        if negative_days > positive_days:
            warnings.append("Mais dias negativos do que positivos.")
 
        if dd_remaining < 0:
            warnings.append("Limite de drawdown ultrapassado.")
 
        if daily_remaining < 0:
            warnings.append("Limite diário ultrapassado.")
 
        headline = "Análise comportamental concluída com sucesso."
 
    elif language == "Español":
 
        if ai_score >= 80:
            status = "Excelente"
            profile = "Trader consistente con perfil institucional"
        elif ai_score >= 60:
            status = "Saludable"
            profile = "Trader en evolución con buena consistencia"
        elif ai_score >= 40:
            status = "Atención"
            profile = "Trader inconsistente con riesgo elevado"
        else:
            status = "Crítico"
            profile = "Trader en fase crítica de riesgo"
 
        executive_summary = [
            f"Resultado neto actual: {money(net_pnl)}.",
            f"Profit Factor actual: {profit_factor:.2f}.",
            f"Winrate operacional: {winrate:.2f}%.",
            f"Mayor drawdown registrado: {money(max_drawdown)}.",
        ]
 
        action_plan = [
            f"Priorizar operaciones alrededor de las {best_hour}h.",
            f"Evitar operaciones alrededor de las {worst_hour}h.",
            "Reducir exposición después de pérdidas consecutivas.",
            "Mantener control rígido de drawdown.",
            "Evitar overtrading en días negativos.",
        ]
 
        rules = [
            "Parar después de 2 pérdidas consecutivas.",
            "No aumentar lote después de pérdida.",
            "Cerrar el día al alcanzar el límite diario.",
            "Operar solo horarios validados.",
            "Evitar operar emocionalmente.",
        ]
 
        warnings = []
 
        if profit_factor < 1:
            warnings.append("Profit Factor debajo de 1.0.")
 
        if negative_days > positive_days:
            warnings.append("Más días negativos que positivos.")
 
        if dd_remaining < 0:
            warnings.append("Límite de drawdown excedido.")
 
        if daily_remaining < 0:
            warnings.append("Límite diario excedido.")
 
        headline = "Análisis conductual completado exitosamente."
 
    else:
 
        if ai_score >= 80:
            status = "Excellent"
            profile = "Consistent trader with institutional profile"
        elif ai_score >= 60:
            status = "Healthy"
            profile = "Developing trader with good consistency"
        elif ai_score >= 40:
            status = "Attention"
            profile = "Inconsistent trader with elevated risk"
        else:
            status = "Critical"
            profile = "Trader in critical risk phase"
 
        executive_summary = [
            f"Current net result: {money(net_pnl)}.",
            f"Current Profit Factor: {profit_factor:.2f}.",
            f"Operational winrate: {winrate:.2f}%.",
            f"Maximum drawdown recorded: {money(max_drawdown)}.",
        ]
 
        action_plan = [
            f"Prioritize operations around {best_hour}h.",
            f"Avoid operations around {worst_hour}h.",
            "Reduce exposure after consecutive losses.",
            "Maintain strict drawdown control.",
            "Avoid overtrading during negative days.",
        ]
 
        rules = [
            "Stop after 2 consecutive losses.",
            "Do not increase size after losses.",
            "Stop trading after daily limit.",
            "Trade only validated time windows.",
            "Avoid emotional trading.",
        ]
 
        warnings = []
 
        if profit_factor < 1:
            warnings.append("Profit Factor below 1.0.")
 
        if negative_days > positive_days:
            warnings.append("More negative days than positive days.")
 
        if dd_remaining < 0:
            warnings.append("Drawdown limit exceeded.")
 
        if daily_remaining < 0:
            warnings.append("Daily limit exceeded.")
 
        headline = "Behavioral analysis completed successfully."
 
    return {
        "score": ai_score,
        "status": status,
        "profile": profile,
        "headline": headline,
        "executive_summary": executive_summary,
        "action_plan": action_plan,
        "rules": rules,
        "warnings": warnings,
        "main_numbers": {
            "Net P&L": money(net_pnl),
            "Profit Factor": f"{profit_factor:.2f}",
            "Winrate": f"{winrate:.2f}%",
            "Max Drawdown": money(max_drawdown),
            "Trades": str(total_trades),
            "AI Score": f"{ai_score}/100",
        },
    }
