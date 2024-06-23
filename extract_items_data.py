## IMPORTAR LIBRERIAS
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import functions
from dotenv import load_dotenv

## CONFIGURACION
load_dotenv() ## cargar variables de entorno
ml_search_endpoint = os.getenv("ML_SEARCH_ENDPOINT")
ml_item_endpoint = os.getenv("ML_ITEM_ENDPOINT")

## CONEXION A LA BASE DE DATOS
dbname = os.getenv("DBNAME") # obtener parametros de conexión
user = os.getenv("DBUSER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")

## EXTRACCIÓN Y ALMACENAMIENTO DE DATOS
def main():
    """
    Función principal que realiza la extracción de datos desde MercadoLibre,
    procesa los detalles de los ítems en paralelo, y luego almacena los resultados
    en un archivo CSV y en una base de datos PostgreSQL.
    """
    if not functions.test_database_connection(dbname, user, password, host, port): # probar la conexion a la base de datos
        return

    search_queries = [ # seleccion de items 
        "Google Home",
        "Apple Tv",
        "Amazon Fire Tv",
        "PlayStation",
        "Xbox",
        "Nintendo",
        "PC Gaming"
    ]
    limit = 50  # api tiene un limite de max 50 records por query
    
    all_items = []
    item_ids = []
    for search_query in search_queries:
        item_ids = item_ids + functions.get_item_ids(search_query, ml_search_endpoint, limit)
        
    unique_item_ids = list(set(item_ids)) # eliminar duplicados de item_id obtenidos
    start_time = time.time() # funcion para marcar el tiempo de inicio del proceso
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(functions.get_item_details, item_id, ml_item_endpoint) for item_id in unique_item_ids]
        
        for future in as_completed(futures):
            item_details = future.result() # obtener el resultado del proceso en paralelo
            if item_details:
                all_items.append(item_details)
                print(f"Item '{item_details['id']}' processed in {time.time() - start_time:.2f} seconds")

    csv_filename = "meli_items_hub.csv"
    functions.write_to_csv(all_items, csv_filename) # escribir las consultas obtenidas en un csv
    print(f"{len(all_items)} items have been written to the {csv_filename} file ")

    functions.insert_into_database(all_items, dbname, user, password, host, port ) # insertar la data en la base de datos PostgreSQL
    
if __name__ == "__main__":
    main()
