from app.database import SessionLocal
from app.models import Users, Role
from app.security import hash_password
from app.config import settings

db = SessionLocal()
try:
    admin = db.query(Users).filter(Users.role == Role.admin).first()
    if not admin:
        admin = Users(
            name=settings.ADMIN_USER,
            email=settings.ADMIN_EMAIL.lower(),
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role=Role.admin,
        )
        db.add(admin)
        db.commit()
finally:
    db.close()
    