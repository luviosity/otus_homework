from .books import router as books_router
from fastapi import APIRouter


pages_router = APIRouter()
pages_router.include_router(books_router)