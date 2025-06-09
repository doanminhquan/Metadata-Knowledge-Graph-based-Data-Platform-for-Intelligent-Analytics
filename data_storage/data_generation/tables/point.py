from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_points(n=10, student_codes=[], course_section_codes = [], term_codes=[]):
    point_list = []
    generated_pairs = set()

    for i in range(n):
        while True:
            student_code = random.choice(student_codes)
            course_section_code = random.choice(course_section_codes)
            term_code = random.choice(term_codes)
            pair = (student_code, course_section_code, term_code)
            
            if pair not in generated_pairs:
                generated_pairs.add(pair)
                break

        point_4 = round(random.uniform(2.0, 4.0), 2)  
        point_10 = round(point_4 * 10 / 4, 2)

        point = {
            "student_code": student_code,
            "course_section_code": course_section_code,
            "term_code": term_code,
            "point_4": point_4,
            "point_10": point_10,
        }
        point_list.append(point)
    
    return point_list
