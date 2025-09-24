# app/utils/generate_entity_id.py
"""
Generate entity id.
class EtityType:
    TASK = "task"
    CATEGORY = "category"
~generate_entity_id(type: EntityType) -> str:
    Task: 3mixofrandomcapitalandsmallletters-2randomnumbers-3randommixofcapitalsmallletterand numbers
    category: 2randomcapitalletters-6randomnumbrs
"""
from enum import Enum
from random import choices
from string import ascii_letters, digits

class EntityType(Enum):
    TASK = "task"
    CATEGORY = "category"

def generate_entity_id(type: EntityType) -> str:
    """
    Generate entity ID based on entity type.
    
    TASK: 3 letters - 2 digits - 3 alphanumeric (e.g. Abc-42-Xy9)
    CATEGORY: 2 capital letters + 6 digits (e.g. AB123456)
    """
    if type == EntityType.TASK:
        letters = "".join(choices(ascii_letters, k=3))
        nums = "".join(choices(digits, k=2))
        mix = "".join(choices(ascii_letters + digits, k=3))
        return f"{letters}-{nums}-{mix}"
    
    elif type == EntityType.CATEGORY:
        caps = "".join(choices(ascii_letters.upper(), k=2))
        nums = "".join(choices(digits, k=6))
        return f"{caps}{nums}"
    
    else:
        raise ValueError(f"Invalid entity type: {type}")
