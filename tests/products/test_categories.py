from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from ecommerce.products.models import Category


@pytest.mark.anyio
async def test_create_new_category(authorized_client: AsyncClient):
    data = {
        "name": "Apparels",
        "description": "Apparel products fall under this category",
    }

    response = await authorized_client.post("/product/category", json=data)
    category = response.json()
    assert response.status_code == 201
    assert category["name"] == data["name"]
    assert category["description"] == data["description"]


@pytest.mark.anyio
async def test_get_categories(authorized_client: AsyncClient):
    response = await authorized_client.get("/product/categories")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_category(authorized_client: AsyncClient):
    category = await Category.get_or_none(name="Apparels")

    response = await authorized_client.get(f"/product/category/{category.id}")
    category_data = response.json()
    assert response.status_code == 200
    assert UUID(category_data["id"]) == category.id

    response = await authorized_client.get(f"/product/category/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_category(authorized_client: AsyncClient):
    category = await Category.get_or_none(name="Apparels")
    payload = {"name": "Foods", "description": "Daily food-related-products"}

    response = await authorized_client.put(
        f"/product/category/{category.id}", json=payload
    )
    category_data = response.json()
    assert response.status_code == 200
    assert UUID(category_data["id"]) == category.id
    assert category_data["name"] == payload["name"]
    assert category_data["description"] == payload["description"]


@pytest.mark.anyio
async def test_delete_category(authorized_client: AsyncClient):
    category = await Category.get_or_none(name="Foods")
    response = await authorized_client.delete(f"/product/category/{category.id}")
    assert response.status_code == 200

    response = await authorized_client.delete(f"/product/category/{category.id}")
    assert response.status_code == 404
