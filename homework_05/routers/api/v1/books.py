from fastapi import APIRouter, HTTPException, status, Depends
from homework_05.schemas import Book, BookCreate
from homework_05.db import MockDB, get_db

router = APIRouter(prefix='/book')


@router.get('/list', response_model=list[Book])
async def book_list(db: MockDB = Depends(get_db)):
    return db.data


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def book_create(book_in: BookCreate, db: MockDB = Depends(get_db)) -> dict[str, int]:
    book_id = db.save_to_db(book_in)
    return {"id": book_id}


@router.get('/{book_id}', response_model=Book)
async def book_detail(book_id: int, db: MockDB = Depends(get_db)):
    book = db.get_book_detail(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Книга с id {book_id} не найдена.')
    return book
