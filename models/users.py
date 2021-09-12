from database import sql_write, sql_select, sql_select_id

def all_users():
    results = sql_select('SELECT user_id, email, name, password_hash, avatar, role from users')
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

def single_user():
    result = sql_select_id()
    return result