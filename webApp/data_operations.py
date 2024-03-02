from webApp import init_db
from flask_login import current_user

# Fetch relevant data from the database
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

def get_pests():
  dbConnection = init_db()
  cursor = dbConnection.cursor(dictionary=True)
  query = """
    SELECT 
      pests.*, 
      pest_images.image AS image
    FROM 
      pests
    JOIN 
      pest_images ON pests.img_id = pest_images.id
    WHERE
      pests.state_id = 1
  """
  cursor.execute(query)
  pests = cursor.fetchall()
  return pests

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
        users.state_id = 1
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
  cursor = dbConnection.cursor(dictionary=True)
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
          customer.*
      FROM 
          customer
      JOIN 
          user ON customer.user_id = users.id
      JOIN 
          roles ON users.role_id = roles.id
      WHERE 
          users.id = %s
      AND
          roles.id = %s;
    """
  
  cursor.execute(query, (user_id, role_id))

  user_info = cursor.fetchone()
  print(user_info)
  # # Fetch column names
  # column_names = [desc[0] for desc in cursor.description]

  # # Create a dictionary with column names as keys and values from the tuple
  # user_info_dict = dict(zip(column_names, user_info))
  return user_info

def get_customers():
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  query = """
    SELECT 
      customer.*,
      users.email AS email,
      roles.role AS role
    FROM 
      customer
    JOIN users ON customer.user_id = users.id
    JOIN roles ON users.role_id = roles.id
    WHERE 
      users.state_id = 1
  """
  cursor.execute(query)
  # Fetch all rows as tuples
  customers_tuples = cursor.fetchall()
  # Get column names
  column_names = [desc[0] for desc in cursor.description]
  # Convert each tuple to a dictionary using column names
  customers_dict_list = [
      dict(zip(column_names, customer))
      for customer in customers_tuples
  ]

  return customers_dict_list

def get_user_by_email(email):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
  user = cursor.fetchone()
  return user

def is_pest_exist(common_name, scientific_name):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT id FROM pests WHERE common_name = %s OR scientific_name = %s', (common_name, scientific_name))
  id = cursor.fetchone()
  return id

def is_pest_image_exist(pest_id, image):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  cursor.execute('SELECT id FROM pest_images WHERE pest_id = %s AND image = %s', (pest_id, image))
  id = cursor.fetchone()
  return id

# Create new 
def save_pest_image(image):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  query = """
    INSERT INTO pest_images (image)
    VALUES (%s)
  """
  cursor.execute(query, (image,))
  img_id = cursor.lastrowid
  dbConnection.commit()
  return img_id

def create_pest(**kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()

  common_name = kwargs.get('common_name')
  scientific_name = kwargs.get('scientific_name')
  description = kwargs.get('description')
  distinctive_features = kwargs.get('distinctive_features')
  size = kwargs.get('size')
  droppings = kwargs.get('droppings')
  footprints = kwargs.get('footprints')
  distribution = kwargs.get('distribution')
  impacts = kwargs.get('impacts')
  control_methods = kwargs.get('control_methods')
  image = kwargs.get('image')

  img_id = save_pest_image(image)
  cursor.execute('SELECT id FROM pests WHERE common_name = %s OR scientific_name = %s', (common_name, scientific_name))
  id = cursor.fetchone()
  print(id)
  if id:
    raise Exception('Pest already exist')
  else:
    query = """
      INSERT INTO pests (
        common_name, 
        scientific_name, 
        description, 
        distinctive_features, 
        size, 
        droppings, 
        footprints, 
        distribution, 
        impacts, 
        control_methods, 
        img_id)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    if img_id:
      cursor.execute(query, (
        common_name, 
        scientific_name, 
        description, 
        distinctive_features, 
        size, 
        droppings, 
        footprints, 
        distribution, 
        impacts, 
        control_methods, 
        img_id))
      # Get the last inserted ID from pests table
      pest_id = cursor.lastrowid

      # Update img_id in pest_images table
      cursor.execute("""
          UPDATE pest_images
          SET pest_id = %s
          WHERE id = %s
      """, (pest_id, img_id))

      dbConnection.commit()
    else:
      return None

# Create new user (can be employee or customer)
def create_user(**kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  user_query = """
    INSERT INTO users (email, password, role_id)
    VALUES (%s, %s, %s)
  """
  email = kwargs.get('email')
  password = kwargs.get('password')
  role_id = kwargs.get('role_id')

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

  if role_id != 3 and role_id != '3':
    employee_query = """
      INSERT INTO employee (user_id, department_id, position_id, first_name, last_name, work_phone)
      VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(employee_query, (user_id, department_id, position_id, first_name, last_name, work_phone))
  # INSERT INTO customer table
  else:
    customer_query = """
      INSERT INTO customer (user_id, first_name, last_name, address, phone)
      VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(customer_query, (user_id, first_name, last_name, address, phone))

  dbConnection.commit()

def add_pests_image(pest_id, image):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  query = """
    INSERT INTO pest_images (pest_id, image)
    VALUES (%s, %s)
  """
  cursor.execute(query, (pest_id, image))
  dbConnection.commit()

# Update user state and password
def update_user_password_by_email(email, password):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  
  cursor.execute('UPDATE users SET password = %s WHERE email = %s', (password, email))
  dbConnection.commit()

def update_user_status_by_id(user_id, state):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  query ="""
      UPDATE users
      SET state_id = (SELECT id FROM state WHERE state = %s)
      WHERE id = %s;
    """
  cursor.execute(query, (state, user_id))
  dbConnection.commit()

# Update employee by id
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
    """
    data = (
      kwargs['department_id'],
      kwargs['position_id'],
      kwargs['first_name'],
      kwargs['last_name'],
      kwargs['work_phone'],  # This is the role_id but I dont want to change
      employee_id
    )

    cursor.execute(query, data)
    dbConnection.commit()
  except Exception as e:
    print(f"Error in update_employee_by_id: {e}")
    raise e

# Update customer by id
def update_customer_by_id(user_id, **kwargs):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  try:
    query = """
      UPDATE customer
      JOIN users ON customer.user_id = users.id
      SET 
          customer.first_name = COALESCE(%s, customer.first_name),
          customer.last_name = COALESCE(%s, customer.last_name),
          customer.address = COALESCE(%s, customer.address),
          customer.phone = COALESCE(%s, customer.phone)
      WHERE
          customer.user_id = %s;
    """
    data = (
      kwargs['first_name'],
      kwargs['last_name'],
      kwargs['address'],
      kwargs['phone'],
      user_id
    )
    cursor.execute(query, data)
    dbConnection.commit()
  except Exception as e:
    print(f"Error in update_customer_by_id: {e}")
    raise e

# Update pest state by id
def update_pest_state_by_id(pest_id, state):
  dbConnection = init_db()
  cursor = dbConnection.cursor()
  query = """
    UPDATE pests
    SET state_id = (SELECT id FROM state WHERE state = %s)
    WHERE id = %s;
  """
  cursor.execute(query, (state, pest_id))
  dbConnection.commit()