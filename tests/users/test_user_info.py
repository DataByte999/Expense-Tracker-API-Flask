from http import HTTPStatus
from unittest.mock import patch


def test_user_info_success(client, auth_user):
    """GET /me Should return correct user info when token is valid."""
    user, headers = auth_user

    response = client.get("/me", headers=headers)

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()

    assert data["username"] == user["username"]
    assert data["email"] == user["email"]


def test_user_info_user_not_found(client, auth_user):
    """Should return 404 when user no longer exists."""
    _user, headers = auth_user
    with patch("src.services.users_service.get_user", return_value=None):
        response = client.get("/me", headers=headers)
        assert response.status_code == HTTPStatus.NOT_FOUND
