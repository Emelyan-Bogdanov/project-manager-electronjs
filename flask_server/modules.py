from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250) , nullable=False)


class Workspace(db.Model) :
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text , nullable=False)
    iconPath = db.Column(db.String(300) , default="[NO IMAGE]")


class Task(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    """ tags are arrays , but stored as json dumped """
    tags = db.Column(db.String(300) , nullable=False)
    views = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    deadline = db.Column(db.String(70) , nullable=False)
    authorId = db.Column(db.Integer)
    """ images paths are arrays , but stored as json dumped """
    images = db.Column(db.String(250) , default="")
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text,nullable=False)
