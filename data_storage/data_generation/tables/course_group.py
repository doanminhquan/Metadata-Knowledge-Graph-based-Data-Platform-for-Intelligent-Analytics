from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_course_groups(course_section_codes=[], n_per_section=1):
    course_group_list = []
    group_types = ["LT", "TH"] 

    for section_code in course_section_codes:
        for group_order in range(n_per_section):
            cleaned_section_code = remove_accents(section_code).replace(' ', '')
            course_group_code = f"{cleaned_section_code}_{group_order}"

            course_group_entry = {
                "course_group_code": course_group_code,
                "course_section_code": section_code,
                "student_amount": random.randint(10, 100),  
                "type": random.choice(group_types),
                "group_order": group_order
            }
            course_group_list.append(course_group_entry)

    return course_group_list

