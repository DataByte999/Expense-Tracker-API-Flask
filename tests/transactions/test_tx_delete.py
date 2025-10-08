from http import HTTPStatus


def test_tx_delete_success(client, auth_user, added_transaction):
    """Delete /transactions/<tx_id> Should delete transaction , return 200 with transaction_id deleted"""
    _user, headers = auth_user
    response = client.delete(
        f"/transactions/{added_transaction['id']}", headers=headers
    )
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert (
        data["message"]
        == f"Transaction with id: {added_transaction['id']}, deleted successfully!"
    )


def test_tx_delete_transaction_not_found(client, auth_user):
    """Should return 404 when transaction does not exist"""
    _user, headers = auth_user
    nonexistent_tx_id = 999999999
    response = client.delete(f"/transactions/{nonexistent_tx_id}", headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_tx_delete_invalid_transaction_id(client, auth_user):
    """Should return 400 when transaction id is invalid"""
    _user, headers = auth_user
    invalid_tx_id = -1
    response = client.delete(f"/transactions/{invalid_tx_id}", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
