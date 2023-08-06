import hashlib

__default_secret_key = "'Opet-CmS_SecKey$~"


def hash_password(password: str, salt: str | None = None):
    if not salt:
        salt = __default_secret_key
    string = f"{salt}{password}".encode()
    hashed_password = hashlib.sha512(string).hexdigest()
    return hashed_password


p = hash_password("1234@QweR", "dsfsd")
print(p)
