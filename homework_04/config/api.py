from pydantic import BaseModel


class APIConfig(BaseModel):
    jsonplaceholder_url: str = "https://jsonplaceholder.typicode.com"
