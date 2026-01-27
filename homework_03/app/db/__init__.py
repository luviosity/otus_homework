from .db import MockDB
from fastapi import Request


def get_db(request:Request) -> MockDB:
    return request.app.state.db