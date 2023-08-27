import secrets
import string


def generate_invitation_code(length=6):
    characters = string.ascii_letters + string.digits
    invitation_code = ''.join(secrets.choice(characters) for _ in range(length))
    return invitation_code


def generate_session_id(length=15):
    characters = string.ascii_letters + string.digits
    session_id = ''.join(secrets.choice(characters) for _ in range(length))
    return session_id
