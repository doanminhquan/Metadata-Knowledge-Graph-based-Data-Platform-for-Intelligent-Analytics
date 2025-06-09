from faker import Faker
import random
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_course_group_detail(n=5, course_group_codes=[], room_codes=[], staff_codes=[]):
    course_group_detail_list = []

    for i in range(n):
        course_group_code = random.choice(course_group_codes)
        room_code = random.choice(room_codes)
        staff_code = random.choice(staff_codes)
        
        session_start = random.randint(1, 11)  
        session_end = session_start + random.randint(1, 2)
        
        if session_end > 12:  
            session_end = 12
        
        weekday = random.randint(2, 7)  

        chi_tiet = {
            "course_group_code": course_group_code,
            "room_code": room_code,
            "session_start": session_start,
            "session_end": session_end,
            "weekday": weekday,
            "staff_code": staff_code
        }
        course_group_detail_list.append(chi_tiet)

    return course_group_detail_list
