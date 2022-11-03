from database import db

# Project model - contains project information
class Project(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column('title', db.String(200))
    detail = db.Column('detail', db.String(1000))
    company_name = db.Column('company_name', db.String(100))

    def __init__(self, id, title, detail, company_name):
        self.id = id
        self.title = title
        self.detail = detail
        self.company_name = company_name

# Task model - contains task information for associated project_id
class Task(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    project_id = db.Column('project_id', db.Integer)
    title = db.Column('title', db.String(200))
    description = db.Column('description', db.String(1000))

    def __init__(self, id, project_id, title, description):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description

# Comment model - contains comment information for associated task_id
class Comment(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    task_id = db.Column('task_id', db.Integer)
    name = db.Column('name', db.String(100))
    comment = db.Column('comment', db.String(300))

    def __init__(self, id, task_id, name, comment):
        self.id = id
        self.task_id = task_id
        self.name = name
        self.comment = comment

# User model - contains user information
class User(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(20))
    email = db.Column('email', db.String(50))
    password = db.Column('password', db.String(30))

# functions to interact with models