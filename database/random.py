import random
import string

def generate_unique_id(length=8) -> str:
    characters = string.ascii_letters + string.digits  # Буквы и цифры
    unique_id = ''.join(random.choice(characters) for _ in range(length))
    return unique_id
