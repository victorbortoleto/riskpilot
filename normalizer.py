import pandas as pd

def load_trading_file(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin1")

    if name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    raise ValueError("Formato não suportado. Use CSV ou XLSX.")
