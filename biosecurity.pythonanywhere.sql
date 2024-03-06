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
)ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE pests ADD FOREIGN KEY (img_id) REFERENCES pest_images(id) ON UPDATE CASCADE ON DELETE CASCADE;


INSERT INTO roles (role) VALUES ('Staff');
INSERT INTO roles (role) VALUES ('Admin');
INSERT INTO roles (role) VALUES ('Customer');

INSERT INTO departments (department) VALUES ('Customer Success');
INSERT INTO departments (department) VALUES ('Market');
INSERT INTO departments (department) VALUES ('IT');
INSERT INTO departments (department) VALUES ('HR');

INSERT INTO positions (position) VALUES ('Manager'), ('Front desk'),('Customer support'), ('Technical leader');
INSERT INTO state (state) VALUES ('active'),('inactive');

-- Insert Admin User
INSERT INTO users (email, password, role_id) 
VALUES ('admin@biosecurity.co.nz', 'scrypt:32768:8:1$IH8e6yRLPq5TCo64$4cfc75c5daf26761ba3e3b4839911d4857da991ee249cb4144ba9d3a57036495320f122ea488ab3aed54b9d0d49571367bfb361606be2ca34864fa66c22b6a35', 2);

-- Insert Staff Users
INSERT INTO users (email, password, role_id) 
VALUES 
  ('staff1@biosecurity.co.nz', 'scrypt:32768:8:1$UXGHjf1wQ4PaOygP$17aabc240f09a50b7684e58ee4977c10bbee0ca5fdfc78999999a9f262a0f064ad25f77a956f9a5086303c31fdaa730cd3232155e88c3acbb0f2d36702e2952a', 1),
  ('staff2@biosecurity.co.nz', 'scrypt:32768:8:1$UXGHjf1wQ4PaOygP$17aabc240f09a50b7684e58ee4977c10bbee0ca5fdfc78999999a9f262a0f064ad25f77a956f9a5086303c31fdaa730cd3232155e88c3acbb0f2d36702e2952a', 1),
  ('staff3@biosecurity.co.nz', 'scrypt:32768:8:1$UXGHjf1wQ4PaOygP$17aabc240f09a50b7684e58ee4977c10bbee0ca5fdfc78999999a9f262a0f064ad25f77a956f9a5086303c31fdaa730cd3232155e88c3acbb0f2d36702e2952a', 1);

-- Insert Pest controller Users
INSERT INTO users (email, password, role_id) 
VALUES 
  ('customer1@biosecurity.co.nz', 'scrypt:32768:8:1$ig0Kzo3m5MxI8h3b$008002fbfc61109efedc94f0b5328ca5c00e5b4d7c900a385386873714e1c7f12c9e865c5f7f19b24d08308f25ad3e46a44af3e8276e309b4a9e3bd1b2d5caa2', 3),
  ('customer2@biosecurity.co.nz', 'scrypt:32768:8:1$ig0Kzo3m5MxI8h3b$008002fbfc61109efedc94f0b5328ca5c00e5b4d7c900a385386873714e1c7f12c9e865c5f7f19b24d08308f25ad3e46a44af3e8276e309b4a9e3bd1b2d5caa2', 3),
  ('customer3@biosecurity.co.nz', 'scrypt:32768:8:1$ig0Kzo3m5MxI8h3b$008002fbfc61109efedc94f0b5328ca5c00e5b4d7c900a385386873714e1c7f12c9e865c5f7f19b24d08308f25ad3e46a44af3e8276e309b4a9e3bd1b2d5caa2', 3),
  ('customer4@biosecurity.co.nz', 'scrypt:32768:8:1$ig0Kzo3m5MxI8h3b$008002fbfc61109efedc94f0b5328ca5c00e5b4d7c900a385386873714e1c7f12c9e865c5f7f19b24d08308f25ad3e46a44af3e8276e309b4a9e3bd1b2d5caa2', 3),
  ('customer5@biosecurity.co.nz', 'scrypt:32768:8:1$ig0Kzo3m5MxI8h3b$008002fbfc61109efedc94f0b5328ca5c00e5b4d7c900a385386873714e1c7f12c9e865c5f7f19b24d08308f25ad3e46a44af3e8276e309b4a9e3bd1b2d5caa2', 3);

-- Insert employee 
INSERT INTO employee (user_id, first_name, last_name)
VALUES
	(1, 'NoraA', 'Wang'),
	(2, 'HaroldS', 'Zhang'),
	(3, 'LunaS', 'Wang'),
	(4, 'MiaS', 'Zhang');
    
-- Insert customer
INSERT INTO customer (user_id, first_name, last_name)
VALUES
	(5, 'NoraC', 'Wang'),
	(6, 'HaroldC', 'Zhang'),
	(7, 'LunaC', 'Wang'),
	(8, 'MiaC', 'Zhang'),
  (9, 'John', 'Zhang');
