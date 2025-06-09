from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_program_courses(n=10, program_codes=[], course_codes=[]):
    program_course_list = []
    generated_pairs = set()
    
    if not program_codes or not course_codes:
        raise ValueError("Please provide both program_codes and course_codes.")

    types = [
        'khoi kien thuc bo tro', 'khoi kien thuc chuyen nganh', 'khoi kien thuc chung cua nhom nganh',
        'khoi kien thuc nganh', 'khoi kien thuc co ban', 'khoi kien thuc dinh huong chuyen sau',
        'khoi kien thuc chung', 'khoi kien thuc thuc tap va tot nghiep', 'khoi kien thuc co so',
        'khoi kien thuc theo nhom nganh', 'khoi kien thuc nganh va bo tro', 'khoi kien thuc theo khoi nganh',
        'khoi kien thuc chung theo linh vuc', 'kien thuc bo tro', 'khoi kien thuc nganh tu chon'
    ]

    types = list(set(types))

    for i in range(n):
        while True:
            program_code = random.choice(program_codes)
            course_code = random.choice(course_codes)
            pair = (program_code, course_code)
            
            if pair not in generated_pairs:
                generated_pairs.add(pair)
                break

        program_course = {
            "program_code": program_code,
            "course_code": course_code,
            "type": random.choice(types)
        }
        program_course_list.append(program_course)
    
    return program_course_list
