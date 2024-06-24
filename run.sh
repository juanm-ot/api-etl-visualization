#!/bin/bash

source .env  # cargar variables de entorno
PSQL_PATH="C:\Program Files\PostgreSQL\16\bin\psql.exe" # ruta a psql. **Se ajusta segun la maquina**

echo "Starting DDL script execution..."

echo "Creating database 'transactional_core'..."
PGPASSWORD=$ROOT_PASSWORD "$PSQL_PATH" -h $HOST -U $ROOT_USER -d postgres -f create_database.sql  # conectar a bd de PostgreSQL y ejectutar DDL
if [ $? -ne 0 ]; then # verificar si el DDL se ejecuto correctamente
    echo "ERROR: Failed to execute create_database.sql"
    exit 1
else
    echo "Success: Database 'transactional_core' created successfully"
fi

echo "Creating Data base table mercado_libre_items"
PGPASSWORD=$ROOT_PASSWORD "$PSQL_PATH" -h $HOST -U $ROOT_USER -d postgres -d transactional_core -f mercado_libre_items.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to execute mercado_libre_items.sql"
    exit 1
else
    echo "Success: Data base table mercado_libre_items created successfully"
fi


echo "Creating conexion user cnx and grant permisions..."
PGPASSWORD=$ROOT_PASSWORD "$PSQL_PATH" -h $HOST -U $ROOT_USER -d postgres -d transactional_core  -f user_cnx.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed conexion user cnx"
    exit 1
else
    echo "Success: Conexion user cnx and grant permisions created successfully"
fi

echo "******  Database schema is ready  ******"


echo "Setting up virtual environment..."
python -m venv data_eng  # crear y activar el entorno virtual
source data_eng/Scripts/activate

echo "Installing dependencies..."
pip install -r requirements.txt # instalar los paquetes requeridos
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Error: Failed to install dependencies."
    exit 1
fi

echo "Starting data ingestion from APIs into the meli_items_hub.csv and mercado_libre_items database table..."
echo "Running extract_items_data.py"
python extract_items_data.py # ejecutar el script de Python para poblar la base de datos
if [ $? -ne 0 ]; then
    echo "Error: extract_items_data.py failed."
    exit 1
else
    echo "Success: The API data was succesfully ingest to plain text and database"
    echo "Check meli_items_hub.csv and ecommerce.mercado_libre_items table in transactional_core"
fi

deactivate # desactivar el entorno virtual
