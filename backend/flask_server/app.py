import os
from flask import Flask
from .modules import db, seed_database
from flask_cors import CORS

def create_app() :
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)
    CORS(app)

    with app.app_context() :
        db.create_all()
        # seed_database(db)

    from .routes import message_bp, workspace_bp, task_bp, users_bp, files_bp

    app.register_blueprint(message_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(files_bp)

    return app
