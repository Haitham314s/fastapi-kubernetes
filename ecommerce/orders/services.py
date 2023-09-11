import asyncio
from typing import List

from fastapi import HTTPException, status

from ecommerce.cart import Cart, CartItem
from ecommerce.user import User

from .models import Order, OrderDetail
from .schema import OrderDetailOut, OrderOut
from .tasks import send_email


async def clear_cart_items(cart_items: List[CartItem]):
    for item in cart_items:
        await item.delete()


async def initiate_order(cart: Cart, user: User) -> OrderOut:
    cart_items = await CartItem.filter(cart_id=cart.id).prefetch_related("product")
    if len(cart_items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No items found in cart"
        )

    total_amount: float = 0.0
    for item in cart_items:
        total_amount += item.product.price

    new_order = await Order.create(
        price=total_amount, shipping_address="", user_id=user.id
    )

    order_details = await asyncio.gather(
        *[
            OrderDetail.create(
                quantity=item.product.quantity,
                order_id=new_order.id,
                product_id=item.product.id,
            )
            for item in cart_items
        ]
    )

    await clear_cart_items(cart_items)

    send_email.delay(user.email)

    return OrderOut(
        **{
            "id": new_order.id,
            "price": new_order.price,
            "status": new_order.status,
            "shipping_address": new_order.shipping_address,
            "created_at": new_order.created_at,
            "modified_at": new_order.modified_at,
            "order_details": OrderDetailOut.create_from_list(order_details),
        }
    )


async def show_order_details(orders: List[Order]) -> List[OrderOut]:
    if len(orders) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Orders found"
        )

    order_details = await asyncio.gather(
        *[
            OrderDetail.filter(order_id=order.id).prefetch_related("product")
            for order in orders
        ]
    )

    order_list = []
    for i, order in enumerate(orders):
        order.order_details = OrderDetailOut.create_from_list(order_details[i])
        order_list.append(OrderOut.model_validate(order))

    return [order for order in order_list]
