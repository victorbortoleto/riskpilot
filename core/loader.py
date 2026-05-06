import pandas as pd
from core.mt5_parser import parse_mt5_strategy_report


def load_trading_file(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin1")

    if name.endswith(".xlsx"):
        raw = pd.read_excel(uploaded_file)

        # detectar relatório MT5
        first_cells = raw.astype(str).head(20).to_string().lower()

        if "expert advisor" in first_cells or "strategy tester" in first_cells:
            return parse_mt5_strategy_report(raw)

        return raw

    raise ValueError("Formato não suportado. Use CSV ou XLSX.")
