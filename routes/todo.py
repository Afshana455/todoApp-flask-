from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.todo import create_todo,get_todos,get_todo, update_todo, delete_todo
todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"message":"Request body is required"}),400
    title = data.get("title")
    description = data.get("description")
    if not title:
        return jsonify({"message": "Title is required" }), 400
    title = title.strip()
    if not title:
        return jsonify({"message": "Title cannot be empty"}),400
    if len(title) > 200:
        return jsonify({"message":"Title cannot exceed 200 characters"}),400
    todo_id = create_todo(user_id, title, description)

    return jsonify({"message": "Todo created successfully","todo_id": todo_id}), 201

@todo_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    user_id = get_jwt_identity()
    search = request.args.get("search","").strip()
    todos = get_todos(user_id,search)
    return jsonify({"todos": todos}), 200

@todo_bp.route("/<int:todo_id>", methods=["GET"])
@jwt_required()
def get_one(todo_id):
    user_id = get_jwt_identity()
    todo = get_todo(todo_id, user_id)
    if not todo:
        return jsonify({"message": "Todo not found"}), 404
    return jsonify({ "todo": todo}), 200

@todo_bp.route("/<int:todo_id>", methods=["PUT"])
@jwt_required()
def update(todo_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"message":"Request body is required"}),400
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed")
    if not title:
        return jsonify({ "message": "Title is required"}), 400
    title = title.strip()
    if not title:
        return jsonify({"message": "title cannot be empty"}), 400

    if len(title)>200:
        return jsonify({"message": "Title cannot exceed 200 characters"}),400

    if not isinstance(completed, bool):
        return jsonify({ "message": "Completed must be true or false"}), 400

    if completed is None:
        completed = False

    affected_rows = update_todo( todo_id, user_id, title, description, completed)

    if affected_rows == 0:
        return jsonify({ "message": "Todo not found"}), 404

    return jsonify({"message": "Todo updated successfully" }), 200

@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete(todo_id):
    user_id = get_jwt_identity()
    affected_rows = delete_todo(todo_id,user_id)

    if affected_rows == 0:
        return jsonify({"message": "Todo not found"}), 404

    return jsonify({"message": "Todo deleted successfully" }), 200