from database import db

# Project model - contains project information
class Project(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column('title', db.String(200))
    detail = db.Column('detail', db.String(1000))
    company_name = db.Column('company_name', db.String(100))

    def __init__(self, title, detail, company_name):
        self.title = title
        self.detail = detail
        self.company_name = company_name

# Project Comment model - contains project comment information for associated project_id
class Project_Comment(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column('name', db.String(100))
    comment = db.Column('comment', db.String(300))

    def __init__(self, project_id, name, comment):
        self.project_id = project_id
        self.name = name
        self.comment = comment

# Task model - contains task information for associated project_id
class Task(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column('title', db.String(200))
    description = db.Column('description', db.String(1000))

    def __init__(self, project_id, title, description):
        self.project_id = project_id
        self.title = title
        self.description = description

# Comment model - contains comment information for associated task_id
class Comment(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    name = db.Column('name', db.String(100))
    comment = db.Column('comment', db.String(300))

    def __init__(self, task_id, name, comment):
        self.task_id = task_id
        self.name = name
        self.comment = comment

# User model - contains user information
class User(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(20))
    email = db.Column('email', db.String(50))
    password = db.Column('password', db.String(30), nullable=False)
    theme = db.Column('theme', db.Integer, nullable=False)
    
    def __init__(self, username, email, password, theme):
        self.username = username
        self.email = email
        self.password = password
        self.theme = theme

# functions to interact with models
# read operations
def find_projects():
    return db.session.query(Project).all()

def find_project_by_id(p_id):
    return db.session.query(Project).filter_by(id = p_id).one()

def find_tasks_by_project(p_id):
    return db.session.query(Task).filter_by(project_id = p_id).all()

def find_task_by_id(p_id, t_id):
    return db.session.query(Task).filter_by(project_id = p_id, id = t_id).one()

def find_comments_by_task(t_id):
    return db.session.query(Comment).filter_by(task_id = t_id).all()

def find_comments_by_project(p_id):
    return db.session.query(Project_Comment).filter_by(project_id = p_id).all()

def find_comment_by_id(t_id, c_id):
    return db.session.query(Comment).filter_by(task_id = t_id, id = c_id).one()

def find_users():
    return db.session.query(User).all()

def find_user_by_id(u_id):
    return db.session.query(User).filter_by(id = u_id).one()

def find_users_by_email(u_email):
    return db.session.query(User).filter_by(email = u_email).all()

# create operations
def create_project(title, detail, company_name):
    project = Project(title, detail, company_name)
    db.session.add(project)
    db.session.commit()

def create_task(project_id, title, description):
    task = Task(project_id, title, description)
    db.session.add(task)
    db.session.commit()

def create_comment(task_id, name, comment):
    comment = Comment(task_id, name, comment)
    db.session.add(comment)
    db.session.commit()

def create_pcomment(project_id, name, comment):
    comment = Project_Comment(project_id, name, comment)
    db.session.add(comment)
    db.session.commit()

def create_user(username, email, password, theme):
    user = User(username, email, password, theme)
    db.session.add(user)
    db.session.commit()

# update operations
def update_project(p_id, title, detail, company):
    # get project from db and update values
    project = find_project_by_id(p_id)
    project.title = title
    project.detail = detail
    project.company_name = company
    # push changes
    db.session.add(project)
    db.session.commit()

def update_task(t_id, project_id, title, description):
    # get task from db and update values
    task = find_task_by_id(project_id, t_id)
    task.project_id = project_id
    task.title = title
    task.description = description
    # push changes
    db.session.add(task)
    db.session.commit()

def update_comment(c_id, name, comment):
    # get comment from db and update values
    comment_object = find_comment_by_id(c_id)
    comment_object.name = name
    comment_object.comment = comment
    # push changes
    db.session.add(comment_object)
    db.session.commit()

def update_user(u_id, username, email, password, theme):
    # get user from db and update values
    user = find_user_by_id(u_id)
    user.username = username
    user.email = email
    user.password = password
    user.theme = theme
    # push changes
    db.session.add(user)
    db.session.commit()

# delete operations
def remove_project(p_id):
    # get project from db and delete
    project = find_project_by_id(p_id)
    db.session.delete(project)
    db.session.commit()

def remove_task(t_id, project_id):
    # get task from db and delete
    task = find_task_by_id(project_id, t_id)
    db.session.delete(task)
    db.session.commit()

def remove_comment(c_id, task_id):
    # get comment from db and delete
    comment = find_comment_by_id(task_id, c_id)
    db.session.delete(comment)
    db.session.commit()

def remove_user(u_id):
    # get user from db and delete
    user = find_user_by_id(u_id)
    db.session.delete(user)
    db.session.commit()