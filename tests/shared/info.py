from faker import Faker

from ecommerce.products.models import Category, Product


async def create_category_info() -> Category:
    fake = Faker()
    category = await Category.all().order_by("-created_at").first()
    if category is None:
        category = await Category.create(name=fake.name())

    return category


async def create_product_info(category: Category) -> Product:
    payload = {
        "name": "Chicken sandwich",
        "quantity": 5,
        "description": "Good quality chicken sandwich for 35 AED",
        "price": 35.50,
        "category_id": category.id,
    }
    return await Product.create(**payload)
