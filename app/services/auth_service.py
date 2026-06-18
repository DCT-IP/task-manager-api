from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_pswd, verify_pswd
from fastapi import HTTPException

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


# -------------------------
# Logging in  USER 
# -------------------------
def login_user_service(
        db: Session,
        username: str, 
        password: str
): 
        user = (
                db.query(User)
                .filter(User.username == username)
                .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_pswd(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")

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