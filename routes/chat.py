from flask import Blueprint, jsonify, request
from service.user_service import UserService
from dotenv import load_dotenv
from groq import Groq
import os

# Load environment variables from .env file
load_dotenv()

chat = Blueprint("chat", __name__, url_prefix="/api/v1/chat")
API_KEY = os.getenv('API_KEY')

# Function to check API key in headers
def check_api_key():
    if 'x-api-key' not in request.headers or request.headers['x-api-key'] != API_KEY:
        return False
    return True


@chat.route("", methods=["POST"])
def post_chat():
    # Check API key
    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    json_data = request.json
    user_id = json_data.get("user_id")
    chat    = json_data.get("msg")
    if not user_id or not chat:
        return jsonify({"message": 'Required parameters are missing'}), 422

    user_result = UserService.get_user_by_id(
        user_id=user_id
    )    
    
    if user_result:
        try:
            client = Groq(
                api_key=os.environ.get("GROQ_API_KEY"),
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": str(chat),
                    }
                ],
                model=os.environ.get("model"),
            )
            return jsonify({"response":str(chat_completion.choices[0].message.content)}), 200  
        except Exception as  e:
            return jsonify({"error": "Conflict", "error_message": "LLM backend Server error"}), 409  
    else: 
        return jsonify({"error": "Conflict", "error_message": "User invalid"}), 403       