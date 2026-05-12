import os
import json
import pandas as pd
from sqlalchemy import create_engine, text


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL não encontrada. Configure a variável de ambiente no Render."
        )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    return database_url


engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
)


# =========================================================
# INIT / MIGRATIONS
# =========================================================

def init_db():
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS uploads (
                    id SERIAL PRIMARY KEY,
                    account_name TEXT,
                    platform TEXT,
                    file_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_trades INTEGER,
                    net_pnl DOUBLE PRECISION,
                    winrate DOUBLE PRECISION,
                    profit_factor DOUBLE PRECISION,
                    max_drawdown DOUBLE PRECISION,
                    trades_json TEXT
                );
                """
            )
        )

        ensure_uploads_columns(conn)


def ensure_uploads_columns(conn):
    columns = pd.read_sql(
        text(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'uploads';
            """
        ),
        conn,
    )["column_name"].tolist()

    required_columns = {
        "user_email": "TEXT",
        "account_name": "TEXT",
        "platform": "TEXT",
        "file_name": "TEXT",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "total_trades": "INTEGER",
        "net_pnl": "DOUBLE PRECISION",
        "winrate": "DOUBLE PRECISION",
        "profit_factor": "DOUBLE PRECISION",
        "max_drawdown": "DOUBLE PRECISION",
        "trades_json": "TEXT",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in columns:
            conn.execute(
                text(
                    f"ALTER TABLE uploads ADD COLUMN {column_name} {column_type};"
                )
            )


# =========================================================
# USERS
# =========================================================

def create_user(name, email, password):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO users (name, email, password)
                VALUES (:name, :email, :password);
                """
            ),
            {
                "name": name,
                "email": email,
                "password": password,
            },
        )


def get_user_by_email(email):
    if not email:
        return None

    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                SELECT id, name, email, password, created_at
                FROM users
                WHERE email = :email
                LIMIT 1;
                """
            ),
            {"email": email},
        ).mappings().first()

    if result is None:
        return None

    return dict(result)


# =========================================================
# UPLOADS
# =========================================================

def save_upload(
    account_name,
    platform,
    file_name,
    trades_df,
    metrics,
    user_email=None,
):
    df = trades_df.copy()

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)

    trades_json = df.to_json(
        orient="records",
        date_format="iso",
        force_ascii=False,
    )

    total_trades = int(metrics.get("total_trades", len(df)))
    net_pnl = float(metrics.get("net_pnl", 0))
    winrate = float(metrics.get("winrate", 0))
    profit_factor = float(metrics.get("profit_factor", 0))
    max_drawdown = float(metrics.get("max_drawdown", 0))

    with engine.begin() as conn:
        ensure_uploads_columns(conn)

        conn.execute(
            text(
                """
                INSERT INTO uploads (
                    user_email,
                    account_name,
                    platform,
                    file_name,
                    total_trades,
                    net_pnl,
                    winrate,
                    profit_factor,
                    max_drawdown,
                    trades_json
                )
                VALUES (
                    :user_email,
                    :account_name,
                    :platform,
                    :file_name,
                    :total_trades,
                    :net_pnl,
                    :winrate,
                    :profit_factor,
                    :max_drawdown,
                    :trades_json
                );
                """
            ),
            {
                "user_email": user_email,
                "account_name": account_name,
                "platform": platform,
                "file_name": file_name,
                "total_trades": total_trades,
                "net_pnl": net_pnl,
                "winrate": winrate,
                "profit_factor": profit_factor,
                "max_drawdown": max_drawdown,
                "trades_json": trades_json,
            },
        )


def load_upload_history(user_email=None):
    with engine.begin() as conn:
        ensure_uploads_columns(conn)

        if user_email:
            query = text(
                """
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
                WHERE user_email = :user_email
                   OR user_email IS NULL
                ORDER BY created_at DESC;
                """
            )

            df = pd.read_sql(
                query,
                conn,
                params={"user_email": user_email},
            )

        else:
            query = text(
                """
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
                ORDER BY created_at DESC;
                """
            )

            df = pd.read_sql(query, conn)

    return df


def load_upload_by_id(upload_id):
    with engine.begin() as conn:
        ensure_uploads_columns(conn)

        result = conn.execute(
            text(
                """
                SELECT trades_json
                FROM uploads
                WHERE id = :upload_id
                LIMIT 1;
                """
            ),
            {"upload_id": int(upload_id)},
        ).mappings().first()

    if result is None:
        return pd.DataFrame()

    trades_json = result.get("trades_json")

    if not trades_json:
        return pd.DataFrame()

    try:
        data = json.loads(trades_json)
        return pd.DataFrame(data)
    except Exception:
        try:
            return pd.read_json(trades_json)
        except Exception:
            return pd.DataFrame()
