from tortoise import Tortoise

from . import config

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_PORT = config.DATABASE_PORT
DATABASE_NAME = config.DATABASE_NAME

DATABASE_URL = f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
# DATABASE_URL = "sqlite://db.sqlite3"
print(f"DATABASE_URL: {DATABASE_URL}")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["ecommerce", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["ecommerce"]})

    await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()
