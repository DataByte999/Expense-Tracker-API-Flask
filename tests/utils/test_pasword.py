
from src.repositories.users_repo import get_user_by_email
from src.utils.password import verify_password

def test_password_is_hashed_on_registration(client, registered_user):
    """Password should never be stored in plain text."""
    user = get_user_by_email(registered_user["email"])

    assert user["password_hash"] != registered_user["password"]
    assert verify_password(registered_user["password"], user["password_hash"])




