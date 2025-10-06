import pytest
from faker import Faker
from src.app import create_app
from tests.factories import make_user, make_token, make_transaction

fake = Faker()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def faker():
    return fake


@pytest.fixture()
def auth_user(client):
    """Fixture: Creates a user and access token, returns (user, headers) """
    user = make_user()
    token = make_token(user["id"])
    headers = {"Authorization": f"Bearer {token}"}
    return user, headers


@pytest.fixture()
def nonexisting_user_headers():
    """Fixture: Creates a JWT token for user that doesn't exist. Deleted user that still has valid access token """
    token = make_token(99999)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


@pytest.fixture()
def user_payload(faker):
    """Fixture: Creates a fake user payload and returns it."""
    fake_user = {
        "username": faker.user_name(),
        "email": faker.unique.email(),
        "password": "Secret1234!"
    }
    return fake_user


@pytest.fixture()
def registered_user():
    """Fixture: Creates a user and returns registered in database user data. """
    user = make_user()
    return user


@pytest.fixture()
def tx_payload(faker):
    """Fixture: Creates a fake transaction payload and returns it."""
    fake_tx = {
        "kind": "expense",
        "transaction_date": fake.date_this_decade().isoformat(),
        "amount": str(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=1)),
        "description": fake.sentence(nb_words=4)
    }
    return fake_tx


@pytest.fixture()
def added_transaction(auth_user):
    """Fixture: Creates a transaction for logged-in user."""
    user = auth_user[0]
    new_tx = make_transaction(user_id=user["id"])
    return new_tx