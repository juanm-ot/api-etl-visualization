## IMPORTAR LIBRERIAS
import os
import csv
import requests
import psycopg2
from psycopg2 import sql
import psycopg2.extras


## FUNCIONES
def test_database_connection(dbname, user, password, host, port):
    """
    Prueba la conexión a una base de datos PostgreSQL utilizando los parámetros proporcionados
    
    Parámetros:
    dbname (str): Nombre de la base de datos.
    user (str): Nombre de usuario de la base de datos.
    password (str): Contraseña del usuario de la base de datos.
    host (str): Dirección del host de la base de datos.
    port (int): Puerto de conexión a la base de datos.
    
    Retorna:
    bool: True si la conexión es exitosa, False en caso contrario.
    """
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) 
        print("Connection to the database was successful")
        conn.close()
        return True
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return False
    
    
def get_item_ids(search_query, ml_search_endpoint, limit=50 ):
    """
    Obtiene una lista de item_id desde el endpoint de búsqueda de Mercado Libre

    Parámetros:
    search_query (str): Término de búsqueda para consultar ítems.
    ml_search_endpoint (str): URL del endpoint de búsqueda de MercadoLibre.
    limit (int, opcional): Número máximo de ítems a recuperar. Por defecto es 50, pero por limitante de la API.

    Retorna:
    list: Lista de IDs de ítems obtenidos de la búsqueda. Si ocurre un error, retorna una lista vacía.

    """
    url = f"{ml_search_endpoint}?q={search_query}&limit={limit}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        item_ids = [item['id'] for item in data.get('results', [])]
        return item_ids
    else:
        print(f"Error retrieving item IDs for '{search_query}': {response.status_code}")
        return []
    

def get_item_details(item_id, ml_item_endpoint):
    """
    Obtiene los detalles de un ítem desde el endpoint de detalles de Mercado Libre.

    Parámetros:
    item_id (str): id del ítem para el cual se desean obtener detalles.
    ml_item_endpoint (str): url del endpoint de detalles de Mercado Libre con un marcador de posición para el id del ítem.

    Retorna:
    dict or None: Un diccionario con los detalles del ítem si la solicitud es exitosa, de lo contrario None.
    """
    url = ml_item_endpoint.format(item_id=item_id) # formatear la url del endpoint con el id extraido
    
    response = requests.get(url) # hacer la solicitus GET al endpoint con los detalles del item
    if response.status_code == 200:
        return response.json() # retornar la data del item en formato json
    else:
        print(f"Error retrieving item details '{item_id}': {response.status_code}")
        return None


def write_to_csv(items, filename):
    """
    Escribe una lista de ítems en un archivo CSV con los campos especificados.

    Parámetros:
    items (list): Lista de diccionarios, donde cada diccionario contiene los detalles de un ítem.
    filename (str): Nombre del archivo CSV a crear o sobrescribir.
    """
    fields = [ # campos/columnas csv
            "id", 
            "title", 
            "condition", 
            "price", 
            "currency_id", 
            "available_quantity", 
            "permalink", 
            "thumbnail", 
            "seller_id", 
            "category_id", 
            "base_price", 
            "warranty", 
            "color"
            ]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file: # abrir csv para escritura
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for item in items: # escribir cada item en cada fila del csv
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
                "warranty": item.get("warranty"),
                "color": next((attr.get("value_name") for attr in item.get("attributes", []) if attr.get("id") == "COLOR"), None)
            })


def insert_into_database(items, dbname, user, password, host, port ):
    """
    Inserta una lista de ítems en una base de datos PostgreSQL.
    """
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) 
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ecommerce.mercado_libre_items")
        conn.commit()
        # definir la consulta de inserción
        query = """  
            INSERT INTO ecommerce.mercado_libre_items (
                id, title, condition, price, currency_id, available_quantity, permalink, thumbnail,
                seller_id, category_id, base_price, warranty, color
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        data = [ # prepar los datos para la insercion 
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
                item.get("warranty"),
                next((attr.get("value_name") for attr in item.get("attributes", []) if attr.get("id") == "COLOR"), " ")

            )
            for item in items
        ]
        psycopg2.extras.execute_batch(cursor, query, data) # ejecutar la consulta en lotes
        conn.commit()
        print("Items have been inserted into the PostgreSQL database")

    except Exception as e:
        print(f"Error inserting item into the database: {str(e)}")
    finally:
        cursor.close()
        conn.close()
