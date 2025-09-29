import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from src.database.db_connection import get_conn


def insert_transaction(user_id: int, kind: str, transaction_date: str, amount: float, description: str) -> dict:
    query = """
            INSERT INTO transactions (user_id, kind, transaction_date, amount, description) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING id, kind, transaction_date, amount, description;
            """
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (user_id, kind, transaction_date, amount, description))
                transaction_data = cur.fetchone()
                return transaction_data
    except psycopg.Error as e:
        raise e


def get_transaction(user_id: int, transaction_id: int) -> dict | None:
    query = """SELECT id, kind, transaction_date, amount, description 
               FROM transactions 
               WHERE id = (%s) AND user_id = (%s);"""
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (transaction_id, user_id))
                transaction_data = cur.fetchone()
                return transaction_data
    except psycopg.Error as e:
        raise e


def list_transactions(user_id: int) -> list[dict]:
    query = """SELECT id, kind, transaction_date, amount, description 
               FROM transactions 
               WHERE user_id = (%s)"""
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (user_id,))
                transactions_list = cur.fetchall() or []
                return transactions_list
    except psycopg.Error as e:
        raise e


def update_transaction(user_id: int, transaction_id: int, data: dict) -> dict | None:
    set_parts = [sql.SQL("{} = %({})s").format(sql.Identifier(col), sql.SQL(col)) for col in data.keys()]
    set_clause = sql.SQL(", ").join(set_parts)
    params = {**data, "transaction_id": transaction_id,"user_id": user_id}
    query = sql.SQL("""UPDATE transactions 
                       SET {set_clause} 
                       WHERE id = %(transaction_id)s AND user_id = %(user_id)s
                       RETURNING id, kind, transaction_date, amount, description;
                    """).format(set_clause=set_clause)
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                updated_row = cur.fetchone()
                return updated_row
    except psycopg.Error as e:
        raise e


def delete_transaction(user_id: int, transaction_id: int) -> int | None:
    query = """DELETE FROM transactions WHERE id = (%s) AND user_id = (%s) RETURNING id"""
    try:
        with get_conn() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (transaction_id, user_id))
                deleted_tx_id = cur.fetchone()
                return deleted_tx_id
    except psycopg.Error as e:
        raise e
