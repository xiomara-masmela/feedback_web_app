from database import sql_write, sql_select, sql_select_id

def all_projects():
    results = sql_select('SELECT project_id, title, image, description, category, project_link from projects')
    total_projects = []
    for row in results:
        project = {
            'id': row[0],
            'title': row[1],
            'img_url': row[2],
            'description': row[3],
            'category': row[4],
            'link': row[5]
        }
        total_projects.append(project)
    return total_projects

def single_project():
    result = sql_select_id()
    return result

