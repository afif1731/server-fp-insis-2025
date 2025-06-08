from src.middleware.custom_error import CustomError

def do_validate(validation, req):
    data = validation.validate_and_return_json_object(req)
    if 'error' in data:
            raise CustomError(422, data['error'])
    return data['data']