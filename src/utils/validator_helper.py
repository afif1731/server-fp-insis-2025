import re
from src.middleware.custom_error import CustomError

def validate_email(email: str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email) is None:
        raise CustomError(422, 'email tidak valid')
    return email