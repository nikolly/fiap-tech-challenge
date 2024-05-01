from fastapi import HTTPException, status
from security.auth import Auth


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
    
    return {"access_token": access_token, "token_type": "bearer"}
    