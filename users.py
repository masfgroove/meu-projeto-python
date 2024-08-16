from werkzeug.security import generate_password_hash, check_password_hash

users = {
    "admin": generate_password_hash("admin123")
}

def validate_user(username, password):
    if username in users:
        return check_password_hash(users[username], password)
    return False
