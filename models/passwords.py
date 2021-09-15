import bcrypt

def convert_secure_password(password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return password_hash

def check_password(password, password_hash):
    valid = bcrypt.checkpw(password.encode(), password_hash.encode())
    return valid