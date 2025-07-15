from api.database import SessionLocal
from api.models import User


def test_signup_and_login(client, test_run_id):
    email = f"authuser-{test_run_id}@example.com"

    signup_resp = client.post(
        "/api/auth/signup",
        json={
            "email": email,
            "password": "strongpassword",
            "full_name": "Auth User",
        },
    )
    assert signup_resp.status_code == 201

    login_resp = client.post(
        "/api/auth/login",
        json={"email": email, "password": "strongpassword"},
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

    # Local cleanup
    db = SessionLocal()
    try:
        db.query(User).filter(User.email.like(f"%{test_run_id}%")).delete(
            synchronize_session=False
        )
        db.commit()
    finally:
        db.close()
