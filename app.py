
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS, cross_origin
import cloudinary
import cloudinary.uploader
import os
import psycopg2
import bcrypt
from werkzeug.utils import secure_filename


#local imports
from database import sql_write, sql_select_one
from models.users import all_users
from models.projects import all_projects


DB_URL = os.environ.get("DATABASE_URL", "dbname=feedback_app")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Random string. Do not store keys in code!!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#cloudinary
CORS(app)

# ******* Home ******
@app.route('/home')
@app.route('/')
def index():
    name = session.get('name')
    user_id = session.get('user_id')
    projects = all_projects()
    
    return render_template('index.html', name=name, user_id = user_id, projects= projects)

# ***** Login *****
@app.route('/login')
def login():
    return render_template('login.html')

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
            return redirect('/')
        else:
            error_message = 'Email address or password is incorrect'
            return render_template('login.html', error_message = error_message, users = all_users())
    return " user not found"

# ***** Signup *****
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup-action', methods = ['POST'])
def signupAction():
    name = request.form.get('namesignup')
    email = request.form.get('emailsignup')
    role = request.form.get('role')
    password = request.form.get('passwordsignup')
    confirm_password = request.form.get('confirmpasswordsignup')
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    if password == confirm_password:
        sql_write('INSERT INTO users(email, name, password_hash, role) VALUES(%s, %s, %s, %s)',
        [email, name, password_hash, role ])
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

   

# upload project
@app.route('/upload-project')
def uploadProject():
    name = session.get('name')
    user_id = session.get('user_id')
    return render_template('upload-project.html')

@app.route('/upload-project-action' , methods = ['POST'])
def uploadProjectAction() :
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
    
    sql_write('INSERT INTO projects(title, image, description, category) VALUES(%s, %s, %s, %s)',
        [title, uploaded_img_url, description, category ])
    return redirect('/')

  
# ***** PROJECT *****
@app.route('/project')
def projectSingle():
    name = session.get('name')
    project_id = request.args.get('project_id')
    # conn = psycopg2.connect("dbname=feedback_app")
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM projects WHERE project_id =(%s)", [id])
    # results = cur.fetchone()
    result = sql_select_one('SELECT * FROM projects WHERE project_id = %s', [project_id])
    print(type(result))
    return render_template('project.html', result = result)


if __name__ == "__main__":
    app.run(debug=True)