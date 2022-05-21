from passlib.context import CryptContext

hashing_function = CryptContext( schemes=['bcrypt'], deprecated="auto")


def hash_function(password: str):
    return hashing_function.hash(password)
