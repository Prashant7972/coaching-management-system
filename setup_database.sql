-- MySQL Setup Script for Coaching Management System
-- Run this script in your MySQL client / terminal:
-- mysql -u root -p < setup_database.sql

CREATE DATABASE IF NOT EXISTS coaching_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Optional: Create a dedicated user for the coaching management system
-- Replace 'strong_password_here' with your secure password
CREATE USER IF NOT EXISTS 'coaching_user'@'localhost' IDENTIFIED BY 'Coaching@123';
GRANT ALL PRIVILEGES ON coaching_db.* TO 'coaching_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify database creation
SHOW DATABASES LIKE 'coaching_db';
