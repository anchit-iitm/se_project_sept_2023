from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required


register_user_schema = {
    "type": "object",
    "properties": {
        "name": { 
            "type": "string",
            "minLength": 5,
            "maxLength": 55
            },
        "email": {
            "type": "string",
            "maxLength": 55
            },
        "password": {
            "type": "string", 
            "minLength": 5,
            "maxLength": 100
            },
    },
    "required": ["name", "email", "password"]
}


@app.route("/api/v1/user/auth", methods=["POST"])
def login():
    try:
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = User.get_user_by_email(email)

        if user:
            if user.check_password(password):                
                return jsonify(
                auth={
                    "message":"Login Successful",
                    "authToken": create_access_token(identity=user.id, additional_claims={"role": user.role[0].role})
                    },
                profile= {
                    "name": user.name,
                    "email": user.email,
                    "role": user.role[0].role
                }), 200
        
        return show_400("Bad username or Password")
    except:
        app.logger.exception("API_LOGIN: Error occurred")
        return show_500()

@app.route("/api/v1/user/auth/register", methods=["POST"])
@expects_json(register_user_schema)
def register():
    try:
        name = request.json.get("name", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = User.get_user_by_email(email)

        if user == None:
            new_user = User(name=name, email=email)
            new_user.role.append(Role.stu_role())
            new_user.set_password(password)
            new_user.save()            
            return jsonify(                
                        message="User Created",
                        authToken= create_access_token(identity=new_user.id, additional_claims={"role": new_user.role[0].role})
                    ), 201
        else:
            return show_400('email already exists')
    except:
        db.session.rollback()
        app.logger.exception("API_REGISTER: Error occurred")
        return show_500()
    

@app.route('/api/v1/test', methods=['GET'])
@role_required('student')
def abcd():
    return jsonify(name="HI")