
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS, cross_origin
import cloudinary
import cloudinary.uploader
import os
import psycopg2
import bcrypt
from werkzeug.utils import secure_filename


#local imports
from database import sql_write, sql_select_id, sql_select_user_project
from models.users import all_users
from models.projects import all_projects


DB_URL = os.environ.get("HEROKU_POSTGRESQL_TEAL_URL", "dbname=feedback_app")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


#cloudinary
CORS(app)

# ******* Home ******
@app.route('/home')
@app.route('/')
def index():
    name = session.get('name')
    user_id = session.get('user_id')
    avatar = session.get('avatar')
    projects = all_projects()
    
    return render_template('index.html', name=name, user_id = user_id, projects= projects, avatar = avatar )

# ***** Login *****
@app.route('/login')
def login():
    name = session.get('name')
    user_id = session.get('user_id')
    avatar = session.get('avatar')
    
    return render_template('login.html', name = name, user_id = user_id, avatar=avatar)

@app.route('/login_action', methods=['POST'])
def loginAction():
    #form
    username = request.form.get('emailLogin')
    password = request.form.get('passwordlogin')
    
    #db
    users = all_users()
    for user in users:  
        password_hash = user['password_hash']
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if user['email'] == username and valid == True:
            session['email'] = username
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['avatar']= user['avatar']
            return redirect('/')
        else:
            error_message = 'Email address or password is incorrect'
            return render_template('login.html', error_message = error_message)
    return " user not found"

# ***** Signup *****
@app.route('/signup')
def signup():
    name = session.get('name')
    user_id = session.get('user_id')
    avatar = session.get('avatar')
    return render_template('signup.html',name=name, user_id = user_id, avatar = avatar)

@app.route('/signup-action', methods = ['POST'])
def signupAction():
    name = request.form.get('namesignup')
    email = request.form.get('emailsignup')
    role = request.form.get('role')
    password = request.form.get('passwordsignup')
    confirm_password = request.form.get('confirmpasswordsignup')
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    #upload avatar
    app.logger.info('in upload route')
    cloudinary.config( 
        cloud_name = "dtdhdix1f", 
        api_key = "546218847156792", 
        api_secret = "ects6SDSdPX94um0t3sIpp-uJgk" 
    )
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['avatar']
        app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = cloudinary.uploader.upload(
          file_to_upload,
          folder = "feedback-app/", 

          )
    app.logger.info(upload_result)
    uploaded_img_url = upload_result["secure_url"]

    if password == confirm_password:
        sql_write('INSERT INTO users(email, name, password_hash, avatar,role) VALUES(%s, %s, %s, %s, %s)',
        [email, name, password_hash, uploaded_img_url, role ])
        return redirect('/login')
    else:
        return "Could not sign up"


# ***** signout *****
@app.route('/signout')
def signout():
    session.clear()
    return render_template('login.html')
  
# ***** UPLOAD *****
#upload images
@app.route('/upload-image', methods = ['POST'])
def upload_file():
  app.logger.info('in upload route')
  cloudinary.config( 
    cloud_name = "dtdhdix1f", 
    api_key = "546218847156792", 
    api_secret = "ects6SDSdPX94um0t3sIpp-uJgk" 
    )
  upload_result = None
  if request.method == 'POST':
    file_to_upload = request.files['projectImage']
    app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = cloudinary.uploader.upload(
          file_to_upload,
          folder = "feedback-app/", 

          )
      app.logger.info(upload_result)
      uploade_img_url = upload_result["secure_url"]
    #   uploaded_img_json = jsonify(upload_result)
    return upload_result["secure_url"]

   

# Create project
@app.route('/upload-project')
def uploadProject():
    name = session.get('name')
    user_id = session.get('user_id')
    avatar = session.get('avatar')
    
    return render_template('upload-project.html', avatar = avatar)

@app.route('/upload-project-action' , methods = ['POST'])
def uploadProjectAction() :
    user_id = session.get('user_id')
    title = request.form.get('title')
    description = request.form.get('projectDescription')
    category = request.form.get('projectCategory')

    #upload project image
    app.logger.info('in upload route')
    cloudinary.config( 
        cloud_name = "dtdhdix1f", 
        api_key = "546218847156792", 
        api_secret = "ects6SDSdPX94um0t3sIpp-uJgk" 
    )
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['projectImage']
        app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = cloudinary.uploader.upload(
          file_to_upload,
          folder = "feedback-app/", 

          )
    app.logger.info(upload_result)
    uploaded_img_url = upload_result["secure_url"]
    
    sql_write('INSERT INTO projects(title, image, description, category, user_id) VALUES(%s, %s, %s, %s, %s)',
        [title, uploaded_img_url, description, category, user_id ])
    return redirect('/')

  
# ***** PROJECT *****
@app.route('/project')
def projectSingle():
    #Current user - session
    name = session.get('name')
    current_user_id = session.get('user_id')
    avatar = session.get('avatar')
    #project information
    project_id = request.args.get('project_id')
    #Get project, users(author) from db
    result = sql_select_id('SELECT * FROM projects WHERE project_id = %s' , [project_id])
    author = sql_select_user_project('SELECT name FROM users INNER JOIN projects ON users.user_id = projects.user_id')
    author_avatar = sql_select_user_project('SELECT avatar FROM users INNER JOIN projects ON users.user_id = projects.user_id')
    
    return render_template('project.html', result = result, author = author, author_avatar = author_avatar, avatar = avatar, name = name, current_user_id = current_user_id)

#Edit Project
@app.route('/edit-project')
def editProject():
    project_id = request.args.get('id')
    project =sql_select_id("SELECT project_id, title, image, description, category FROM projects WHERE project_id =(%s)", [project_id])
    return render_template('edit-project.html', project = project)

@app.route('/edit-project-action', methods=['POST'])
def editProjectAction():
    project_id = request.form.get('projectId')
    title = request.form.get('title')
    image = request.form.get('projectImage')
    description = request.form.get('projectDescription')
    category = request.form.get('project Category')
    link = request.form.get('link')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    if title != '':
        cur.execute('UPDATE projects SET title=(%s) WHERE project_id=(%s)',[title, project_id])
    if image != '':
        cur.execute('UPDATE projects SET image=(%s) WHERE project_id=(%s)',[image, project_id])
    else:
        upload_file()
    if description != '':
        cur.execute('UPDATE projects SET description=(%s) WHERE project_id=(%s)',[description, project_id])
    if category != '':
        cur.execute('UPDATE projects SET category =(%s) WHERE project_id=(%s)',[category, project_id])
    if link != '':
        cur.execute('UPDATE projects SET link=(%s) WHERE project_id=(%s)',[link, project_id])


    conn.commit()
    return redirect('/')

@app.route('/delete-project', methods=['POST'])
def deleteProject():
    project_id = request.form.get('id')
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE project_id =(%s)", [project_id])
    conn.commit()

    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)