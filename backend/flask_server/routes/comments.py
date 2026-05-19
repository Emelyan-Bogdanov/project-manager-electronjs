from datetime import datetime
from flask import Blueprint, request, jsonify
from ..modules import Comment, User, Task, db

comments_bp = Blueprint("comments", __name__)

@comments_bp.route("/api/tasks/<int:task_id>/comments", methods=["GET"])
def list_comments(task_id):
    comments = Comment.query.filter_by(taskId=task_id).order_by(Comment.id.asc()).all()
    result = []
    for c in comments:
        u = User.query.get(c.userId)
        result.append({
            "id": c.id,
            "taskId": c.taskId,
            "userId": c.userId,
            "userName": (u.name or u.username) if u else "Inconnu",
            "userAvatar": u.avatar if u else "",
            "text": c.text,
            "created_at": c.created_at
        })
    return jsonify(result)

@comments_bp.route("/api/tasks/<int:task_id>/comments", methods=["POST"])
def add_comment(task_id):
    data = request.json or {}
    user_id = data.get("userId")
    text = (data.get("text") or "").strip()
    if not user_id:
        return jsonify({"error": "userId requis"}), 400
    if not text:
        return jsonify({"error": "Le commentaire ne peut pas etre vide"}), 400
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tache introuvable"}), 404
    Comment.add(task_id, user_id, text)
    db.session.commit()
    task = Task.query.get(task_id)
    return jsonify({"success": True, "message": "Commentaire ajoute", "comments": task.comments or 0})
