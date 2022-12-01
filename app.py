# import modules
import os
from flask import Flask
from database import db
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import *
from forms import *
import bcrypt
from flask import session

app = Flask(__name__)
app.static_folder = './static'
app.template_folder = './templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'

# initialize the database and bind it to flask
db.init_app(app)
with app.app_context():
    db.create_all()

# routing

# GET / - show the user the landing page
@app.route('/')
@app.route('/index')
@app.route('/projects') # can delete this later if needed
@app.route('/notes/')
def index():
    if session.get('user'):
        projects = find_projects()
        return render_template("index.html", user=session['user'], user_projects=projects, theme=session['user_theme'])
    return redirect(url_for('login'))
    #a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
    #projects = find_projects()
    #return render_template('index.html',user=a_user,user_projects=projects)

# VIEW PROJECT
@app.route('/view_project/<project_id>')
def get_project(project_id):
    if session.get('user'):
        my_project = find_project_by_id(project_id)
        tasks = find_tasks_by_project(project_id)
        return render_template('view_project.html', project=my_project, user=session['user'], proj_tasks=tasks, theme=session['user_theme'])
    return redirect(url_for('login'))

# ADD NEW PROJECT
@app.route('/new_project', methods=['GET','POST'])
def new_project():
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['detail']
            company = request.form['company_name']
            create_project(title, text, company)
            return redirect(url_for('index'))
        else:
            return render_template('new_project.html', user=session['user'], theme=session['user_theme'])
    return redirect(url_for('login'))

# EDIT PROJECT
@app.route('/project/edit/<project_id>',methods=['GET','POST'])
def edit_project(project_id):
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            detail = request.form['detail']
            company_name = request.form['company_name']
            update_project(project_id, title, detail, company_name)
            return redirect(url_for('index'))
        else:
            my_project = find_project_by_id(project_id)
            return render_template('new_project.html', project=my_project, user=session['user'], theme=session['user_theme'])
    return redirect(url_for('login'))

# DELETE PROJECT
@app.route('/project/delete/<project_id>',methods=['POST'])
def delete_project(project_id):
    if session.get('user'):
        remove_project(project_id)
        return redirect(url_for('index'))
    return redirect(url_for('login'))

#Placeholder code for creating new task
@app.route('/view_project/<project_id>/new_task', methods=['GET','POST'])
def new_task(project_id):
    if session.get('user'):
        if request.method == 'POST':
            my_project = find_project_by_id(project_id)
            title = request.form['title']
            text = request.form['description']
            create_task(my_project.id, title, text)
            return redirect(url_for('get_project', project_id=my_project.id))
        else:
            my_project = find_project_by_id(project_id)
            return render_template('new_task.html', user=session['user'], project=my_project, theme=session['user_theme'])
    return redirect(url_for('login'))

@app.route('/view_project/<project_id>/edit/<t_id>', methods=['GET','POST'])
def edit_task(project_id, t_id):
    if session.get('user'):
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
            return render_template('new_task.html', user=session['user'], project=my_project, task=my_task, theme=session['user_theme'])
    return redirect(url_for('login'))

@app.route('/view_project/<project_id>/view_task/<t_id>', methods=['GET','POST'])
def view_task(project_id, t_id):
    if session.get('user'):
        my_project = find_project_by_id(project_id)
        my_task = find_task_by_id(project_id, t_id)
        comments = find_comments_by_task(t_id)
        #testing
        return render_template('view_task.html', project=my_project, user=session['user'], task=my_task, task_comments=comments, theme=session['user_theme'])
    return redirect(url_for('login'))

@app.route('/view_project/<project_id>/delete/<t_id>', methods=['POST'])
def delete_task(project_id, t_id):
    if session.get('user'):
        my_project = find_project_by_id(project_id)
        remove_task(t_id, project_id)
        return redirect(url_for('get_project', project_id=my_project.id))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        
        username = request.form['username']
        
        new_user = User(username, request.form['email'], h_password, 1)
        
        create_user(username, request.form['email'], h_password, 1)

        session['user'] = username
        session['user_id'] = new_user.id
        session['user_theme'] = 1
        
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.username
            session['user_id'] = the_user.id
            session['user_theme'] = the_user.theme
            # render view
            return redirect(url_for('index'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))

@app.route('/view_project/<project_id>/view_task/<t_id>/comment', methods=['POST'])
def task_comment(t_id, project_id):
    if session.get('user'):
        comment_text = request.form['comment']
        create_comment(int(t_id),session['user'], comment_text)
        return redirect(url_for('view_task', project_id=project_id, t_id=t_id))
    else:
        return redirect(url_for('login'))
@app.route('/view_project/<project_id>/comment', methods=['POST'])
def project_comment(project_id):
    if session.get('user'):
        comment_text = request.form['comment']
        create_comment(int(project_id),session['user'], comment_text)
        return redirect(url_for('view_project', project_id=project_id))
    else:
        return redirect(url_for('login'))

@app.route('/style/<theme_id>', methods=['GET','POST'])
def change_style(theme_id):
    if session.get('user'):
        user = find_user_by_id(session['user_id'])
        if request.method == 'POST':
            update_user(session['user_id'], user.username, user.email, user.password, theme_id)
            after_user = find_user_by_id(session['user_id'])
            session['user_theme'] = after_user.theme
            return redirect(url_for('index'))
        else:
            return render_template("change_theme.html", user=session['user'], theme_id=session['user_theme'])
    else:
        return redirect(url_for('login'))

# start server at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)