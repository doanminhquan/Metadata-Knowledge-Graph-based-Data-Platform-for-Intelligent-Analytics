import random
import string

def generate_fake_course_sections(n=5, course_codes=[], term_codes=[]):
    course_sections = []
    generated_codes = set()

    for _ in range(n):
        while True:
            course_section_code = 'CSC' + ''.join(random.choices(string.digits, k=3))
            if course_section_code not in generated_codes:
                generated_codes.add(course_section_code)
                break

        course_section = {
            "course_section_code": course_section_code,
            "course_code": random.choice(course_codes),
            "term_code": str(random.choice(term_codes)) 
        }
        course_sections.append(course_section)

    return course_sections
