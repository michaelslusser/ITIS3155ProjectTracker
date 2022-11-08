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

# routing

# GET / - show the user the landing page
@app.route('/')
def index():
    a_user = {'name':'Amal', 'email':'ajoshy@uncc.edu'}
    return render_template('index.html',user=a_user)



# start server at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)