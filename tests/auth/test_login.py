

def test_login_success(client, registered_user):
    """POST /auth/login should return an access token."""
    response = client.post('/auth/login', json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })

    assert response.status_code == 200
    data = response.get_json()

    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "Bearer"



def test_login_wrong_password(client, registered_user):
    """Wrong password should fail login and return 401"""
    response = client.post('/auth/login', json={
        "email": registered_user["email"],
        "password": "wrong_password"
    })

    assert response.status_code == 401


def test_login_non_existing_user(client):
    """Login with unregistered email should return 401"""
    response = client.post('/auth/login', json={
        "email": "non_existing_email@example.com",
        "password": "whatever"
    })

    assert response.status_code == 401