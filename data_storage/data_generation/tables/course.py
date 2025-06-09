from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_courses(n=5):
    course_list = []
    generated_codes = set()
    
    subjects = [
        ("Triet hoc Mac-Lenin", "Marxist Philosophy"),
        ("Kinh te chinh tri Mac-Lenin", "Marxist Political Economy"),
        ("Chu nghia xa hoi khoa hoc", "Scientific Socialism"),
        ("Lich su Dang Cong san Viet Nam", "History of the Communist Party of Vietnam"),
        ("Tu tuong Ho Chi Minh", "Ho Chi Minh Ideology"),
        ("Toan cao cap", "Advanced Mathematics"),
        ("Vat ly dai cuong", "General Physics"),
        ("Hoa hoc dai cuong", "General Chemistry"),
        ("Sinh hoc dai cuong", "General Biology"),
        ("Tieng Anh chuyen nganh", "English for Specific Purposes")
    ]
    
    for i in range(n):
        while True:
            prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
            number = ''.join(random.choices(string.digits, k=4))
            course_code = f"{prefix}{number}"
            if course_code not in generated_codes:
                generated_codes.add(course_code)
                break
        
        subject = random.choice(subjects)
        course = {
            "course_code": course_code,
            "name": remove_accents(subject[0]),  
            "eng_name": subject[1]
        }
        course_list.append(course)
    
    return course_list
