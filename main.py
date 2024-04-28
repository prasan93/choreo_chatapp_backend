from dynaconf import FlaskDynaconf
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from routes.user import user
from routes.chat import chat
from flask_cors import CORS  
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
FlaskDynaconf(app, settings_files=["settings.toml"])

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{app.config['POSTGRES_USER']}:"
    f"{app.config['POSTGRES_PASSWORD']}@"
    f"{app.config['POSTGRES_HOST']}:"
    f"{app.config['POSTGRES_PORT']}/"
    f"{app.config['POSTGRES_DB_NAME']}"
)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)  
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=2)  


db = SQLAlchemy(app)
jwt = JWTManager(app)


app.register_blueprint(user)
app.register_blueprint(chat)
CORS(app, origins=app.config['FRONTEND_URL'])

embedding = None

@app.errorhandler(Exception)
def exceptions(e):
    return jsonify({
        'error': 'Internal Server Error',
        'error_message': str(e)
    }), 500

@app.route("/")
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
        debug=app.config.get("DEBUG"),
    )
