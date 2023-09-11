import asyncio
from typing import List

from fastapi import HTTPException, status

from ecommerce.products import Product

from .models import Cart, CartItem
from .schema import CartOut


async def add_items(cart: Cart, product: Product) -> CartItem:
    return await CartItem.create(cart_id=cart.id, product_id=product.id)


async def get_user_carts(carts: List[Cart]) -> List[CartOut]:
    if len(carts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    cart_items = await asyncio.gather(
        *[
            CartItem.filter(cart_id=cart.id).prefetch_related("product")
            for cart in carts
        ]
    )

    cart_list = []
    for i, cart in enumerate(carts):
        cart_list.append(
            CartOut(
                **{
                    "id": cart.id,
                    "created_at": cart.created_at,
                    "modified_at": cart.modified_at,
                    "cart_items": cart_items[i],
                }
            )
        )

    return [cart for cart in cart_list]
