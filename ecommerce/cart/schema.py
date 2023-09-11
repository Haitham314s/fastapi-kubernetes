from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from ecommerce.products import Product

from .models import Cart, CartItem

ProductGenOut = pydantic_model_creator(Product)

CartGenOut = pydantic_model_creator(Cart)
CartItemGenOut = pydantic_model_creator(CartItem)


class CartItemsOut(CartItemGenOut, BaseModel):
    product: ProductGenOut


class CartOut(CartGenOut, BaseModel):
    cart_items: List[CartItemsOut] = []
