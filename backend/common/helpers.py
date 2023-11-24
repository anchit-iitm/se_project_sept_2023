from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from common.response_codes import *


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def role_required(role):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == role:
                return fn(*args, **kwargs)
            else:
                return show_403()
        return decorator
    return wrapper