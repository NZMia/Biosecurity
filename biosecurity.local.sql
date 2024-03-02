DROP SCHEMA IF EXISTS biosecurity;
CREATE SCHEMA biosecurity;
USE biosecurity;

CREATE TABLE IF NOT EXISTS state (
  id INT AUTO_INCREMENT PRIMARY KEY,
  state ENUM('active', 'inactive') NOT NULL
);


CREATE TABLE IF NOT EXISTS roles (
  id INT auto_increment PRIMARY KEY,
  role VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS positions (
  id INT auto_increment PRIMARY KEY,
  position VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
  id INT auto_increment PRIMARY KEY,
  department VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id INT auto_increment PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  role_id INT DEFAULT 3,
  state_id INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES roles(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE,
  FOREIGN KEY (state_id) REFERENCES state(id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
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


CREATE TABLE IF NOT EXISTS customer (
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

CREATE TABLE IF NOT EXISTS pests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img_id INT,
    common_name VARCHAR(255),
    scientific_name VARCHAR(255),
    description TEXT,
    distinctive_features TEXT,
    size VARCHAR(255),
    droppings TEXT,
    footprints TEXT,
    distribution TEXT,
    impacts TEXT,
    control_methods TEXT,
    state_id INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pest_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pest_id INT,
    image LONGBLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pest_id) REFERENCES pests(id)
    ON UPDATE CASCADE
	ON DELETE CASCADE
);

ALTER TABLE pests ADD FOREIGN KEY (img_id) REFERENCES pest_images(id) ON UPDATE CASCADE ON DELETE CASCADE;


INSERT INTO roles (role) VALUES ('Staff');
INSERT INTO roles (role) VALUES ('Admin');
INSERT INTO roles (role) VALUES ('Customer');

INSERT INTO departments (department) VALUES ('Customer Success');
INSERT INTO departments (department) VALUES ('Market');
INSERT INTO departments (department) VALUES ('IT');
INSERT INTO departments (department) VALUES ('HR');

INSERT INTO positions (position) VALUES ('Manager'), ('Front desk'),('Customer support'), ('Technical leader');
INSERT INTO state (state)
VALUES
  ('active'),
  ('inactive');
  
  
-- INSERT INTO pest_controller (user_id, first_name, last_name, address, phone) VALUES (29, 'mia', 'zhang', '63 nortons ', '021234848');

-- admin123: scrypt:32768:8:1$m4Ol75KV0cA66N4X$468ce636ee9db0fe648336511de4be1646744d02c8c235a4249cb480e3da330701d7c04301ffc3194c76dbcd04eab4600091ff5abb0e6eda965749cc1bf3bbcb  