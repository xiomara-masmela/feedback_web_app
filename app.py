from flask import Flask, render_template, request, redirect, session
import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "dbname=feedback_app")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# home
@app.route('/home')
@app.route('/')
def index():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT 1', []) # Query to check that the DB connected
    conn.close()
    return render_template('index.html')

# login
@app.route('/login')
def login():
    return render_template('login.html')

# @app.route('/login_action', methods=['POST'])
# def loginAction():
#     #form
#     username = request.form.get('username')
#     password = request.form.get('password')
    
#     #db
#     users = all_users()
#     for user in users:  
#         password_hash = user['password_hash']
#         valid = bcrypt.checkpw(password.encode(), password_hash.encode())
#         print(password_hash, valid, password)
#         if user['email'] == username and valid == True:
#             session['email'] = username
#             session['user_id'] = user['id']
#             session['name'] = user['name']
#             return redirect('/')
#         else:
#             error_message = 'Email address or password is incorrect'
#             return render_template('login.jinja', error_message = error_message)
#     return " user not found"

# signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

# logout

# upload project
@app.route('/upload-project')
def uploadProject():
    return render_template('upload-project.html')



if __name__ == "__main__":
    app.run(debug=True)