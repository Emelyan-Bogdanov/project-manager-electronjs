import os
from flask import Flask
from .modules import db, seed_database
from flask_cors import CORS
from sqlalchemy import text

def create_app() :
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.config["IMAGES_FOLDER"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
    os.makedirs(app.config["IMAGES_FOLDER"], exist_ok=True)
    db.init_app(app)
    CORS(app)

    with app.app_context() :
        db.create_all()
        try:
            db.session.execute(text("ALTER TABLE task ADD COLUMN workspaceId INTEGER DEFAULT NULL"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE task ADD COLUMN created_at VARCHAR(30) DEFAULT ''"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE task ADD COLUMN reminder VARCHAR(30) DEFAULT ''"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE workspace_members ADD COLUMN joined_at VARCHAR(30) DEFAULT ''"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE task ADD COLUMN views INTEGER DEFAULT 0"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE task ADD COLUMN comments INTEGER DEFAULT 0"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        # seed_database(db)

    from .routes import message_bp, workspace_bp, task_bp, users_bp, files_bp, images_bp, comments_bp

    app.register_blueprint(message_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(comments_bp)

    return app
