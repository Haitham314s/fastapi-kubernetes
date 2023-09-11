from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, constr
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Category, Product

CategoryGenOut = pydantic_model_creator(Category)
ProductGenOut = pydantic_model_creator(Product)


class CategoryIn(BaseModel):
    name: constr(min_length=2, max_length=50)
    description: Optional[str] = None


class CategoryOut(CategoryGenOut, BaseModel):
    products: List[ProductGenOut]


class ProductBase(BaseModel):
    name: constr(min_length=2, max_length=50)
    quantity: Optional[int] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ProductIn(ProductBase):
    category_id: UUID = None


class ProductUpdateIn(ProductBase):
    category_id: Optional[UUID] = None


class ProductOut(BaseModel):
    id: UUID
    name: str
    quantity: Optional[int] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: CategoryGenOut
