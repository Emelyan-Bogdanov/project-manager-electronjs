from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250) , nullable=False)


    @staticmethod
    def create_synthetic(db,count=5,):
        import random
        for i in range(count):
            user = User(username=f"user_{random.randint(999,99999999)}" , email=f"email_{random.randint(999,99999999)}",password="1234{i}")
            db.session.add(user)
            db.session.commit()

class Workspace(db.Model) :
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text , nullable=False)
    iconPath = db.Column(db.String(300) , default="[NO IMAGE]")

    @staticmethod
    def create_synthetic(db,count=5):
        for i in range(count):
           db.session.add( Workspace(f"workspace_{i}" , f"description_{i}"))
           db.session.commit()


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
    
    @staticmethod
    def create_synthetic(db,count=5):
        import random
        for i in range(count):
            db.session.add(Task(f"title_{i}" , f"deadline_{i}",f"{random.randint(555,999999)}{random.randint(555,999999)}{random.randint(555,999999)}"))
            db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text,nullable=False)
    
    @staticmethod
    def create_synthetic(db,count=5):
        import random
        for i in range(count):
            db.session.add(Workspace(f"text_blablabla_{random.randint(666,5955)}"))
            db.session.commit()
