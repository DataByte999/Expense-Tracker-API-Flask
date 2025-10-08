from http import HTTPStatus


def test_tx_list_success(client, auth_user, added_transaction):
    """GET transactions/ Should return a 200, and a list of transactions that belong to that user."""
    _user, headers = auth_user
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    transactions = data["transactions"]
    for tx in transactions:
        if tx["id"] == added_transaction["id"]:
            assert tx["kind"] == added_transaction["kind"]
            assert tx["transaction_date"] == str(added_transaction["transaction_date"])
            assert tx["amount"] == str(added_transaction["amount"])
            assert tx["description"] == added_transaction["description"]


def test_tx_list_user_not_found(client, nonexisting_user_headers):
    """Should return 200, with transactions empty list"""

    response = client.get("/transactions/", headers=nonexisting_user_headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["transactions"] == []
