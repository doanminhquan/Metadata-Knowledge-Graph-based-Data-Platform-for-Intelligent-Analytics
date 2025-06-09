from faker import Faker
import random
import unicodedata

faker = Faker('vi_VN')

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_staff(n=10):
    staff_list = []
    generated_codes = set()
    
    while len(staff_list) < n:
        staff_code = str(random.randint(100000000, 999999999)) 
        if staff_code in generated_codes:
            continue 
        generated_codes.add(staff_code)
        
        staff_name = remove_accents(faker.name())
        staff = {
            "staff_code": staff_code,
            "staff_name": staff_name
        }
        staff_list.append(staff)
    
    return staff_list