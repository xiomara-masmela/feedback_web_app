
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS, cross_origin
import cloudinary
import cloudinary.uploader
import os
import psycopg2

from werkzeug.utils import secure_filename


#local imports
from database import sql_write, sql_select_id, sql_select_user_project
from models.users import create_user, select_all_users, select_user, select_user_email
from models.projects import create_new_project, select_project, edit_category, edit_link, edit_image, edit_description, edit_title, select_all_projects, delete_project_id
from models.passwords import check_password, convert_secure_password
from models.comments import select_comment, insert_comment
# from models.uploads import cl_config



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
    projects = select_all_projects()
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
    
    username = request.form.get('emailLogin')
    password = request.form.get('passwordlogin')
    password_hash = convert_secure_password(password)
    users = select_all_users()
    
    user = select_user_email(username)
    print(user)
    userEmail = user[1]
    userPh = user[3]
    valid = check_password(password, userPh)

    if userEmail == username and valid == True:
        session['email'] = username
        session['user_id'] = user[0]
        session['name'] = user[2]
        session['avatar']= user[4]
        print(session['email'], session['user_id'])
        return redirect('/')
    else:
        error_message = 'Email address or password is incorrect'
        
    return render_template('login.html', error_message = error_message, userEmail=userEmail, username=username, users = users, user = x_user)
    
    return render_template('login.html', error_message="User not found")

    

    

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
    
    password_hash = convert_secure_password(password)

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
    image_url = upload_result["secure_url"]

    if password == confirm_password:
        query = create_user(email,name, password_hash, image_url, role)
        return redirect('/login')
    else:
        error_message = "Could not sign up"
        return render_template("signup.html", error_message = error_message)


# ***** signout *****
@app.route('/signout')
def signout():
    print(session['email'])
    session.clear()
    
    return redirect('/')
  
# ***** UPLOAD *****
  

# Create project
@app.route('/upload-project')
def createProject():
    name = session.get('name')
    user_id = session.get('user_id')
    avatar = session.get('avatar')
    return render_template('upload-project.html', avatar = avatar, user_id = user_id, name = name)

@app.route('/upload-project-action' , methods = ['POST'])
def createProjectAction() :
    user_id = session.get('user_id')
    title = request.form.get('title')
    description = request.form.get('projectDescription')
    category = request.form.get('projectCategory')
    link = request.form.get('link')

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
    image = upload_result["secure_url"]
    
    query = create_new_project(title, image, description, category, link, user_id)
    return redirect('/')

  
# ***** PROJECT *****
@app.route('/project')
def projectSingle():
    #Current user - session
    name = session.get('name')
    current_user_id = session.get('user_id')
    avatar = session.get('avatar')
    #Get project 
    project_id = request.args.get('project_id')
    project = select_project(project_id)
    author_id = project[6]
    author = select_user(author_id)
    #Get comments
    comments = select_comment(project_id)
    return render_template('project.html', project = project , author = author, avatar = avatar, name = name, current_user_id = current_user_id, comments = comments)
   
#Edit Project
@app.route('/edit-project')
def editProject():
    #session
    name = session.get('name')
    current_user_id = session.get('user_id')
    avatar = session.get('avatar')
    project_id = request.args.get('id')
    project = select_project(project_id)
    author = project[6]
    return render_template('edit-project.html', project = project, name=name, avatar=avatar, current_user_id = current_user_id, author_id = author)

@app.route('/edit-project-action', methods=['POST'])
def editProjectAction():
    project_id = request.form.get('projectId')
    title = request.form.get('title')
    # image = request.form.get('projectImage')
    description = request.form.get('projectDescription')
    category = request.form.get('projectCategory')
    link = request.form.get('link')
    
    if request.form.get('projectImage') != None:
        #Edit project image
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
        image = upload_result["secure_url"]
        print(f'imageis:',image)

        query_update_image = edit_image(image, project_id)
    
    if title != '':
        query_update = edit_title(title, project_id)
    # if image != '':
    #     query_update_image = edit_image(image, project_id)
    #     print(query_update_image)
    if description != '':
        query_update_description = edit_description(description, project_id)
    if category != '':
        query_update_category= edit_category(category, project_id)
    if link != '':
        query_update_link = edit_link(link, project_id)
    return redirect('/')

@app.route('/delete-project', methods=['POST'])
def deleteProject():
    project_id = request.form.get('id')
    query = delete_project_id(project_id)
    return redirect('/')

# Feedback - comments
@app.route('/post-comment', methods=['POST'])
def postComment():
    content = request.form.get('feedback')
    project_id = request.form.get('projectId')
    user_id = session.get('user_id')
    query = insert_comment(content, project_id, user_id)
    return redirect(f'/project?project_id={project_id}')

if __name__ == "__main__":
    app.run(debug=True)