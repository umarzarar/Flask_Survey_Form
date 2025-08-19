-- schema.sql

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS auth_survey_app;
USE auth_survey_app;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Survey responses table
CREATE TABLE IF NOT EXISTS survey_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(20) NOT NULL,
    satisfaction_lab_sessions VARCHAR(50) NOT NULL,
    suggestions TEXT,
    preferred_language VARCHAR(50) NOT NULL,
    rating_lab_infrastructure INT,
    email VARCHAR(100) NOT NULL,
    programming_languages_known TEXT,
    satisfaction_level_lab_sessions VARCHAR(50) NOT NULL,
    favorite_ide VARCHAR(50) NOT NULL,
    preferred_lab_time VARCHAR(50) NOT NULL,
    additional_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
