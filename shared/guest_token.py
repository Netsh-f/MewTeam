"""
============================
# @Time    : 2023/8/27 13:48
# @Author  : Elaikona
# @FileName: guest_token.py
===========================
"""

from cryptography.fernet import Fernet
from datetime import datetime, timedelta

SECRET_KEY = Fernet.generate_key()

print(SECRET_KEY)


def encrypt_data(data):
    fernet = Fernet(SECRET_KEY)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data):
    fernet = Fernet(SECRET_KEY)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data


# 生成加密的Token
def generate_encrypted_token(document_id, edit_permission, expiration_days):
    expiration_date = datetime.utcnow() + timedelta(days=expiration_days)
    data = f"{document_id}:{edit_permission}:{expiration_date.timestamp()}"
    encrypted_data = encrypt_data(data)
    return encrypted_data


# 验证并解析Token
def validate_and_parse_token(token):
    try:
        decrypted_data = decrypt_data(token)
        document_id, edit_permission, expiration_timestamp = decrypted_data.split(':')
        current_time = datetime.utcnow().timestamp()
        if float(expiration_timestamp) < current_time:
            # Token已过期
            return None
        return {
            'document_id': int(document_id),
            'edit_permission': edit_permission == 'True',
            'expiration_date': datetime.fromtimestamp(float(expiration_timestamp))
        }
    except Exception as e:
        # Token无效或解析错误
        return None


expiration_days = 7
document_id = 123
edit_permission = True

token = generate_encrypted_token(document_id, edit_permission, expiration_days)
print("Generated Token:", token)

parsed_data = validate_and_parse_token(token)
if parsed_data:
    print("Valid Token:", parsed_data)
else:
    print("Invalid Token")

