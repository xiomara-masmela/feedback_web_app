from database import sql_write, sql_select, sql_select_id

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

def create_new_user(email,name, password_hash, image, role):
    query = sql_write('INSERT INTO users(email, name, password_hash, avatar, role) VALUES(%s, %s, %s, %s, %s)',
        [email, name, password_hash, image, role ])
    return query

