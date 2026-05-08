import numpy as np
import pandas as pd


def _max_streak(values, condition):
    max_streak = 0
    current = 0

    for value in values:
        if condition(value):
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0

    return max_streak


def calculate_metrics(trades, starting_balance=0):
    df = trades.copy()

    if "net_pnl" not in df.columns:
        if "pnl" in df.columns:
            df["net_pnl"] = df["pnl"]
        else:
            raise ValueError("Coluna net_pnl ou pnl não encontrada.")

    pnl = pd.to_numeric(df["net_pnl"], errors="coerce").fillna(0)

    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]

    gross_profit = wins.sum()
    gross_loss = abs(losses.sum())

    total_trades = len(pnl)
    winning_trades = len(wins)
    losing_trades = len(losses)

    winrate = (
        winning_trades / total_trades * 100
        if total_trades > 0
        else 0
    )

    lossrate = (
        losing_trades / total_trades * 100
        if total_trades > 0
        else 0
    )

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 0
    )

    average_win = wins.mean() if len(wins) > 0 else 0
    average_loss = losses.mean() if len(losses) > 0 else 0

    max_win = wins.max() if len(wins) > 0 else 0
    max_loss = losses.min() if len(losses) > 0 else 0

    net_pnl = pnl.sum()

    if "equity" in df.columns:
        equity = pd.to_numeric(
            df["equity"],
            errors="coerce"
        ).fillna(method="ffill")
    else:
        equity = starting_balance + pnl.cumsum()

    equity_peak = equity.cummax()

    drawdown_series = equity - equity_peak

    max_drawdown = (
        abs(drawdown_series.min())
        if len(drawdown_series)
        else 0
    )

    expectancy = (
        (winrate / 100) * average_win
    ) - (
        (lossrate / 100) * abs(average_loss)
    )

    payoff_ratio = (
        abs(average_win / average_loss)
        if average_loss != 0
        else 0
    )

    recovery_factor = (
        net_pnl / max_drawdown
        if max_drawdown != 0
        else 0
    )

    ending_balance = starting_balance + net_pnl

    return {
        "net_pnl": float(net_pnl),
        "gross_profit": float(gross_profit),
        "gross_loss": float(gross_loss),
        "total_trades": int(total_trades),
        "winning_trades": int(winning_trades),
        "losing_trades": int(losing_trades),
        "winrate": float(winrate),
        "lossrate": float(lossrate),
        "profit_factor": float(profit_factor),
        "average_win": float(average_win),
        "average_loss": float(average_loss),
        "max_win": float(max_win),
        "max_loss": float(max_loss),
        "max_drawdown": float(max_drawdown),
        "expectancy": float(expectancy),
        "payoff_ratio": float(payoff_ratio),
        "recovery_factor": float(recovery_factor),
        "max_win_streak": int(
            _max_streak(pnl, lambda x: x > 0)
        ),
        "max_loss_streak": int(
            _max_streak(pnl, lambda x: x < 0)
        ),
        "ending_balance": float(ending_balance),
    }
