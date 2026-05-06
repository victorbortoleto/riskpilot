import pandas as pd


def parse_mt5_strategy_report(df):
    """
    Parser para relatórios XLSX do Strategy Tester do MT5.
    """

    trades_start = None

    # procurar linha onde começam operações
    for idx in range(len(df)):
        row = df.iloc[idx].astype(str).str.lower().tolist()

        joined = " ".join(row)

        if "time" in joined and "symbol" in joined:
            trades_start = idx
            break

    if trades_start is None:
        raise ValueError("Não consegui localizar tabela de operações do MT5")

    # definir cabeçalhos
    headers = df.iloc[trades_start].tolist()

    # pegar linhas abaixo
    trades = df.iloc[trades_start + 1:].copy()

    trades.columns = headers

    # remover linhas totalmente vazias
    trades = trades.dropna(how="all")

    # remover linhas sem data
    possible_date_col = trades.columns[0]

    trades = trades[
        trades[possible_date_col].astype(str).str.contains(":", na=False)
    ]

    trades = trades.reset_index(drop=True)

    return trades
