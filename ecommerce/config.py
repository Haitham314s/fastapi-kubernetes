import os

APP_ENV = os.getenv("APP_ENV", "development")

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "admin")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "admin123")
DATABASE_HOST = os.getenv("DATABASE_HOST", "postgres-service")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommercedb")

TEST_DATABASE_NAME = os.getenv("DATABASE_NAME", "test_ecommercedb")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0" if APP_ENV == "TESTING" else "0")

SUCCESS_RESPONSE = {"status": "success"}
