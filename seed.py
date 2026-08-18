"""
Fuel4Exam - Seed data for database initialization
Works with the existing database schema
"""
import logging
from app.core.config import settings
from app.db.session import SessionLocal, init_db
from app.db.models import User, UserProfile, Role
from app.core.security import hash_password

logger = logging.getLogger(__name__)


def seed_database():
    """Seed database with initial data"""
    init_db()
    
    db = SessionLocal()
    try:
        # Check if roles exist, create if needed
        student_role = db.query(Role).filter(Role.role_id == 1).first()
        if not student_role:
            student_role = Role(role_id=1, role_code="student", description="Student role")
            db.add(student_role)
        
        instructor_role = db.query(Role).filter(Role.role_id == 2).first()
        if not instructor_role:
            instructor_role = Role(role_id=2, role_code="instructor", description="Instructor role")
            db.add(instructor_role)
        
        admin_role = db.query(Role).filter(Role.role_id == 3).first()
        if not admin_role:
            admin_role = Role(role_id=3, role_code="admin", description="Administrator role")
            db.add(admin_role)
        
        db.commit()
        logger.info("Roles initialized")
        
        # Check if database is already seeded
        existing_admin = db.query(User).filter(User.role_id == 3).first()
        if existing_admin:
            logger.info("Database already seeded")
            return
        
        # Create admin user
        admin_user = User(
            full_name="Administrator",
            email="admin@fuel4exam.com",
            phone="+1-555-0001",
            password_hash=hash_password("admin@123456"),
            role_id=3,
            is_active=True,
            is_email_verified=True,
        )
        db.add(admin_user)
        db.flush()  # Get the user_id
        
        admin_profile = UserProfile(
            user_id=admin_user.user_id,
            city="New York",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=admin",
            bio="System administrator"
        )
        db.add(admin_profile)
        
        # Create sample instructor
        instructor_user = User(
            full_name="John Instructor",
            email="instructor@fuel4exam.com",
            phone="+1-555-0002",
            password_hash=hash_password("instructor@123456"),
            role_id=2,
            is_active=True,
            is_email_verified=True,
        )
        db.add(instructor_user)
        db.flush()
        
        instructor_profile = UserProfile(
            user_id=instructor_user.user_id,
            city="Boston",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=instructor",
            bio="Experienced exam instructor"
        )
        db.add(instructor_profile)
        
        # Create sample student
        student_user = User(
            full_name="Jane Student",
            email="student@fuel4exam.com",
            phone="+1-555-0003",
            password_hash=hash_password("student@123456"),
            role_id=1,
            is_active=True,
            is_email_verified=True,
        )
        db.add(student_user)
        db.flush()
        
        student_profile = UserProfile(
            user_id=student_user.user_id,
            city="San Francisco",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=student",
            bio="Exam preparation student"
        )
        db.add(student_profile)
        
        db.commit()
        
        logger.info("Database seeded successfully with sample users")
        logger.info(f"Admin User: admin@fuel4exam.com / admin@123456 (Role ID: 3)")
        logger.info(f"Instructor User: instructor@fuel4exam.com / instructor@123456 (Role ID: 2)")
        logger.info(f"Student User: student@fuel4exam.com / student@123456 (Role ID: 1)")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_database()
