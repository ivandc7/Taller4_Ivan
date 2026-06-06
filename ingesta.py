import requests
from pymongo import MongoClient
import time

def extraer_y_guardar_obras():
    print("Iniciando proceso de ingesta de datos...")

    # 1. Conexión a MongoDB
    try:
        cliente_mongo = MongoClient('mongodb://localhost:27017/')
        db = cliente_mongo['taller4_db']
        coleccion = db['raw_data']
        print("Conexión a MongoDB exitosa.")
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        return

    # 2. Configuración de la API (El Disfraz)
    url_base = "https://api.artic.edu/api/v1/artworks"
    # Nos disfrazamos de un navegador Chrome estándar para evitar el Error 403
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    obras_totales = []
    limite_por_pagina = 50 # Pedimos de a 50 para no asustar al servidor
    paginas_a_pedir = 3    # 3 páginas * 50 = 150 obras (cumplimos el requisito de >100)

    # 3. Extracción Paginada
    print("Consultando la API por lotes...")
    for pagina in range(1, paginas_a_pedir + 1):
        parametros = {
            "page": pagina,
            "limit": limite_por_pagina,
            "fields": "id,title,artist_display,date_display,medium_display,department_title,place_of_origin"
        }
        
        try:
            print(f"  -> Descargando página {pagina}...")
            respuesta = requests.get(url_base, headers=cabeceras, params=parametros)
            respuesta.raise_for_status()
            
            datos_json = respuesta.json()
            obras_pagina = datos_json.get("data", [])
            obras_totales.extend(obras_pagina) # Agregamos las obras a nuestra lista maestra
            
            # Pausa de cortesía de 1 segundo para no saturar la API
            time.sleep(1)
            
        except Exception as e:
            print(f"Error en la página {pagina}: {e}")
            break # Si hay error, salimos del ciclo pero guardamos lo que ya descargamos

    cantidad_obras = len(obras_totales)
    print(f"Se descargaron un total de {cantidad_obras} obras de arte.")

    # 4. Almacenamiento en MongoDB
    if cantidad_obras > 0:
        try:
            coleccion.delete_many({}) # Vaciamos la colección vieja
            coleccion.insert_many(obras_totales)
            print(f"¡Éxito! {cantidad_obras} documentos guardados crudos en MongoDB (taller4_db.raw_data).")
        except Exception as e:
            print(f"Error guardando en MongoDB: {e}")
    else:
        print("No se encontraron obras para guardar.")

if __name__ == "__main__":
    extraer_y_guardar_obras()
    
