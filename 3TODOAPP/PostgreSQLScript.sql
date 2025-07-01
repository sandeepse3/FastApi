-- PostgreSQL script used to create a simple TODO application database schema
DROP TABLE IF EXISTS users;

-- By default these tables will be created in the public schema
CREATE TABLE users (
  id SERIAL,
  email varchar(200) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  hashed_password varchar(200) DEFAULT NULL,
  is_active boolean DEFAULT NULL,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS todos;

CREATE TABLE todos (
  id SERIAL,
  title varchar(200) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer  DEFAULT NULL,
  complete boolean  DEFAULT NULL,
  owner_id integer  DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- CREATE SCHEMA analytics;
INSERT INTO users (id, email, username, first_name, last_name, hashed_password, is_active, role)
VALUES 
(1, 'sandeepse3@gmail.com', 'Sandeep', 'Sandeep', 'Puttur', 'hashed_password_here', true, 'user');

INSERT INTO todos (id, title, description, priority, complete, owner_id)
VALUES 
(1, 'Go to the store', 'Pick up eggs', 5, false, 1),
(2, 'Cut the lawn', 'Grass is getting long', 3, false, 1),
(3, 'Feed the dog', 'He is getting hungry', 5, false, 1);

SELECT * FROM public.users ORDER BY id ASC;

SELECT * FROM public.todos ORDER BY id ASC;
