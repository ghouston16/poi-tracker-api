from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash(password: str):
    return pwd_context.hash(password)


# Check hashed password and return True or False
def check(plain_password, hashed_passord):
    return pwd_context.verify(plain_password, hashed_passord)
