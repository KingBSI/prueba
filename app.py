import json
import os

def cargar_datos():
    if not os.path.exists("data.json"):
        print("❌ Error: No se encontró el archivo 'data.json'.")
        return None
    with open("data.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_datos(datos):
    with open("data.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)

def mostrar_reporte(datos):
    capital = datos.get("income", 0)
    moneda = datos.get("labels", {}).get("currencySymbol", "S/")
    total_gastos = 0
    
    print("\n" + "="*45)
    print(f"📊 REPORTE CONSOLIDADO DE PRESUPUESTO")
    print("="*45)
    
    for categoria in datos.get("categories", []):
        print(f"\n📂 {categoria['label']} ({categoria['key'].upper()}):")
        for elemento in categoria.get("fields", []):
            print(f"   • [{elemento['key']}] {elemento['label']}: {moneda} {elemento['value']}")
            total_gastos += elemento["value"]
            
    restante = capital - total_gastos
    print("-"*45)
    print(f"💰 Fondo Inicial: {moneda} {capital}")
    print(f"📉 Total Gastado: {moneda} {total_gastos}")
    if restante >= 0:
        print(f"✅ Saldo Disponible: {moneda} {restante}")
    else:
        print(f"⚠️ Alerta Deuda: {moneda} {restante}")
    print("="*45)

def agregar_nuevo_articulo(datos):
    print("\n➕ AÑADIR NUEVO ARTÍCULO AL PRESUPUESTO")
    print("Categorías disponibles: seguridad, accesorios, operacion")
    cat_key = input("Ingresa la clave de la categoría: ").strip().lower()
    
    if cat_key not in [c["key"] for c in datos.get("categories", [])]:
        print("❌ Error: Esa categoría no existe.")
        return

    clave_corta = input("Crea una clave corta para el artículo (ej. inflador): ").strip().lower()
    nombre_largo = input("Escribe el nombre completo del artículo: ").strip()
    
    try:
        costo = float(input("Ingresa el costo en soles: "))
        min_val = float(input("Define el precio mínimo del slider: "))
        max_val = float(input("Define el precio máximo del slider: "))
    except ValueError:
        print("❌ Error: Debes ingresar números válidos.")
        return

    nuevo_elemento = {
        "key": clave_corta,
        "label": nombre_largo,
        "value": costo,
        "min": min_val,
        "max": max_val,
        "step": 1
    }

    for categoria in datos.get("categories", []):
        if categoria.get("key") == cat_key:
            categoria.get("fields", []).append(nuevo_elemento)
            guardar_datos(datos)
            print(f"🎉 ¡'{nombre_largo}' inyectado con éxito en data.json!")
            break

# ✨ FUNCIÓN NUEVA: Borrar un artículo por su clave
def eliminar_articulo(datos):
    print("\n❌ ELIMINAR UN ARTÍCULO")
    llave_buscar = input("Ingresa la clave corta del artículo que deseas borrar: ").strip().lower()
    
    encontrado = False
    
    # Recorremos las categorías del JSON
    for categoria in datos.get("categories", []):
        campos = categoria.get("fields", [])
        
        # Buscamos si la clave corta existe en esta lista de campos
        for elemento in campos:
            if elemento.get("key") == llave_buscar:
                # El método .remove() elimina el objeto exacto de la lista en memoria
                campos.remove(elemento)
                encontrado = True
                print(f"🗑️ ¡El artículo '{elemento['label']}' ha sido eliminado del presupuesto!")
                break
        if encontrado:
            break
            
    if encontrado:
        guardar_datos(datos)
    else:
        print("❌ No se encontró ningún artículo con esa clave corta.")

def menu_interactivo():
    datos = cargar_datos()
    if not datos: return

    while True:
        mostrar_reporte(datos)
        print("\n🛠️ MENÚ DE CONTROL:")
        print("1. Modificar precio de un artículo existente")
        print("2. Añadir un artículo TOTALMENTE NUEVO")
        print("3. ELIMINAR un artículo")
        print("4. Salir del programa")
        
        opcion = input("Selecciona una opción (1, 2, 3 o 4): ").strip()
        
        if opcion == "1":
            llave_articulo = input("Ingresa la clave corta del artículo a cambiar: ").strip().lower()
            try:
                nuevo_precio = float(input("Ingresa el nuevo costo en soles: "))
            except ValueError:
                print("❌ Error: Número inválido.")
                continue
            
            encontrado = False
            for categoria in datos.get("categories", []):
                for elemento in categoria.get("fields", []):
                    if elemento.get("key") == llave_articulo:
                        elemento["value"] = nuevo_precio
                        encontrado = True
                        break
            if encontrado:
                guardar_datos(datos)
                print("💾 ¡Precio modificado y guardado!")
            else:
                print("❌ No se encontró el artículo.")
                
        elif opcion == "2":
            agregar_nuevo_articulo(datos)
            
        elif opcion == "3":
            eliminar_articulo(datos) # Llamada a la nueva función de borrado
            
        elif opcion == "4":
            print("\n👋 ¡Entorno cerrado! Sigue practicando para volverte un crack.")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    menu_interactivo()
