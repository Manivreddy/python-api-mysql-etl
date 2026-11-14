CREATE DATABASE IF NOT EXISTS etl_database;
USE etl_database;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    username VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(100),
    website VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS posts (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(500) NOT NULL,
    body TEXT,
    CONSTRAINT fk_posts_users
        FOREIGN KEY (user_id) REFERENCES users(id)
);
