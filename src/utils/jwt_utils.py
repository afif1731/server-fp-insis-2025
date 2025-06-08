from src.config.jwt_config import JWT
from src.middleware.custom_error import CustomError
import time
import jwt

def jwt_encode(payload):
    new_payload = {
        'exp': time.time() + JWT['duration'],
        'data': payload
    }
    return jwt.encode(payload=new_payload, key=JWT['secret'], algorithm=JWT['method'])

def jwt_verify(token):
    try:
        decoded_token = jwt.decode(jwt=token, key=JWT['secret'], algorithms=JWT['method'], options={'verify_exp': True}, verify=True)
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise CustomError(401, 'expired token')
    except jwt.InvalidTokenError:
        raise CustomError(401, 'invalid token')