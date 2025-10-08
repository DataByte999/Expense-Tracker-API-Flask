from http import HTTPStatus
from unittest.mock import patch

from src.repositories.users_repo import get_user_by_email


def test_user_delete_success(client, auth_user):
    """Should delete logged-in user and return 200 with deleted username"""
    user, headers = auth_user
    response = client.delete("/me", headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["message"] == f"User {user['username']}, was deleted successfully!"
    assert not get_user_by_email(user["email"])


def test_user_delete_user_not_found(client, auth_user):
    """Should return 404 when user no longer exists."""
    _user, headers = auth_user
    with patch("src.services.users_service.delete_user", return_value=None):
        response = client.delete("/me", headers=headers)
        assert response.status_code == HTTPStatus.NOT_FOUND
