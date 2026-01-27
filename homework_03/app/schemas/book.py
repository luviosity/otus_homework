from pydantic import BaseModel, PositiveInt, Field, HttpUrl, field_validator
from enum import Enum
from typing import Optional


class BookGenre(str, Enum):
    FANTASY = "фэнтези"
    SCIENCE_FICTION = "фантастика"
    CONTEMPORARY_PROSE = "современная проза"
    ROMANCE = "романтика"
    MYSTERY = "детектив"
    THRILLER = "триллер"
    HORROR = "ужас"
    ADVENTURE = "приключения"
    HISTORICAL_FICTION = "историческая проза"
    DYSTOPIA = "антиутопия"
    DRAMA = "драма"
    LITERARY_FICTION = "литературная проза"
    POETRY = "поэзия"
    SELF_HELP = "саморазвитие"
    SCIENCE = "популярная наука"
    BIOGRAPHY = "биография"
    CRIME = "криминал"
    PARANORMAL = "паранормальное"


class BookBase(BaseModel):
    author: str = Field(..., min_length=5, max_length=100, examples=['Лев Толстой'])
    title: str = Field(..., min_length=5, examples=['Война и Мир'])
    genre: BookGenre
    pages_number: PositiveInt
    img_url: Optional[HttpUrl] = None

    @field_validator('img_url', mode='before')
    @classmethod
    def validate_img_url(cls, v):
        if not v or (isinstance(v, str) and v.strip() == ''):
            return None
        return v

class Book(BookBase):
    id: int

class BookCreate(BookBase):
    ...
