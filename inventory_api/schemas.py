from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "johnny"})
    password: str = Field(..., json_schema_extra={"example": "Password123"})
    email: EmailStr = Field(..., json_schema_extra={"example": "johnny_d@example.com"})
    role: Optional[str] = Field(default="user", json_schema_extra={"example": "user"})


class User(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    role: str

    class ConfigDict:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, json_schema_extra={"example": "johnny"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "johnny@example.com"})
    role: Optional[str] = Field(None, json_schema_extra={"example": "admin"})


class UserLogin(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "johnny"})
    password: str = Field(..., json_schema_extra={"example": "Password123"}, min_length=8)


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    quantity: int
    price: float

    class ConfigDict:
        orm_mode = True


class ItemCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Example Name"})
    description: str = Field(None, json_schema_extra={"example": "Example description"})
    category: str = Field(..., json_schema_extra={"example": "Example Category"})
    quantity: int = Field(..., json_schema_extra={"example": 1})
    price: float = Field(..., json_schema_extra={"example": 9.99})


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None


class ItemInDBBase(ItemBase):
    id: int

    class ConfigDict:
        orm_mode = True


class Item(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass
