from pydantic import ValidationError

from src.exceptions import AppError, BadRequestError, NotFoundError
from src.repositories.transactions_repo import (
    erase_transaction,
    get_all_transactions,
    get_transaction_by_id,
    insert_transaction,
    update_transaction,
)
from src.schemas.transaction_schemas import (
    TransactionId,
    TransactionOut,
    TransactionsOut,
)


def create_transaction(
    user_id: int, kind: str, transaction_date: str, amount: float, description: str
) -> dict:
    """
    Create a transaction for the current user.

    Args:
        user_id (int): User ID
        kind (str): Transaction kind ('expense' or 'income')
        transaction_date (str): Transaction date (YYYY-MM-DD)
        amount (float): Transaction amount
        description (str): Transaction description

    Returns:
        dict: Validated transaction information (TransactionOut schema)

        {tx_id, tx_kind, tx_date, tx_amount, tx_description}

    Raises:
        AppError: If schema validation fails.
    """
    new_tx = insert_transaction(user_id, kind, transaction_date, amount, description)
    try:
        return TransactionOut.model_validate(new_tx).model_dump(mode="json")
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def get_transaction_info(user_id: int, transaction_id: int) -> dict:
    """
    Retrieve a transaction by ID for the current user.

    Args:
        user_id (int): User ID
        transaction_id (int): Transaction ID

    Returns:
        dict: Validated transaction information (TransactionOut schema)

        {tx_id, tx_kind, tx_date, tx_amount, tx_description}
    Raises:
        NotFoundError: If transaction not found.

        AppError: If schema validation fails.
    """
    tx_info = get_transaction_by_id(user_id, transaction_id)
    if not tx_info:
        raise NotFoundError("Transaction not found")
    try:
        return TransactionOut.model_validate(tx_info).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def get_transaction_list(user_id: int) -> dict:
    """
    Retrieve all transactions for the current user.

    Args:
        user_id (int): User ID

    Returns:
          list[dict]: Validated List of transactions (TransactionOut schema).

          [{tx_id, tx_kind, tx_date, tx_amount, tx_description},...]

          []: If no transactions exist or user doesn't exist.
    Raises:
        AppError: If schema validation fails.
    """
    tx_list = get_all_transactions(user_id)
    try:
        return TransactionsOut.model_validate({"transactions": tx_list}).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def update_transaction_info(user_id: int, transaction_id: int, data: dict) -> dict:
    """
    Update transaction fields for current user.

    Args:
        user_id (int): User ID
        transaction_id (int): Transaction ID
        data (dict): Fields to update (e.g. kind, transaction_date, amount, description).

    Returns:
        dict: Validated and updated transaction information (TransactionOut schema).

    Raises:
        BadRequestError: If no data is provided.
        NotFoundError: If transaction not found.
        AppError: If schema validation fails.
    """
    if not data:
        raise BadRequestError("No data provided")
    updated_tx = update_transaction(user_id, transaction_id, data)
    if not updated_tx:
        raise NotFoundError("Transaction not found")
    try:
        return TransactionOut.model_validate(updated_tx).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def delete_transaction(user_id: int, transaction_id: int) -> dict:
    """
    Delete a transaction for the current user.

    Args:
        user_id (int): User ID
        transaction_id (int): Transaction ID

    Returns:
        dict: Validated transaction ID of deleted transaction (TransactionOut schema).

    Raises:
        NotFoundError: If transaction not found.
        AppError: If schema validation fails.
    """
    deleted_tx = erase_transaction(user_id, transaction_id)
    if not deleted_tx:
        raise NotFoundError("Transaction not found")
    try:
        return TransactionId.model_validate(deleted_tx).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err
