from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from ecommerce.products.models import Product
from ecommerce.products.schema import ProductGenOut

from . import Order
from .models import OrderDetail

OrderGenOut = pydantic_model_creator(Order)


class OrderDetailOut(BaseModel):
    id: UUID
    order_id: UUID
    quantity: int | None = Field(default=1)
    product: ProductGenOut | None = Field(default=None)
    created_at: datetime
    modified_at: datetime

    @staticmethod
    def create_from_list(order_details: List[OrderDetail]) -> "OrderDetailOut":
        return [
            OrderDetailOut(
                **{
                    "id": order_detail.id,
                    "order_id": order_detail.order_id,
                    "quantity": order_detail.quantity,
                    "product": order_detail.product
                    if isinstance(order_detail.product, Product)
                    else None,
                    "created_at": order_detail.created_at,
                    "modified_at": order_detail.modified_at,
                }
            )
            for order_detail in order_details
        ]


class OrderOut(OrderGenOut, BaseModel):
    order_details: List[OrderDetailOut] = []
