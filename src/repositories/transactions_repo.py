from psycopg import sql
from psycopg.rows import dict_row

from src.database.db_connection import get_conn


def insert_transaction(
    user_id: int, kind: str, transaction_date: str, amount: float, description: str
) -> dict:
    """
    Insert a transaction into the database.

    Args:
        user_id (int): User ID.
        kind (str): Transaction kind (expense, income).
        transaction_date (str): Transaction date.
        amount (float): Transaction amount.
        description (str): Transaction description.

    Returns:
        dict: Newly inserted transaction information.

        {tx_id, tx_kind, tx_date, tx_amount, tx_description}

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """
            INSERT INTO transactions (user_id, kind, transaction_date, amount, description)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, kind, transaction_date, amount, description;
            """
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user_id, kind, transaction_date, amount, description))
        return cur.fetchone()


def get_transaction_by_id(user_id: int, transaction_id: int) -> dict | None:
    """
    Get transaction data by from the database.

    Args:
        user_id (int): User ID.
        transaction_id (int): Transaction ID.

    Returns:
          dict: Transaction data.

          {tx_id, tx_kind, tx_date, tx_amount, tx_description}

          None: If transaction does not exist.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """SELECT id, kind, transaction_date, amount, description
               FROM transactions
               WHERE id = (%s) AND user_id = (%s);"""
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (transaction_id, user_id))
        return cur.fetchone()


def get_all_transactions(user_id: int) -> list[dict]:
    """
    Get all transactions data from the database.

    Args:
        user_id (int): User ID.

    Returns:
        list[dict]: List of dictionaries containing transaction information.

        [{tx_id, tx_kind, tx_date, tx_amount, tx_description},...]

        []: If no transactions exist.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = """SELECT id, kind, transaction_date, amount, description
               FROM transactions
               WHERE user_id = (%s)"""
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user_id,))
        return cur.fetchall()


def update_transaction(user_id: int, transaction_id: int, data: dict) -> dict | None:
    """
    Updates transaction fields in the database.

    Args:
        user_id (int): User ID.
        transaction_id (int): Transaction ID.
        data (dict): Key-value pairs of fields to update.

    Returns:
        dict: Updated transaction data.

        {tx_id, tx_kind, tx_date, tx_amount, tx_description}

        None: If transaction does not exist.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    set_parts = [
        sql.SQL("{} = %({})s").format(sql.Identifier(col), sql.SQL(col)) for col in data
    ]
    set_clause = sql.SQL(", ").join(set_parts)
    params = {**data, "transaction_id": transaction_id, "user_id": user_id}
    query = sql.SQL("""UPDATE transactions
                       SET {set_clause}
                       WHERE id = %(transaction_id)s AND user_id = %(user_id)s
                       RETURNING id, kind, transaction_date, amount, description;
                    """).format(set_clause=set_clause)
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, params)
        return cur.fetchone()


def erase_transaction(user_id: int, transaction_id: int) -> dict | None:
    """
    Deletes a transaction from the database.

    Args:
        user_id (int): User ID.
        transaction_id (int): Transaction ID.

    Returns:
          dict: ID of deleted transaction.

          None: If transaction does not exist.

    Raises:
        psycopg.errors.Error: If any database-related error occurs during the query execution.
    """
    query = (
        """DELETE FROM transactions WHERE id = (%s) AND user_id = (%s) RETURNING id"""
    )
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (transaction_id, user_id))
        return cur.fetchone()
