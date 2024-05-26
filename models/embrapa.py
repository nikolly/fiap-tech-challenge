from pydantic import BaseModel
from typing import List, Any


class YearData(BaseModel):
    year: int
    value: Any

class ItemData(BaseModel):
    id: str
    name: str
    data: List[YearData]

class ApiResponse(BaseModel):
    items: List[ItemData]      
    