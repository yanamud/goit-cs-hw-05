DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    fullname VARCHAR(100), 
    email VARCHAR(100) UNIQUE
);

-- Table: status
DROP TABLE IF EXISTS status;

CREATE TABLE status (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(50) UNIQUE
);

-- Table: tasks
DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY, 
    title VARCHAR(100), 
    description TEXT,
    status_id INTEGER, 
    user_id INTEGER,
    	FOREIGN KEY (status_id) REFERENCES status (id) ON DELETE CASCADE ON UPDATE CASCADE,
    	FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
);