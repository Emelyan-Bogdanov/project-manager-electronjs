import json
from flask import Blueprint, request, jsonify
from ..modules import Task, User, db

task_bp = Blueprint("tasks", __name__)

def parse_tags(tags_raw):
    if not tags_raw:
        return []
    if isinstance(tags_raw, list):
        return tags_raw
    try:
        return json.loads(tags_raw)
    except (json.JSONDecodeError, TypeError):
        try:
            return eval(tags_raw)
        except:
            return [tags_raw]

def task_to_dict(task):
    author = User.query.get(task.authorId) if task.authorId else None
    return {
        "id": task.id,
        "title": task.title,
        "tags": parse_tags(task.tags),
        "deadline": task.deadline,
        "authorId": task.authorId,
        "authorName": author.username if author else "Utilisateur",
        "status": task.status,
        "priority": task.priority
    }

@task_bp.route("/tasks")
def all_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/api/tasks")
def api_all_tasks():
    tasks = Task.query.all()
    return jsonify([task_to_dict(t) for t in tasks])

@task_bp.route("/addtask", methods=["POST"])
def add_task():
    data = request.json
    task = Task.add_task(
        title=data.get("title"),
        tags=data.get("tags"),
        deadline=data.get("deadline"),
        authorId=data.get("authorId"),
        images=data.get("images", ""),
        priority=data.get("priority", 1),
        status=data.get("status", "todo")
    )
    return jsonify({"id": task.id, "message": "Task added"})

@task_bp.route("/task/<int:task_id>")
def task_info(task_id):
    # try to find the task
    try :
        task = Task.query.get(task_id)
        return {
            "id":task.id,
            "title":task.title,
            "tags" : task.tags,
            "views" : task.views,
            "comments" : task.comments,
            "deadline" : task.deadline,
            "authorId" : task.authorId,
            "images" : task.images, # remember to convert to array using json loadString
        }
    except :
        print("ERROR WHILE GETTING THE TASK INFO USING ITS ID")
        return {
            "id":"ERROR",
            "title":"ERROR",
            "tags" :"ERROR",
            "views" :"ERROR",
            "comments" :"ERROR",
            "deadline" :"ERROR",
            "authorId" :"ERROR",
            "images" :"ERROR",
        }
