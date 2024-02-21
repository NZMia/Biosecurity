DROP SCHEMA IF EXISTS biosecurity;
CREATE SCHEMA biosecurity;
USE biosecurity;

/*===============================USER===============================*/
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  pwd VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  status VARCHAR(10) DEFAULT 'ACTIVE'
);

/*===============================ROLE===============================*/
CREATE TABLE IF NOT EXISTS role (
  id SERIAL PRIMARY KEY,
  role VARCHAR(255) NOT NULL
);

/*===============================POSITION===============================*/
CREATE TABLE IF NOT EXISTS position (
  id SERIAL PRIMARY KEY,
  position VARCHAR(255) NOT NULL
);

/*===============================DEPARTMENT===============================*/
CREATE TABLE IF NOT EXISTS department (
  id SERIAL PRIMARY KEY,
  department VARCHAR(255) NOT NULL
);

-- NOT BUILD YET
/*===============================EMPLOYEE===============================*/
CREATE TABLE IF NOT EXISTS employee (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  position_id INT NOT NULL,
  department_id INT NOT NULL,
  role_id INT NOT NULL,
  hired_at DATE,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  work_phone VARCHAR(50) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (department_id) REFERENCES department(id),
  FOREIGN KEY (position_id) REFERENCES position(id),
  FOREIGN KEY (role_id) REFERENCES role(id)
);

/*===============================PEST CONTROLLER===============================*/
CREATE TABLE IF NOT EXISTS pest_controller (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  address VARCHAR(255) NOT NULL,
  joined_at DATE,
  FOREIGN KEY (user_id) REFERENCES user(id)
);

