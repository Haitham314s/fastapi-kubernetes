import os

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from ecommerce import config
from ecommerce.auth.jwt import create_access_token
from main import app

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.TEST_DATABASE_NAME

DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
# DATABASE_URL = "sqlite://db-test.sqlite3"


async def init_db(create_db: bool = False, schemas: bool = False):
    await Tortoise.init(
        db_url=DATABASE_URL, modules={"models": ["ecommerce"]}, _create_db=create_db
    )
    if schemas:
        await Tortoise.generate_schemas()
    if create_db:
        print(f"database created: {DATABASE_URL}")


async def init():
    await init_db(True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://localhost:8001") as client:
        yield client


@pytest.fixture(scope="session")
async def test_user(client):
    data = {"name": "test", "email": "test@gmail.com", "password": "test123"}
    response = await client.post("/user", params=data)
    user = response.json()
    assert response.status_code == 201
    return user


@pytest.fixture(scope="session")
async def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture(scope="session")
async def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
