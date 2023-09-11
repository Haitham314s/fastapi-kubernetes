from tortoise import fields
from tortoise.models import Model

from .hashing import verify_password


class User(Model):
    class Meta:
        table = "user"

    id = fields.UUIDField(pk=True, index=True, unique=True)
    name = fields.CharField(max_length=50, index=True, null=True)
    email = fields.CharField(max_length=255, unique=True, index=True, null=True)

    password = fields.TextField(null=True)
    description = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def check_password(self, password):
        return verify_password(self.password, password)
