"""User authentication endpoints for signup and login.

Raises:
    HTTPException:
    HTTPException: _description_
    HTTPException: _description_

Returns:
    dict: Mock access token for the user.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api import models, schemas
from api.dependencies import get_db
from api.enums import UserRoleEnum

from jose import jwt

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token.

    Args:
        data (dict): Data to encode in the token.
        expires_delta (timedelta | None, optional): Expiration time for the token. Defaults to None.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password (str): plain password to verify.
        hashed_password (str): Hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
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
def signup(user_data: schemas.UserSignup, db: Session = Depends(get_db)):
    """Create a new user account.

    All fields are required. The `role` defaults to `junior` if not provided.

    Args:
        user_data (schemas.UserSignup): User data for signup.
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

    # Hash password.
    hashed_pw = hash_password(user_data.password)

    # Create user.
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_pw,
        full_name=user_data.full_name,
        role=user_data.role
        or UserRoleEnum.junior,  # Default to junior role if not provided.
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
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token.

    You only need to provide email and password. The role is not required for login.

    Args:
        user_data (schemas.UserLogin): User data for login, including email and password.
        db (Session, optional): Database session dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user does not exist or the password is incorrect.
        HTTPException: If the credentials are invalid.

    Returns:
        dict: Mock access token for the user.
    """
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    user_read = schemas.UserRead.model_validate(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_read.model_dump_json(exclude={"hashed_password"}),
    }
