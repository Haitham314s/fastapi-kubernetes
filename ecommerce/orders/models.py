from enum import Enum

from tortoise import fields
from tortoise.models import Model


class OrderStatus(str, Enum):
    processing = "processing"


class Order(Model):
    class Meta:
        table = "order"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    price = fields.FloatField(default=0.0, null=True)
    status = fields.CharEnumField(
        OrderStatus, default=OrderStatus.processing, index=True
    )
    shipping_address = fields.TextField(null=True)

    user = fields.ForeignKeyField(
        "models.User", related_name="order_user", on_delete="CASCADE"
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class OrderDetail(Model):
    class Meta:
        table = "order_detail"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    quantity = fields.IntField(default=0)
    order = fields.ForeignKeyField(
        "models.Order", related_name="details_for_order", on_delete="CASCADE"
    )
    product = fields.ForeignKeyField(
        "models.Product", related_name="product_order_details", on_delete="CASCADE"
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
