from pydantic import BaseModel
from typing import List, Any, Dict

class Slot(BaseModel):
    name: str
    type: str
    required: bool = True
    default: Any = None

class IntentSchema(BaseModel):
    name: str
    trigger_patterns: List[str]
    slots: List[Slot]
