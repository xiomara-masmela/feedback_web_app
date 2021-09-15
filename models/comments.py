from database import  sql_write, sql_select, sql_select_id, sql_delete

def select_comment(project_id):
    project =sql_select_id("SELECT content, user_id FROM comments WHERE project_id =(%s)", [project_id])
    return project

def insert_comment(content,project_id, user_id):
    query = sql_write('INSERT INTO comments(content, project_id, user_id) VALUES(%s, %s, %s)',
        [content, project_id, user_id])
    return query