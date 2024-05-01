from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi import Depends

from core.domains import embrapa
from security.auth import Auth


router = APIRouter(prefix="/api/embrapa")
auth = Auth()


@router.get("/")
def get(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.get_data()
