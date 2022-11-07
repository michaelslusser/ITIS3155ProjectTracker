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

# Task model - contains task information for associated project_id
class Task(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    project_id = db.Column('project_id', db.Integer)
    title = db.Column('title', db.String(200))
    description = db.Column('description', db.String(1000))

    def __init__(self, project_id, title, description):
        self.project_id = project_id
        self.title = title
        self.description = description

# Comment model - contains comment information for associated task_id
class Comment(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    task_id = db.Column('task_id', db.Integer)
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
    password = db.Column('password', db.String(30))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# functions to interact with models
# read operations
def find_projects():
    return db.query(Project).all()

def find_project_by_id(p_id):
    return db.query(Project).filter_by(id = p_id).one()

def find_tasks_by_project(p_id):
    return db.query(Task).filter_by(project_id = p_id).all()

def find_task_by_id(p_id, t_id):
    return db.query(Task).filter_by(project_id = p_id, id = t_id).one()

def find_comments_by_task(t_id):
    return db.query(Comment).filter_by(task_id = t_id).all()

def find_comment_by_id(t_id, c_id):
    return db.query(Comment).filter_by(task_id = t_id, id = c_id).one()

def find_users():
    return db.query(User).all()

def find_user_by_id(u_id):
    return db.query(User).filter_by(id = u_id).one()

def find_users_by_email(u_email):
    return db.query(User).filter_by(email = u_email).all()

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

def create_user(username, email, password):
    print('Not implemented yet')

# update operations
def edit_project(new_title, new_detail, new_company):
    print('Not implemented yet')

def edit_task(new_project_id, new_title, new_description):
    print('Not implemented yet')

def edit_comment(new_name, new_comment):
    print('Not implemented yet')

def edit_user(new_username, new_email, new_password):
    print('Not implemented yet')

# delete operations
def remove_project(p_id):
    print('Not implemented yet')

def remove_task(p_id, t_id):
    print('Not implemented yet')

def remove_comment(t_id, c_id):
    print('Not implemented yet')

def remove_user(u_id):
    print('Not implemented yet')