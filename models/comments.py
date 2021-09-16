from database import  sql_write, sql_select, sql_select_id, sql_delete, sql_select_all_id

def select_comment(params):
    project = sql_select_all_id('SELECT name, avatar, content FROM users INNER JOIN comments ON users.user_id= comments.user_id WHERE project_id=%s ORDER BY comment_id DESC',[params])
    print(project)
    return project

def insert_comment(content,project_id, user_id):
    query = sql_write('INSERT INTO comments(content, project_id, user_id) VALUES(%s, %s, %s)',
        [content, project_id, user_id])
    return query