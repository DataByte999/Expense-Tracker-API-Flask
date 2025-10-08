from http import HTTPStatus


def test_tx_info_success(client, auth_user, added_transaction):
    """GET /transactions/<tx_id> Should return transaction data"""

    _user, headers = auth_user
    response = client.get(f"/transactions/{added_transaction['id']}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["id"] == added_transaction["id"]
    assert data["kind"] == added_transaction["kind"]
    assert data["transaction_date"] == str(added_transaction["transaction_date"])
    assert data["amount"] == str(added_transaction["amount"])
    assert data["description"] == added_transaction["description"]


def test_tx_info_user_not_found(client, nonexisting_user_headers, added_transaction):
    """Should return 404 when user doesn't exist"""
    response = client.get(
        f"/transactions/{added_transaction['id']}", headers=nonexisting_user_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_tx_info_transaction_not_found(client, auth_user):
    """Should return 404 when transaction doesn't exist"""
    nonexisting_transaction = 99999999
    _user, headers = auth_user
    response = client.get(f"/transactions/{nonexisting_transaction}", headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
