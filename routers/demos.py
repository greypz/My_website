from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException,Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.templating import Jinja2Templates
import os
from schemas.userschema import UserCreate,Token
from schemas.messageschema import MessageData
from dependencies.auth import hash_password, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,get_current_user
from DataBase.get_db import get_db
from models.user import User
from models.message import Message
statpath = os.path.join(os.path.dirname(__file__), os.pardir, "static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/portfolio/authorize/log-in")
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/",response_class=HTMLResponse)
async def portfolio(request:Request):
    return templates.TemplateResponse("demos.html", {"request": request})

@router.get("/authorize",response_class=HTMLResponse)
async def auth(request:Request):
    return templates.TemplateResponse("authorization.html", {"request": request})

# Sign-up route
@router.post("/authorize/sign-up", response_class=JSONResponse)
async def sign_up(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_pass=hash_password(user_data.password)
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_pass
    )
    db.add(new_user)
    db.commit()

    # Return a success response
    return JSONResponse({"redirect_to": "/portfolio"}, status_code=200)

@router.post("/authorize/log-in",response_model=Token)
async def login(db:Session=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/project1", response_class=HTMLResponse)
async def projects(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Fetch previous messages from the database for the user
    messages = db.query(Message).filter(Message.user_id == current_user.id, Message.project == 1).all()
    message_list = [{"username": current_user.username, "message": msg.content} for msg in messages]

    return templates.TemplateResponse(
        "project1.html",
        {"request": request, "username": current_user.username, "messages": message_list}
    )

@router.get("/project2", response_class=HTMLResponse)
async def projects(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Fetch previous messages from the database for the user
    messages = db.query(Message).filter(Message.project == 2).all()
    users=db.query(User).all()
    message_list = [{"username": msg.user.username, "message": msg.content} for msg in messages]

    return templates.TemplateResponse(
        "project2.html",
        {"request": request, "username": current_user.username, "messages": message_list}
    )
@router.post("/project1/send-message",response_class=JSONResponse)
async def save_message(payload:MessageData,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==payload.username).first()
    message = Message(content=payload.message, user_id=user.id,project=int(payload.project))
    db.add(message)
    db.commit()
    return JSONResponse( {"message":"is submiting"},status_code=200)
