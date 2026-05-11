import os
import json
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def init_db():
    with engine.begin() as conn:

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS uploads (
            id SERIAL PRIMARY KEY,
            account_name TEXT,
            platform TEXT,
            file_name TEXT,
            metrics_json TEXT,
            trades_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_email TEXT
        )
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))


def save_upload(
    account_name,
    platform,
    file_name,
    trades_df,
    metrics,
    user_email
):

    metrics_json = json.dumps(metrics)

    trades_json = trades_df.to_json(
        orient="records",
        date_format="iso"
    )

    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO uploads (
            account_name,
            platform,
            file_name,
            metrics_json,
            trades_json,
            user_email
        )
        VALUES (
            :account_name,
            :platform,
            :file_name,
            :metrics_json,
            :trades_json,
            :user_email
        )
        """), {
            "account_name": account_name,
            "platform": platform,
            "file_name": file_name,
            "metrics_json": metrics_json,
            "trades_json": trades_json,
            "user_email": user_email
        })


def load_upload_history(user_email):

    query = text("""
    SELECT
        id,
        account_name,
        platform,
        file_name,
        created_at
    FROM uploads
    WHERE user_email = :user_email
    ORDER BY created_at DESC
    """)

    with engine.begin() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={"user_email": user_email}
        )

    return df


def load_upload_by_id(upload_id):

    query = text("""
    SELECT trades_json
    FROM uploads
    WHERE id = :id
    """)

    with engine.begin() as conn:

        result = conn.execute(
            query,
            {"id": upload_id}
        ).fetchone()

    if not result:
        return pd.DataFrame()

    trades_json = result[0]

    return pd.read_json(trades_json)


def create_user(
    name,
    email,
    password
):

    with engine.begin() as conn:

        conn.execute(text("""
        INSERT INTO users (
            name,
            email,
            password
        )
        VALUES (
            :name,
            :email,
            :password
        )
        """), {
            "name": name,
            "email": email,
            "password": password
        })


def get_user_by_email(email):

    query = text("""
    SELECT *
    FROM users
    WHERE email = :email
    """)

    with engine.begin() as conn:

        result = conn.execute(
            query,
            {"email": email}
        ).mappings().fetchone()

    return result
