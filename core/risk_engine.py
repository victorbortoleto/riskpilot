def generate_risk_alerts(trades, daily_loss_limit, max_drawdown_limit):
    alerts = []

    if trades.empty:
        return alerts

    daily = trades.groupby(trades["date"].dt.date)["net_pnl"].sum()
    worst_day = daily.min()

    max_drawdown = abs(trades["drawdown"].min())

    if daily_loss_limit > 0 and abs(worst_day) >= daily_loss_limit:
        alerts.append(
            f"⚠️ Pior dia foi ${worst_day:,.2f}, atingindo ou ultrapassando o limite diário configurado."
        )

    if max_drawdown_limit > 0 and max_drawdown >= max_drawdown_limit:
        alerts.append(
            f"⚠️ Drawdown máximo de ${max_drawdown:,.2f} atingiu ou ultrapassou o limite configurado."
        )

    pnl = trades["net_pnl"].tolist()

    loss_streak = 0
    max_loss_streak = 0
    for value in pnl:
        if value < 0:
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)
        else:
            loss_streak = 0

    if max_loss_streak >= 4:
        alerts.append(
            f"⚠️ Sequência de {max_loss_streak} perdas consecutivas detectada. Isso pode indicar tilt, revenge trade ou setup ruim."
        )

    if "quantity" in trades.columns:
        qty_after_loss_alert = False

        for i in range(1, len(trades)):
            previous_loss = trades.loc[i - 1, "net_pnl"] < 0
            increased_size = trades.loc[i, "quantity"] > trades.loc[i - 1, "quantity"]

            if previous_loss and increased_size:
                qty_after_loss_alert = True
                break

        if qty_after_loss_alert:
            alerts.append(
                "⚠️ Foi detectado aumento de lote/quantidade após uma operação perdedora. Isso pode indicar revenge trading."
            )

    return alerts
