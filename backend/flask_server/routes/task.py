import json
import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from ..modules import Task, User, Workspace, db

task_bp = Blueprint("tasks", __name__)

def parse_json_field(raw):
    if not raw:
        return []
    if isinstance(raw, list):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return [raw]

def task_to_dict(task):
    author = User.query.get(task.authorId) if task.authorId else None
    workspace = Workspace.query.get(task.workspaceId) if task.workspaceId else None
    return {
        "id": task.id,
        "title": task.title,
        "taskType": task.taskType or "basic",
        "description": task.description or "",
        "tags": parse_json_field(task.tags),
        "urls": parse_json_field(task.urls),
        "images": parse_json_field(task.images),
        "files": parse_json_field(task.files),
        "deadline": task.deadline,
        "authorId": task.authorId,
        "authorName": (author.name or author.username) if author else "Utilisateur",
        "authorUsername": author.username if author else "",
        "authorAvatar": author.avatar if author else "",
        "views": task.views or 0,
        "comments": task.comments or 0,
        "status": task.status,
        "priority": task.priority,
        "workspaceId": task.workspaceId,
        "workspaceName": workspace.name if workspace else "",
        "created_at": task.created_at or "",
        "reminder": task.reminder or ""
    }

@task_bp.route("/tasks")
def all_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/api/tasks")
def api_all_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/api/tasks/upcoming-reminders")
def upcoming_reminders():
    window_minutes = request.args.get("window", 5, type=int)
    now = datetime.now()
    end = now + timedelta(minutes=window_minutes)
    tasks = Task.query.all()
    upcoming = []
    for task in tasks:
        if not task.reminder or task.status == "done":
            continue
        try:
            reminder_time = datetime.strptime(task.reminder, "%Y-%m-%dT%H:%M")
            if now <= reminder_time <= end:
                upcoming.append(task_to_dict(task))
        except ValueError:
            pass
    return jsonify(upcoming)

@task_bp.route("/api/workspaces/<int:workspace_id>/tasks")
def workspace_tasks(workspace_id):
    tasks = Task.query.filter_by(workspaceId=workspace_id).all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/addtask", methods=["POST"])
def add_task():
    data = request.json
    if not data.get("workspaceId"):
        return jsonify({"error": "Le projet est requis pour creer une tache"}), 400
    if not data.get("reminder"):
        return jsonify({"error": "Le rappel est requis pour creer une tache"}), 400
    task = Task.add_task(
        title=data.get("title"),
        tags=data.get("tags"),
        description=data.get("description", ""),
        urls=data.get("urls", "[]"),
        deadline=data.get("deadline"),
        authorId=data.get("authorId"),
        images=data.get("images", "[]"),
        files=data.get("files", "[]"),
        taskType=data.get("taskType", "basic"),
        priority=data.get("priority", 1),
        status=data.get("status", "todo"),
        workspaceId=data.get("workspaceId"),
        reminder=data.get("reminder")
    )
    return jsonify({"id": task.id, "task": task_to_dict(task), "message": "Task added"})

@task_bp.route("/task/<int:task_id>")
def task_info(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task_to_dict(task))

@task_bp.route("/api/tasks/<int:task_id>/view", methods=["POST"])
def increment_view(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task.views = (task.views or 0) + 1
    db.session.commit()
    return jsonify({"success": True, "views": task.views})

@task_bp.route("/api/tasks/<int:task_id>/comments/count", methods=["GET"])
def task_comment_count(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"comments": task.comments or 0, "views": task.views or 0})

@task_bp.route("/task/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.json
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if "images" in data:
        old_images = parse_json_field(task.images)
        new_images = data["images"]
        if isinstance(new_images, str):
            new_images = parse_json_field(new_images)

        def extract_filename(img):
            if isinstance(img, dict):
                return img.get("filename", "")
            if isinstance(img, str):
                return img.rsplit("/", 1)[-1]
            return ""

        old_filenames = set(extract_filename(img) for img in old_images)
        new_filenames = set(extract_filename(img) for img in new_images)
        removed = old_filenames - new_filenames

        images_folder = current_app.config["IMAGES_FOLDER"]
        for fname in removed:
            if fname:
                fpath = os.path.join(images_folder, fname)
                if os.path.exists(fpath):
                    os.remove(fpath)

    task = Task.update_task(task_id, **data)
    return jsonify(task_to_dict(task))

@task_bp.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    data = request.json or {}
    user_id = data.get("userId")
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if not user_id or task.authorId != user_id:
        return jsonify({"error": "Vous n'etes pas autorise a supprimer cette tache"}), 403

    old_images = parse_json_field(task.images)
    images_folder = current_app.config["IMAGES_FOLDER"]
    for img in old_images:
        if isinstance(img, dict):
            fname = img.get("filename", "")
        elif isinstance(img, str):
            fname = img.rsplit("/", 1)[-1]
        else:
            continue
        if fname:
            fpath = os.path.join(images_folder, fname)
            if os.path.exists(fpath):
                os.remove(fpath)

    Task.delete_task(task_id)
    return jsonify({"success": True, "message": "Task deleted"})