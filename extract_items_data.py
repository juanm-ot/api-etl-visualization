import os
import requests
import csv
import time
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
from psycopg2 import sql

load_dotenv()

# Variables de entorno para la configuración
ML_SEARCH_ENDPOINT = os.getenv("ML_SEARCH_ENDPOINT")
ML_ITEM_ENDPOINT = os.getenv("ML_ITEM_ENDPOINT")

# Configuración de la conexión a la base de datos PostgreSQL
HOST = os.getenv("HOST")
PORT = os.getenv("PORT", "5432")  # Puerto predeterminado de PostgreSQL
DBUSER = os.getenv("DBUSER")
PASSWORD = os.getenv("PASSWORD")
DBNAME = os.getenv("DBNAME")

# Función para probar la conexión a la base de datos PostgreSQL
def test_database_connection():
    try:
        conn = psycopg2.connect(dbname=DBNAME, user=DBUSER, password=PASSWORD, host=HOST, port=PORT)
        print("Conexión a la base de datos PostgreSQL exitosa.")
        conn.close()
        return True
    except Exception as e:
        print(f"Error al conectar a la base de datos PostgreSQL: {str(e)}")
        return False

# Función para obtener IDs de ítems desde el primer endpoint
def get_item_ids(search_query, limit=50):
    url = f"{ML_SEARCH_ENDPOINT}?q={search_query}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        item_ids = [item['id'] for item in data.get('results', [])]
        return item_ids
    else:
        print(f"Error al obtener IDs de ítems para '{search_query}': {response.status_code}")
        return []

# Función para obtener detalles de un ítem por su ID desde el segundo endpoint
def get_item_details(item_id):
    url = ML_ITEM_ENDPOINT.format(item_id=item_id)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener detalles del ítem '{item_id}': {response.status_code}")
        return None

# Función para escribir los detalles de los ítems en un archivo CSV
def write_to_csv(items, filename):
    fields = [
        "id", "title", "condition", "price", "currency_id", "available_quantity",
        "permalink", "thumbnail", "seller_id", "category_id", "base_price", "warranty"
    ]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for item in items:
            writer.writerow({
                "id": item.get("id"),
                "title": item.get("title"),
                "condition": item.get("condition"),
                "price": item.get("price"),
                "currency_id": item.get("currency_id"),
                "available_quantity": item.get("available_quantity", 0),
                "permalink": item.get("permalink"),
                "thumbnail": item.get("thumbnail"),
                "seller_id": item.get("seller_id"),
                "category_id": item.get("category_id"),
                "base_price": item.get("base_price"),
                "warranty": item.get("warranty")
            })

# Función para insertar los detalles de los ítems en la base de datos PostgreSQL
def insert_into_database(items):
    conn = psycopg2.connect(dbname=DBNAME, user=DBUSER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    try:
        # Truncate the table before inserting new data
        cursor.execute("DELETE FROM ecommerce.mercado_libre_items")
        conn.commit()

        query = """
            INSERT INTO ecommerce.mercado_libre_items (
                id, title, condition, price, currency_id, available_quantity, permalink, thumbnail,
                seller_id, category_id, base_price, warranty
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        data = [
            (
                item.get("id"),
                item.get("title"),
                item.get("condition"),
                item.get("price"),
                item.get("currency_id"),
                item.get("available_quantity", 0),
                item.get("permalink"),
                item.get("thumbnail"),
                item.get("seller_id"),
                item.get("category_id"),
                item.get("base_price"),
                item.get("warranty")
            )
            for item in items
        ]
        psycopg2.extras.execute_batch(cursor, query, data)
        conn.commit()
    except Exception as e:
        print(f"Error al insertar ítem en la base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Función principal para obtener detalles y escribir en CSV y base de datos
def main():
    # Probar la conexión a la base de datos antes de continuar
    if not test_database_connection():
        return

    search_queries = [
        "Google Home",
        "Apple Tv",
        "Amazon Fire Tv"
        # Agrega aquí otros términos de búsqueda según tu interés
    ]
    limit = 50  # Cantidad de resultados a obtener (máximo 50 por página según la API)
    
    all_items = []
    for search_query in search_queries:
        item_ids = get_item_ids(search_query, limit)
        for item_id in item_ids:
            item_details = get_item_details(item_id)
            if item_details:
                all_items.append(item_details)
                time.sleep(0.5)  # Añade un pequeño delay para no sobrecargar la API

    # Escribir los resultados en un archivo CSV
    csv_filename = "mercado_libre_items_multi.csv"
    write_to_csv(all_items, csv_filename)
    print(f"Se han escrito {len(all_items)} ítems en el archivo {csv_filename}")

    # Insertar los resultados en la base de datos PostgreSQL
    insert_into_database(all_items)
    print(f"Se han insertado {len(all_items)} ítems en la base de datos PostgreSQL")

if __name__ == "__main__":
    main()
