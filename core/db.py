import os
from io import StringIO
import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = "sqlite:///riskpilot.db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS uploads (
                id SERIAL PRIMARY KEY,
                account_name TEXT,
                platform TEXT,
                file_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_trades INTEGER,
                net_pnl FLOAT,
                winrate FLOAT,
                profit_factor FLOAT,
                max_drawdown FLOAT,
                raw_json TEXT
            )
        """))


def save_upload(account_name, platform, file_name, trades_df, metrics):
    init_db()

    data_json = trades_df.to_json(orient="records", date_format="iso")

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO uploads (
                    account_name,
                    platform,
                    file_name,
                    total_trades,
                    net_pnl,
                    winrate,
                    profit_factor,
                    max_drawdown,
                    raw_json
                ) VALUES (
                    :account_name,
                    :platform,
                    :file_name,
                    :total_trades,
                    :net_pnl,
                    :winrate,
                    :profit_factor,
                    :max_drawdown,
                    :raw_json
                )
            """),
            {
                "account_name": account_name,
                "platform": platform,
                "file_name": file_name,
                "total_trades": int(metrics.get("total_trades", 0)),
                "net_pnl": float(metrics.get("net_pnl", 0)),
                "winrate": float(metrics.get("winrate", 0)),
                "profit_factor": float(metrics.get("profit_factor", 0)),
                "max_drawdown": float(metrics.get("max_drawdown", 0)),
                "raw_json": data_json,
            }
        )


def load_upload_history(limit=50):
    init_db()

    query = text("""
        SELECT
            id,
            account_name,
            platform,
            file_name,
            created_at,
            total_trades,
            net_pnl,
            winrate,
            profit_factor,
            max_drawdown
        FROM uploads
        ORDER BY created_at DESC
        LIMIT :limit
    """)

    with engine.begin() as conn:
        result = conn.execute(query, {"limit": limit})
        rows = result.fetchall()
        columns = result.keys()

    return pd.DataFrame(rows, columns=columns)


def load_upload_by_id(upload_id):
    init_db()

    query = text("""
        SELECT raw_json
        FROM uploads
        WHERE id = :upload_id
    """)

    with engine.begin() as conn:
        row = conn.execute(query, {"upload_id": int(upload_id)}).fetchone()

    if not row:
        return pd.DataFrame()

    raw_json = row[0]

    if not raw_json:
        return pd.DataFrame()

    return pd.read_json(StringIO(raw_json))
