DROP SCHEMA IF EXISTS biosecurity;
CREATE SCHEMA biosecurity;
USE biosecurity;


CREATE TABLE IF NOT EXISTS roles (
  id INT auto_increment PRIMARY KEY,
  role VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS users (
  id INT auto_increment PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  status VARCHAR(50) DEFAULT 'ACTIVE',
  role_id INT DEFAULT 3,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES roles(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS positions (
  id INT auto_increment PRIMARY KEY,
  position VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS departments (
  id INT auto_increment PRIMARY KEY,
  department VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS employee (
  id INT auto_increment PRIMARY KEY,
  user_id INT NOT NULL,
  position_id INT,
  department_id INT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  work_phone VARCHAR(50),
  hired_at DATE NOT NULL DEFAULT (CURRENT_DATE),
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE,
  FOREIGN KEY (department_id) REFERENCES departments(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE,
  FOREIGN KEY (position_id) REFERENCES positions(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS pest_controller (
  id INT auto_increment PRIMARY KEY,
  user_id INT NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  address VARCHAR(255),
  joined_at DATE NOT NULL DEFAULT (CURRENT_DATE),
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

INSERT INTO roles (role) VALUES ('staff');
INSERT INTO roles (role) VALUES ('admin');
INSERT INTO roles (role) VALUES ('pest controller');

INSERT INTO departments (department) VALUES ('custom success');
INSERT INTO departments (department) VALUES ('market');
INSERT INTO departments (department) VALUES ('IT');
INSERT INTO departments (department) VALUES ('HR');

INSERT INTO positions (position) VALUES ('manager'), ('front desk'),('customer support'), ('technical lead');

-- admin123: scrypt:32768:8:1$m4Ol75KV0cA66N4X$468ce636ee9db0fe648336511de4be1646744d02c8c235a4249cb480e3da330701d7c04301ffc3194c76dbcd04eab4600091ff5abb0e6eda965749cc1bf3bbcb  