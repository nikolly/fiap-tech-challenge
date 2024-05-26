from fastapi import HTTPException, status
from security.auth import Auth
from fastapi.responses import JSONResponse
from models.login import ApiResponse


auth = Auth()

def authenticate(dto):    
    user = auth.authenticate_user(dto.username, dto.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = auth.create_access_token(data={"sub": user["username"]})
    
    response_data = ApiResponse(token=access_token, token_type="bearer")
    
    return JSONResponse(content=response_data.model_dump(), status_code=200, headers={"Content-Type": "application/json"})
    