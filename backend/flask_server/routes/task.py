import json
from flask import Blueprint, request, jsonify
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
        "status": task.status,
        "priority": task.priority,
        "workspaceId": task.workspaceId,
        "workspaceName": workspace.name if workspace else ""
    }

@task_bp.route("/tasks")
def all_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/api/tasks")
def api_all_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/api/workspaces/<int:workspace_id>/tasks")
def workspace_tasks(workspace_id):
    tasks = Task.query.filter_by(workspaceId=workspace_id).all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/addtask", methods=["POST"])
def add_task():
    data = request.json
    if not data.get("workspaceId"):
        return jsonify({"error": "Le projet est requis pour creer une tache"}), 400
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
        workspaceId=data.get("workspaceId")
    )
    return jsonify({"id": task.id, "task": task_to_dict(task), "message": "Task added"})

@task_bp.route("/task/<int:task_id>")
def task_info(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task_to_dict(task))

@task_bp.route("/task/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.json
    task = Task.update_task(task_id, **data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task_to_dict(task))
