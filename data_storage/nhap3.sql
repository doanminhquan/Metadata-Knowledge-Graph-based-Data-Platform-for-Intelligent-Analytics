CREATE DATABASE IF NOT EXISTS school;
USE school;

CREATE TABLE departments (
    id VARCHAR(50) PRIMARY KEY, 
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NULL
);

CREATE TABLE faculties (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NULL
);

CREATE TABLE labs (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    faculty_id VARCHAR(50) NULL,
    description TEXT NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE SET NULL
);

CREATE TABLE employees (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email LIKE '%@%.%'),
    phone VARCHAR(50) NULL,
    department_id VARCHAR(50) NULL,
    faculty_id VARCHAR(50) NULL,
    lab_id VARCHAR(50) NULL,
    position VARCHAR(255) NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE SET NULL,
    FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE SET NULL
);

CREATE TABLE students (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email LIKE '%@%.%'),
    phone VARCHAR(50) NULL,
    faculty_id VARCHAR(50) NOT NULL,
    lab_id VARCHAR(50) NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE CASCADE
);

CREATE TABLE lecturers (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email LIKE '%@%.%'),
    phone VARCHAR(50) NULL,
    faculty_id VARCHAR(50) NULL,
    department_id VARCHAR(50) NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE SET NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE TABLE courses (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL
);

CREATE TABLE class_sections (
    id VARCHAR(50) PRIMARY KEY,
    course_id VARCHAR(50) NOT NULL,
    lecturer_id VARCHAR(50) NULL,
    schedule TEXT NULL, 
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(id) ON DELETE SET NULL
);

CREATE TABLE grades (
    student_id VARCHAR(50) NOT NULL,
    class_section_id VARCHAR(50) NOT NULL,
    score DECIMAL(5,2) NULL,
    PRIMARY KEY (student_id, class_section_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (class_section_id) REFERENCES class_sections(id) ON DELETE CASCADE
);
