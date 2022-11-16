# import modules
import os
from flask import Flask
from database import db
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import *

app = Flask(__name__)
app.static_folder = './static'
app.template_folder = './templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

# initialize the database and bind it to flask
db.init_app(app)
with app.app_context():
    db.create_all()

# routing

# GET / - show the user the landing page
@app.route('/')
@app.route('/index')
@app.route('/notes') # can delete this later if needed
def index():
    a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
    projects = find_projects()
    return render_template('index.html',user=a_user,user_projects=projects)

# VIEW PROJECT
@app.route('/view_project/<project_id>')
def get_project(project_id):
    a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
    my_project = find_project_by_id(project_id)
    tasks = find_tasks_by_project(project_id)
    return render_template('view_project.html', project=my_project, user=a_user, proj_tasks=tasks)

# ADD NEW PROJECT
@app.route('/new_project', methods=['GET','POST'])
def new_project():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['detail']
        company = request.form['company_name']
        create_project(title, text, company)
        return redirect(url_for('index'))
    else:
        a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
        return render_template('new_project.html', user=a_user)

# EDIT PROJECT
@app.route('/project/edit/<project_id>',methods=['GET','POST'])
def edit_project(project_id):
    if request.method == 'POST':
        title = request.form['title']
        detail = request.form['detail']
        company_name = request.form['company_name']
        update_project(project_id, title, detail, company_name)
        return redirect(url_for('index'))
    else:
        a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
        my_project = find_project_by_id(project_id)
        return render_template('new_project.html',project=my_project,user=a_user)

# DELETE PROJECT
@app.route('/project/delete/<project_id>',methods=['POST'])
def delete_project(project_id):
    remove_project(project_id)
    return redirect(url_for('index'))

#Placeholder code for creating new task
@app.route('/view_project/<project_id>/new_task', methods=['GET','POST'])
def new_task(project_id):
    if request.method == 'POST':
        my_project = find_project_by_id(project_id)
        title = request.form['title']
        text = request.form['description']
        create_task(my_project.id, title, text)
        return redirect(url_for('get_project', project_id=my_project.id))
    else:
        my_project = find_project_by_id(project_id)
        a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
        return render_template('new_task.html', user=a_user, project=my_project)

@app.route('/view_project/<project_id>/edit/<t_id>', methods=['GET','POST'])
def edit_task(project_id, t_id):
    if request.method == 'POST':
        my_project = find_project_by_id(project_id)
        my_task = find_task_by_id(project_id, t_id)
        title = request.form['title']
        text = request.form['description']
        update_task(my_task.id, my_task.project_id, title, text)
        return redirect(url_for('get_project', project_id=my_project.id))
    else:
        my_project = find_project_by_id(project_id)
        my_task = find_task_by_id(project_id, t_id)
        a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
        return render_template('new_task.html', user=a_user, project=my_project, task=my_task)

# start server at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)