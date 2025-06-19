import os 
from logic.auth import save_master_password, load_master_hash
from logic.config import HASH_PATH




def is_first_time_setup() -> bool:
    return load_master_hash() is None
    
def setup_master_password(password: str, confirm: str) -> bool:
    if password != confirm or not password:
        return False
        
    save_master_password(password)
    return True