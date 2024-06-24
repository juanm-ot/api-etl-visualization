-- (A) Crear la base de datos
-- Crear la base de datos transactional_core si no existe
-- Verificar si la base de datos transactional_core existe y eliminarla si es necesario
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'transactional_core') THEN
        -- Cierra todas las conexiones a la base de datos
        PERFORM pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'transactional_core' AND pid <> pg_backend_pid();
        
        -- Elimina la base de datos
        EXECUTE 'DROP DATABASE transactional_core';
        
        RAISE NOTICE 'Base de datos transactional_core eliminada correctamente.';
    END IF;
END $$;

-- Crear la base de datos transactional_core
CREATE DATABASE transactional_core;

