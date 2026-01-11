from fastapi import APIRouter
from .api import v1_router
from .pages import pages_router


root_router = APIRouter()

root_router.include_router(pages_router)
root_router.include_router(v1_router, prefix='/api')
