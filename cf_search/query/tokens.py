from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

@dataclass
class CfToken:
    type_name: str
    content: Dict[str, Any]  # field values
    #foreign_keys: Dict[str, List[Any]]  # values that help us look up neighbors

def make_contest_token(raw_data) -> Optional[CfToken]:
    type_name = "Contest"

    content: Dict[str, Any] = {
        "name": raw_data["name"]
    }

    return CfToken(type_name, content)
