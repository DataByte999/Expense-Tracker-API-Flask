from http import HTTPStatus


def test_create_tx_success(client, auth_user, tx_payload):
    """POST /transactions should create a transaction, returns 201 and transaction data"""

    _user, headers = auth_user

    response = client.post("/transactions/", json=tx_payload, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert "id" in data
    assert data["kind"] == tx_payload["kind"]
    assert data["transaction_date"] == tx_payload["transaction_date"]
    assert data["amount"] == tx_payload["amount"]
    assert data["description"] == tx_payload["description"]


def test_create_tx_user_not_found(client, nonexisting_user_headers, tx_payload):
    """Should return 404, creating a transaction when user doesn't exist"""

    response = client.post(
        "/transactions/", json=tx_payload, headers=nonexisting_user_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_tx_invalid_kind(client, auth_user, tx_payload):
    """Should return 400, creating a transaction when kind is invalid"""
    _user, headers = auth_user

    tx_payload["kind"] = "invalid"  # accepts only "expense" or "income"
    response = client.post("/transactions/", json=tx_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_tx_invalid_transaction_date(client, auth_user, tx_payload):
    """Should return 400, creating a transaction when transaction_date is invalid"""
    _user, headers = auth_user
    tx_payload["transaction_date"] = "2025/09/25"
    response = client.post("/transactions/", json=tx_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_tx_invalid_amount(client, auth_user, tx_payload):
    """Should return 400, creating a transaction when amount is invalid"""
    _user, headers = auth_user
    tx_payload["amount"] = -100
    response = client.post("/transactions/", json=tx_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_tx_invalid_description_too_short(client, auth_user, tx_payload):
    """Should return 400, creating a transaction when description is too short"""
    _user, headers = auth_user
    tx_payload["description"] = ""
    response = client.post("/transactions/", json=tx_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_tx_invalid_description_too_long(client, auth_user, tx_payload):
    """Should return 400, creating a transaction when description is too long"""
    _user, headers = auth_user
    tx_payload["description"] = (
        "aokmokmokmokmokmokmokmokmokmokmokmokmokmokijnijnjinaokmokmokmokmokmokmokmokmokmokmokm"
        "okmokmokijnijnjinaokmokmokmokmokmokmokmokmokmokmokmokmokmokijnijnjinaokmokmokmokmokmo"
        "kmokmokmokmokmokmokmokmokijnijnjinaokmokmokmokmokmokmokmokmokmokmokmokmokmokijnijnjin"
        "256"
    )
    response = client.post("/transactions/", json=tx_payload, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
