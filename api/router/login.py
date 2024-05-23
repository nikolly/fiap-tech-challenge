from fastapi import APIRouter, HTTPException
from fastapi.openapi.utils import get_openapi
from api.dto.login import Login as DTO

from core.domains import login


router = APIRouter(prefix="/api/login")

@router.post("")
def post(dto: DTO):
    
    return login.authenticate(dto)
