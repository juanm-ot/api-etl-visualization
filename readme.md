# Consumo de API para análisis de productos en Mercado Libre

Este proyecto se centra en el consumo de la API pública de MercadoLibre para realizar un análisis de la oferta de productos en diversas categorías, para este proyecto se proponen las categorias: Xbox, Nintendo, PC gaming y Playstation. El objetivo es **obtener datos** relevantes sobre estos productos, desnormalizarlos y almacenarlos en un formato accesible para facilitar su análisis posterior.


## Estructura repositorio

```linux

.
├── readme.md                          # descripcion del repositorio
├── .env                               # contiene las variables de entorno
├── mercado_libre_items.sql            # script DDL 
├── user_cnx.sql                       # contiene la confg del usuario de conexion
├── functions.py                       # funciones para conectarse a la bd, consumir la API, generar el archivo plano
├── extract_items_data.py              # orquesta las funciones para escribir los items en el archivo plano y en la bd
│
├── meli_items_hub.csv                 # output: archivo de texto plano con la data de los items
├── resources                          # carpeta para almacenar recursos de apoyo
│   └── algún-archivo
│
└── requirements.txt                   # requerimientos para correr el repositorio

```
