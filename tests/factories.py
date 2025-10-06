from faker import Faker
from src.repositories.users_repo import insert_user, get_user_by_email
from src.repositories.transactions_repo import insert_transaction
from src.utils.password import hash_password
from src.utils.jwt_utils import create_access_token

fake = Faker()


def make_user(username: str | None = None, email: str | None = None, password: str | None = "Secret1234!"):
    """Factory: Create a test user in Database. Returns new user data.
    {"id": ..., "username": ..., "email": ..., "password": ...}"""
    username = username or fake.user_name()
    email = email or fake.unique.email()
    password_hash = hash_password(password)

    insert_user(username=username, email=email, password_hash=password_hash)

    new_user = get_user_by_email(email=email)
    new_user.pop("password_hash")
    new_user["password"] = password
    return new_user


def make_transaction(user_id: int, kind: str = "expense"):
    """Factory: Create a test transaction in Database. Returns new transaction data"""
    tx = insert_transaction(
        user_id=user_id,
        kind=kind,
        transaction_date=fake.date_this_decade().isoformat(),
        amount= fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=1),
        description=fake.sentence(nb_words=4)
    )
    return tx


def make_token(user_id: int):
    """Factory: Create a JWT token for a given user_id. Returns new token"""
    token = create_access_token(user_id=user_id)
    return token
