from fastapi import APIRouter
from .v1 import books_router


v1_router = APIRouter()
v1_router.include_router(books_router, prefix='/v1')