from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user
from user_database import authenticate_user, login_manager
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = authenticate_user(username, password)

        if user:
            login_user(user)
            return redirect(url_for('index.html'))

    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('index'))


@app.route('/files')
def list_files():
    upload_folder = 'static/uploads'
    file_list = []

    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        file_info = get_file_info(file_path)
        file_list.append(file_info)

    return render_template('index.html', files=file_list)


if __name__ == '__main__':
    app.run(debug=True)
