from fastapi import APIRouter
from starlette import status

from .api import v1_router
from .pages import pages_router


root_router = APIRouter()

root_router.include_router(pages_router)
root_router.include_router(v1_router, prefix='/api')

@root_router.get("/ping", status_code=status.HTTP_200_OK)
async def check():
    return {"message": "pong"}
