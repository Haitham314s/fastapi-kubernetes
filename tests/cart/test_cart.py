import pytest
from httpx import AsyncClient

from tests.shared.info import create_category_info, create_product_info


@pytest.mark.anyio
async def test_add_to_cart(authorized_client):
    category = await create_category_info()
    product = await create_product_info(category)
    response = await authorized_client.post("/cart", params={"product_id": product.id})

    assert response.status_code == 201
    return response.json()


@pytest.mark.anyio
async def test_get_all_carts(authorized_client: AsyncClient):
    response = await authorized_client.get("/carts")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_get_cart(authorized_client: AsyncClient):
    cart = await test_add_to_cart(authorized_client)
    response = await authorized_client.get(f"/cart/{cart['id']}")
    cart_data = response.json()

    assert response.status_code == 200
    assert cart["id"] == cart_data["id"]


@pytest.mark.anyio
async def test_delete_cart_item(authorized_client: AsyncClient):
    cart = await test_add_to_cart(authorized_client)
    cart_items = cart["cart_items"]
    response = await authorized_client.delete(f"/cart/{cart_items[0]['id']}")

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
