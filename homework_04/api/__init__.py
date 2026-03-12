from api.v1 import router as v1_router
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

root_router = APIRouter()

root_router.include_router(v1_router, prefix="/api")


@root_router.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")
