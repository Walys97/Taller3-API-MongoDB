"""
Taller 3 - Fases 1 y 2: Extraccion desde una API publica y almacenamiento RAW en MongoDB.

API utilizada: Art Institute of Chicago
    https://api.artic.edu/api/v1/artworks
Autor: Walys Vera Herrera
"""

import requests
from pymongo import MongoClient

# ---------------- Configuracion ----------------
API_URL = "https://api.artic.edu/api/v1/artworks"
HEADERS = {"AIC-User-Agent": "Taller3-UdeA (proyecto academico)"}

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "taller3_db"
COLLECTION_NAME = "raw_data"

REGISTROS_POR_PAGINA = 100   # maximo que permite la API por peticion
PAGINAS = 2                  # 2 x 100 = 200 obras (el taller pide minimo 100)


def conectar_mongo():
    """Se conecta a MongoDB y devuelve la coleccion raw_data de la base taller3_db."""
    cliente = MongoClient(MONGO_URI)
    base = cliente[DB_NAME]
    return base[COLLECTION_NAME]


def descargar_obras(pagina):
    """Descarga una pagina de obras de arte y devuelve la lista de JSON crudos."""
    parametros = {"page": pagina, "limit": REGISTROS_POR_PAGINA}
    respuesta = requests.get(API_URL, params=parametros, headers=HEADERS, timeout=30)
    respuesta.raise_for_status()          # corta si la API responde con error
    return respuesta.json()["data"]


def guardar_raw(coleccion, obras):
    """Guarda cada obra TAL CUAL llega de la API, usando el id de la API como _id."""
    guardadas = 0
    for obra in obras:
        documento = dict(obra)            # copia del JSON crudo, sin transformar
        documento["_id"] = obra["id"]     # el id de la API es la llave del documento
        # replace_one con upsert evita duplicados si el script se ejecuta varias veces
        coleccion.replace_one({"_id": documento["_id"]}, documento, upsert=True)
        guardadas += 1
    return guardadas


def main():
    """Descarga las obras y las guarda crudas en MongoDB."""
    coleccion = conectar_mongo()
    total = 0

    for pagina in range(1, PAGINAS + 1):
        print(f"Descargando pagina {pagina} de {PAGINAS}...")
        obras = descargar_obras(pagina)
        total += guardar_raw(coleccion, obras)

    print(f"Documentos guardados o actualizados: {total}")
    print(f"Total en {DB_NAME}.{COLLECTION_NAME}: {coleccion.count_documents({})}")


if __name__ == "__main__":
    main()