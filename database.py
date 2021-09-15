import psycopg2
import os

DB_URL = os.environ.get("HEROKU_POSTGRESQL_TEAL_URL", "dbname=feedback_app")


def sql_select(query):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query)
  results = cur.fetchall()
  cur.close()
  conn.close()
  return results

def sql_select_id(query, params):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query,params)
  results = cur.fetchone()
  cur.close()
  conn.close()
  return results

def sql_select_user_project(query):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query)
  user = cur.fetchone()
  cur.close()
  conn.close()
  return user

def sql_write(query, params):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()


def sql_delete(query,params):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()


