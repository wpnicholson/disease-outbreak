from api.endpoints.auth import hash_password, verify_password


def test_password_hashing(client):
    pw = "supersecret"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)
