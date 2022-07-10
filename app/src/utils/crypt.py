from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(hashed_pw: str, pw: str) -> bool:
    return pwd_context.verify(pw, hashed_pw)
