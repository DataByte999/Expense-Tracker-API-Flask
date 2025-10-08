from flask import Blueprint, g, jsonify, request

from src.schemas.transaction_schemas import (
    TransactionId,
    TransactionIn,
    UpdateTransactionIn,
)
from src.services.transactions_service import (
    create_transaction,
    delete_transaction,
    get_transaction_info,
    get_transaction_list,
    update_transaction_info,
)
from src.utils.jwt_utils import jwt_required

tx_bp = Blueprint("tx", __name__, url_prefix="/transactions")


@tx_bp.get("/")
@jwt_required
def list_transactions():
    """
    Retrieves a list of all transactions for logged-in user.

    Returns:
        JSON response (200 OK) containing validated list of transactions.
    """
    all_transactions = get_transaction_list(g.user_id)
    return jsonify(all_transactions), 200


@tx_bp.get("/<transaction_id>")
@jwt_required
def get_transaction(transaction_id: int):
    """
    Retrieves a transaction by ID (path parameter) for logged-in user.

    Args:
        transaction_id (int): Transaction ID from URL path.

    Returns:
          JSON response (200 OK) containing validated transaction information.
    """
    tx = TransactionId.model_validate({"id": transaction_id})
    transaction = get_transaction_info(g.user_id, tx.id)
    return jsonify(transaction), 200


@tx_bp.post("/")
@jwt_required
def add_transaction():
    """
    Creates a new transaction for the logged-in user.

    Request Body:
        kind (str): 'expense' or 'income'.
        transaction_date (str): Date in 'YYYY-MM-DD' format.
        amount (str): Transaction amount.
        description (str): Transaction description.

    Returns:
          JSON response (201 Created) containing created transaction information.
    """
    request_data = TransactionIn.model_validate(request.json)
    new_tx = create_transaction(
        g.user_id,
        request_data.kind,
        str(request_data.transaction_date),
        float(request_data.amount),
        request_data.description,
    )
    return jsonify(new_tx), 201


@tx_bp.patch("/<transaction_id>")
@jwt_required
def patch_transaction(transaction_id: int):
    """
    Updates fields of an existing transaction for the logged-in user.

    Args:
        transaction_id (int): Transaction ID from the URL path.

    Request Body:
        Optional fields: kind, transaction_date, amount, description.

    Returns:
          JSON response (200 OK) containing updated transaction information.
    """
    tx = TransactionId.model_validate({"id": transaction_id})
    request_data = UpdateTransactionIn.model_validate(request.json).model_dump(
        exclude_unset=True
    )
    updated_tx = update_transaction_info(g.user_id, tx.id, request_data)
    return jsonify(updated_tx), 200


@tx_bp.delete("/<transaction_id>")
@jwt_required
def remove_transaction(transaction_id: int):
    """
    Deletes transaction for logged-in user.

    Args:
        transaction_id (int): Transaction ID from the URL path.

    Returns:
          JSON response (200 OK) containing deleted transaction ID and confirming deletion .
    """
    tx = TransactionId.model_validate({"id": transaction_id})
    deleted_tx = delete_transaction(g.user_id, tx.id)
    return {
        "message": f"Transaction with id: {deleted_tx['id']}, deleted successfully!"
    }, 200
