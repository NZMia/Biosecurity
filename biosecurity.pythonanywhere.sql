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
VALUES ('admin@biosecurity.co.nz', 'scrypt:32768:8:1$ag4HTO6GachMQuyn$fd4304001c25127e473fc0241761abf9dd4cb54c663066e2f52e94807bc47948f7c17254e78d80bd78ecbfca5d658cd22748e387da63c42f862486a6fe3e3be3', 2);

-- Insert Staff Users
INSERT INTO users (email, password, role_id) 
VALUES 
  ('staff1@biosecurity.co.nz', 'scrypt:32768:8:1$43wnQTlQhdFFI6nC$d94a54fadbe745da9680c99dc8689ad0385a75b660e1e88611beb184b324ac1f05dbbdc4570dae98583785814af8a16b6037299db4874e4e1903a8a821c744af', 1),
  ('staff2@biosecurity.co.nz', 'scrypt:32768:8:1$43wnQTlQhdFFI6nC$d94a54fadbe745da9680c99dc8689ad0385a75b660e1e88611beb184b324ac1f05dbbdc4570dae98583785814af8a16b6037299db4874e4e1903a8a821c744af', 1),
  ('staff3@biosecurity.co.nz', 'scrypt:32768:8:1$43wnQTlQhdFFI6nC$d94a54fadbe745da9680c99dc8689ad0385a75b660e1e88611beb184b324ac1f05dbbdc4570dae98583785814af8a16b6037299db4874e4e1903a8a821c744af', 1);

-- Insert employee 
INSERT INTO employee (user_id, first_name, last_name)
VALUES
	(1, 'Nora', 'Wang'),
	(2, 'Harold', 'Zhang'),
	(3, 'Luna', 'Wang'),
	(4, 'Mia', 'Zhang')