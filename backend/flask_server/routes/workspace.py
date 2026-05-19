from flask import Blueprint, request, jsonify
from ..modules import Workspace, WorkspaceMember, JoinRequest, User, Task, db

workspace_bp = Blueprint("workspaces", __name__)

def workspace_to_dict(ws):
    return {
        "id": ws.id,
        "name": ws.name,
        "description": ws.description,
        "iconPath": ws.iconPath,
        "ownerId": ws.ownerId
    }

@workspace_bp.route("/workspaces")
def allWorkspaces():
    workspaces = Workspace.query.all()
    return jsonify([workspace_to_dict(ws) for ws in workspaces])

@workspace_bp.route("/api/workspaces")
def api_all_workspaces():
    workspaces = Workspace.query.all()
    return jsonify([workspace_to_dict(ws) for ws in workspaces])

@workspace_bp.route("/api/workspaces/mine")
def my_workspaces():
    user_id = request.args.get("userId", type=int)
    if not user_id:
        return jsonify([])
    member_rows = WorkspaceMember.query.filter_by(userId=user_id).all()
    ws_ids = [r.workspaceId for r in member_rows]
    workspaces = Workspace.query.filter(Workspace.id.in_(ws_ids)).all() if ws_ids else []
    return jsonify([workspace_to_dict(ws) for ws in workspaces])

@workspace_bp.route("/addworkspace", methods=["POST"])
def add_workspace():
    try:
        data = request.json or {}
        if not data.get("name"):
            return jsonify({"error": "Le nom du projet est requis"}), 400
        workspace = Workspace.add_workspace(
            name=data.get("name"),
            description=data.get("description"),
            iconPath=data.get("iconPath", "[NO IMAGE]"),
            ownerId=data.get("ownerId")
        )
        if data.get("ownerId"):
            WorkspaceMember.add_member(workspace.id, data["ownerId"])
        return jsonify({"id": workspace.id, "message": "Workspace added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@workspace_bp.route("/workspace/<int:workspace_id>")
def workspace_info(workspace_id):
    workspace = Workspace.get_workspace(workspace_id)
    if workspace:
        return jsonify(workspace_to_dict(workspace))
    return jsonify({"error": "Workspace not found"}), 404

@workspace_bp.route("/updateworkspace/<int:workspace_id>", methods=["POST"])
def update_workspace(workspace_id):
    data = request.json
    workspace = Workspace.update_workspace(
        workspace_id,
        name=data.get("name"),
        description=data.get("description"),
        iconPath=data.get("iconPath")
    )
    if workspace:
        return jsonify({"message": "Workspace updated"})
    return jsonify({"error": "Workspace not found"}), 404

@workspace_bp.route("/deleteworkspace/<int:workspace_id>")
def delete_workspace(workspace_id):
    Task.query.filter_by(workspaceId=workspace_id).delete()
    WorkspaceMember.query.filter_by(workspaceId=workspace_id).delete()
    JoinRequest.query.filter_by(workspaceId=workspace_id).delete()
    Workspace.delete_workspace(workspace_id)
    return jsonify({"message": "Workspace deleted"})

# ── Members ──

@workspace_bp.route("/api/workspaces/<int:workspace_id>/members")
def list_members(workspace_id):
    rows = WorkspaceMember.query.filter_by(workspaceId=workspace_id).all()
    users = []
    for r in rows:
        u = User.query.get(r.userId)
        if u:
            users.append({
                "id": u.id,
                "name": u.name or u.username,
                "username": u.username,
                "avatar": u.avatar or ""
            })
    return jsonify(users)

@workspace_bp.route("/api/workspaces/<int:workspace_id>/members", methods=["POST"])
def add_member(workspace_id):
    data = request.json or {}
    user_id = data.get("userId")
    requester_id = data.get("requesterId")
    ws = Workspace.query.get(workspace_id)
    if not ws:
        return jsonify({"error": "Workspace not found"}), 404
    if ws.ownerId != requester_id:
        return jsonify({"error": "Seul le proprietaire peut ajouter des membres"}), 403
    if not user_id:
        return jsonify({"error": "userId requis"}), 400
    WorkspaceMember.add_member(workspace_id, user_id)
    return jsonify({"success": True, "message": "Membre ajoute"})

@workspace_bp.route("/api/workspaces/<int:workspace_id>/members/<int:user_id>", methods=["DELETE"])
def remove_member(workspace_id, user_id):
    requester_id = (request.json or {}).get("requesterId") or request.args.get("requesterId", type=int)
    ws = Workspace.query.get(workspace_id)
    if not ws:
        return jsonify({"error": "Workspace not found"}), 404
    if ws.ownerId != requester_id:
        return jsonify({"error": "Seul le proprietaire peut retirer des membres"}), 403
    WorkspaceMember.remove_member(workspace_id, user_id)
    return jsonify({"success": True, "message": "Membre retire"})

# ── Join Requests ──

@workspace_bp.route("/api/workspaces/<int:workspace_id>/join-requests", methods=["GET"])
def list_join_requests(workspace_id):
    ws = Workspace.query.get(workspace_id)
    if not ws:
        return jsonify({"error": "Workspace not found"}), 404
    requester_id = request.args.get("userId", type=int)
    if ws.ownerId != requester_id:
        return jsonify([])
    rows = JoinRequest.query.filter_by(workspaceId=workspace_id, status="pending").all()
    result = []
    for r in rows:
        u = User.query.get(r.userId)
        result.append({
            "id": r.id,
            "workspaceId": r.workspaceId,
            "userId": r.userId,
            "userName": (u.name or u.username) if u else "Inconnu",
            "userAvatar": u.avatar if u else "",
            "status": r.status,
            "created_at": r.created_at
        })
    return jsonify(result)

@workspace_bp.route("/api/workspaces/<int:workspace_id>/join-requests", methods=["POST"])
def send_join_request(workspace_id):
    data = request.json or {}
    user_id = data.get("userId")
    if not user_id:
        return jsonify({"error": "userId requis"}), 400
    existing = WorkspaceMember.query.filter_by(workspaceId=workspace_id, userId=user_id).first()
    if existing:
        return jsonify({"error": "Vous etes deja membre de ce projet"}), 400
    r = JoinRequest.send(workspace_id, user_id)
    return jsonify({"id": r.id, "status": r.status, "message": "Demande envoyee"})

@workspace_bp.route("/api/join-requests/<int:request_id>/approve", methods=["POST"])
def approve_join_request(request_id):
    data = request.json or {}
    requester_id = data.get("userId")
    r = JoinRequest.query.get(request_id)
    if not r:
        return jsonify({"error": "Demande introuvable"}), 404
    ws = Workspace.query.get(r.workspaceId)
    if ws.ownerId != requester_id:
        return jsonify({"error": "Non autorise"}), 403
    JoinRequest.approve(request_id)
    return jsonify({"success": True, "message": "Demande approuvee"})

@workspace_bp.route("/api/join-requests/<int:request_id>/reject", methods=["POST"])
def reject_join_request(request_id):
    data = request.json or {}
    requester_id = data.get("userId")
    r = JoinRequest.query.get(request_id)
    if not r:
        return jsonify({"error": "Demande introuvable"}), 404
    ws = Workspace.query.get(r.workspaceId)
    if ws.ownerId != requester_id:
        return jsonify({"error": "Non autorise"}), 403
    JoinRequest.reject(request_id)
    return jsonify({"success": True, "message": "Demande rejetee"})

@workspace_bp.route("/api/users/<int:user_id>/join-requests")
def my_join_requests(user_id):
    rows = JoinRequest.query.filter_by(userId=user_id).order_by(JoinRequest.id.desc()).all()
    result = []
    for r in rows:
        ws = Workspace.query.get(r.workspaceId)
        result.append({
            "id": r.id,
            "workspaceId": r.workspaceId,
            "workspaceName": ws.name if ws else "Inconnu",
            "status": r.status,
            "created_at": r.created_at
        })
    return jsonify(result)
