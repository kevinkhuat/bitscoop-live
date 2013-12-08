import hashlib
import uuid


def get_auth_str(password):
    salt = uuid.uuid4().hex

    return gen_auth(password, salt)


def check_auth_str(password, salt, auth_str):
    hash = gen_auth(password, salt)

    return hash['auth_str'] == auth_str


def gen_auth(password, salt):
    digest = hashlib.sha512(password + salt).hexdigest()
    maxlen = max(len(password), len(salt), len(digest))
    mondo = ''
    for n in range(maxlen):
        mondo += password[n % len(password)] + salt[n % len(salt)] + digest[n % len(digest)]

    auth_str = hashlib.sha512(mondo + salt).hexdigest()

    return {
        'salt': salt,
        'auth_str': auth_str
    }