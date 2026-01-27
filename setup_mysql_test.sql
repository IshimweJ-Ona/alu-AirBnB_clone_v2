-- AirBnB Clone DBStorage Setup

-- Main development database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Test database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create users
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant privileges
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

FLUSH PRIVILEGES;

-- Use test database for testing
USE hbnb_test_db;

-- -------------------------------
-- Create tables for DBStorage
-- -------------------------------

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id CHAR(60) PRIMARY KEY,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128)
);

-- States table
CREATE TABLE IF NOT EXISTS states (
    id CHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    id CHAR(60) PRIMARY KEY,
    state_id CHAR(60) NOT NULL,
    name VARCHAR(128) NOT NULL,
    FOREIGN KEY (state_id) REFERENCES states(id) ON DELETE CASCADE
);

-- Places table
CREATE TABLE IF NOT EXISTS places (
    id CHAR(60) PRIMARY KEY,
    city_id CHAR(60) NOT NULL,
    user_id CHAR(60) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    number_rooms INT DEFAULT 0,
    number_bathrooms INT DEFAULT 0,
    max_guest INT DEFAULT 0,
    price_by_night INT DEFAULT 0,
    latitude DOUBLE,
    longitude DOUBLE,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Amenities table
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(60) PRIMARY KEY,
    place_id CHAR(60) NOT NULL,
    user_id CHAR(60) NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
