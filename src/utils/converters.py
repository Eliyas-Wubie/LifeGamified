from typing import Any

def orm_to_name_value(orms:Any)->list[dict[str,float]]:
    
    return [{orm.name:orm.load} for orm in orms]