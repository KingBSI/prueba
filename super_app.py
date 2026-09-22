import sqlite3
import urllib.request
import json

# 1. FUNCIÓN CON API: Se conecta a internet para traer el tipo de cambio del dólar en vivo
def obtener_tipo_cambio_api():
    url = "https://er-api.com"
    try:
        # Creamos una petición asignándole un "User-Agent" para simular un navegador real
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as respuesta:
             datos_api = json.loads(respuesta.read().decode())
             precio_soles = datos_api["rates"]["PEN"]
             return precio_soles
    except Exception as e:
        # Si de verdad no hubiera internet, imprimimos el error real para auditarlo
        print(f"⚠️ Error de red: {e}. Usando tipo de cambio fijo: 3.75")
        return 3.75

# 2. FUNCIÓN CON PARÁMETROS Y FILTROS SQL: Filtra la base de datos de forma inteligente
def consultar_con_filtro_avanzado(categoria_buscar, precio_maximo):
    # Conectamos con el archivo creado en la otra lección
    conexion = sqlite3.connect("bicicleta.db")
    cursor = conexion.cursor()
    
    # Traemos el valor del dólar usando nuestra función de API
    tipo_cambio = obtener_tipo_cambio_api()

    # Comando SQL usando "WHERE" para filtrar por categoría y que el costo sea menor al máximo
    # El "AND" nos permite encadenar dos filtros al mismo tiempo
    query = "SELECT id, articulo, costo, categoria FROM presupuesto WHERE categoria = ? AND costo <= ?"
    
    cursor.execute(query, (categoria_buscar, precio_maximo))
    filas = cursor.fetchall()
    
    print("\n" + "="*65)
    print(f"🔍 RESULTADOS FILTRADOS (Categoría: {categoria_buscar} | Máx: S/ {precio_maximo})")
    print(f"💱 Tipo de cambio hoy según API: 1 USD = S/ {tipo_cambio:.2f}")
    print("="*65)
    
    if not filas:
        print(" No se encontraron artículos que cumplan con este filtro.")
    else:
        for fila in filas:
            costo_soles = fila[2]
            # Convertimos matemáticamente los soles a dólares dividiendo por el tipo de cambio de internet
            costo_dolares = costo_soles / tipo_cambio
            
            print(f" 🆔 ID: {fila[0]} | 📦 {fila[1]} | 🇵🇪 S/ {costo_soles:.2f} | 🇺🇸 $ {costo_dolares:.2f}")
            
    print("="*65)
    conexion.close()

if __name__ == "__main__":
    print("--- Probando tu sistema avanzado de Backend ---")
    
    # Ponemos "Seguridad" y un tope de 400 soles para que pesque al Casco (150) y a las Rodilleras (300)
    consultar_con_filtro_avanzado(categoria_buscar="Seguridad", precio_maximo=400.0)
