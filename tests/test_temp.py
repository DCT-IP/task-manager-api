from app.core.security import hash_pswd, verify_pswd

def test_password_hash():
    pw = "Password123!"
    hashed = hash_pswd(pw)

    print(hashed)
    print(verify_pswd(pw, hashed))

    assert verify_pswd(pw, hashed)