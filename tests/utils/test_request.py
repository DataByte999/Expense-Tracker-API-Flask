from http import HTTPStatus


def test_api_request_invalid_json_payload(client):
    """Should return 415 when sending a request with invalid json"""
    response = client.post("/auth/register", data="not a json")
    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


def test_api_request_missing_content_type(client, user_payload):
    """Should return 415 when sending a request with wrong/missing content type.
    ex. content_type='application/json'"""
    response = client.post(
        "/auth/register", json=user_payload, content_type="text/plain"
    )
    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
