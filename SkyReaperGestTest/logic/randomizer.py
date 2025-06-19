import secrets
import string

def generate_random_password(length: int = 16, use_symbols: bool = True) -> str:
    #"""Genera una contraseña aleatoria segura."""
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation
        
    if length < 4:
        raise ValueError("La longitud minima segura es 4 caracteres. ")
        
        
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password