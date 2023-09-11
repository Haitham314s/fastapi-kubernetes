from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Cart(Model):
    class Meta:
        table = "cart"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="cart_user",
        index=True,
        on_delete="CASCADE",
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class CartItem(Model):
    class Meta:
        table = "cart_item"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    cart = fields.ForeignKeyField(
        "models.Cart", related_name="items_cart_connection", on_delete="CASCADE"
    )
    product = fields.ForeignKeyField(
        "models.Product", related_name="cart_items_product", on_delete="CASCADE"
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
