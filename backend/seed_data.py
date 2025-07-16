import os
import uuid
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import User, UserRoleEnum
from api.endpoints.auth import hash_password
from api.sample_data import create_sample_data


def seed():
    """Seed database with initial users and sample data."""
    load_dotenv()
    db: Session = SessionLocal()

    unique_id = str(uuid.uuid4())[:8]

    junior_password = os.getenv("JUNIOR_PASSWORD")
    senior_password = os.getenv("SENIOR_PASSWORD")

    if not junior_password or not senior_password:
        raise ValueError(
            "JUNIOR_PASSWORD and SENIOR_PASSWORD must be set in environment variables."
        )

    # Create Junior User
    junior_email = f"junior-{unique_id}@example.com"
    if not db.query(User).filter_by(email=junior_email).first():
        junior_user = User(
            email=junior_email,
            hashed_password=hash_password(junior_password),
            full_name="Junior Test User",
            role=UserRoleEnum.junior,
        )
        db.add(junior_user)
        db.commit()
        db.refresh(junior_user)
        print(f"Created junior user: {junior_email}")
    else:
        junior_user = db.query(User).filter_by(email=junior_email).first()
        print(f"Junior user {junior_email} already exists, skipping creation.")

    # Create Senior User
    senior_email = f"senior-{unique_id}@example.com"
    if not db.query(User).filter_by(email=senior_email).first():
        senior_user = User(
            email=senior_email,
            hashed_password=hash_password(senior_password),
            full_name="Senior Test User",
            role=UserRoleEnum.senior,
        )
        db.add(senior_user)
        db.commit()
        db.refresh(senior_user)
        print(f"Created senior user: {senior_email}")
    else:
        senior_user = db.query(User).filter_by(email=senior_email).first()
        print(f"Senior user {senior_email} already exists, skipping creation.")

    # Seed sample data with junior user as creator
    create_sample_data(db, created_by_user_id=junior_user.id)  # type: ignore

    print("Sample data seeded successfully.")

    db.close()


if __name__ == "__main__":
    seed()
