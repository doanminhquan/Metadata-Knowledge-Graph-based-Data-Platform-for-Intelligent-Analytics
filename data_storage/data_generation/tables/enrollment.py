from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_enrollments(n=10, student_codes=[], course_group_codes=[]):
    enrollment_list = []
    generated_pairs = set()

    for i in range(n):
        while True:
            student_code = random.choice(student_codes)
            course_group_code = random.choice(course_group_codes)
            pair = (student_code, course_group_code)
            
            if pair not in generated_pairs:
                generated_pairs.add(pair)
                break

        enrollment = {
            "student_code": student_code,
            "course_group_code": course_group_code
        }
        enrollment_list.append(enrollment)
    
    return enrollment_list
