import random

def remove_accents(input_str):
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_majors(n=5):
    major_list = []
    generated_codes = set()

    majors = [
        ("Ky thuat dieu khien va tu dong hoa", "11"),
        ("Cong nghe thong tin", "12"),
        ("He thong thong tin", "12"),
        ("Ky thuat phan mem", "12"),
        ("Tri tue nhan tao", "12"),
        ("Dien tu vien thong", "11"),
        ("Co dien tu", "11"),
        ("Ky thuat may tinh", "12"),
        ("Mang may tinh va truyen thong du lieu", "12"),
        ("Bao mat thong tin", "12")
    ]

    for i in range(n):
        while True:
            major_code = ''.join(random.choices('0123456789', k=7))  # VD: 7520216
            if major_code not in generated_codes:
                generated_codes.add(major_code)
                break

        major = random.choice(majors)

        major_entry = {
            "major_code": major_code,
            "name": remove_accents(major[0])
        }
        major_list.append(major_entry)

    return major_list