import os

import cv2
from flask import render_template, request, flash, url_for
from pip._internal.cli.cmdoptions import no_cache
from werkzeug.utils import redirect, secure_filename


from app import app
from .Utils import *

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

UPLOAD_FOLDER = os.path.join('static', 'upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

fn = None
num_img = 0
STATIC_IMAGES_FOLDER = os.path.join('static', 'photo')
app.config['STATIC_IMAGES_FOLDER'] = STATIC_IMAGES_FOLDER
app.config["CACHE_TYPE"] = "null"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/", methods=['GET'])
def render_page():
    if fn == None:
        full_filename = os.path.join(app.config['STATIC_IMAGES_FOLDER'], 'def_image.jpg')
        print(full_filename)
        return render_template("index.html")

    return render_template("index.html", user_image=os.path.join('static', 'upload', f"render_image_{num_img}.jpg"))

@app.route('/', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join("/home/ateryohin/workspace/python/mail_cv/app/static/upload", filename)
        file.save(file_path)
        global fn, num_img
        num_img += 1
        fn = filename
        request_to_cv(file_path, num_img)
        return redirect(url_for('render_page'))