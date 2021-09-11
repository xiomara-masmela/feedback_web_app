import psycopg2

def sql_select(query):
  conn = psycopg2.connect("dbname=feedback_app")
  cur = conn.cursor()
  cur.execute(query)
  results = cur.fetchall()
  cur.close()
  conn.close()
  return results

def sql_select_one(query, id):
  conn = psycopg2.connect("dbname=feedback_app")
  cur = conn.cursor()
  cur.execute(query,id)
  results = cur.fetchone()
  cur.close()
  conn.close()
  return results

def sql_write(query, params):
  conn = psycopg2.connect("dbname=feedback_app")
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()