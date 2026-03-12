from api import root_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(root_router)
