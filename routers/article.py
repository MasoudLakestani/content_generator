import schemas
from typing import Optional, List
from functions import create_article
from fastapi import APIRouter, Depends, Query, HTTPException
from painless.dependencies import get_api_key
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get("/api/v1/", response_class=HTMLResponse)
# def get_article(param:schemas.Parameter):#api_key:str=Depends(get_api_key)):
def get_article(subject: str, keywords: Optional[List[str]] = Query(None)):
    try:
        if not subject:
            raise HTTPException(status_code=400, detail="Subject is required")
        
        if not keywords:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        article = create_article(subject, keywords)
        # article = create_article(param.subject, param.keywords)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return HTMLResponse(content=article, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error accrued in openai server | {e}")