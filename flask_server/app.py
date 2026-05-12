from flask import Flask
from .modules import db



def create_app() :
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.init_app(app)

    with app.app_context() :
        db.create_all()
        # # create admin
        # from .modules import User
        # db.session.add(User(username="ibrahim",password="ahmed",email="ibrahim@admin.com"))
        # db.session.commit()

    # ======= routes =========
    @app.route("/users")
    def allUsers():
        from flask import jsonify
        # get all users
        from .modules import User
        users = User.query.all()
        
        return jsonify([{
            "id" : user.id,
            "username":f"{user.username}",
            "email" : user.email,
            # "password" : user.password
        } for user in users])        
    return app