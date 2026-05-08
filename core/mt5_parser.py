import pandas as pd


def parse_mt5_strategy_report(df):
    asset = "Unknown"

    # tenta descobrir o ativo no cabeçalho
    for idx in range(min(len(df), 30)):
        row_values = [str(x) for x in df.iloc[idx].tolist()]
        if "Ativo:" in row_values:
            try:
                asset = str(df.iloc[idx, 3])
            except Exception:
                asset = "Unknown"

    deals_section = None

    # procura a seção "Transações"
    for idx in range(len(df)):
        row_text = " ".join([str(x).lower() for x in df.iloc[idx].tolist()])
        if "transações" in row_text or "deals" in row_text:
            deals_section = idx
            break

    if deals_section is None:
        raise ValueError("Não encontrei a seção de transações do MT5.")

    header_row = deals_section + 1
    headers = [str(x).strip() for x in df.iloc[header_row].tolist()]

    deals = df.iloc[header_row + 1:].copy()
    deals.columns = headers
    deals = deals.dropna(how="all")

    # mantém apenas linhas com horário válido
    if "Horário" not in deals.columns:
        raise ValueError("Não encontrei a coluna Horário nas transações do MT5.")

    deals = deals[deals["Horário"].astype(str).str.contains(":", na=False)]

    # remove depósito inicial / balance
    if "Tipo" in deals.columns:
        deals = deals[deals["Tipo"].astype(str).str.lower() != "balance"]

    # usa apenas saídas de posição, pois são as que carregam lucro/prejuízo
    if "Direção" in deals.columns:
        deals = deals[deals["Direção"].astype(str).str.lower() == "out"]

    result = pd.DataFrame()

    result["Date"] = deals["Horário"]
    result["Symbol"] = deals["Ativo"].fillna(asset) if "Ativo" in deals.columns else asset
    result["Side"] = deals["Tipo"] if "Tipo" in deals.columns else "unknown"
    result["Qty"] = deals["Volume"] if "Volume" in deals.columns else 1
    result["Entry"] = deals["Preço"] if "Preço" in deals.columns else None
    result["Exit"] = deals["Preço"] if "Preço" in deals.columns else None
    result["Profit"] = deals["Lucro"] if "Lucro" in deals.columns else 0
    result["Fees"] = deals["Comissão"] if "Comissão" in deals.columns else 0

    return result.reset_index(drop=True)
