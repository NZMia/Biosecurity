from webApp import init_db
from flask_login import current_user

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

def create_pest_controller(user_id, first_name, last_name):
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

def get_positions():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM positions')
  positions = cursor.fetchall()
  return positions

def get_departments():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM departments')
  departments = cursor.fetchall()
  return departments

def get_employees_by_role(role_id):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT employee.* FROM employee JOIN users ON employee.user_id = users.id WHERE users.role_id = %s', (role_id,))
  employees = cursor.fetchall()
  return employees

def get_user_info_by_user_id():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  user_id = current_user.id
  role_id = current_user.role_id


  if role_id != 3:
    query = """
      SELECT 
          users.email AS user_email,
          roles.role AS user_role,
          departments.department AS department,
          positions.position AS position,
          employee.*
      FROM 
          employee
      JOIN 
          users ON employee.user_id = users.id
      JOIN 
          roles ON users.role_id = roles.id
      LEFT JOIN 
          positions ON employee.position_id = positions.id
      LEFT JOIN 
          departments ON employee.department_id = departments.id
      WHERE
          users.id = %s
      AND
          roles.id = %s;
    """
  else:
    query = """
      SELECT 
          users.email AS user_email,
          roles.role AS user_role,
          departments.department AS department,
          positions.position AS position,
          pest_controller.*
      FROM 
          pest_controller
      JOIN 
          user ON pest_controller.user_id = users.id
      JOIN 
          roles ON users.role_id = roles.id
      WHERE 
          users.id = %s
      AND
          user.id = %s;
    """
  
  cursor.execute(query, (role_id, user_id))

  user_info = cursor.fetchone()

  # Fetch column names
  column_names = [desc[0] for desc in cursor.description]

  # Create a dictionary with column names as keys and values from the tuple
  user_info_dict = dict(zip(column_names, user_info))
  return user_info_dict

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
