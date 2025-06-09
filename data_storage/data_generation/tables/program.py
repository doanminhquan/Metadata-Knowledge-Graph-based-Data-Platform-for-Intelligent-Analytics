from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_programs(n=5, major_codes=[]):
    program_list = []
    generated_codes = set()

    programs = [
        ("He thong thong tin", "7480104"),
        ("Ky thuat may tinh", "7480103"),
        ("Khoa hoc may tinh", "7480101"),
        ("Tri tue nhan tao", "7480107"),
        ("Mang may tinh va truyen thong", "7480102"),
        ("Cong nghe thong tin", "7480201")
    ]

    
    
    for i in range(n):
        while True:
            program_code = ''.join(random.choices(string.digits, k=3))  # VD: 123
            if program_code not in generated_codes:
                generated_codes.add(program_code)
                break
        major_code = random.choice(major_codes) if major_codes else None
        program_code = f"{major_code}_{program_code}"
        program = random.choice(programs)
        program_entry = {
            "program_code": program_code,
            "name": remove_accents(program[0]),
            "major_code": major_code
        }
        program_list.append(program_entry)
    
    return program_list
