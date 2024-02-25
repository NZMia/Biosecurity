from webApp import init_db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

def get_roles():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM roles')
  roles = cursor.fetchall()
  return roles

def get_user_by_email(email):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
  user = cursor.fetchone()
  return user

def create_user(email, password, role_id):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('INSERT INTO users (email, password, role_id) VALUES (%s, %s, %s)', (email, password, role_id))
  dbConnection.commit()

def create_employee(user_id, first_name, last_name):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('INSERT INTO employee (user_id, first_name, last_name) VALUES (%s, %s, %s)', (user_id, first_name, last_name))
  dbConnection.commit()