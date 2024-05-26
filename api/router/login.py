from fastapi import APIRouter
from api.dto.login import Login as DTO

from core.domains import login


router = APIRouter(prefix="/api/login")

@router.post("", response_model=login.ApiResponse, tags=["Login"], responses={401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Incorrect username or password"}}}}})
def post(dto: DTO):
    """
    Authenticate user login.
    """
    return login.authenticate(dto)
