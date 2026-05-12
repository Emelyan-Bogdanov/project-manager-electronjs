from flask import Flask
from .modules import db



def create_app() :
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.init_app(app)

    with app.app_context() :
        db.create_all()

    # ======= routes =========

    
    return app