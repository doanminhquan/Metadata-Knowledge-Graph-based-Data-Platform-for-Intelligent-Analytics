from faker import Faker
import random
import string
import unicodedata

faker = Faker()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_rank(avg_score):
    if avg_score >= 3.6:
        return 'Xuat sac' 
    elif avg_score >= 3.2:
        return 'Gioi'
    elif avg_score >= 2.8:
        return 'Kha'  
    else:
        return 'Trung binh'  

def generate_fake_graduates(n=10, student_codes=[], program_codes=[], term_codes=[]):
    graduate_list = []
    generated_keys = set()

    for i in range(n):
        while True:
            student_code = random.choice(student_codes)
            program_code = random.choice(program_codes)
            term_code = random.choice(term_codes)
            key = (student_code, program_code)
            
            if key not in generated_keys:
                generated_keys.add(key)
                break
        
        avg_score = round(random.uniform(2.0, 4.0), 2)  

        graduate = {
            "student_code": student_code,
            "program_code": program_code,
            "term_code": term_code,
            "rank": get_rank(avg_score),
            "avg_score": avg_score
        }
        graduate_list.append(graduate)
    
    return graduate_list
