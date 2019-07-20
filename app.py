from flask import Flask
from flask import request
from flask import render_template
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from os.path import isfile, join

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/<name>')
def index(name=None):
    images = [image for image in os.listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, image))]
    return render_template('index.html', name=name, images=images)

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