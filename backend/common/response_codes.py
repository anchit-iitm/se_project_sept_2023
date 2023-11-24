from flask import jsonify, make_response
from jsonschema import ValidationError
from flask import current_app as app

def show_200(message="success"):
        return make_response(jsonify({"message": message, "status": "success"}), 200)

def show_404(message = "The requested resource was not found on this server"):
    return make_response(jsonify({"message": message, "status": "error"}), 404)

def show_500():
    return make_response(jsonify({"message": "Internal server error occurred", "status": "error"}), 500)

def show_400(message = "Bad Request sent"):
    return make_response(jsonify({"message": message, "status": "error"}), 400)

def show_403(message = "Access Denied"):
    return make_response(jsonify({"message": message, "status": "error"}), 400)

def show_401(message = "Bad data sent"):
    return make_response(jsonify({"message": message, "status": "error"}), 401)

def show_201(message="created"):
    return make_response(jsonify({"message": message, "status": "success"}), 201)

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'message': original_error.message, "status": "error"}), 400)
    return error