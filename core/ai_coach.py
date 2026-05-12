import pandas as pd


def money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def build_ai_coach_report(
    language,
    metrics,
    normalized_df,
    daily,
    hourly,
    weekday,
    risk_score,
    consistency_score,
    behavior_score,
    approval,
    daily_remaining,
    dd_remaining,
    target_distance,
):
    """
    Rule-based AI Coach.
    This is intentionally deterministic now.
    Later it can be replaced or enhanced with OpenAI API.
    """

    net_pnl = _safe_float(metrics.get("net_pnl", 0))
    profit_factor = _safe_float(metrics.get("profit_factor", 0))
    winrate = _safe_float(metrics.get("winrate", 0))
    max_drawdown = _safe_float(metrics.get("max_drawdown", 0))
    total_trades = _safe_int(metrics.get("total_trades", len(normalized_df)))
    max_loss_streak = _safe_int(metrics.get("max_loss_streak", 0))
    max_win_streak = _safe_int(metrics.get("max_win_streak", 0))

    best_hour = hourly.idxmax() if not hourly.empty else "N/A"
    best_hour_result = hourly.max() if not hourly.empty else 0
    worst_hour = hourly.idxmin() if not hourly.empty else "N/A"
    worst_hour_result = hourly.min() if not hourly.empty else 0

    best_day = daily.idxmax() if not daily.empty else "N/A"
    best_day_result = daily.max() if not daily.empty else 0
    worst_day = daily.idxmin() if not daily.empty else "N/A"
    worst_day_result = daily.min() if not daily.empty else 0

    best_weekday = weekday.idxmax() if not weekday.empty else "N/A"
    worst_weekday = weekday.idxmin() if not weekday.empty else "N/A"

    negative_days = int((daily < 0).sum()) if not daily.empty else 0
    positive_days = int((daily > 0).sum()) if not daily.empty else 0

    ai_score = round(
        (risk_score * 0.30)
        + (consistency_score * 0.25)
        + (behavior_score * 0.25)
        + (approval * 0.20)
    )

    ai_score = max(0, min(100, ai_score))

    if language == "Português":
        return _pt_report(
            ai_score,
            net_pnl,
            profit_factor,
            winrate,
            max_drawdown,
            total_trades,
            max_loss_streak,
            max_win_streak,
            best_hour,
            best_hour_result,
            worst_hour,
            worst_hour_result,
            best_day,
            best_day_result,
            worst_day,
            worst_day_result,
            best_weekday,
            worst_weekday,
            negative_days,
            positive_days,
            risk_score,
            consistency_score,
            behavior_score,
            approval,
            daily_remaining,
            dd_remaining,
            target_distance,
        )

    if language == "Español":
        return _es_report(
            ai_score,
            net_pnl,
            profit_factor,
            winrate,
            max_drawdown,
            total_trades,
            max_loss_streak,
            max_win_streak,
            best_hour,
            best_hour_result,
            worst_hour,
            worst_hour_result,
            best_day,
            best_day_result,
            worst_day,
            worst_day_result,
            best_weekday,
            worst_weekday,
            negative_days,
            positive_days,
            risk_score,
            consistency_score,
            behavior_score,
            approval,
            daily_remaining,
            dd_remaining,
            target_distance,
        )

    return _en_report(
        ai_score,
        net_pnl,
        profit_factor,
        winrate,
        max_drawdown,
        total_trades,
        max_loss_streak,
        max_win_streak,
        best_hour,
        best_hour_result,
        worst_hour,
        worst_hour_result,
        best_day,
        best_day_result,
        worst_day,
        worst_day_result,
        best_weekday,
        worst_weekday,
        negative_days,
        positive_days,
        risk_score,
        consistency_score,
        behavior_score,
        approval,
        daily_remaining,
        dd_remaining,
        target_distance,
    )


def _profile(ai_score, profit_factor, net_pnl, max_loss_streak, approval, language):
    if language == "Português":
        if ai_score >= 80:
            return "Trader consistente com perfil próximo do institucional"
        if ai_score >= 65:
            return "Trader em evolução com boa base de risco"
        if ai_score >= 45:
            return "Trader instável com necessidade de filtros operacionais"
        return "Trader em fase crítica de controle de risco"

    if language == "Español":
        if ai_score >= 80:
            return "Trader consistente con perfil cercano al institucional"
        if ai_score >= 65:
            return "Trader en evolución con buena base de riesgo"
        if ai_score >= 45:
            return "Trader inestable con necesidad de filtros operativos"
        return "Trader en fase crítica de control de riesgo"

    if ai_score >= 80:
        return "Consistent trader with near-institutional profile"
    if ai_score >= 65:
        return "Developing trader with a solid risk foundation"
    if ai_score >= 45:
        return "Unstable trader requiring operational filters"
    return "Critical risk-control phase trader"


def _score_status(ai_score, language):
    if language == "Português":
        if ai_score >= 80:
            return "Excelente"
        if ai_score >= 65:
            return "Saudável"
        if ai_score >= 45:
            return "Atenção"
        return "Crítico"

    if language == "Español":
        if ai_score >= 80:
            return "Excelente"
        if ai_score >= 65:
            return "Saludable"
        if ai_score >= 45:
            return "Atención"
        return "Crítico"

    if ai_score >= 80:
        return "Excellent"
    if ai_score >= 65:
        return "Healthy"
    if ai_score >= 45:
        return "Attention"
    return "Critical"


def _pt_report(
    ai_score,
    net_pnl,
    profit_factor,
    winrate,
    max_drawdown,
    total_trades,
    max_loss_streak,
    max_win_streak,
    best_hour,
    best_hour_result,
    worst_hour,
    worst_hour_result,
    best_day,
    best_day_result,
    worst_day,
    worst_day_result,
    best_weekday,
    worst_weekday,
    negative_days,
    positive_days,
    risk_score,
    consistency_score,
    behavior_score,
    approval,
    daily_remaining,
    dd_remaining,
    target_distance,
):
    profile = _profile(ai_score, profit_factor, net_pnl, max_loss_streak, approval, "Português")
    status = _score_status(ai_score, "Português")

    executive_summary = []
    action_plan = []
    rules = []
    warnings = []

    if net_pnl < 0:
        executive_summary.append("O resultado líquido está negativo. O foco agora deve ser reduzir a exposição e preservar capital até a curva voltar a estabilizar.")
    else:
        executive_summary.append("O resultado líquido está positivo. A prioridade é preservar consistência e evitar aumento agressivo de risco.")

    if profit_factor < 1:
        executive_summary.append("O Profit Factor abaixo de 1 indica que o operacional ainda não possui vantagem estatística suficiente no período analisado.")
        action_plan.append("Reduzir lote temporariamente até o Profit Factor voltar acima de 1.20.")
    else:
        executive_summary.append("O Profit Factor acima de 1 sugere vantagem operacional inicial, mas ainda deve ser analisado junto com drawdown e consistência.")

    if worst_hour != "N/A":
        executive_summary.append(f"O horário mais problemático foi {worst_hour}h, com resultado de {money(worst_hour_result)}.")
        action_plan.append(f"Evitar ou reduzir exposição no horário de {worst_hour}h até que esse bloco volte a apresentar resultado positivo.")

    if best_hour != "N/A":
        action_plan.append(f"Priorizar operações no horário de {best_hour}h, onde o desempenho foi de {money(best_hour_result)}.")

    if max_loss_streak >= 4:
        warnings.append(f"Sequência de {max_loss_streak} perdas detectada. Isso pode indicar tilt, insistência ou revenge trading.")
        rules.append("Parar de operar após 2 perdas consecutivas.")
    else:
        rules.append("Manter limite de perdas consecutivas em no máximo 2 operações.")

    if daily_remaining < 0:
        warnings.append("A margem de perda diária foi violada ou ficou negativa. Isso é crítico para prop firms.")
    else:
        action_plan.append(f"Manter margem diária mínima acima de {money(daily_remaining * 0.5)} antes de encerrar o dia.")

    if dd_remaining < 0:
        warnings.append("O limite de drawdown máximo foi violado ou ficou negativo. O risco de reprovação é extremo.")
    else:
        action_plan.append(f"Preservar pelo menos {money(dd_remaining * 0.5)} de margem de drawdown antes de aumentar risco.")

    if approval < 50:
        warnings.append("A probabilidade de aprovação está baixa. O sistema precisa de mais consistência antes de tentar escalar.")
    elif approval < 75:
        warnings.append("A probabilidade de aprovação está moderada. Ainda existe risco relevante de reprovação por inconsistência ou drawdown.")
    else:
        executive_summary.append("A probabilidade de aprovação está saudável, desde que o trader mantenha o mesmo padrão de risco.")

    if negative_days > positive_days:
        action_plan.append("Reduzir a frequência operacional e focar apenas nos melhores horários, pois há mais dias negativos do que positivos.")

    rules.extend([
        "Não aumentar lote após lucro grande.",
        "Não dobrar posição após perda.",
        "Encerrar o dia ao atingir o limite diário definido.",
        "Operar somente nos horários com vantagem estatística comprovada.",
    ])

    return {
        "ai_score": ai_score,
        "status": status,
        "profile": profile,
        "headline": "Análise comportamental e operacional concluída.",
        "executive_summary": executive_summary,
        "action_plan": action_plan[:6],
        "rules": rules[:7],
        "warnings": warnings[:6],
        "main_numbers": {
            "Resultado líquido": money(net_pnl),
            "Profit Factor": f"{profit_factor:.2f}",
            "Winrate": f"{winrate:.2f}%",
            "Drawdown máximo": money(max_drawdown),
            "Trades": str(total_trades),
            "Aprovação": f"{approval}/100",
        },
    }


def _en_report(
    ai_score,
    net_pnl,
    profit_factor,
    winrate,
    max_drawdown,
    total_trades,
    max_loss_streak,
    max_win_streak,
    best_hour,
    best_hour_result,
    worst_hour,
    worst_hour_result,
    best_day,
    best_day_result,
    worst_day,
    worst_day_result,
    best_weekday,
    worst_weekday,
    negative_days,
    positive_days,
    risk_score,
    consistency_score,
    behavior_score,
    approval,
    daily_remaining,
    dd_remaining,
    target_distance,
):
    profile = _profile(ai_score, profit_factor, net_pnl, max_loss_streak, approval, "English")
    status = _score_status(ai_score, "English")

    executive_summary = []
    action_plan = []
    rules = []
    warnings = []

    if net_pnl < 0:
        executive_summary.append("Net result is negative. The priority should be reducing exposure and preserving capital until the equity curve stabilizes.")
    else:
        executive_summary.append("Net result is positive. The priority is preserving consistency and avoiding aggressive risk increases.")

    if profit_factor < 1:
        executive_summary.append("Profit Factor below 1 indicates the operation does not yet show enough statistical edge in this period.")
        action_plan.append("Reduce position size temporarily until Profit Factor returns above 1.20.")
    else:
        executive_summary.append("Profit Factor above 1 suggests an initial operational edge, but it must be evaluated together with drawdown and consistency.")

    if worst_hour != "N/A":
        executive_summary.append(f"The weakest hour was {worst_hour}h, with a result of {money(worst_hour_result)}.")
        action_plan.append(f"Avoid or reduce exposure around {worst_hour}h until this block becomes positive again.")

    if best_hour != "N/A":
        action_plan.append(f"Prioritize trading around {best_hour}h, where performance reached {money(best_hour_result)}.")

    if max_loss_streak >= 4:
        warnings.append(f"A {max_loss_streak}-loss streak was detected. This may indicate tilt, overtrading or revenge trading.")
        rules.append("Stop trading after 2 consecutive losses.")
    else:
        rules.append("Keep consecutive losses limited to a maximum of 2 trades.")

    if daily_remaining < 0:
        warnings.append("Daily loss margin was violated or turned negative. This is critical for prop firms.")
    else:
        action_plan.append(f"Keep at least {money(daily_remaining * 0.5)} of daily margin before ending the day.")

    if dd_remaining < 0:
        warnings.append("Max drawdown limit was violated or turned negative. Failure risk is extreme.")
    else:
        action_plan.append(f"Preserve at least {money(dd_remaining * 0.5)} of drawdown margin before increasing risk.")

    if approval < 50:
        warnings.append("Approval probability is low. The system needs more consistency before scaling.")
    elif approval < 75:
        warnings.append("Approval probability is moderate. There is still relevant failure risk due to inconsistency or drawdown.")
    else:
        executive_summary.append("Approval probability is healthy as long as the trader maintains the same risk pattern.")

    if negative_days > positive_days:
        action_plan.append("Reduce trading frequency and focus only on the strongest time windows, since negative days exceed positive days.")

    rules.extend([
        "Do not increase size after a large winning day.",
        "Do not double position after a loss.",
        "Stop the day when the daily limit is reached.",
        "Trade only during statistically favorable windows.",
    ])

    return {
        "ai_score": ai_score,
        "status": status,
        "profile": profile,
        "headline": "Behavioral and operational analysis completed.",
        "executive_summary": executive_summary,
        "action_plan": action_plan[:6],
        "rules": rules[:7],
        "warnings": warnings[:6],
        "main_numbers": {
            "Net result": money(net_pnl),
            "Profit Factor": f"{profit_factor:.2f}",
            "Winrate": f"{winrate:.2f}%",
            "Max Drawdown": money(max_drawdown),
            "Trades": str(total_trades),
            "Approval": f"{approval}/100",
        },
    }


def _es_report(
    ai_score,
    net_pnl,
    profit_factor,
    winrate,
    max_drawdown,
    total_trades,
    max_loss_streak,
    max_win_streak,
    best_hour,
    best_hour_result,
    worst_hour,
    worst_hour_result,
    best_day,
    best_day_result,
    worst_day,
    worst_day_result,
    best_weekday,
    worst_weekday,
    negative_days,
    positive_days,
    risk_score,
    consistency_score,
    behavior_score,
    approval,
    daily_remaining,
    dd_remaining,
    target_distance,
):
    profile = _profile(ai_score, profit_factor, net_pnl, max_loss_streak, approval, "Español")
    status = _score_status(ai_score, "Español")

    executive_summary = []
    action_plan = []
    rules = []
    warnings = []

    if net_pnl < 0:
        executive_summary.append("El resultado neto está negativo. La prioridad debe ser reducir exposición y preservar capital hasta estabilizar la curva.")
    else:
        executive_summary.append("El resultado neto está positivo. La prioridad es preservar consistencia y evitar aumentos agresivos de riesgo.")

    if profit_factor < 1:
        executive_summary.append("El Profit Factor debajo de 1 indica que la operación aún no muestra suficiente ventaja estadística.")
        action_plan.append("Reducir lote temporalmente hasta que el Profit Factor vuelva por encima de 1.20.")
    else:
        executive_summary.append("El Profit Factor encima de 1 sugiere ventaja operativa inicial, pero debe evaluarse junto con drawdown y consistencia.")

    if worst_hour != "N/A":
        executive_summary.append(f"El horario más débil fue {worst_hour}h, con resultado de {money(worst_hour_result)}.")
        action_plan.append(f"Evitar o reducir exposición alrededor de {worst_hour}h hasta que este bloque vuelva a ser positivo.")

    if best_hour != "N/A":
        action_plan.append(f"Priorizar operaciones alrededor de {best_hour}h, donde el rendimiento fue {money(best_hour_result)}.")

    if max_loss_streak >= 4:
        warnings.append(f"Se detectó una secuencia de {max_loss_streak} pérdidas. Esto puede indicar tilt, overtrading o revenge trading.")
        rules.append("Parar de operar después de 2 pérdidas consecutivas.")
    else:
        rules.append("Mantener pérdidas consecutivas limitadas a máximo 2 operaciones.")

    if daily_remaining < 0:
        warnings.append("El margen de pérdida diaria fue violado o quedó negativo. Esto es crítico para prop firms.")
    else:
        action_plan.append(f"Mantener al menos {money(daily_remaining * 0.5)} de margen diario antes de cerrar el día.")

    if dd_remaining < 0:
        warnings.append("El límite de drawdown máximo fue violado o quedó negativo. El riesgo de reprobación es extremo.")
    else:
        action_plan.append(f"Preservar al menos {money(dd_remaining * 0.5)} de margen de drawdown antes de aumentar riesgo.")

    if approval < 50:
        warnings.append("La probabilidad de aprobación está baja. El sistema necesita más consistencia antes de escalar.")
    elif approval < 75:
        warnings.append("La probabilidad de aprobación está moderada. Aún existe riesgo relevante por inconsistencia o drawdown.")
    else:
        executive_summary.append("La probabilidad de aprobación está saludable si el trader mantiene el mismo patrón de riesgo.")

    if negative_days > positive_days:
        action_plan.append("Reducir frecuencia operativa y enfocarse solo en los mejores horarios, ya que hay más días negativos que positivos.")

    rules.extend([
        "No aumentar lote después de un gran día positivo.",
        "No doblar posición después de una pérdida.",
        "Cerrar el día al alcanzar el límite diario definido.",
        "Operar solo en horarios con ventaja estadística comprobada.",
    ])

    return {
        "ai_score": ai_score,
        "status": status,
        "profile": profile,
        "headline": "Análisis conductual y operativo concluido.",
        "executive_summary": executive_summary,
        "action_plan": action_plan[:6],
        "rules": rules[:7],
        "warnings": warnings[:6],
        "main_numbers": {
            "Resultado neto": money(net_pnl),
            "Profit Factor": f"{profit_factor:.2f}",
            "Winrate": f"{winrate:.2f}%",
            "Drawdown máximo": money(max_drawdown),
            "Trades": str(total_trades),
            "Aprobación": f"{approval}/100",
        },
    }
