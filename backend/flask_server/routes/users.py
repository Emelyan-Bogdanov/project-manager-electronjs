from flask import Blueprint, request, jsonify
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

@users_bp.route("/api/users")
def api_all_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email
    } for user in users])
    



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
    try:
        user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password", "1234")
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username, "email": user.email, "message": "User created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
