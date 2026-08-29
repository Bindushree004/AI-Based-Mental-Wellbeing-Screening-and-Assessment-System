CREATE DATABASE IF NOT EXISTS mental_wellbeing_db;
USE mental_wellbeing_db;

ALTER TABLE assessments
ADD COLUMN age INT NULL,
ADD COLUMN gender VARCHAR(20) NULL,
ADD COLUMN occupation VARCHAR(100) NULL,
ADD COLUMN sleep_hours FLOAT NULL,
ADD COLUMN exercise_days_per_week INT NULL,
ADD COLUMN screen_time_hours FLOAT NULL;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assessments (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    age INT NULL,

    gender VARCHAR(20) NULL,

    occupation VARCHAR(100) NULL,

    sleep_hours FLOAT NULL,

    exercise_days_per_week INT NULL,

    screen_time_hours FLOAT NULL,

    status VARCHAR(50) NOT NULL DEFAULT 'started',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    completed_at TIMESTAMP NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS assessment_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL,
    question_id INT NOT NULL,
    response INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id)
);

CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT NOT NULL UNIQUE,
    score INT NULL,
    risk_level VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id)
);