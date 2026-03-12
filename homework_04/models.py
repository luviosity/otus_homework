"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

from config.settings import settings
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    MetaData,
    Text,
    func,
    text,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

engine = create_async_engine(
    url=settings.db.url,
    echo=settings.db.sqla.echo,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(
        Text,
    )
    username: Mapped[str] = mapped_column(
        Text,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        Text,
        unique=True,
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint(
            func.length(text("name")) <= 32,
            name="name_length_constraint",
        ),
        CheckConstraint(
            func.length(text("username")) <= 32,
            name="username_length_constraint",
        ),
        CheckConstraint(
            func.length(text("email")) <= 32,
            name="email_length_constraint",
        ),
    )


class Post(Base):
    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(
        Text,
    )
    body: Mapped[str] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="posts")

    __table_args__ = (
        CheckConstraint(
            func.length(text("title")) <= 100,
            name="title_length_constraint",
        ),
    )
