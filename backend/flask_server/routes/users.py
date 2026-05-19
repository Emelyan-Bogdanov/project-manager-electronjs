import json
from flask import Blueprint, request, jsonify
from ..modules import User

users_bp = Blueprint("users",__name__)

def serialize_user(user):
    try:
        tags = json.loads(user.tags or "[]")
    except json.JSONDecodeError:
        tags = []
    return {
        "id": user.id,
        "name": user.name or user.username,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar or "",
        "tags": tags,
        "location": user.location or "",
    }


@users_bp.route("/users")
def allUsers():
    # get all users
    users = User.query.all()
    
    return jsonify([serialize_user(user) for user in users])        

@users_bp.route("/api/users")
def api_all_users():
    users = User.query.all()
    return jsonify([serialize_user(user) for user in users])
    



# how many users are in the app
@users_bp.route("/howmanyusers")
def getnUser():
    return str(User.query.count())

# delete a user
@users_bp.route("/deleteuser/<userid>")
def deleteUser(userid:int):
    from ..modules import db
    try :
        user = User.query.get(userid)
        db.session.delete(user)
        db.session.commit()
        return f"user {userid} deleted"
    except Exception as e :
        if str(e) == "Class 'builtins.NoneType' is not mapped" :
            return "ERROR : maybe user not found : \n" + str(e)
        return f"ERROR : {str(e)}"



@users_bp.route("/api/users", methods=["POST"])
def add_user():
    data = request.json
    from ..modules import db
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    name = (data.get("name") or username).strip()
    tags = data.get("tags") or []
    if not username or not email or not password:
        return jsonify({"success": False, "error": "Username, email and password are required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "error": "Ce nom d'utilisateur est deja pris"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "error": "Cet email est deja utilise"}), 409
    try:
        user = User(
            name=name,
            username=username,
            email=email,
            password=password,
            avatar=data.get("avatar") or "",
            tags=json.dumps(tags if isinstance(tags, list) else []),
            location=data.get("location") or "",
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User created", "user": serialize_user(user)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@users_bp.route("/api/users/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    data = request.json or {}
    from ..modules import db
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    username = data.get("username")
    email = data.get("email")
    if username and User.query.filter(User.id != user_id, User.username == username).first():
        return jsonify({"success": False, "error": "Ce nom d'utilisateur est deja pris"}), 409
    if email and User.query.filter(User.id != user_id, User.email == email).first():
        return jsonify({"success": False, "error": "Cet email est deja utilise"}), 409
    try:
        for field in ["name", "username", "email", "avatar", "location"]:
            if field in data:
                setattr(user, field, (data.get(field) or "").strip() if field != "avatar" else data.get(field) or "")
        if "tags" in data:
            tags = data.get("tags") or []
            user.tags = json.dumps(tags if isinstance(tags, list) else [])
        db.session.commit()
        return jsonify({"success": True, "message": "User updated", "user": serialize_user(user)})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 400

@users_bp.route("/api/users/<int:user_id>/stats")
def user_stats(user_id):
    from ..modules import Workspace, Task, FileEntry, WorkspaceMember
    ws_as_owner = Workspace.query.filter_by(ownerId=user_id).count()
    member_rows = WorkspaceMember.query.filter_by(userId=user_id).all()
    ws_ids = [r.workspaceId for r in member_rows]
    ws_joined = len(ws_ids)
    tasks_created = Task.query.filter_by(authorId=user_id).count()
    files_uploaded = FileEntry.query.filter_by(uploaded_by=user_id).count()
    ws_with_tasks = set(t.workspaceId for t in Task.query.filter(Task.authorId == user_id, Task.workspaceId.isnot(None)).all())
    avg_tasks = round(tasks_created / len(ws_with_tasks), 1) if ws_with_tasks else 0
    return jsonify({
        "projectsCreated": ws_as_owner,
        "projectsJoined": ws_joined,
        "tasksCreated": tasks_created,
        "avgTasksPerProject": avg_tasks,
        "filesUploaded": files_uploaded,
        "totalProjects": len(set(list(ws_with_tasks) + [r.workspaceId for r in WorkspaceMember.query.filter_by(userId=user_id).all()]))
    })

@users_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"success": False, "error": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    return jsonify({"success": True, "user": serialize_user(user)})
