from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model) :
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(120), default="")
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250) , nullable=False)
    avatar = db.Column(db.Text, default="")
    tags = db.Column(db.Text, default="[]")
    location = db.Column(db.String(120), default="")


    @staticmethod
    def create_synthetic(db,count=5,):
        import random
        for i in range(count):
            user = User(username=f"user_{random.randint(999,99999999)}" , email=f"email_{random.randint(999,99999999)}",password="1234{i}")
            db.session.add(user)
            db.session.commit()

class Workspace(db.Model) :
    __tablename__ = "workspaces"
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text , nullable=False)
    iconPath = db.Column(db.String(300) , default="[NO IMAGE]")

    @staticmethod
    def create_synthetic(db,count=5):
        for i in range(count):
           db.session.add( Workspace(name=f"workspace_{i}" , description=f"description_{i}"))
           db.session.commit()

    @staticmethod
    def add_workspace(name, description, iconPath="[NO IMAGE]"):
        workspace = Workspace(
            name=name,
            description=description,
            iconPath=iconPath
        )
        db.session.add(workspace)
        db.session.commit()
        return workspace

    @staticmethod
    def get_workspace(workspace_id):
        return Workspace.query.get(workspace_id)

    @staticmethod
    def update_workspace(workspace_id, **kwargs):
        workspace = Workspace.query.get(workspace_id)
        if workspace:
            for key, value in kwargs.items():
                if hasattr(workspace, key):
                    setattr(workspace, key, value)
            db.session.commit()
        return workspace

    @staticmethod
    def delete_workspace(workspace_id):
        workspace = Workspace.query.get(workspace_id)
        if workspace:
            db.session.delete(workspace)
            db.session.commit()
        return workspace


class Task(db.Model) : 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    taskType = db.Column(db.String(50), default="basic")
    """ tags are arrays , but stored as json dumped """
    tags = db.Column(db.String(300) , nullable=False)
    description = db.Column(db.Text, default="")
    urls = db.Column(db.Text, default="[]")
    views = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    deadline = db.Column(db.String(70) , nullable=False)
    authorId = db.Column(db.Integer)
    """ images paths are arrays , but stored as json dumped """
    images = db.Column(db.Text , default="[]")
    files = db.Column(db.Text, default="[]")
    priority = db.Column(db.Integer, default=1)  # 1 = Low, 2 = Medium, 3 = High
    status = db.Column(db.String(50), default="todo")  # todo, in_progress, done
    workspaceId = db.Column(db.Integer, default=None)
    created_at = db.Column(db.String(30), default="")
    reminder = db.Column(db.String(30), default="")
    
    @staticmethod
    def create_synthetic(db,count=5):
        import random
        for i in range(count):
            db.session.add(Task(title=f"title_{i}" , deadline=f"deadline_{i}",tags=f"{random.randint(555,999999)}{random.randint(555,999999)}{random.randint(555,999999)}"))
            db.session.commit()

    @staticmethod
    def add_task(title, tags, deadline, authorId, description="", urls="[]", images="[]", files="[]", taskType="basic", priority=1, status="todo", workspaceId=None, reminder=""):
        from datetime import datetime
        task = Task(
            title=title,
            taskType=taskType,
            tags=tags,
            description=description,
            urls=urls,
            deadline=deadline,
            authorId=authorId,
            images=images,
            files=files,
            priority=priority,
            status=status,
            workspaceId=workspaceId,
            created_at=datetime.now().isoformat(),
            reminder=reminder
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_task(task_id):
        return Task.query.get(task_id)

    @staticmethod
    def update_task(task_id, **kwargs):
        task = Task.query.get(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return task


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text,nullable=False)
    
    @staticmethod
    def create_synthetic(db,count=5):
        import random
        for i in range(count):
            db.session.add(Comment(text=f"text_blablabla_{random.randint(666,5955)}"))
            db.session.commit()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text,nullable=False)
    authorId = db.Column(db.Integer,nullable=False)
    workspaceId = db.Column(db.Integer,nullable=False)
    
    @staticmethod
    def create_synthetic(db, count=5):
        import random
        for i in range(count):
            msg = Message(
                text=f"Message texte {i}",
                authorId=random.randint(1, 100),
                workspaceId=random.randint(1, 10)
            )
            db.session.add(msg)
            db.session.commit()


class FileEntry(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(250), nullable=False)
    original_name = db.Column(db.String(250), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    size = db.Column(db.Integer, default=0)
    mime_type = db.Column(db.String(100), default="")
    uploaded_by = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(70), default="")


def seed_database(db):
    import random, json
    if User.query.count() == 0:
        for i in range(8):
            user = User(
                username=f"user_{i}",
                email=f"user{i}@example.com",
                password="1234"
            )
            db.session.add(user)
        db.session.commit()
        print("Seeded 8 users")
    if Task.query.count() == 0:
        statuses = ["todo", "in_progress", "done"]
        titles = [
            "Design system", "API Auth", "Tests unitaires", "Page parametres",
            "Tableau de bord", "Base de donnees", "Notification email",
            "Maquettes mobile", "CI/CD Pipeline", "Page connexion"
        ]
        tag_pool = ["Frontend", "Backend", "Design", "DevOps", "Mobile", "UI", "BDD", "Auth"]
        descriptions = [
            "Mettre en place le systeme de design pour l'application",
            "Implementer l'authentification via JWT",
            "Ecrire les tests unitaires pour les modules principaux",
            "Creer la page de parametres utilisateur",
            "Developper le tableau de bord avec les statistiques",
            "Concevoir le schema de la base de donnees",
            "Configurer les notifications par email",
            "Realiser les maquettes pour la version mobile",
            "Mettre en place le pipeline CI/CD",
            "Developper la page de connexion et d'inscription"
        ]
        for i in range(10):
            task = Task(
                title=titles[i],
                tags=json.dumps([tag_pool[i % 8]]),
                description=descriptions[i],
                deadline=f"{random.randint(1, 28)} Mai",
                authorId=random.randint(1, 8),
                images="[]",
                priority=random.randint(1, 3),
                status=statuses[i % 3]
            )
            db.session.add(task)
        db.session.commit()
        print("Seeded 10 tasks")
    if Workspace.query.count() == 0:
        for i in range(3):
            ws = Workspace(name=f"Projet {i+1}", description=f"Description du projet {i+1}")
            db.session.add(ws)
        db.session.commit()
        print("Seeded 3 workspaces")
