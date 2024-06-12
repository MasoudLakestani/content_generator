import models
from .get_db import get_db
from sqlalchemy.orm import Session # type: ignore 
from fastapi import Depends, status, HTTPException, Request # type: ignore

def get_api_key(request: Request, db: Session = Depends(get_db)):
    # Attempt to retrieve the API key from the 'Authorization' header
    api_key = request.headers.get('api_key')
    if api_key is None: #or not api_key.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key is missing or improperly formatted")
    
    api_key = api_key# # Get the actual key past 'Bearer'
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return user


def get_register_key(request: Request, db: Session = Depends(get_db)):
    
    register_key = request.headers.get('Register_key')
    if register_key is None: #or not api_key.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Register key is missing or improperly formatted")
    
    register_key = register_key
    register = db.query(models.RegisterKey).filter(models.RegisterKey.register_key == register_key).first()
    print(register,"--")
    if not register:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Register Key")
    return register