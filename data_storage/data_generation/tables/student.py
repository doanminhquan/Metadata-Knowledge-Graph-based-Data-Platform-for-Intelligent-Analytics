import random
import string

def generate_fake_students(n=5, class_codes = []):
    students = []
    generated_student_codes = set()

    for _ in range(n):
        while True:
            student_code = int(''.join(random.choices(string.digits, k=8)))
            if student_code not in generated_student_codes:
                generated_student_codes.add(student_code)
                break

        student = {
            "student_code": student_code,
            "class_code": random.choice(class_codes)
        }
        students.append(student)

    return students