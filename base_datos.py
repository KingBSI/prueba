import sqlite3

def inicializar_sistema():
    conexion = sqlite3.connect("bicicleta.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presupuesto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            articulo TEXT NOT NULL,
            costo REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def insertar_articulo():
    print("\n➕ AÑADIR ARTÍCULO A LA BASE DE DATOS")
    while True:
        nombre = input("Nombre del artículo (ej. Casco): ").strip()
        if nombre: break
        print("❌ Error: El nombre no puede estar vacío.")

    while True:
        categoria = input("Categoría (ej. Seguridad): ").strip()
        if categoria: break
        print("❌ Error: La categoría no puede estar vacía.")
    
    while True:
        try:
            costo = float(input("Costo estimado en soles: "))
            if costo >= 0: break
            print("❌ Error: El costo no puede ser negativo.")
        except ValueError:
            print("❌ Error: Ingresa un número válido.")

    conexion = sqlite3.connect("bicicleta.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO presupuesto (articulo, costo, categoria) VALUES (?, ?, ?)", (nombre, costo, categoria))
    conexion.commit()
    conexion.close()
    print(f"🎉 ¡'{nombre}' guardado con éxito en SQL!")

def mostrar_presupuesto():
    conexion = sqlite3.connect("bicicleta.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, articulo, costo, categoria FROM presupuesto")
    filas = cursor.fetchall()
    
    print("\n" + "="*50)
    print("📋 REGISTROS EN TU BASE DE DATOS SQL")
    print("="*50)
    
    if not filas:
        print(" El inventario está vacío actualmente.")
    else:
        for fila in filas:
            # fila[0] es el ID, fila[1] es el nombre, fila[2] el costo y fila[3] la categoría
            print(f" 🆔 ID: {fila[0]} | 📦 {fila[1]} | 💰 S/ {fila[2]} | 📂 {fila[3]}")
            
    print("="*50)
    conexion.close()

# ✨ FUNCIÓN NUEVA: Eliminar un registro usando comandos SQL reales
def eliminar_articulo_sql():
    # Primero mostramos lo que hay para que el usuario vea los IDs disponibles
    mostrar_presupuesto()
    
    print("\n❌ ELIMINAR ARTÍCULO POR ID")
    try:
        id_borrar = int(input("Ingresa el número de ID del artículo que deseas borrar: "))
    except ValueError:
        print("❌ Error: Debes ingresar un número entero para el ID.")
        return

    conexion = sqlite3.connect("bicicleta.db")
    cursor = conexion.cursor()
    
    # El comando profesional de SQL para borrar una fila específica es DELETE FROM ... WHERE
    cursor.execute("DELETE FROM presupuesto WHERE id = ?", (id_borrar,))
    
    # cursor.rowcount nos dice cuántas filas se vieron afectadas por el comando
    if cursor.rowcount > 0:
        print(f"🗑️ ¡Registro con ID {id_borrar} eliminado físicamente de la base de datos!")
    else:
        print(f"⚠️ No se encontró ningún artículo con el ID {id_borrar}.")
        
    conexion.commit()
    conexion.close()

def menu_interactivo():
    inicializar_sistema()
    while True:
        print("\n🗄️ CONTROL DE BASE DE DATOS SQLITE:")
        print("1. Ver artículos guardados")
        print("2. Agregar artículo nuevo")
        print("3. ELIMINAR artículo por ID")
        print("4. Salir")
        
        opcion = input("Selecciona una opción (1, 2, 3 o 4): ").strip()
        
        if opcion == "1":
            mostrar_presupuesto()
        elif opcion == "2":
            insertar_articulo()
        elif opcion == "3":
            eliminar_articulo_sql() # Llamamos a la nueva función de borrado SQL
        elif opcion == "4":
            print("\n👋 ¡Conexión con SQLite cerrada! Sigue rompiéndola.")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    menu_interactivo()
