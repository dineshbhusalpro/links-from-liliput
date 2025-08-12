import string
import random
import validators
from typing import Optional

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code using letters and digits"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_url(url: str) -> bool:
    """Validate if URL is properly formatted"""
    try:
        return validators.url(url)
    except:
        return False

def validate_custom_code(code: str, min_length: int = 3, max_length: int = 20) -> bool:
    """Validate custom short code format"""
    if not code:
        return False
    if len(code) < min_length or len(code) > max_length:
        return False
    return all(c.isalnum() or c in '-_' for c in code)