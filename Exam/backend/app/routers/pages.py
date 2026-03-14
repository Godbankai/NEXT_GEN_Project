from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(Path("backend/app/templates")))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "join_code": None})


@router.get("/join/{join_code}", response_class=HTMLResponse)
def join_page(request: Request, join_code: str):
    return templates.TemplateResponse("login.html", {"request": request, "join_code": join_code})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "join_code": request.query_params.get("join_code")})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/exam/{exam_id}", response_class=HTMLResponse)
def exam_page(request: Request, exam_id: int):
    return templates.TemplateResponse("exam_room.html", {"request": request, "exam_id": exam_id})
