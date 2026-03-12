from pydantic import (
    BaseModel,
    EmailStr,
    constr,
)


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr | None


class UserCreate(UserBase):
    name: constr(max_length=32)
    username: constr(min_length=3, max_length=32)
    email: EmailStr | None = None


class UserRead(UserBase):
    id: int
