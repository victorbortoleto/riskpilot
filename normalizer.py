import pandas as pd
import numpy as np
import re

COLUMN_ALIASES = {
    "date": [
        "date", "time", "datetime", "open time", "close time", "data", "hora", "horario",
        "execution time", "entry time", "exit time"
    ],
    "asset": [
        "symbol", "asset", "instrument", "ativo", "ticker", "market", "contract"
    ],
    "side": [
        "side", "type", "operation", "buy/sell", "direction", "compra/venda", "tipo"
    ],
    "quantity": [
        "qty", "quantity", "volume", "contracts", "lots", "lotes", "quantidade", "size"
    ],
    "entry_price": [
        "entry", "entry price", "open price", "price", "preco entrada", "entrada"
    ],
    "exit_price": [
        "exit", "exit price", "close price", "preco saida", "saida"
    ],
    "pnl": [
        "pnl", "p&l", "profit", "profit/loss", "net profit", "gross profit",
        "resultado", "lucro", "lucro/prejuizo", "lucro/prejuízo", "pl", "gain", "realized pnl"
    ],
    "fees": [
        "fees", "commission", "commissions", "costs", "taxas", "corretagem"
    ]
}

def _clean_column_name(col):
    col = str(col).strip().lower()
    col = re.sub(r"[_\-]+", " ", col)
    col = re.sub(r"\s+", " ", col)
    return col

def _find_column(df_columns, aliases):
    cleaned_map = {_clean_column_name(c): c for c in df_columns}

    for alias in aliases:
        alias_clean = _clean_column_name(alias)
        if alias_clean in cleaned_map:
            return cleaned_map[alias_clean]

    for cleaned, original in cleaned_map.items():
        for alias in aliases:
            alias_clean = _clean_column_name(alias)
            if alias_clean in cleaned:
                return original

    return None

def _to_numeric(series):
    if series is None:
        return None

    return (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace("R$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .replace({"": np.nan, "nan": np.nan, "None": np.nan})
        .astype(float)
    )

def normalize_trades(raw_df):
    df = raw_df.copy()
    normalized = pd.DataFrame()

    mapped = {}
    for standard_col, aliases in COLUMN_ALIASES.items():
        mapped[standard_col] = _find_column(df.columns, aliases)

    if mapped["date"] is None:
        raise ValueError("Coluna de data não encontrada.")

    if mapped["pnl"] is None:
        raise ValueError("Coluna de P&L/resultado não encontrada.")

    normalized["date"] = pd.to_datetime(df[mapped["date"]], errors="coerce")
    normalized["pnl"] = _to_numeric(df[mapped["pnl"]])

    if mapped["asset"]:
        normalized["asset"] = df[mapped["asset"]].astype(str)
    else:
        normalized["asset"] = "Unknown"

    if mapped["side"]:
        normalized["side"] = df[mapped["side"]].astype(str).str.lower()
    else:
        normalized["side"] = "unknown"

    if mapped["quantity"]:
        normalized["quantity"] = _to_numeric(df[mapped["quantity"]])
    else:
        normalized["quantity"] = 1

    if mapped["entry_price"]:
        normalized["entry_price"] = _to_numeric(df[mapped["entry_price"]])
    else:
        normalized["entry_price"] = np.nan

    if mapped["exit_price"]:
        normalized["exit_price"] = _to_numeric(df[mapped["exit_price"]])
    else:
        normalized["exit_price"] = np.nan

    if mapped["fees"]:
        normalized["fees"] = _to_numeric(df[mapped["fees"]])
    else:
        normalized["fees"] = 0.0

    normalized["net_pnl"] = normalized["pnl"] - normalized["fees"]

    normalized = normalized.dropna(subset=["date", "pnl"]).reset_index(drop=True)
    normalized = normalized.sort_values("date").reset_index(drop=True)

    if normalized.empty:
        raise ValueError("Nenhuma operação válida encontrada após normalização.")

    return normalized
