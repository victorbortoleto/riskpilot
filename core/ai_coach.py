import os
import json
import re
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


def _compact_series(series, limit=12):
    if series is None or getattr(series, "empty", True):
        return {}
    try:
        data = series.sort_index().tail(limit).to_dict()
        return {str(k): _safe_float(v) for k, v in data.items()}
    except Exception:
        return {}


def _extract_json(text):
    if not text:
        return None
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        return None


def _normalize_list(value, fallback, max_items=6):
    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
    elif isinstance(value, str) and value.strip():
        items = [value.strip()]
    else:
        items = fallback

    if not items:
        items = fallback

    return items[:max_items]


def _language_name(language):
    if language == "Português":
        return "Brazilian Portuguese"
    if language == "Español":
        return "Spanish"
    return "English"


def _base_report(
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
    net_pnl = _safe_float(metrics.get("net_pnl", 0))
    profit_factor = _safe_float(metrics.get("profit_factor", 0))
    winrate = _safe_float(metrics.get("winrate", 0))
    max_drawdown = _safe_float(metrics.get("max_drawdown", 0))
    total_trades = _safe_int(metrics.get("total_trades", 0))
    max_loss_streak = _safe_int(metrics.get("max_loss_streak", 0))

    ai_score = int(
        risk_score * 0.30
        + consistency_score * 0.25
        + behavior_score * 0.25
        + approval_probability * 0.20
    )
    ai_score = max(0, min(100, ai_score))

    best_hour = "N/A"
    worst_hour = "N/A"

    if not hourly.empty:
        best_hour = hourly.idxmax()
        worst_hour = hourly.idxmin()

    positive_days = int((daily > 0).sum()) if not daily.empty else 0
    negative_days = int((daily < 0).sum()) if not daily.empty else 0

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
        if max_loss_streak >= 4:
            warnings.append(f"Sequência de {max_loss_streak} perdas detectada, com possível risco de tilt.")

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
        if max_loss_streak >= 4:
            warnings.append(f"Secuencia de {max_loss_streak} pérdidas detectada, con posible riesgo de tilt.")

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
        if max_loss_streak >= 4:
            warnings.append(f"A {max_loss_streak}-loss streak was detected, with possible tilt risk.")

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
        "source": "RiskPilot Rule Engine",
    }


def _build_openai_prompt(language):
    output_language = _language_name(language)
    return f"""
You are RiskPilot AI Trading Coach, an institutional trading performance analyst.

Analyze the trader using ONLY the supplied trading metrics and aggregated behavior data.
Do not invent trades, prices, assets, psychology, medical claims, or hidden facts.
You may infer behavioral risk from trading patterns, such as loss streaks, poor time windows,
daily loss concentration, drawdown pressure, and prop firm violation risk.

Tone: premium, direct, institutional, practical.
Language: {output_language}.

Return ONLY valid JSON with this exact schema:
{{
  "status": "short status label",
  "profile": "short trader profile",
  "headline": "one concise headline",
  "executive_summary": ["3 to 5 concise bullets"],
  "action_plan": ["4 to 6 actionable recommendations"],
  "rules": ["4 to 6 objective trading rules"],
  "warnings": ["0 to 5 behavioral/risk warnings"]
}}
""".strip()


def _try_openai_enrichment(
    language,
    base_report,
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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return base_report

    try:
        from openai import OpenAI
    except Exception:
        base_report["headline"] = base_report["headline"] + " OpenAI package not installed; using internal engine."
        return base_report

    net_pnl = _safe_float(metrics.get("net_pnl", 0))
    profit_factor = _safe_float(metrics.get("profit_factor", 0))
    winrate = _safe_float(metrics.get("winrate", 0))
    max_drawdown = _safe_float(metrics.get("max_drawdown", 0))
    total_trades = _safe_int(metrics.get("total_trades", 0))
    max_loss_streak = _safe_int(metrics.get("max_loss_streak", 0))

    payload = {
        "language": language,
        "core_metrics": {
            "net_pnl": net_pnl,
            "profit_factor": profit_factor,
            "winrate": winrate,
            "max_drawdown": max_drawdown,
            "total_trades": total_trades,
            "max_loss_streak": max_loss_streak,
        },
        "scores": {
            "risk_score": risk_score,
            "consistency_score": consistency_score,
            "behavior_score": behavior_score,
            "approval_probability": approval_probability,
            "ai_score": base_report["score"],
        },
        "prop_firm_context": {
            "target_distance": target_distance,
            "daily_remaining": daily_remaining,
            "drawdown_remaining": dd_remaining,
        },
        "daily_pnl_recent": _compact_series(daily, limit=20),
        "pnl_by_hour": _compact_series(hourly, limit=24),
        "current_rule_based_report": {
            "status": base_report["status"],
            "profile": base_report["profile"],
            "headline": base_report["headline"],
            "executive_summary": base_report["executive_summary"],
            "action_plan": base_report["action_plan"],
            "rules": base_report["rules"],
            "warnings": base_report["warnings"],
        },
    }

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": _build_openai_prompt(language)},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            temperature=0.25,
            max_output_tokens=1200,
        )
        content = getattr(response, "output_text", None)
    except Exception as first_error:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _build_openai_prompt(language)},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
                ],
                temperature=0.25,
                max_tokens=1200,
            )
            content = response.choices[0].message.content
        except Exception:
            base_report["source"] = "RiskPilot Rule Engine"
            return base_report

    parsed = _extract_json(content)
    if not isinstance(parsed, dict):
        return base_report

    enriched = dict(base_report)
    enriched["status"] = str(parsed.get("status") or base_report["status"])
    enriched["profile"] = str(parsed.get("profile") or base_report["profile"])
    enriched["headline"] = str(parsed.get("headline") or base_report["headline"])
    enriched["executive_summary"] = _normalize_list(parsed.get("executive_summary"), base_report["executive_summary"], max_items=5)
    enriched["action_plan"] = _normalize_list(parsed.get("action_plan"), base_report["action_plan"], max_items=6)
    enriched["rules"] = _normalize_list(parsed.get("rules"), base_report["rules"], max_items=6)
    enriched["warnings"] = _normalize_list(parsed.get("warnings"), base_report["warnings"], max_items=5)
    enriched["source"] = "OpenAI"

    return enriched


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
    """
    V29: Real AI ready.

    If OPENAI_API_KEY is configured, this function enriches the report with OpenAI.
    If not configured, or if the API fails, it safely returns the internal rule-based report.
    """
    base = _base_report(
        language=language,
        metrics=metrics,
        daily=daily,
        hourly=hourly,
        risk_score=risk_score,
        consistency_score=consistency_score,
        behavior_score=behavior_score,
        approval_probability=approval_probability,
        target_distance=target_distance,
        daily_remaining=daily_remaining,
        dd_remaining=dd_remaining,
    )

    return _try_openai_enrichment(
        language=language,
        base_report=base,
        metrics=metrics,
        daily=daily,
        hourly=hourly,
        risk_score=risk_score,
        consistency_score=consistency_score,
        behavior_score=behavior_score,
        approval_probability=approval_probability,
        target_distance=target_distance,
        daily_remaining=daily_remaining,
        dd_remaining=dd_remaining,
    )
