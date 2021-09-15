from database import  sql_write, sql_select, sql_select_id, sql_delete

def select_all_projects():
    results = sql_select('SELECT project_id, title, image, description, category, project_link from projects')
    total_projects = []
    for row in results:
        project = {
            'id': row[0],
            'title': row[1],
            'imgage': row[2],
            'description': row[3],
            'category': row[4],
            'link': row[5]
        }
        total_projects.append(project)
    return total_projects
def select_project(project_id):
    project =sql_select_id("SELECT project_id, title, image, description, category, project_link FROM projects WHERE project_id =(%s)", [project_id])
    return project
    
def edit_title(title, project_id):
    query = sql_write('UPDATE projects SET title=(%s) WHERE project_id=(%s)',[title, project_id])
    return query

def edit_image(image, project_id):
    query = sql_write('UPDATE projects SET image=(%s) WHERE project_id=(%s)',[image, project_id])
    return query

def edit_description(description, project_id):
    query = sql_write('UPDATE projects SET description=(%s) WHERE project_id=(%s)',[description, project_id])
    return query

def edit_category(category, project_id):
    query = sql_write('UPDATE projects SET category=(%s) WHERE project_id=(%s)',[category, project_id])
    return query

def edit_link(link, project_id):
    query = sql_write('UPDATE projects SET link=(%s) WHERE project_id=(%s)',[link, project_id])
    return query

def delete_project_id(project_id):
    delete_query = sql_delete('DELETE FROM projects WHERE project_id =(%s)',[project_id])
    return delete_query


