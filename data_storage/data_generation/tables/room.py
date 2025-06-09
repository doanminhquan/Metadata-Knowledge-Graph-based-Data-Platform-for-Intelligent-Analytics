from faker import Faker
import random
import unicodedata

faker = Faker('vi_VN')

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_fake_rooms(n=10):
    room_list = []
    generated_codes = set()

    while len(room_list) < n:
        room_code = random.randint(100, 999) 
        if room_code in generated_codes:
            continue
        generated_codes.add(room_code)

        building_code = random.choice(['GĐ1', 'GĐ2', 'GĐ3', 'GĐ4', 'G3', 'E5'])
        location_code = remove_accents(faker.city())[:2].upper()
        room_name = f"{random.randint(100, 999)}-{building_code}-{location_code}"

        capacity = random.choice([30, 50, 80, 100, 120, 150])

        room = {
            "room_code": room_code,
            "room_name": room_name,
            "capacity": capacity
        }
        room_list.append(room)

    return room_list
