

def test_tx_update_success(client, auth_user, added_transaction):
    """PATCH /transactions/<tx_id> Should update transaction with provided fields by transaction id,
     returning 200 with updated transaction data"""
    user, headers = auth_user
    update_fields = {"amount": 100000, "description": "New description"}
    response = client.patch(f"/transactions/{added_transaction['id']}",  json=update_fields, headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == added_transaction["id"]
    assert data["kind"] == added_transaction["kind"]
    assert data["transaction_date"] == str(added_transaction["transaction_date"])
    assert data["amount"] == str(update_fields["amount"])
    assert data["description"] == update_fields["description"]


def test_tx_update_transaction_not_found(client, auth_user, tx_payload):
    """Should return 404 when transaction does not exist"""
    user, headers = auth_user
    nonexistent_tx_id = 999999
    response = client.patch(f"/transactions/{nonexistent_tx_id}", json=tx_payload, headers=headers)
    assert response.status_code == 404


def test_tx_update_empty_payload(client, auth_user, added_transaction):
    """Should return 400 when payload is empty"""
    user, headers = auth_user
    response = client.patch(f"/transactions/{added_transaction["id"]}", json={}, headers=headers)
    assert response.status_code == 400


def test_tx_update_amount_invalid_type(client, auth_user, added_transaction, tx_payload):
    """Should return 400 when payload data type is invalid"""
    user, headers = auth_user
    tx_payload["amount"] = "One hundred"
    response = client.patch(f"/transactions/{added_transaction["id"]}", json=tx_payload, headers=headers)
    assert response.status_code == 400
