from webApp import init_db
from flask_login import current_user

def create_user(**kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  user_query = """
    INSERT INTO users (email, password, role_id)
    VALUES (%s, %s, %s)
  """
  email = kwargs['email']
  password = kwargs['password']
  role_id = kwargs['role_id']

  # INSERT INTO users table
  cursor.execute(user_query, (email, password, role_id))
  user_id = cursor.lastrowid

  department_id = kwargs.get('department_id', None)
  position_id = kwargs.get('position_id', None)
  first_name = kwargs.get('first_name', None)
  last_name = kwargs.get('last_name', None)
  address = kwargs.get('address', None)
  work_phone = kwargs.get('work_phone', None)
  phone = kwargs.get('phone', None)

  # INSERT INTO employee table
  if role_id != 3:
    employee_query = """
      INSERT INTO employee (user_id, department_id, position_id, first_name, last_name, work_phone)
      VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(employee_query, (user_id, department_id, position_id, first_name, last_name, work_phone))

  # INSERT INTO pest_controller table
  else:
    pest_controller_query = """
      INSERT INTO pest_controller (user_id, first_name, last_name， address, phone)
      VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(pest_controller_query, (user_id, first_name, last_name, address, phone))
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
  try:
    cursor.execute('SELECT * FROM departments')
    departments = cursor.fetchall()
    return departments
  except Exception as e:
    print(f"Error in get_departments: {e}")
    return None 

def get_employees_by_role(role_id):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  query = """
    SELECT 
      employee.*, 
      users.email AS email, 
      users.role_id AS role_id,
      roles.*,
      departments.department,
      positions.position
    FROM 
        employee 
        JOIN users ON employee.user_id = users.id 
        JOIN roles ON users.role_id = roles.id
        LEFT JOIN departments ON employee.department_id = departments.id
        LEFT JOIN positions ON employee.position_id = positions.id
    WHERE 
        users.status = 'ACTIVE'
    AND
        users.role_id = %s
  """
  cursor.execute(query, (role_id,))
   # Fetch all rows as tuples
  employees_tuples = cursor.fetchall()

  # Get column names from the cursor description
  column_names = [desc[0] for desc in cursor.description]

  # Convert each tuple to a dictionary using column names
  employees = [dict(zip(column_names, employee)) for employee in employees_tuples]

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
  try:
    query = """
      UPDATE employee
      JOIN users ON employee.user_id = users.id
      JOIN roles ON users.role_id = roles.id
      LEFT JOIN positions ON employee.position_id = positions.id
      LEFT JOIN departments ON employee.department_id = departments.id
      SET 
          employee.department_id = COALESCE(%s, employee.department_id),
          employee.position_id = COALESCE(%s, employee.position_id),
          employee.first_name = COALESCE(%s, employee.first_name),
          employee.last_name = COALESCE(%s, employee.last_name),
          employee.work_phone = COALESCE(%s, employee.work_phone)
      WHERE
          employee.user_id = %s;

      UPDATE users
      SET
          users.role_id = COALESCE(%s, users.role_id)
      WHERE
          users.id = %s;

    """
    data = (
      kwargs['department_id'],
      kwargs['position_id'],
      kwargs['first_name'],
      kwargs['last_name'],
      kwargs['work_phone'],
      employee_id,
      kwargs['role'],  # This is the role_id but I dont want to change
      employee_id
    )
  
    cursor.execute(query, data)
    dbConnection.commit()
  except Exception as e:
    print(e)

def update_user_status_by_id(user_id, status):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('UPDATE users SET status = %s WHERE id = %s', (status, user_id))
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
