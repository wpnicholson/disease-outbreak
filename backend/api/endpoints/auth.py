"""User authentication endpoints for signup and login.

Raises:
    HTTPException:
    HTTPException: _description_
    HTTPException: _description_

Returns:
    dict: Mock access token for the user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api import models, schemas
from api.dependencies import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# POST /api/auth/signup
# -------------------------------
@router.post(
    "/signup",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User successfully created"},
        400: {"description": "Email already registered"},
    },
    summary="User Signup",
    description="Create a new user account.",
    response_description="The newly created user account.",
)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user account.

    Args:
        user_data (schemas.UserCreate): User data for signup.
        db (Session, optional): Database session dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the email is already registered.

    Returns:
        schemas.UserRead: The newly created user account.
    """
    # Check if user already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == user_data.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = hash_password(user_data.password)

    # Create user
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_pw,
        full_name=user_data.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------------
# POST /api/auth/login
# -------------------------------
@router.post(
    "/login",
    responses={
        200: {"description": "User successfully logged in"},
        401: {"description": "Invalid credentials"},
    },
    summary="User Login",
    description="Authenticate user and return access token.",
    response_description="Access token for the user.",
)
def login(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Authenticate user and return access token.

    Args:
        user_data (schemas.UserCreate): User data for login, including email and password.
        db (Session, optional): Database session dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user does not exist or the password is incorrect.
        HTTPException: If the credentials are invalid.

    Returns:
        dict: Mock access token for the user.
    """
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Note: Replace this with real JWT token logic
    return {"access_token": f"mock-token-for-{user.email}", "token_type": "bearer"}
