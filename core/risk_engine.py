import pandas as pd


ALERTS = {
    "Português": {
        "missing_result": "Não encontrei coluna de resultado para gerar alertas.",
        "worst_day": "Pior dia foi ${value:,.2f}, atingindo ou ultrapassando o limite diário configurado.",
        "losing_days": "Foram encontrados {count} dias negativos. Avalie reduzir exposição ou filtrar horários.",
        "max_drawdown": "Drawdown máximo de ${value:,.2f} atingiu ou ultrapassou o limite configurado.",
        "loss_streak": "Sequência de {count} perdas consecutivas detectada. Isso pode indicar tilt, overtrading ou setup ruim.",
        "revenge": "Foi detectado aumento de lote/quantidade após operação perdedora. Isso pode indicar revenge trading.",
        "worst_hour": "Seu pior horário foi {hour}h, com resultado de ${value:,.2f}.",
        "pf_low": "Profit Factor abaixo de 1. O sistema está perdendo mais do que ganha.",
        "negative_result": "Resultado líquido negativo de ${value:,.2f}. Reavalie risco, horários e tamanho de posição.",
        "no_alerts": "Nenhum alerta crítico encontrado com os limites atuais.",
    },
    "English": {
        "missing_result": "Could not find a result column to generate alerts.",
        "worst_day": "Worst day was ${value:,.2f}, reaching or exceeding the configured daily loss limit.",
        "losing_days": "Found {count} negative days. Consider reducing exposure or filtering trading hours.",
        "max_drawdown": "Maximum drawdown of ${value:,.2f} reached or exceeded the configured limit.",
        "loss_streak": "A sequence of {count} consecutive losses was detected. This may indicate tilt, overtrading, or a poor setup.",
        "revenge": "Position size increased after a losing trade. This may indicate revenge trading.",
        "worst_hour": "Your worst hour was {hour}h, with a result of ${value:,.2f}.",
        "pf_low": "Profit Factor is below 1. The system is losing more than it wins.",
        "negative_result": "Negative net result of ${value:,.2f}. Review risk, timing, and position sizing.",
        "no_alerts": "No critical alerts found with the current limits.",
    },
    "Español": {
        "missing_result": "No encontré una columna de resultado para generar alertas.",
        "worst_day": "El peor día fue ${value:,.2f}, alcanzando o superando el límite diario configurado.",
        "losing_days": "Se encontraron {count} días negativos. Considera reducir exposición o filtrar horarios.",
        "max_drawdown": "El drawdown máximo de ${value:,.2f} alcanzó o superó el límite configurado.",
        "loss_streak": "Se detectó una secuencia de {count} pérdidas consecutivas. Esto puede indicar tilt, overtrading o un setup débil.",
        "revenge": "Se detectó aumento de lote/cantidad después de una operación perdedora. Esto puede indicar revenge trading.",
        "worst_hour": "Tu peor horario fue {hour}h, con resultado de ${value:,.2f}.",
        "pf_low": "Profit Factor por debajo de 1. El sistema pierde más de lo que gana.",
        "negative_result": "Resultado neto negativo de ${value:,.2f}. Revisa riesgo, horarios y tamaño de posición.",
        "no_alerts": "No se encontraron alertas críticas con los límites actuales.",
    },
}


def _t(language, key, **kwargs):
    dictionary = ALERTS.get(language, ALERTS["Português"])
    message = dictionary.get(key, ALERTS["Português"].get(key, key))
    return message.format(**kwargs)


def generate_risk_alerts(
    trades,
    max_daily_loss=500,
    max_drawdown=2000,
    max_loss_streak_limit=4,
    language="Português",
):
    alerts = []

    if trades is None or trades.empty:
        return alerts

    df = trades.copy()

    if "net_pnl" not in df.columns:
        if "pnl" in df.columns:
            df["net_pnl"] = df["pnl"]
        else:
            return [_t(language, "missing_result")]

    df["net_pnl"] = pd.to_numeric(
        df["net_pnl"],
        errors="coerce"
    ).fillna(0)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df["day"] = df["date"].dt.date

        daily = df.groupby("day")["net_pnl"].sum()

        if not daily.empty:
            worst_day = daily.min()

            if abs(worst_day) >= max_daily_loss:
                alerts.append(
                    _t(language, "worst_day", value=worst_day)
                )

            losing_days = daily[daily < 0]

            if len(losing_days) >= 3:
                alerts.append(
                    _t(
                        language,
                        "losing_days",
                        count=len(losing_days)
                    )
                )

    if "drawdown" in df.columns:
        actual_max_drawdown = abs(
            pd.to_numeric(
                df["drawdown"],
                errors="coerce"
            ).min()
        )

        if actual_max_drawdown >= max_drawdown:
            alerts.append(
                _t(
                    language,
                    "max_drawdown",
                    value=actual_max_drawdown
                )
            )

    pnl = df["net_pnl"].tolist()

    loss_streak = 0
    max_loss_streak = 0

    for value in pnl:
        if value < 0:
            loss_streak += 1
            max_loss_streak = max(
                max_loss_streak,
                loss_streak
            )
        else:
            loss_streak = 0

    if max_loss_streak >= max_loss_streak_limit:
        alerts.append(
            _t(
                language,
                "loss_streak",
                count=max_loss_streak
            )
        )

    if "quantity" in df.columns:
        qty = pd.to_numeric(
            df["quantity"],
            errors="coerce"
        ).fillna(0)

        df["quantity"] = qty

        for i in range(1, len(df)):
            previous_loss = (
                df.iloc[i - 1]["net_pnl"] < 0
            )

            increased_size = (
                df.iloc[i]["quantity"]
                > df.iloc[i - 1]["quantity"]
            )

            if previous_loss and increased_size:
                alerts.append(
                    _t(language, "revenge")
                )
                break

    if "hour" in df.columns:
        hourly = df.groupby("hour")["net_pnl"].sum()

        if not hourly.empty:
            worst_hour = hourly.idxmin()
            worst_hour_pnl = hourly.min()

            if worst_hour_pnl < 0:
                alerts.append(
                    _t(
                        language,
                        "worst_hour",
                        hour=worst_hour,
                        value=worst_hour_pnl
                    )
                )

    total_pnl = df["net_pnl"].sum()

    gross_profit = df[
        df["net_pnl"] > 0
    ]["net_pnl"].sum()

    gross_loss = abs(
        df[df["net_pnl"] < 0]["net_pnl"].sum()
    )

    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss

        if profit_factor < 1:
            alerts.append(
                _t(language, "pf_low")
            )

    if total_pnl < 0:
        alerts.append(
            _t(
                language,
                "negative_result",
                value=total_pnl
            )
        )

    if not alerts:
        alerts.append(
            _t(language, "no_alerts")
        )

    return alerts
