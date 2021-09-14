import psycopg2
from app import DB_URL

def sql_select(query):
  conn = psycopg2.connect("DB_URL")
  cur = conn.cursor()
  cur.execute(query)
  results = cur.fetchall()
  cur.close()
  conn.close()
  return results

def sql_select_id(query, id):
  conn = psycopg2.connect("DB_URL")
  cur = conn.cursor()
  cur.execute(query,id)
  results = cur.fetchone()
  cur.close()
  conn.close()
  return results

def sql_select_user_project(query):
  conn = psycopg2.connect("DB_URL")
  cur = conn.cursor()
  cur.execute(query,id)
  user = cur.fetchone()
  cur.close()
  conn.close()
  return user

def sql_write(query, params):
  conn = psycopg2.connect("DB_URL")
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()