from flask import Blueprint
from .modules import User , Workspace , Comment , Task
from flask import jsonify


main_bp = Blueprint("main",__name__)

@main_bp.route("/users")
def allUsers():
    # get all users
    users = User.query.all()
    
    return jsonify([{
        "id" : user.id,
        "username":f"{user.username}",
        "email" : user.email,
        # "password" : user.password
    } for user in users])        
    
@main_bp.route("/workspaces")
def allWorkspaces():
    workspaces = Workspace.query.all()
    
    return jsonify([
        {
            "id": workspace.id,
            "name" : workspace.name,
            "description" : workspace.description,
            "iconPath" : workspace.iconPath
        }
     for workspace in workspaces])

User.create_synthetic(50)