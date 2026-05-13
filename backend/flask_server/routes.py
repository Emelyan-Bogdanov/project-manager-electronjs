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

@main_bp.route("/task/<taskid>")
def taskInfo(taskid:int):
    # try to find the task
    try :
        task = Task.query.get(taskid)
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
        {
            "id":"ERROR",
            "title":"ERROR",
            "tags" :"ERROR",
            "views" :"ERROR",
            "comments" :"ERROR",
            "deadline" :"ERROR",
            "authorId" :"ERROR",
            "images" :"ERROR",
        }


# how many users are in the app
@main_bp.route("/howmanyusers")
def getnUser():
    import requests
    
    r = requests.get("http://127.0.0.1:8080/users").json()
    
    return str(len(r))

@main_bp.route("/deleteuser/<userid>")
def deleteUser(userid:int):
    from .modules import db
    try :
        user = User.query.get(userid)
        db.session.delete(user)
        db.session.commit()
        return f"user {userid} deleted"
    except Exception as e :
        if str(e) == "Class 'builtins.NoneType' is not mapped" :
            return "ERROR : maybe user not found : \n" + str(e)
        return f"ERROR : {str(e)}"