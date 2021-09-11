
from flask import Flask, render_template, request, redirect, session
import os
import psycopg2
import bcrypt


#local imports
from database import sql_write
from models.users import all_users

DB_URL = os.environ.get("DATABASE_URL", "dbname=feedback_app")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Random string. Do not store keys in code!!'



# home
@app.route('/home')
@app.route('/')
def index():
    name = session.get('name')
    user_id = session.get('user_id')
    return render_template('index.html', name=name, user_id = user_id)

# login
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
    print(all_users)
    for user in users:  
        password_hash = user['password_hash']
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        print(password_hash, valid, password)
        if user['email'] == username and valid == True:
            session['email'] = username
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect('/')
        else:
            error_message = 'Email address or password is incorrect'
            return render_template('login.html', error_message = error_message, users = all_users())
    return " user not found"

# signup
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


# logout

# upload project
@app.route('/upload-project')
def uploadProject():
    return render_template('upload-project.html')

@app.route('/upload-project-action')
def uploadProjectAction():
    projectTitle = request.form.get('title')
    projectImage = request.form.get('projectImage')
    projectDescription = request.form.get('projectDescription')

    return render_template('upload-project.html')



if __name__ == "__main__":
    app.run(debug=True)