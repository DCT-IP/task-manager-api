from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

def hash_pswd(password: str) -> str:
    pre_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(pre_hashed)

def verify_pswd(
        plain_pswd: str,
        hashed_pswd: str
) -> bool:
    pre_hashed = hashlib.sha256(plain_pswd.encode('utf-8')).hexdigest()
    return pwd_context.verify(pre_hashed, hashed_pswd)