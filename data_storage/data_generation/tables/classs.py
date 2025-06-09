import random
import string

def generate_fake_classes(n=5, program_codes=[]):
    class_list = []
    generated_codes = set()
    
    for i in range(n):
        program_code = random.choice(program_codes)
        year_start = random.randint(2015, 2025)  
        year_start = 2021
        khoa = 55 + (year_start - 2010)         

        while True:
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            class_code = f"QH-{year_start}-I/CQ-{suffix}"
            if class_code not in generated_codes:
                generated_codes.add(class_code)
                break

        name = f"K{khoa}{suffix}"  

        class_entry = {
            "program_code": program_code,
            "class_code": class_code,
            "name": name,
            "year_start": year_start
        }
        class_list.append(class_entry)
    
    return class_list
