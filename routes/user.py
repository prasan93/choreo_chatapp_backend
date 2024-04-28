from flask import Blueprint, jsonify, request, Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_required, create_refresh_token,
    get_jwt_identity
)
import os
from dotenv import load_dotenv
from service.user_service import UserService
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

user = Blueprint("user", __name__, url_prefix="/api/v1/user")

# Define your API key here
API_KEY = os.getenv('API_KEY')
ACCESS_TOKEN_EXPIRATION = timedelta(minutes=1)
REFRESH_TOKEN_EXPIRATION = timedelta(days=2)

# Function to check API key in headers
def check_api_key():
    if 'x-api-key' not in request.headers or request.headers['x-api-key'] != API_KEY:
        return False
    return True

@user.route("", methods=["POST"])
def add_user():
    # Check API key
    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    json_data = request.json
    required_fields = ["fullname", "user_name", "email", "password"]
    missing_fields = [field for field in required_fields if field not in json_data]
    if missing_fields:
        return jsonify({"message": f'Required parameter "{missing_fields[0]}" is missing'}), 422
    try:
        user_result = UserService.create_new_user_record(
            json_data["fullname"],
            json_data["user_name"],
            json_data["email"],
            json_data["password"],
        )
        # Convert User object to dictionary
        user_dict = user_result.__dict__
        # Remove password from the response for security reasons
        user_dict.pop('password', None)
        return jsonify({"data": "success"}), 200
    except IntegrityError as e:
        error_message = str(e.orig)
        return jsonify({"error": "Conflict", "error_message": error_message}), 409


@user.route("/get", methods=["POST"])
def get_user_by_id():
    # Check API key
    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    json_data = request.json
    user_id = json_data.get("user_id")
    if not user_id:
        return jsonify({"message": 'Required parameter "user_id" is missing'}), 422

    user_result = UserService.get_user_by_id(
        user_id=user_id
    )
    return jsonify({"data": user_result}), 200


@user.route("/by-credentials", methods=["POST"])
def get_user_by_username_password():
    # Check API key
    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    json_data = request.json
    user_name = json_data.get("user_name")
    if not user_name:
        return jsonify({"message": 'Required parameter "user_name" is missing'}), 422
    password = json_data.get("password")
    if not password:
        return jsonify({"message": 'Required parameter "password" is missing'}), 422

    try:
        user_result = UserService.get_user_by_credentials(
            user_name=user_name,
            password=password
        )
        
        if user_result:
            access_token = create_access_token(identity=user_name, expires_delta=ACCESS_TOKEN_EXPIRATION)
            refresh_token = create_refresh_token(identity=user_name, expires_delta=REFRESH_TOKEN_EXPIRATION)
            # user_id = user_result.id
            return jsonify({'access_token':access_token,'refresh_token':refresh_token,'user_id':user_result['id']}), 200
        else:
            return jsonify({"message": "No user available"}), 404
    except:
        return jsonify({"message": "Internal Error"}), 500    
    
    
# Endpoint to refresh access token
@user.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200
