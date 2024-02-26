from webApp import init_db
# from werkzeug.security import generate_password_hash, check_password_hash
# from .models import User

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

def creact_pest_controller(user_id, first_name, last_name):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('INSERT INTO pest_controller (user_id, first_name, last_name) VALUES (%s, %s, %s)', (user_id, first_name, last_name))
  dbConnection.commit()

def get_roles():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM roles')
  roles = cursor.fetchall()
  return roles

def get_employees_by_role(role_id):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM employee WHERE role_id = %s', (role_id,))
  employees = cursor.fetchall()
  return employees

def get_pest_controllers():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM pest_controller')
  pest_controllers = cursor.fetchall()
  return pest_controllers

def get_user_by_email(email):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
  user = cursor.fetchone()
  return user

def update_user_password_by_email(email, password):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('UPDATE users SET password = %s WHERE email = %s', (password, email))
  dbConnection.commit()

def update_employee_by_id(employee_id, **kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('UPDATE employee SET first_name = %s, last_name = %s WHERE id = %s', (kwargs['first_name'], kwargs['last_name'], employee_id))
  dbConnection.commit()

def update_pest_controller_by_id(pest_controller_id, **kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('UPDATE pest_controller SET first_name = %s, last_name = %s WHERE id = %s', (kwargs['first_name'], kwargs['last_name'], pest_controller_id))
  dbConnection.commit()

def update_pest_by_id(pest_id, **kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('UPDATE pest SET name = %s, description = %s WHERE id = %s', (kwargs['name'], kwargs['description'], pest_id))
  dbConnection.commit()
