
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from api import models
from api.dependencies import get_db
from fastapi import status

@pytest.mark.asyncio
async def test_signup_creates_user(async_client: AsyncClient, db_session: Session):
    payload = {
        "email": "newuser@example.com",
        "password": "securepassword123",
        "full_name": "New User",
        "role": "Junior"
    }
    response = await async_client.post("/api/auth/signup", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["role"] == "Junior"
    # Verify in database
    user = db_session.query(models.User).filter_by(email=payload["email"]).first()
    assert user is not None

@pytest.mark.asyncio
async def test_signup_existing_email_returns_400(async_client: AsyncClient, db_session: Session):
    existing_user = models.User(
        email="existing@example.com",
        hashed_password="$2b$12$abcdefghijklmnopqrstuv",
        full_name="Existing User",
        role="Junior"
    )
    db_session.add(existing_user)
    db_session.commit()

    payload = {
        "email": "existing@example.com",
        "password": "password123",
        "full_name": "Existing User",
        "role": "Junior"
    }
    response = await async_client.post("/api/auth/signup", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, db_session: Session):
    from api.auth import hash_password
    hashed_pw = hash_password("testpassword")
    user = models.User(
        email="loginuser@example.com",
        hashed_password=hashed_pw,
        full_name="Login User",
        role="Junior"
    )
    db_session.add(user)
    db_session.commit()

    payload = {
        "email": "loginuser@example.com",
        "password": "testpassword"
    }
    response = await async_client.post("/api/auth/login", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "loginuser@example.com"
    assert data["role"] == "Junior"

@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient, db_session: Session):
    from api.auth import hash_password
    user = models.User(
        email="wrongpass@example.com",
        hashed_password=hash_password("correctpassword"),
        full_name="Wrong Pass User",
        role="Junior"
    )
    db_session.add(user)
    db_session.commit()

    payload = {
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    response = await async_client.post("/api/auth/login", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client: AsyncClient):
    payload = {
        "email": "nonexistent@example.com",
        "password": "doesnotmatter"
    }
    response = await async_client.post("/api/auth/login", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"
