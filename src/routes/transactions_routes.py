from flask import Blueprint, request, jsonify, g
from src.utils.jwt_utils import jwt_required
from src.schemas.transaction_schemas import TransactionIn, UpdateTransactionIn, TransactionId
from pydantic import ValidationError
from src.exceptions import BadRequestError
from src.services.transactions_service import (create_transaction, transaction_info, transaction_list,
                                               transaction_update, transaction_delete)


tx_bp = Blueprint("tx", __name__, url_prefix="/transactions")


@tx_bp.get("/")
@jwt_required
def tx_list():
    all_transactions = transaction_list(g.user_id)
    return jsonify(all_transactions), 200


@tx_bp.get("/info/<transaction_id>")
@jwt_required
def tx_info(transaction_id: int):
    payload = TransactionId.model_validate({"id": transaction_id})
    transaction = transaction_info(g.user_id, payload.id)
    return jsonify(transaction), 200


@tx_bp.post("/new")
@jwt_required
def tx_new():
    payload = TransactionIn.model_validate(request.json)
    new_tx = create_transaction(
        g.user_id,
        payload.kind,
        payload.transaction_date,
        payload.amount,
        payload.description
    )
    return jsonify(new_tx), 201


@tx_bp.patch("/update/<transaction_id>")
@jwt_required
def tx_update(transaction_id: int):
    tx = TransactionId.model_validate({"id": transaction_id})
    payload = UpdateTransactionIn.model_validate(request.json).model_dump(exclude_unset=True)
    updated_tx = transaction_update(g.user_id, tx.id, payload)
    return jsonify(updated_tx), 200


@tx_bp.delete("/delete/<transaction_id>")
@jwt_required
def tx_delete(transaction_id: int):
    tx = TransactionId.model_validate({"id": transaction_id})
    deleted_tx = transaction_delete(g.user_id, tx.id)
    return {"message": f"Transaction with id: {deleted_tx["id"]}, deleted successfully!"}, 200
