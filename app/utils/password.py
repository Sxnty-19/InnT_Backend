import bcrypt

def encriptar_password(password: str, rounds: int = 12) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)
