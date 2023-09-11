from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "category" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50)  UNIQUE,
    "description" TEXT,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_category_name_8b0cb9" ON "category" ("name");
CREATE TABLE IF NOT EXISTS "product" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50),
    "quantity" INT,
    "description" TEXT,
    "price" INT,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category_id" CHAR(36) NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_product_name_683352" ON "product" ("name");
CREATE INDEX IF NOT EXISTS "idx_product_categor_2b519b" ON "product" ("category_id");
CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50),
    "email" VARCHAR(255)  UNIQUE,
    "password" TEXT,
    "description" TEXT,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_user_name_76f409" ON "user" ("name");
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
CREATE TABLE IF NOT EXISTS "cart" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_cart_user_id_5e18ab" ON "cart" ("user_id");
CREATE TABLE IF NOT EXISTS "cart_item" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "cart_id" CHAR(36) NOT NULL REFERENCES "cart" ("id") ON DELETE CASCADE,
    "product_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "order" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "price" REAL   DEFAULT 0,
    "status" VARCHAR(10) NOT NULL  DEFAULT 'processing' /* processing: processing */,
    "shipping_address" TEXT,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_order_status_a1c7e6" ON "order" ("status");
CREATE TABLE IF NOT EXISTS "order_detail" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "quantity" INT NOT NULL  DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "order_id" CHAR(36) NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,
    "product_id" CHAR(36) NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
