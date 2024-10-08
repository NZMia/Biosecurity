from flask_login import current_user
from webApp import get_db

# Get all roles
def get_roles():
  connection = get_db()
  cursor = connection.cursor(dictionary=True)

  cursor.execute('SELECT * FROM roles')
  roles = cursor.fetchall()
  
  return roles

# Get all positions
def get_positions():
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  cursor.execute('SELECT * FROM positions')
  positions = cursor.fetchall()
  
  return positions

# Get all departments
def get_departments():
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  try:
    cursor.execute('SELECT * FROM departments')
    departments = cursor.fetchall()
    
    return departments
  except Exception as e:
    print(f"Error in get_departments: {e}")
    return None 

# Get all states
def get_pests():
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
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
  for pest in pests:
    pest_id = pest['id']
    other_images = get_pest_images(pest_id)
    pest['other_images'] = other_images

    if 'image' in pest:
      pest['image'] = pest['image'].decode('utf-8')
  
  return pests

# Get all customers
def get_customers(): 
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
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
  customers= cursor.fetchall()
  
  return customers

# Get all employees by different roles
def get_employees_by_role(role_id):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
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
  employees = cursor.fetchall()
  
  return employees

# Get one pest by id
def get_pest(pest_id):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  query = """
    SELECT * FROM pests WHERE pests.id = %s
  """
  cursor.execute(query, (pest_id,))
  pest = cursor.fetchone()
  if pest:
    other_images = get_pest_images(pest_id)
    pest['other_images'] = other_images
  
  return pest

# Get all images of a pest
def get_pest_images(pest_id):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  query = """
    SELECT 
      pest_images.id,
      pest_images.image
    FROM 
      pest_images
    WHERE
      pest_images.pest_id = %s
  """
  cursor.execute(query, (pest_id,))
  pest_images = cursor.fetchall()
  
  return pest_images

# Get current authenticated user( for session validation)
def get_current_user():

  connection = get_db()
  cursor = connection.cursor(dictionary=True)
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
          users ON customer.user_id = users.id
      JOIN 
          roles ON users.role_id = roles.id
      WHERE 
          users.id = %s
      AND
          roles.id = %s;
    """
  
  cursor.execute(query, (user_id, role_id))

  user_info = cursor.fetchone()

  return user_info

# Get user by email (used for login/password reset...)
def get_user_by_email(email):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
  user = cursor.fetchone()
  
  return user

# Get user by id
def get_user_by_id(user_id):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
  user = cursor.fetchone()
  
  return user

# Check if pest exist
def is_pest_exist(common_name, scientific_name):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  cursor.execute('SELECT id FROM pests WHERE common_name = %s OR scientific_name = %s', (common_name, scientific_name))
  id = cursor.fetchone()
  
  return id

def is_pest_image_exist(pest_id, image):
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  cursor.execute('SELECT id FROM pest_images WHERE pest_id = %s AND image = %s', (pest_id, image))
  id = cursor.fetchone()
  
  return id

# Create and Save pest primary image due to the fact that pest can have multiple images, and pest_images and pests tables are related, so we need to save the primary image first, get the last inserted id and insert it into pests table
def save_pest_image(image):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  query = """
    INSERT INTO pest_images (image)
    VALUES (%s)
  """
  cursor.execute(query, (image,))
  img_id = cursor.lastrowid
  
  return img_id

# Create new pest
def create_pest(**kwargs):
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)

  try: 
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
      else:
        raise Exception('Error: Image not saved')
  except Exception as e:
    print(f"Error in create_pest: {e}")
    raise e
  
    

# Create new user (can be employee or customer)
def create_user(**kwargs):
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  try:
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
  except Exception as e:
    print(f"Error in create_user: {e}")
    raise e
  
    

# Create new pest image, not primary
def add_pests_image(pest_id, image):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  try:
    query = """
      INSERT INTO pest_images (pest_id, image)
      VALUES (%s, %s)
    """
    cursor.execute(query, (pest_id, image))
  except Exception as e:
    print(f"Error in add_pests_image: {e}")
    raise e
  
    

# Update user password
def update_user_password_by_email(email, password):
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  try:
    cursor.execute('UPDATE users SET password = %s WHERE email = %s', (password, email))
  except Exception as e:
    print(f"Error in update_user_password_by_email: {e}")
    raise e
  
    

# Update user state by id
def update_user_status_by_id(user_id, state):
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  try:
    query ="""
        UPDATE users
        SET state_id = (SELECT id FROM state WHERE state = %s)
        WHERE id = %s;
      """
    cursor.execute(query, (state, user_id))
  except Exception as e:
    print(f"Error in update_user_status_by_id: {e}")
    raise e
  
    

# Update employee by id
def update_employee_by_id(employee_id, **kwargs):
  
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
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
  except Exception as e:
    print(f"Error in update_employee_by_id: {e}")
    raise e
  
    

# Update customer by id
def update_customer_by_id(user_id, **kwargs):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
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
  except Exception as e:
    print(f"Error in update_customer_by_id: {e}")
    raise e
  
    

# Update pest state by id
def update_pest_state_by_id(pest_id, state):
  try:
    
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    query = """
      UPDATE pests
      SET state_id = (SELECT id FROM state WHERE state = %s)
      WHERE id = %s;
    """
    cursor.execute(query, (state, pest_id))
  except Exception as e:
    print(f"Error in update_pest_state_by_id: {e}")
    raise e
  
    

# Update pest
def update_pest_by_id(pest_id, **kwargs):
  connection = get_db()
  cursor = connection.cursor(dictionary=True)
  
  try:
    query = """
      UPDATE pests
      SET 
        img_id = COALESCE(%s, img_id),
        common_name = COALESCE(%s, common_name),
        scientific_name = COALESCE(%s, scientific_name),
        description = COALESCE(%s, description),
        distinctive_features = COALESCE(%s, distinctive_features),
        size = COALESCE(%s, size),
        droppings = COALESCE(%s, droppings),
        footprints = COALESCE(%s, footprints),
        distribution = COALESCE(%s, distribution),
        impacts = COALESCE(%s, impacts),
        control_methods = COALESCE(%s, control_methods)
      WHERE
        id = %s;
    """
    data = (
      kwargs['img_id'],
      kwargs['common_name'],
      kwargs['scientific_name'],
      kwargs['description'],
      kwargs['distinctive_features'],
      kwargs['size'],
      kwargs['droppings'],
      kwargs['footprints'],
      kwargs['distribution'],
      kwargs['impacts'],
      kwargs['control_methods'],
      pest_id
    )
    cursor.execute(query, data)
  except Exception as e:
    raise e
  
    