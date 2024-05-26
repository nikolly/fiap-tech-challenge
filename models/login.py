from pydantic import BaseModel


class ApiResponse(BaseModel):
    token: str
    token_type: str 
    