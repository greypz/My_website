from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/",response_class=HTMLResponse)
async def home_page(request:Request):
    return templates.TemplateResponse("aboutme.html", {"request": request})
