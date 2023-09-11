from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ecommerce.auth.jwt import get_current_user
from ecommerce.config import SUCCESS_RESPONSE
from ecommerce.user.models import User

from .models import Category, Product
from .schema import (
    CategoryGenOut,
    CategoryIn,
    CategoryOut,
    ProductGenOut,
    ProductIn,
    ProductOut,
    ProductUpdateIn,
)
from .services import update_product_from_dict
from .validator import category_name_exists

router = APIRouter(tags=["Products"], prefix="/product")


@router.post(
    "/category", response_model=CategoryGenOut, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_in: CategoryIn, user: User = Depends(get_current_user)
):
    if await category_name_exists(category_in.name):
        raise HTTPException(status_code=400, detail="Category name already exist")

    return await Category.create(**category_in.model_dump())


@router.get("/categories", response_model=List[CategoryGenOut])
async def get_all_category(user: User = Depends(get_current_user)):
    return await Category.all()


@router.get("/category/{category_id}", response_model=CategoryOut)
async def get_category(category_id: UUID, user: User = Depends(get_current_user)):
    category = await Category.get_or_none(id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    products = await Product.filter(category_id=category.id)
    category.products = products

    return category


@router.put("/category/{category_id}", response_model=CategoryGenOut)
async def update_category(
    category_id: UUID, category_in: CategoryIn, user: User = Depends(get_current_user)
):
    category = await Category.get_or_none(id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    if await category_name_exists(category_in.name):
        raise HTTPException(status_code=400, detail="Category name already exist")

    category_obj = category_in.model_dump()
    if category_in.description is None:
        category_obj["description"] = category.description

    category.update_from_dict(category_obj)
    await category.save()
    return category


@router.delete("/category/{category_id}")
async def delete_category(category_id: UUID, user: User = Depends(get_current_user)):
    category = await Category.get_or_none(id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    await category.delete()

    return SUCCESS_RESPONSE


@router.post("", response_model=ProductGenOut, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductIn, user: User = Depends(get_current_user)):
    category = await Category.get_or_none(id=product_in.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    product = await Product.create(**product_in.model_dump())
    product.category = category
    await product.save()

    return product


@router.get("s", response_model=List[ProductGenOut])
async def get_all_products(user: User = Depends(get_current_user)):
    return await Product.all()


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: UUID, user: User = Depends(get_current_user)):
    product = await Product.get_or_none(id=product_id).prefetch_related("category")
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")

    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdateIn,
    user: User = Depends(get_current_user),
):
    product = await Product.get_or_none(id=product_id).prefetch_related("category")
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")

    new_product = await update_product_from_dict(product, product_in)
    return new_product


@router.delete("/{product_id}")
async def delete_product(product_id: UUID, user: User = Depends(get_current_user)):
    product = await Product.get_or_none(id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")

    await product.delete()
    return SUCCESS_RESPONSE
