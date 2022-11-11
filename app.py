# import modules
import os
from flask import Flask
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
a_user = {'id':1,'username':'Amal', 'email':'ajoshy@uncc.edu', 'password':'password'}
projects = {1:{'title': 'First project', 'detail':'This is the first project', 'company_name': 'verizon' }}

# routing

# GET / - show the user the landing page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',user=a_user,user_projects=projects)
@app.route('/new_project', methods=['GET','POST'])
def new_project():
    #projects = {'title':'First project', 'detail':'This is the first project', 'company_name': 'verizon' }
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['detail']
        company = request.form['company_name']
        id = len(projects)+1
        projects[id] = {'title': title, 'detail': text, 'company_name': company}
        return redirect(url_for('index'))
    else:
        return render_template('new_project.html', user=a_user)




# start server at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)