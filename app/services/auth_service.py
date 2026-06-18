from sqlalchemy.orm import Session
from app.models.user import User

# -------------------------
# REGISTERING USER 
# -------------------------
def register_user_service(
        db: Session,
        username: str,
        email: str, 
        password: str
    ):
        user = User(
            username=username,
            email=email,
            password_hash=password #temperoary
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user