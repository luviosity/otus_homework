from homework_03.app.schemas import Book, BookGenre, BookCreate
from pydantic import TypeAdapter, HttpUrl
from typing import Optional


class MockDB:
    def __init__(self):
        self.data = [
            Book(
                id=1,
                author="Сергей Лукьяненко",
                title="Девятый",
                genre=BookGenre.FANTASY,
                pages_number=512,
                img_url=TypeAdapter(HttpUrl).validate_python(
                    'https://cdn.ast.ru/v2/ASE000000000896190/COVER/cover1__w340.jpg')
            ),
            Book(
                id=2,
                author="Ребекка Яррос",
                title="Железное пламя",
                genre=BookGenre.FANTASY,
                pages_number=896,
                img_url=TypeAdapter(HttpUrl).validate_python(
                    'https://m.media-amazon.com/images/I/91JnZVay00L._UF1000,1000_QL80_.jpg')
            ),
            Book(
                id=3,
                author="Михаил Булгаков",
                title="Мастер и Маргарита",
                genre=BookGenre.SCIENCE_FICTION,
                pages_number=480,
                img_url=TypeAdapter(HttpUrl).validate_python(
                    'https://cdn.azbooka.ru/cv/w1100/98fa6b42-e86d-4f17-9376-25e98cc784e5.jpg')
            ),
            Book(
                id=4,
                author="Наринэ Абгарян",
                title="Люди нашего двора",
                genre=BookGenre.CONTEMPORARY_PROSE,
                pages_number=320,
                img_url=TypeAdapter(HttpUrl).validate_python(
                    'https://cdn.ast.ru/v2/ASE000000000891482/COVER/cover1__w340.jpg')
            )
        ]

    def _get_new_id(self):
        return max((book.id for book in self.data), default=0) + 1

    def get_book_detail(self, book_id: int) -> Optional[Book]:
        book = next((book for book in self.data if book.id == book_id), None)
        return book

    def save_to_db(self, book: BookCreate) -> int:
        book_id = self._get_new_id()
        book = Book(id=book_id, **book.model_dump())
        self.data.append(book)
        return book_id
