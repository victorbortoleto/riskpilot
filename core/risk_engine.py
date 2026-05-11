import pandas as pd
        else:
            return [_t(language, "missing_result")]

    df["net_pnl"] = pd.to_numeric(df["net_pnl"], errors="coerce").fillna(0)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["day"] = df["date"].dt.date
        daily = df.groupby("day")["net_pnl"].sum()

        if not daily.empty:
            worst_day = daily.min()

            if abs(worst_day) >= max_daily_loss:
                alerts.append(_t(language, "worst_day", value=worst_day))

            losing_days = daily[daily < 0]
            if len(losing_days) >= 3:
                alerts.append(_t(language, "losing_days", count=len(losing_days)))

    if "drawdown" in df.columns:
        actual_max_drawdown = abs(pd.to_numeric(df["drawdown"], errors="coerce").min())

        if actual_max_drawdown >= max_drawdown:
            alerts.append(_t(language, "max_drawdown", value=actual_max_drawdown))

    pnl = df["net_pnl"].tolist()

    loss_streak = 0
    max_loss_streak = 0
    win_streak = 0
    max_win_streak = 0

    for value in pnl:
        if value < 0:
            loss_streak += 1
            win_streak = 0
            max_loss_streak = max(max_loss_streak, loss_streak)
        elif value > 0:
            win_streak += 1
            loss_streak = 0
            max_win_streak = max(max_win_streak, win_streak)
        else:
            loss_streak = 0
            win_streak = 0

    if max_loss_streak >= max_loss_streak_limit:
        alerts.append(_t(language, "loss_streak", count=max_loss_streak))

    if "quantity" in df.columns:
        qty = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        df["quantity"] = qty

        for i in range(1, len(df)):
            previous_loss = df.iloc[i - 1]["net_pnl"] < 0
            increased_size = df.iloc[i]["quantity"] > df.iloc[i - 1]["quantity"]

            if previous_loss and increased_size:
                alerts.append(_t(language, "revenge"))
                break

    if "hour" in df.columns:
        hourly = df.groupby("hour")["net_pnl"].sum()

        if not hourly.empty:
            worst_hour = hourly.idxmin()
            worst_hour_pnl = hourly.min()

            if worst_hour_pnl < 0:
                alerts.append(_t(language, "worst_hour", hour=worst_hour, value=worst_hour_pnl))

    total_pnl = df["net_pnl"].sum()
    gross_profit = df[df["net_pnl"] > 0]["net_pnl"].sum()
    gross_loss = abs(df[df["net_pnl"] < 0]["net_pnl"].sum())

    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss

        if profit_factor < 1:
            alerts.append(_t(language, "pf_low"))

    if total_pnl < 0:
        alerts.append(_t(language, "negative_result", value=total_pnl))

    if not alerts:
        alerts.append(_t(language, "no_alerts"))

    return alerts
