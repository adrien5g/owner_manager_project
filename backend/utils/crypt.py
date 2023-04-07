from functools import cache
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

argon = PasswordHasher()

def crypt_password(password: str) -> str:
    encrypted_password = argon.hash(password)
    return encrypted_password

@cache
def verify_password(hash: str, password: str) -> bool:
    try:
        argon.verify(hash, password)
    except VerifyMismatchError:
        return False
    return True
