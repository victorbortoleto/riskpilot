import pandas as pd
import numpy as np

def add_equity_curve(trades, starting_balance):
    df = trades.copy()
    df["equity"] = starting_balance + df["net_pnl"].cumsum()
    df["equity_peak"] = df["equity"].cummax()
    df["drawdown"] = df["equity"] - df["equity_peak"]
    return df

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

def calculate_metrics(trades, starting_balance):
    pnl = trades["net_pnl"]

    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]

    gross_profit = wins.sum()
    gross_loss = abs(losses.sum())

    total_trades = len(trades)
    winrate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf")

    max_drawdown = abs(trades["drawdown"].min()) if "drawdown" in trades else 0

    return {
        "net_pnl": pnl.sum(),
        "total_trades": total_trades,
        "winrate": winrate,
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
        "average_win": wins.mean() if len(wins) else 0,
        "average_loss": losses.mean() if len(losses) else 0,
        "max_win_streak": _max_streak(pnl, lambda x: x > 0),
        "max_loss_streak": _max_streak(pnl, lambda x: x < 0),
        "ending_balance": starting_balance + pnl.sum(),
    }
