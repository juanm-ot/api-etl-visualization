DROP TABLE IF EXISTS ecommerce.mercado_libre_items CASCADE;
DROP SCHEMA IF EXISTS ecommerce CASCADE;

CREATE SCHEMA ecommerce;

CREATE TABLE ecommerce.mercado_libre_items (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255),
    condition VARCHAR(50),
    price NUMERIC(10, 2),
    currency_id VARCHAR(10),
    available_quantity INTEGER,
    permalink VARCHAR(255),
    thumbnail VARCHAR(255),
    seller_id INTEGER,
    category_id VARCHAR(50),
    base_price NUMERIC(10, 2),
    warranty VARCHAR(255)
);