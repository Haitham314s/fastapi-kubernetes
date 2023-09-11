import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from tests.shared.info import create_category_info, create_product_info


@pytest.mark.anyio
async def test_create_new_order(authorized_client: AsyncClient, mocker: MockerFixture):
    mocker.patch("ecommerce.orders.tasks.send_email", return_value=True)
    category = await create_category_info()
    product = await create_product_info(category)

    cart_response = await authorized_client.post(
        "/cart", params={"product_id": product.id}
    )
    cart_data = cart_response.json()
    order_response = await authorized_client.post(f"/order/{cart_data['id']}")

    assert cart_response.status_code == 201
    assert order_response.status_code == 201

    return order_response.json()


@pytest.mark.anyio
async def test_get_all_orders(authorized_client: AsyncClient):
    response = await authorized_client.get("/orders")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_order(authorized_client: AsyncClient, mocker: MockerFixture):
    order = await test_create_new_order(authorized_client, mocker)
    response = await authorized_client.get(f"/order/{order['id']}")
    order_data = response.json()

    assert order_data["id"] == order["id"]
    assert order_data["price"] == order["price"]
    assert order_data["status"] == order["status"]
    assert order_data["shipping_address"] == order["shipping_address"]
