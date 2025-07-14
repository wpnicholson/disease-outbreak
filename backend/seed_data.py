from api.sample_data import create_sample_data
from api.database import SessionLocal
from api.models import User


def seed():
    db = SessionLocal()

    # Ensure there's at least one user to attach reports to
    user = db.query(User).filter(User.email == "seeduser@example.com").first()
    if not user:
        user = User(
            email="seeduser@example.com",
            hashed_password="fakehashed",  # No auth validation in seed
            full_name="Seed User",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    create_sample_data(db, user.id)
    print("✅ Sample data seeded successfully.")
    db.close()


if __name__ == "__main__":
    seed()
