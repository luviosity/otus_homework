from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from homework_03.app.db import get_db, MockDB
from homework_03.app.schemas import BookCreate, BookGenre
from pydantic import ValidationError
import pathlib

router = APIRouter()
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
templates_path = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@router.get("/", response_class=HTMLResponse, name="home")
async def index(request: Request, db: MockDB = Depends(get_db)):
    context = {"request": request, "books": db.data}
    return templates.TemplateResponse("index.html", context=context)


@router.get("/about/", response_class=HTMLResponse, name="about")
async def about(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("about.html", context=context)


@router.get("/create", response_class=HTMLResponse, name="book_create_page")
async def book_create_page(request: Request):
    context = {"request": request, "genres": BookGenre}
    return templates.TemplateResponse("book_create.html", context=context)


@router.post("/create", response_class=HTMLResponse, name="book_create_post")
async def book_create(request: Request, db: MockDB = Depends(get_db)):
    form_data = await request.form()
    try:
        book = BookCreate.model_validate(dict(form_data))
        book_id = db.save_to_db(book)
        return RedirectResponse(
            url=f"/{book_id}/", status_code=status.HTTP_303_SEE_OTHER
        )
    except ValidationError as e:
        import json

        errors_json = json.dumps(e.errors(), indent=4, ensure_ascii=False)
        context = {
            "request": request,
            "genres": BookGenre,
            "errors": errors_json,
            "form_data": form_data,
        }
        return templates.TemplateResponse("book_create.html", context=context)


@router.get("/{book_id}/", response_class=HTMLResponse, name="book_detail")
async def book_detail(request: Request, book_id: int, db: MockDB = Depends(get_db)):
    book = db.get_book_detail(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id {book_id} не найдена.",
        )

    context = {"request": request, "book": book}
    return templates.TemplateResponse("book_detail.html", context=context)
