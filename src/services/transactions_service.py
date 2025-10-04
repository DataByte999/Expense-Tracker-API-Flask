from src.schemas.transaction_schemas import TransactionOut, TransactionsOut, TransactionId
from pydantic import ValidationError
from src.exceptions import AppError, NotFoundError, BadRequestError
from src.repositories.transactions_repo import (insert_transaction, get_transaction, list_transactions,
                                                update_transaction, delete_transaction)


def create_transaction(user_id: int, kind: str, transaction_date: str, amount: float, description: str) -> dict:
    new_tx = insert_transaction(user_id, kind, transaction_date, amount, description)
    try:
        return TransactionOut.model_validate(new_tx).model_dump(mode="json")
    except ValidationError as e:
        raise AppError("Internal schema validation error")


def transaction_info(user_id: int, transaction_id: int) -> dict:
    tx_info = get_transaction(user_id, transaction_id)
    if not tx_info:
        raise NotFoundError("Transaction not found")
    try:
        return TransactionOut.model_validate(tx_info).model_dump()
    except ValidationError as e:
        raise AppError("Internal schema validation error")


def transaction_list(user_id: int) -> dict:
    tx_list = list_transactions(user_id)
    try:
        return TransactionsOut.model_validate({"transactions": tx_list}).model_dump()
    except ValidationError as e:
        raise AppError("Internal schema validation error")


def transaction_update(user_id: int, transaction_id: int, data: dict) -> dict:
    if not data:
        raise BadRequestError("No data provided")
    updated_tx = update_transaction(user_id, transaction_id, data)
    if not updated_tx:
        raise NotFoundError("Transaction not found")
    try:
        return TransactionOut.model_validate(updated_tx).model_dump()
    except ValidationError as e:
        raise AppError("Internal schema validation error")


def transaction_delete(user_id: int, transaction_id: int) -> int:
    delete_tx = delete_transaction(user_id, transaction_id)
    if not delete_tx:
        raise NotFoundError("Transaction not found")
    try:
        return TransactionId.model_validate(delete_tx).model_dump()
    except ValidationError as e:
        raise AppError("Internal schema validation error")
