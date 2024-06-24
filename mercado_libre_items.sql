-- ============================================================================
-- Recurso: DDL almacenamiento de items meli
-- Descripción: Define el esquema 'ecommerce' y la tabla 'mercado_libre_items' 
--              para almacenar información de productos de Mercado Libre.
-- ============================================================================
-- (A) Generar una funcion de borrado si existen las tablas y el schema, con este proceso 
--     se garantiza empezar limpio.
DROP TABLE IF EXISTS ecommerce.mercado_libre_items CASCADE;
DROP SCHEMA IF EXISTS ecommerce CASCADE;

-- (B) Creacion del schema y de las tablas pertenecientes
CREATE SCHEMA ecommerce;

-- (B.1) Almacena items extraidos desde la API
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
    warranty VARCHAR(255),
    color VARCHAR(255)
);
