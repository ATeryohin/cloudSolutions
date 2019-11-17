import os


from flask import render_template, request, flash, url_for
from werkzeug.utils import redirect, secure_filename

from app import app

from .Utils import get_bucket_name, get_file_names_in_bucket, upload_file_to_s3

UPLOAD_FOLDER = '/home/ateryohin/workspace/python/S3FileUploader/tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            upload_file_to_s3(f"{UPLOAD_FOLDER}{filename}")
            return redirect(url_for('upload_file', filename=filename))
    return render_template("index.html", title=get_bucket_name(), file_names=get_file_names_in_bucket())