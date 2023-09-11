from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ecommerce.auth.jwt import get_current_user
from ecommerce.config import SUCCESS_RESPONSE
from ecommerce.products import Product
from ecommerce.user import User

from .models import Cart, CartItem
from .schema import CartItemsOut, CartOut
from .services import add_items, get_user_carts

router = APIRouter(tags=["Cart"], prefix="/cart")


@router.post("", response_model=CartOut, status_code=status.HTTP_201_CREATED)
async def add_to_cart(product_id: UUID, user: User = Depends(get_current_user)):
    product = await Product.get_or_none(id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist"
        )

    if product.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product out of stock"
        )

    cart, _ = await Cart.get_or_create(user_id=user.id)
    await add_items(cart, product)

    cart_list = await get_user_carts([cart])
    return cart_list[0] if cart_list else cart_list


@router.get("s", response_model=List[CartOut])
async def get_cart_item(user: User = Depends(get_current_user)):
    carts = await Cart.filter(user_id=user.id).prefetch_related("user")
    return await get_user_carts(carts)


@router.get("/{cart_id}", response_model=CartOut)
async def get_cart_items(cart_id: UUID, user: User = Depends(get_current_user)):
    carts = await Cart.filter(id=cart_id, user_id=user.id).prefetch_related("user")
    cart_list = await get_user_carts(carts)
    return cart_list[0] if cart_list else cart_list


@router.delete("/{item_id}")
async def delete_cart_item(item_id: UUID, user: User = Depends(get_current_user)):
    cart = await Cart.get_or_none(user_id=user.id)
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    cart_item = await CartItem.get_or_none(id=item_id, cart_id=cart.id)
    if cart_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item does not exist"
        )

    await cart_item.delete()
    return SUCCESS_RESPONSE
