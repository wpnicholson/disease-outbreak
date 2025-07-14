import os
from api.sample_data import create_sample_data
from api.database import SessionLocal
from api.models import User
from api.enums import UserRoleEnum
from api.endpoints.auth import hash_password
from dotenv import load_dotenv


def seed():
    load_dotenv()

    junior_password: str | None = os.getenv("JUNIOR_PASSWORD")
    senior_password: str | None = os.getenv("SENIOR_PASSWORD")

    if not junior_password or not senior_password:
        raise ValueError(
            "JUNIOR_PASSWORD and SENIOR_PASSWORD must be set as environment variables."
        )

    db = SessionLocal()

    # Seed junior user
    junior_email = "junior@example.com"
    junior_user = db.query(User).filter(User.email == junior_email).first()
    if not junior_user:
        junior_user = User(
            email=junior_email,
            hashed_password=hash_password(junior_password),
            full_name="Junior User",
            role=UserRoleEnum.junior,
        )
        db.add(junior_user)
        db.commit()
        db.refresh(junior_user)
        print(f"Created junior user: {junior_email}")

    # Seed senior user
    senior_email = "senior@example.com"
    senior_user = db.query(User).filter(User.email == senior_email).first()
    if not senior_user:
        senior_user = User(
            email=senior_email,
            hashed_password=hash_password(senior_password),
            full_name="Senior User",
            role=UserRoleEnum.senior,
        )
        db.add(senior_user)
        db.commit()
        db.refresh(senior_user)
        print(f"Created senior user: {senior_email}")

    # Create sample data with the junior user.
    create_sample_data(db, junior_user.id)

    print("Sample data seeded successfully.")
    db.close()


if __name__ == "__main__":
    seed()
