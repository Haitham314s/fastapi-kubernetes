from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Category(Model):
    class Meta:
        table = "category"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    name = fields.CharField(50, index=True, unique=True, null=True)
    description = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Product(Model):
    class Meta:
        table = "product"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    name = fields.CharField(50, null=True, index=True)
    quantity = fields.IntField(null=True)
    description = fields.TextField(null=True)
    price = fields.IntField(null=True)
    category = fields.ForeignKeyField(
        "models.Category",
        related_name="product_category",
        index=True,
        on_delete="CASCADE",
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
