from flask import Flask
from flask import request
from flask import render_template
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile, join

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost/flash"
db = SQLAlchemy(app)

class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    votes = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(5000), nullable=True)
    image = db.Column(db.String(300), nullable=True) #link ?
    #comments = db.Column(db.String(120), unique=True, nullable=False)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, primary_key=True)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/<name>')
def index(name=None):
    problems = Problem.query.all()
    return render_template('index.html', problems=problems)

@app.route('/image', methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_image',
                                    filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    return "Task list []"

@app.route('/add_problem', methods=['POST', 'GET'])
def add_problem():
    if request.method == 'POST':
        problem = Problem(votes = 0, description=request.form['description'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_image',
                                    filename=filename))
        db.session.add(problem)
        db.session.commit()
        problems = Problem.query.all()
        return render_template('index.html', problems=problems)
    else:
        return render_template('add_problem.html')