from tables.course import generate_fake_courses
from tables.staff import generate_fake_staff
from tables.room import generate_fake_rooms
from tables.term import generate_fake_terms
from tables.program import generate_fake_programs
from tables.classs import generate_fake_classes
from tables.major import generate_fake_majors
from tables.student import generate_fake_students
from tables.course_section import generate_fake_course_sections
from tables.course_group import generate_fake_course_groups
from tables.course_group_detail import generate_fake_course_group_detail
from tables.enrollment import generate_fake_enrollments
from tables.graduate import generate_fake_graduates
from tables.program_course import generate_fake_program_courses
from tables.point import generate_fake_points
import mysql.connector

def generate():
    courses = generate_fake_courses(5)
    staffs = generate_fake_staff(5)
    terms = generate_fake_terms(4)
    rooms = generate_fake_rooms(10)
    majors = generate_fake_majors(5)
    programs = generate_fake_programs(5, [major.get('major_code') for major in majors])
    classes = generate_fake_classes(20, [program.get('program_code') for program in programs])
    students = generate_fake_students(100, [cls.get('class_code') for cls in classes])
    course_sections = generate_fake_course_sections(5, 
        [course.get('course_code') for course in courses], 
        [term.get('term_code') for term in terms])
    course_groups = generate_fake_course_groups(
        [course_section.get('course_section_code') for course_section in course_sections]
    )
    course_group_details = generate_fake_course_group_detail(
        course_group_codes=[course_group.get('course_group_code') for course_group in course_groups],
        room_codes=[room.get('room_code') for room in rooms],
        staff_codes=[staff.get('staff_code') for staff in staffs]
    )
    enrollments = generate_fake_enrollments(
        student_codes=[student.get('student_code') for student in students],
        course_group_codes=[course_group.get('course_group_code') for course_group in course_groups]
    )
    graduates = generate_fake_graduates(
        student_codes=[student.get('student_code') for student in students],
        program_codes=[program.get('program_code') for program in programs],
        term_codes=[term.get('term_code') for term in terms]
    )
    program_courses = generate_fake_program_courses(
        program_codes=[program.get('program_code') for program in programs],
        course_codes=[course.get('course_code') for course in courses]
    )
    points = generate_fake_points(
        student_codes=[student.get('student_code') for student in students],
        course_section_codes=[course_section.get('course_section_code') for course_section in course_sections],
        term_codes=[term.get('term_code') for term in terms]
    )

    conn = mysql.connector.connect(
        host='localhost',
        port=30306,
        user='root',
        password='123456',
        database='school'
    )
        
    try:
        conn.autocommit = False

        cursor = conn.cursor()

        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute('TRUNCATE TABLE course_group_detail')
        cursor.execute('TRUNCATE TABLE enrollment')
        cursor.execute('TRUNCATE TABLE graduate')
        cursor.execute('TRUNCATE TABLE point')
        cursor.execute('TRUNCATE TABLE program_course')
        cursor.execute('TRUNCATE TABLE course_group')
        cursor.execute('TRUNCATE TABLE course_section')
        cursor.execute('TRUNCATE TABLE student')
        cursor.execute('TRUNCATE TABLE staff')
        cursor.execute('TRUNCATE TABLE course')
        cursor.execute('TRUNCATE TABLE term')
        cursor.execute('TRUNCATE TABLE room')
        cursor.execute('TRUNCATE TABLE program')
        cursor.execute('TRUNCATE TABLE class')
        cursor.execute('TRUNCATE TABLE major')
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

        for item in staffs:
            query = "INSERT INTO staff(staff_code, staff_name) VALUES (%s, %s)"
            values = (item.get('staff_code'), item.get('staff_name'))
            cursor.execute(query, values)
        print('Insert staff successfully')

        for item in terms:
            query = "INSERT INTO term(term_code, term_name) VALUES (%s, %s)"
            values = (item.get('term_code'), item.get('term_name'))
            cursor.execute(query, values)
        print('Insert term successfully')

        for item in courses:
            query = "INSERT INTO course(course_code, `name`, eng_name) VALUES (%s, %s, %s)"
            values = (item.get('course_code'), item.get('name'), item.get('eng_name'))
            cursor.execute(query, values)
        print('Insert course successfully')

        for item in rooms:
            query = "INSERT INTO room(room_code, room_name, capacity) VALUES (%s, %s, %s)"
            values = (item.get('room_code'), item.get('room_name'), item.get('capacity'))
            cursor.execute(query, values)
        print('Insert room successfully')

        for item in majors:
            query = "INSERT INTO major(major_code, name) VALUES (%s, %s)"
            values = (item.get('major_code'), item.get('name'))
            cursor.execute(query, values)
        print('Insert major successfully')

        for item in programs:
            query = "INSERT INTO program(program_code, name, major_code) VALUES (%s, %s, %s)"
            values = (item.get('program_code'), item.get('name'), item.get('major_code'))
            cursor.execute(query, values)
        print('Insert program successfully')

        for item in classes:
            query = "INSERT INTO class(class_code, `name`, program_code, year_start) VALUES (%s, %s, %s, %s)"
            values = (item.get('class_code'), item.get('name'), item.get('program_code'), item.get('year_start'))
            cursor.execute(query, values)
        print('Insert class successfully')  

        for item in students:
            query = "INSERT INTO student(student_code, class_code) VALUES (%s, %s)"
            values = (item.get('student_code'), item.get('class_code'))
            cursor.execute(query, values)
        print('Insert student successfully')

        for item in course_sections:
            query = "INSERT INTO course_section(course_section_code, course_code, term_code) VALUES (%s, %s, %s)"
            values = (item.get('course_section_code'), item.get('course_code'), item.get('term_code'))
            cursor.execute(query, values)
        print('Insert course_section successfully')

        for item in course_groups:
            query = "INSERT INTO course_group(course_group_code, course_section_code, student_amount, type, group_order) VALUES (%s, %s, %s, %s, %s)"
            values = (item.get('course_group_code'), item.get('course_section_code'), item.get('student_amount'), item.get('type'), item.get('group_order'))
            cursor.execute(query, values)
        print('Insert course_group successfully')

        for item in course_group_details:
            query = "INSERT INTO course_group_detail(course_group_code, room_code, session_start, session_end, weekday, staff_code) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (item.get('course_group_code'), item.get('room_code'), item.get('session_start'), item.get('session_end'), item.get('weekday'), item.get('staff_code'))
            cursor.execute(query, values)
        print('Insert course_group_detail successfully')

        for item in enrollments:
            query = "INSERT INTO enrollment(student_code, course_group_code) VALUES (%s, %s)"
            values = (item.get('student_code'), item.get('course_group_code'))
            cursor.execute(query, values)
        print('Insert enrollment successfully')

        for item in graduates:
            query = "INSERT INTO graduate(student_code, program_code, term_code, `rank`, avg_score) VALUES (%s, %s, %s, %s, %s)"
            values = (item.get('student_code'), item.get('program_code'), item.get('term_code'), item.get('rank'), item.get('avg_score'))
            cursor.execute(query, values)
        print('Insert graduate successfully')

        for item in program_courses:
            query = "INSERT INTO program_course(program_code, course_code, type) VALUES (%s, %s, %s)"
            values = (item.get('program_code'), item.get('course_code'), item.get('type'))
            cursor.execute(query, values)
        print('Insert program_course successfully')

        for item in points:
            query = "INSERT INTO point(student_code, course_section_code, term_code, point_4, point_10) VALUES (%s, %s, %s, %s, %s)"
            values = (item.get('student_code'), item.get('course_section_code'), item.get('term_code'), item.get('point_4'), item.get('point_10'))
            cursor.execute(query, values)
        print('Insert point successfully')
    
        conn.commit()

    except Exception as e:
        print(f"error:{e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

generate()