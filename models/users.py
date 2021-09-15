from database import sql_write, sql_select, sql_select_id

# class User: 
#     def __init__(self,id, email, name, password_hash, avatar, role):
#         self.id=id
#         self.name = name   
#         self.email = email
#         self.password = password_hash
#         self.avatar = avatar,
#         self.role = role


    
def select_all_users():
    results = sql_select('SELECT user_id, email, name, password_hash, avatar, role FROM users')
    total_users = []
    for row in results:
        user = {
            'id': row[0],
            'email': row[1],
            'name': row[2],
            'password_hash': row[3],
            'avatar': row[4],
            'role': row[5]
        }
        total_users.append(user)
    return total_users

def create_user(email,name, password_hash, image, role):
    sql_write('INSERT INTO users(email, name, password_hash, avatar, role) VALUES(%s, %s, %s, %s, %s)',
        [email, name, password_hash, image, role ])

def select_user(user_id):
    user = sql_select_id('SELECT * FROM users WHERE user_id =%s', [user_id])
    return user

def select_user_email(email):
    user = sql_select_id('SELECT * FROM users WHERE email =%s', [email])
    return user


