CREATE DATABASE IF NOT EXISTS school;
USE school;

CREATE TABLE staff (
  staff_code VARCHAR(255),
  staff_name VARCHAR(255),
  PRIMARY KEY (staff_code)
);

CREATE TABLE term (
  term_code FLOAT,
  term_name VARCHAR(255),
  PRIMARY KEY (term_code)
);

CREATE TABLE course (
  course_code VARCHAR(255),
  name VARCHAR(255),
  eng_name VARCHAR(255),
  PRIMARY KEY (course_code)
);

CREATE TABLE room (
  room_code INT,
  room_name VARCHAR(255),
  PRIMARY KEY (room_code)
);

CREATE TABLE program (
  program_code VARCHAR(255),
  name VARCHAR(255),
  PRIMARY KEY (program_code)
);

CREATE TABLE class (
  class_code VARCHAR(255),
  name VARCHAR(255),
  PRIMARY KEY (class_code)
);

CREATE TABLE major (
  major_code VARCHAR(255),
  name VARCHAR(255),
  PRIMARY KEY (major_code)
);


CREATE TABLE student (
  student_code INT,
  full_name VARCHAR(255),
  gender VARCHAR(255),
  dob VARCHAR(255),
  class_code VARCHAR(255),
  program_code VARCHAR(255),
  major_code VARCHAR(255),
  PRIMARY KEY (student_code),
  FOREIGN KEY (class_code) REFERENCES class(class_code),
  FOREIGN KEY (program_code) REFERENCES program(program_code),
  FOREIGN KEY (major_code) REFERENCES major(major_code)
);

CREATE TABLE course_section (
  course_section_code VARCHAR(255),
  course_code VARCHAR(255),
  term_code FLOAT,
  PRIMARY KEY (course_section_code),
  FOREIGN KEY (course_code) REFERENCES course(course_code),
  FOREIGN KEY (term_code) REFERENCES term(term_code)
);

CREATE TABLE course_group (
  course_group_code VARCHAR(255),
  course_section_code VARCHAR(255),
  student_amount FLOAT,
  type VARCHAR(255),
  group_order FLOAT,
  PRIMARY KEY (course_group_code),
  FOREIGN KEY (course_section_code) REFERENCES course_section(course_section_code)
);

CREATE TABLE course_group_detail (
  course_group_code VARCHAR(255),
  room_code INT,
  session_start INT,
  session_end INT,
  weekday INT,
  staff_code VARCHAR(255),
  FOREIGN KEY (course_group_code) REFERENCES course_group(course_group_code),
  FOREIGN KEY (room_code) REFERENCES room(room_code),
  FOREIGN KEY (staff_code) REFERENCES staff(staff_code)
);

CREATE TABLE enrollment (
  student_code INT,
  course_group_code VARCHAR(255),
  FOREIGN KEY (student_code) REFERENCES student(student_code),
  FOREIGN KEY (course_group_code) REFERENCES course_group(course_group_code)
);

CREATE TABLE graduate (
  student_code FLOAT,
  program_code VARCHAR(255),
  term_code FLOAT,
  rank VARCHAR(255),
  avg FLOAT,
  FOREIGN KEY (program_code) REFERENCES program(program_code),
  FOREIGN KEY (term_code) REFERENCES term(term_code)
);



CREATE TABLE program_course (
  program_code VARCHAR(255),
  course_code VARCHAR(255),
  FOREIGN KEY (program_code) REFERENCES program(program_code),
  FOREIGN KEY (course_code) REFERENCES course(course_code)
);


CREATE TABLE point (
  student_code INT,
  course_code VARCHAR(255),
  term_code FLOAT,
  avg FLOAT,
  FOREIGN KEY (student_code) REFERENCES student(student_code),
  FOREIGN KEY (course_code) REFERENCES course(course_code),
  FOREIGN KEY (term_code) REFERENCES term(term_code)
);


