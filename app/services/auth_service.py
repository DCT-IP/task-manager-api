from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_pswd
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
            password_hash=hash_pswd(password) #temperoary
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


# post /auth/reg
#      |
#      |
#    route
#      |
#      |
# Auth Service
#      |
#      |
# hash_pswd
#      |
#      |
# bcrypt
#     |
# DB