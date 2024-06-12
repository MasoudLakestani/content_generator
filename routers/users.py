
import models
import schemas
from sqlalchemy.orm import Session
from functions import create_article
from fastapi import APIRouter, Depends, HTTPException
from painless.dependencies import get_db, get_register_key

router = APIRouter()

@router.post('/register', response_model=schemas.User)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db), register_key:str=Depends(get_register_key)):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="The username already exist")
    user = models.User(email=user.email, username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
