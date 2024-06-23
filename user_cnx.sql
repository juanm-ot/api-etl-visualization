-- ============================================================================
-- Recurso: usuario de conexion
-- Descripción: crear un usuario de conexión (cnxuser) en PostgreSQL y otorgarle permisos 
--              adecuados para interactuar con la base de datos transactional_core,
--              el esquema public y ecommerce.
-- ============================================================================
CREATE USER cnxuser WITH PASSWORD 'cnx_password';

-- ----------------------------------------------------------------------------
-- Conceder Permisos
-- ----------------------------------------------------------------------------

-- (A) Para conexión a la bd
GRANT CONNECT ON DATABASE transactional_core TO cnxuser;
-- (B) Sobre public schema
GRANT USAGE ON SCHEMA public,ecommerce  TO cnxuser;
-- (C) Sobre todas las tablas actuales en el esquema public
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public,ecommerce TO cnxuser;
-- (D) Sobre las tablas futuras en el esquema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public, ecommerce GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO cnxuser;
-- (E) Sobre las secuencias de SERIAL
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public, ecommerce TO cnxuser;
-- (F) Sobre las tablas futuras en el esquema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO cnxuser;
