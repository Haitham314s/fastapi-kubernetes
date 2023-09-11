from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ecommerce.auth.jwt import get_current_user
from ecommerce.cart.models import Cart
from ecommerce.user import User

from .models import Order
from .schema import OrderOut
from .services import initiate_order, show_order_details

router = APIRouter(tags=["Orders"], prefix="/order")


@router.post("/{cart_id}", status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order(cart_id: UUID, user: User = Depends(get_current_user)):
    cart = await Cart.get_or_none(id=cart_id, user_id=user.id)
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    return await initiate_order(cart, user)


@router.get("s", response_model=List[OrderOut])
async def get_order_detail(user: User = Depends(get_current_user)):
    orders = await Order.filter(user_id=user.id)
    return await show_order_details(orders)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order_detail(order_id: UUID, user: User = Depends(get_current_user)):
    orders = await Order.filter(id=order_id, user_id=user.id)
    order_list = await show_order_details(orders)
    return order_list[0] if order_list else order_list
