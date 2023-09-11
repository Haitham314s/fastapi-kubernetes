from uuid import UUID

import pytest
from httpx import AsyncClient

from ecommerce.products.models import Product
from tests.shared.info import create_category_info


@pytest.mark.anyio
async def test_create_product(authorized_client: AsyncClient):
    category = await create_category_info()
    payload = {
        "name": "Secret product #1",
        "quantity": 10,
        "description": "First testing product",
        "price": 10.0,
        "category_id": str(category.id),
    }

    response = await authorized_client.post("/product", json=payload)
    product_data = response.json()

    assert response.status_code == 201
    assert product_data["name"] == payload["name"]
    assert product_data["quantity"] == payload["quantity"]
    assert product_data["description"] == payload["description"]
    assert product_data["price"] == payload["price"]


@pytest.mark.anyio
async def test_get_all_products(authorized_client: AsyncClient):
    response = await authorized_client.get("/products")
    product_data = response.json()
    assert response.status_code == 200
    assert len(product_data) > 0


@pytest.mark.anyio
async def test_get_product(authorized_client: AsyncClient):
    product = await Product.get_or_none(name="Secret product #1").prefetch_related(
        "category"
    )
    response = await authorized_client.get(f"/product/{product.id}")
    product_data = response.json()

    assert response.status_code == 200
    assert UUID(product_data["category"]["id"]) == product.category.id


@pytest.mark.anyio
async def test_udpate_product(authorized_client: AsyncClient):
    payload = {
        "name": "Secret product",
        "quantity": 1,
        "description": "Our updated secret product",
        "price": 9.95,
    }
    product = await Product.get_or_none(name="Secret product #1")
    response = await authorized_client.put(f"/product/{product.id}", json=payload)
    product_data = response.json()

    assert response.status_code == 200
    assert product_data["name"] == payload["name"]
    assert product_data["quantity"] == payload["quantity"]
    assert product_data["description"] == payload["description"]
    assert product_data["price"] == payload["price"]


@pytest.mark.anyio
async def test_delete_product(authorized_client: AsyncClient):
    product = await Product.get_or_none(name="Secret product")
    response = await authorized_client.delete(f"/product/{product.id}")
    assert response.status_code == 200

    response = await authorized_client.delete(f"/product/{product.id}")
    assert response.status_code == 404
