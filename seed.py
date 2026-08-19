"""Seed a candidate account using an existing candidate role."""
import logging
from app.core.config import settings
from app.db.session import SessionLocal, init_db
from app.db.models import User, UserProfile, Role
from app.core.security import hash_password

logger = logging.getLogger(__name__)


def seed_database():
    """Seed database with initial data"""
    if not settings.seed_candidate_password:
        raise RuntimeError("Missing SEED_CANDIDATE_PASSWORD in .env")

    init_db()
    
    db = SessionLocal()
    try:
        candidate_role = db.query(Role).filter(Role.role_code == "candidate").first()
        if not candidate_role:
            raise RuntimeError(
                "Candidate role is not configured in the database; "
                "create it through your database migration or admin process."
            )

        candidate_email = "candidate@fuel4exam.com"
        existing_candidate = db.query(User).filter(User.email == candidate_email).first()
        if existing_candidate:
            logger.info("Candidate seed account already exists")
            return

        candidate_user = User(
            full_name="Fuel4Exam Candidate",
            email=candidate_email,
            password_hash=hash_password(settings.seed_candidate_password),
            role_id=candidate_role.role_id,
            is_active=True,
            is_email_verified=True,
        )
        db.add(candidate_user)
        db.flush()
        db.add(UserProfile(user_id=candidate_user.user_id))
        db.commit()
        logger.info("Candidate seed account created successfully")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_database()
