from fastapi import HTTPException

from .models import Category, Product
from .schema import ProductUpdateIn


async def update_product_from_dict(
    product: Product, product_in: ProductUpdateIn
) -> Product:
    product.name = product_in.name
    if product_in.category_id is not None:
        category = await Category.get_or_none(id=product_in.category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category = category

    if product_in.quantity is not None:
        product.quantity = product_in.quantity
    if product_in.description is not None:
        product.description = product_in.description
    if product_in.price is not None:
        product.price = product_in.price

    await product.save()
    return product
