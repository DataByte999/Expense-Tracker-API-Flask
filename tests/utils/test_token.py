from http import HTTPStatus


def test_jwt_required_success(client, auth_user):
    """Should give access to routes that require authentication for loggen_in user."""
    user, headers = auth_user

    response = client.get("/me", headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["email"] == user["email"]


def test_jwt_required_expired_token(client):
    """Should deny access to routes that require authentication when token is required."""
    expired_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MSIsImV4cCI6MTc1OTQwNTc0MX0.66KksPAO3RELwPVIBly2i-"
        "F6Bu5A3JVvBElF7E7le7U"
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_jwt_required_invalid_token(client):
    """Should deny access to routes that require authentication when token is invalid."""
    invalid_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MSIsImV4cCI6MTc1OTQwNTc0MX0.66KksPAO3RELwPVIBly2i-"
        "F6Bu5A3JVvBElF7E7le7"
    )
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_jwt_required_invalid_auth_header(client, auth_user):
    """Should deny access to routes that require authentication when missing or invalid header."""
    _user, headers = auth_user
    token = headers["Authorization"].split()[1]

    new_headers = {"Authorizationnnnn": f"Bearer {token}"}
    response = client.get("/me", headers=new_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_jwt_required_invalid_bearer(client, auth_user):
    """Should deny access to routes that require authentication when missing or invalid header."""
    _user, headers = auth_user
    token = headers["Authorization"].split()[1]

    new_headers = {"Authorization": f"Bearerrrr {token}"}
    response = client.get("/me", headers=new_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
