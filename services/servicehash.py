from passlib.context import CryptContext

pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd.hash(password)

def verify_password(password_plain,password_hash):
    return pwd.verify(password_plain,password_hash)