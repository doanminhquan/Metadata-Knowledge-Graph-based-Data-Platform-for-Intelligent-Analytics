import mysql.connector
import time

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "port": "30306",
    "user": "root",
    "password": "123456",
    "database": "school",
}

# SQL commands to execute
SQL_SCRIPT = """
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM point;
DELETE FROM program_course;
DELETE FROM graduate;
DELETE FROM enrollment;
DELETE FROM course_group_detail;
DELETE FROM course_group;
DELETE FROM course_section;
DELETE FROM student;
DELETE FROM major;
DELETE FROM class;
DELETE FROM program;
DELETE FROM room;
DELETE FROM term;
DELETE FROM course;
DELETE FROM staff;

INSERT INTO staff (staff_code, staff_name) VALUES
('EMP001', 'John Doe'),
('EMP002', 'Alice Johnson'),
('EMP003', 'Bob Williams');

INSERT INTO course (course_code, name, eng_name) VALUES
('CRS001', 'Machine Learning', 'Machine Learning'),
('CRS002', 'Cyber Security', 'Cyber Security'),
('CRS003', 'Blockchain', 'Blockchain');

INSERT INTO term (term_code, term_name) VALUES
('TERM001', 'Semester 1'),
('TERM002', 'Semester 2');

INSERT INTO room (room_code, room_name) VALUES
(101, 'Room A'),
(102, 'Room B');

INSERT INTO program (program_code, name) VALUES
('PRG001', 'Software Engineering');

INSERT INTO class (class_code, name) VALUES
('CLS001', 'SE Class 1');

INSERT INTO major (major_code, name) VALUES
('MAJ001', 'Computer Science');

INSERT INTO student (student_code, class_code) VALUES
(1, 'CLS001'),
(2, 'CLS001');

INSERT INTO course_section (course_section_code, course_code, term_code) VALUES
('SEC001', 'CRS001', 'TERM001'),
('SEC002', 'CRS002', 'TERM001');

INSERT INTO course_group (course_group_code, course_section_code, student_amount, type, group_order) VALUES
('GRP001', 'SEC001', 30, 'Lecture', 1),
('GRP002', 'SEC002', 25, 'Lab', 1);

INSERT INTO course_group_detail (course_group_code, room_code, session_start, session_end, weekday, staff_code) VALUES
('GRP001', 101, 1, 2, 2, 'EMP001'),
('GRP002', 102, 3, 4, 4, 'EMP002');

INSERT INTO enrollment (student_code, course_group_code) VALUES
(1, 'GRP001'),
(2, 'GRP002');

INSERT INTO graduate (student_code, program_code, term_code, `rank`, avg_score) VALUES
(1, 'PRG001', 'TERM001', 'Excellent', 8.5),
(2, 'PRG001', 'TERM001', 'Good', 7.8);

INSERT INTO program_course (program_code, course_code, `type`) VALUES
('PRG001', 'CRS001', 'aaa'),
('PRG001', 'CRS002', 'aaa');

INSERT INTO point (student_code, course_code, term_code, avg_score) VALUES
(1, 'CRS001', 'TERM001', 8.5),
(2, 'CRS002', 'TERM001', 9.0);

DELETE FROM point;
DELETE FROM program_course;
DELETE FROM graduate;
DELETE FROM enrollment;
DELETE FROM course_group_detail;
DELETE FROM course_group;
DELETE FROM course_section;
DELETE FROM student;
DELETE FROM major;
DELETE FROM class;
DELETE FROM program;
DELETE FROM room;
DELETE FROM term;
DELETE FROM course;
DELETE FROM staff;

SET FOREIGN_KEY_CHECKS = 1;

"""

def connect_and_execute():
    """Connect to MySQL and execute the SQL script."""
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            print("✅ Connected to MySQL")

            # Execute SQL statements
            for statement in SQL_SCRIPT.split(";"):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

            # Commit changes
            conn.commit()
            print("✅ SQL script executed successfully!")

            # Close connection
            cursor.close()
            conn.close()
            break
        except mysql.connector.Error as e:
            print(f"⚠️ Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)  # Wait and retry if MySQL is not ready

if __name__ == "__main__":
    connect_and_execute()
