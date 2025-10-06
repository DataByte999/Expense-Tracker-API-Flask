from unittest.mock import patch


def test_user_update_one_field_success(client, auth_user):
    """Should update logged-in user username, returns 200 and updated user information
    (excluding user id and hiding user password)."""

    user, headers = auth_user

    new_username = "This is Jake"

    response = client.patch("/me", json={
        "username": new_username,
    },headers=headers)

    assert response.status_code == 200
    data = response.get_json()

    assert data["username"] != user["username"]
    assert data["username"] == new_username
    assert data["email"] == user["email"]
    assert data["password"] == "********"


def test_user_update_all_fields_success(client, auth_user, user_payload):
    """Should update logged-in user username, email, password. Returns 200 and updated user information
        (excluding user id and hiding user password)."""
    user, headers = auth_user

    response = client.patch("/me", json=user_payload, headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == user_payload["username"]
    assert data["email"] == user_payload["email"]
    assert data["password"] != user["password"]


def test_user_update_user_not_found(client, auth_user, user_payload):
    """Should return 404 when user no longer exists."""
    user, headers = auth_user
    with patch("src.services.users_service.update_user", return_value=None):
        response = client.patch("/me", json=user_payload, headers=headers)
        assert response.status_code == 404


def test_user_update_duplicate_email(client, auth_user, registered_user):
    """Update with existing email in database should fail, returns 409"""
    user, headers = auth_user
    response = client.patch("/me", json={"email": registered_user["email"]}, headers=headers)
    assert response.status_code == 409


def test_update_user_empty_payload(client, auth_user):
    """Should return 400 when payload empty."""
    user, headers = auth_user
    response = client.patch("/me", json={}, headers=headers)
    assert response.status_code == 400