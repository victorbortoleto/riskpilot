import pandas as pd


def generate_risk_alerts(
    trades,
    max_daily_loss=500,
    max_drawdown=2000,
    max_loss_streak_limit=4,
):

    alerts = []

    if trades is None or trades.empty:
        return alerts

    df = trades.copy()

    if "net_pnl" not in df.columns:
        if "pnl" in df.columns:
            df["net_pnl"] = df["pnl"]
        else:
            return [
                "Não encontrei coluna de resultado para gerar alertas."
            ]

    df["net_pnl"] = pd.to_numeric(
        df["net_pnl"],
        errors="coerce"
    ).fillna(0)

    # =========================
    # DAILY LOSS
    # =========================

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
                    f"Pior dia foi ${worst_day:,.2f}, "
                    "atingindo ou ultrapassando "
                    "o limite diário configurado."
                )

            losing_days = daily[daily < 0]

            if len(losing_days) >= 3:

                alerts.append(
                    f"Foram encontrados "
                    f"{len(losing_days)} dias negativos. "
                    "Avalie reduzir exposição "
                    "ou filtrar horários."
                )

    # =========================
    # DRAWDOWN
    # =========================

    if "drawdown" in df.columns:

        actual_max_drawdown = abs(
            pd.to_numeric(
                df["drawdown"],
                errors="coerce"
            ).min()
        )

        if actual_max_drawdown >= max_drawdown:

            alerts.append(
                f"Drawdown máximo de "
                f"${actual_max_drawdown:,.2f} "
                "atingiu ou ultrapassou "
                "o limite configurado."
            )

    # =========================
    # STREAKS
    # =========================

    pnl = df["net_pnl"].tolist()

    loss_streak = 0
    max_loss_streak = 0

    win_streak = 0
    max_win_streak = 0

    for value in pnl:

        if value < 0:

            loss_streak += 1
            win_streak = 0

            max_loss_streak = max(
                max_loss_streak,
                loss_streak
            )

        elif value > 0:

            win_streak += 1
            loss_streak = 0

            max_win_streak = max(
                max_win_streak,
                win_streak
            )

        else:

            loss_streak = 0
            win_streak = 0

    if max_loss_streak >= max_loss_streak_limit:

        alerts.append(
            f"Sequência de "
            f"{max_loss_streak} perdas consecutivas "
            "detectada. Isso pode indicar tilt, "
            "overtrading ou setup ruim."
        )

    # =========================
    # REVENGE TRADE
    # =========================

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
                df.iloc[i]["quantity"] >
                df.iloc[i - 1]["quantity"]
            )

            if previous_loss and increased_size:

                alerts.append(
                    "Foi detectado aumento "
                    "de lote/quantidade após "
                    "operação perdedora. "
                    "Isso pode indicar revenge trading."
                )

                break

    # =========================
    # WORST HOUR
    # =========================

    if "hour" in df.columns:

        hourly = (
            df.groupby("hour")["net_pnl"]
            .sum()
        )

        if not hourly.empty:

            worst_hour = hourly.idxmin()
            worst_hour_pnl = hourly.min()

            if worst_hour_pnl < 0:

                alerts.append(
                    f"Seu pior horário foi "
                    f"{worst_hour}h, "
                    f"com resultado de "
                    f"${worst_hour_pnl:,.2f}."
                )

    # =========================
    # PROFIT FACTOR
    # =========================

    total_pnl = df["net_pnl"].sum()

    gross_profit = (
        df[df["net_pnl"] > 0]["net_pnl"]
        .sum()
    )

    gross_loss = abs(
        df[df["net_pnl"] < 0]["net_pnl"]
        .sum()
    )

    if gross_loss > 0:

        profit_factor = (
            gross_profit / gross_loss
        )

        if profit_factor < 1:

            alerts.append(
                "Profit Factor abaixo de 1. "
                "O sistema está perdendo "
                "mais do que ganha."
            )

    # =========================
    # NEGATIVE RESULT
    # =========================

    if total_pnl < 0:

        alerts.append(
            f"Resultado líquido negativo "
            f"de ${total_pnl:,.2f}. "
            "Reavalie risco, horários "
            "e tamanho de posição."
        )

    # =========================
    # NO ALERTS
    # =========================

    if not alerts:

        alerts.append(
            "Nenhum alerta crítico encontrado "
            "com os limites atuais."
        )

    return alerts
