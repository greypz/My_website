from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from routers import about,blog,contact,demos

app = FastAPI()

# Mount the static files directory
app.mount("/images", StaticFiles(directory="images"), name="images")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(demos.router, prefix="/portfolio",tags=["demos"])
app.include_router(contact.router, prefix="/contact",tags=["demos"])
app.include_router(blog.router, prefix="/blog",tags=["demos"])
app.include_router(about.router, prefix="/about",tags=["demos"])

# Set up the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})





