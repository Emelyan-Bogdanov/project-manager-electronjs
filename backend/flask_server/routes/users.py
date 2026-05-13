from flask import Blueprint , jsonify
from ..modules import User

users_bp = Blueprint("users",__name__)


@users_bp.route("/users")
def allUsers():
    # get all users
    users = User.query.all()
    
    return jsonify([{
        "id" : user.id,
        "username":f"{user.username}",
        "email" : user.email,
        # "password" : user.password
    } for user in users])        
    



# how many users are in the app
@users_bp.route("/howmanyusers")
def getnUser():
    import requests
    
    r = requests.get("http://127.0.0.1:8080/users").json()
    
    return str(len(r))

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