from flask import Flask
from .modules import db
from flask_cors import CORS

# Enable CORS for all routes and specify allowed origins

def create_app() :
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.init_app(app)

    with app.app_context() :
        db.create_all()
        from .modules import User , Task , Comment ,Workspace
        
        # add synthetic data
        print(__name__," : remove comment to add synthetic data ")
        
        # import random
        # for i in range(20):
        #     user = User(username=f"user_{random.randint(999,99999999)}" , email=f"email_{random.randint(999,99999999)}",password=f"1234{i}")
        #     db.session.add(user)
        #     db.session.commit()

    # ======= routes =========
    from .routes import main_bp , message_bp  , workspace_bp , task_bp , users_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(users_bp)
    
    
    return app