import schemas
from typing import Optional, List
from functions import create_article_v1, create_article_v2
from fastapi import APIRouter, Depends, Query, HTTPException
from painless.dependencies import get_api_key
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse


router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.post("/api/v1/", response_class=JSONResponse)
def get_article(param:schemas.Parameter):#api_key:str=Depends(get_api_key)):
# def get_article(subject: str, keywords: Optional[List[str]] = Query(None)):
    try:
        if not param.subject:
            raise HTTPException(status_code=400, detail="Subject is required")
        
        if not param.keywords:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        if not param.tone:
            param.tone = 1
        if not param.brand_name:
            param.brand_name = None
        article = create_article_v1(param.subject, param.keywords, param.tone, param.brand_name)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return JSONResponse(content=article, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error accrued in openai server | {e}")

@router.get("/api/v1/", response_class=JSONResponse)
# def get_article(param:schemas.Parameter):#api_key:str=Depends(get_api_key)):
def get_article(subject: str, keywords: Optional[List[str]] = Query(None)):
    try:
        if not subject:
            raise HTTPException(status_code=400, detail="Subject is required")
        
        if not keywords:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        article = create_article_v1(subject, keywords)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return JSONResponse(content=article, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error accrued in openai server | {e}")


@router.post("/api/v2/", response_class=JSONResponse)
def get_article(param:schemas.Parameter):#api_key:str=Depends(get_api_key)):
# def get_article(subject: str, keywords: Optional[List[str]] = Query(None)):
    try:
        if not param.subject:
            raise HTTPException(status_code=400, detail="Subject is required")
        
        if not param.keywords:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        article = create_article_v2(param.subject, param.keywords)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return JSONResponse(content=article, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error accrued in openai server | {e}")
    

@router.get("/api/v2/", response_class=JSONResponse)
# def get_article(param:schemas.Parameter):#api_key:str=Depends(get_api_key)):
def get_article(subject: str, keywords: Optional[List[str]] = Query(None)):
    try:
        if not subject:
            raise HTTPException(status_code=400, detail="Subject is required")
        
        if not keywords:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        article = create_article_v2(subject, keywords)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return JSONResponse(content=article, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error accrued in openai server | {e}")