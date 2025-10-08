from http import HTTPStatus


def test_register_user_success(client, user_payload):
    """POST /auth/register should create a new user"""

    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == HTTPStatus.CREATED

    data = response.get_json()
    assert data["user"]["username"] == user_payload["username"]
    assert data["user"]["email"] == user_payload["email"]


def test_register_invalid_username_too_short(client, user_payload):
    """Username too short should fail validation"""

    user_payload["username"] = "ab"  # min length = 3
    response = client.post("/auth/register", json=user_payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_invalid_username_too_long(client, user_payload):
    """Username too long should fail validation"""

    user_payload["username"] = (
        "aokmokmokmokmokmokmokmokmokmokmokmokmokmokijnijnjin"  # max length = 50
    )
    response = client.post("/auth/register", json=user_payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_invalid_email(client, user_payload):
    """Invalid email should fail validation"""

    user_payload["email"] = "testexample.com"  # missing @
    response = client.post("/auth/register", json=user_payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_duplicate_email_fails(client, user_payload):
    """Registering with same email twice should fail."""

    client.post("/auth/register", json=user_payload)
    response = client.post("/auth/register", json=user_payload)

    assert response.status_code == HTTPStatus.CONFLICT


def test_register_invalid_password_too_short(client, user_payload):
    """Password too short should fail validation"""

    user_payload["password"] = "Secret1"  # min length = 8
    response = client.post("/auth/register", json=user_payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
