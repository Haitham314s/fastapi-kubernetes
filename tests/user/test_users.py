import pytest
from faker import Faker
from httpx import AsyncClient

from ecommerce.user.models import User


@pytest.mark.anyio
async def test_user_registration(client: AsyncClient):
    fake = Faker()
    data = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    response = await client.post("/user", params=data)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_user_login(client: AsyncClient):
    wrong_data = {"username": "test@gmail.com", "password": "password1213"}
    data = {"username": "test@gmail.com", "password": "test123"}

    response = await client.post("/login", data=wrong_data)
    assert response.status_code == 400
    response = await client.post("/login", data=data)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_all_users(authorized_client):
    response = await authorized_client.get("/user")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_duplicate_user(client: AsyncClient):
    data = {"name": "test", "email": "test@gmail.com", "password": "123"}
    assert await User.filter(email=data["email"]).count() == 1

    response = await client.post("/user", params=data)
    assert response.status_code == 400
