import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from routes.todo import todo_bp
from routes.auth import auth_bp
from datetime import timedelta

load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("jwt_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=20)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=2)
jwt = JWTManager(app)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(todo_bp, url_prefix="/todos")


@app.route("/")
def home():
    return "Flask server is running!"

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)