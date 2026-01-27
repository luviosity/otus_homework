"""
Домашнее задание №5
Первое веб-приложение

- в модуле `app` создайте базовое FastAPI приложение
- создайте обычные представления
  - создайте index view `/`
  - добавьте страницу `/about/`, добавьте туда текст, информацию о сайте и разработчике
  - создайте базовый шаблон (используйте https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template)
  - в базовый шаблон подключите статику Bootstrap 5 (подключите стили), примените стили Bootstrap
  - в базовый шаблон добавьте навигационную панель `nav` (https://getbootstrap.com/docs/5.0/components/navbar/)
  - в навигационную панель добавьте ссылки на главную страницу `/` и на страницу `/about/` при помощи `url_for`
  - добавьте новые зависимости в файл `requirements.txt` в корне проекта
    (лучше вручную, но можно командой `pip freeze > requirements.txt`, тогда обязательно проверьте, что туда попало, и удалите лишнее)
- создайте api представления:
  - создайте api router, укажите префикс `/api`
  - добавьте вложенный роутер для вашей сущности (если не можете придумать тип сущности, рассмотрите варианты: товар, книга, автомобиль)
  - добавьте представление для чтения списка сущностей
  - добавьте представление для чтения сущности
  - добавьте представление для создания сущности
"""
from fastapi import FastAPI, staticfiles
import uvicorn
from homework_03.app.routers import root_router
from homework_03.app.db import MockDB
from contextlib import asynccontextmanager
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
static_path = BASE_DIR / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Подключение к БД...")
    db_client = MockDB()

    app.state.db = db_client

    yield  # Здесь приложение работает и принимает запросы

    # Этот код срабатывает при выключении сервера
    print("Закрытие соединения с БД...")
    del app.state.db

app = FastAPI(lifespan=lifespan)
app.mount("/static", staticfiles.StaticFiles(directory=str(static_path)), name="static")
app.include_router(root_router, tags=["books"])

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)