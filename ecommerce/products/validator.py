from .models import Category


async def category_name_exists(name: str):
    category = await Category.get_or_none(name__iexact=name)
    if category is not None:
        return True

    return False
