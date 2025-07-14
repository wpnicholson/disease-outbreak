from typing import Optional
from api.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from api.enums import UserRoleEnum
from api import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = "your_secret_here"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise credentials_exception
    return user


def senior_required(user: models.User = Depends(get_current_user)):
    if user.role != UserRoleEnum.senior:
        raise HTTPException(status_code=403, detail="Access forbidden for your role")
    return user
