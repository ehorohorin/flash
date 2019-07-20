from flask import Flask
from flask import request
from flask import render_template
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile, join
from flask_migrate import Migrate

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost/flash"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

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
    short_name = db.Column(db.String(200), nullable=True)
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
    return main_page()

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

@app.route('/add_problem', methods=['POST', 'GET'])
def add_problem():
    if request.method == 'POST':
        print(request.form['shortname'])
        problem = Problem(votes = 0, description=request.form['description'], short_name=request.form['shortname'])
        db.session.add(problem)

        db.session.flush()
        db.session.refresh(problem)
        print(problem.id)
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(f"problem_{problem.id}_.{file.filename.split('.')[1]}")

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('upload_image',
            #                         filename=filename))

        problem.image = filename
        print(problem.image)
        # db.session.add(problem)
        # db.session.refresh(problem)
        db.session.commit()

        return main_page()
    else:
        return render_template('add_problem.html')

@app.route('/upvote/<int:problem_id>')
def upvote(problem_id=None):
    problem = Problem.query.filter_by(id=problem_id).first()

    if problem != None:
        problem.votes += 1
        db.session.commit()
    return main_page()
@app.route('/problem/<int:problem_id>')
def problem_page(problem_id=None):
    problem = Problem.query.filter_by(id=problem_id).first()
    return render_template('problem.html', problem=problem)

def main_page():
    problems = Problem.query.all()
    problems = sorted(problems, key=lambda problem: problem.votes, reverse=True)
    return render_template('index.html', problems=problems)