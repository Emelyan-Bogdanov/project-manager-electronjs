from flask import Blueprint, request, jsonify
from ..modules import Workspace, db

workspace_bp = Blueprint("workspaces", __name__)

@workspace_bp.route("/workspaces")
def allWorkspaces():
    workspaces = Workspace.query.all()
    return jsonify([{
        "id": workspace.id,
        "name": workspace.name,
        "description": workspace.description,
        "iconPath": workspace.iconPath
    } for workspace in workspaces])

@workspace_bp.route("/addworkspace", methods=["POST"])
def add_workspace():
    data = request.json
    workspace = Workspace.add_workspace(
        name=data.get("name"),
        description=data.get("description"),
        iconPath=data.get("iconPath", "[NO IMAGE]")
    )
    return jsonify({"id": workspace.id, "message": "Workspace added"})

@workspace_bp.route("/workspace/<int:workspace_id>")
def workspace_info(workspace_id):
    workspace = Workspace.get_workspace(workspace_id)
    if workspace:
        return jsonify({
            "id": workspace.id,
            "name": workspace.name,
            "description": workspace.description,
            "iconPath": workspace.iconPath
        })
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
    Workspace.delete_workspace(workspace_id)
    return jsonify({"message": "Workspace deleted"})
