print("=== SISTEMA DE INVENTARIO ===")
# Lista donde se guardarán los productos
inventario = []

# FUNCIÓN PARA AGREGAR PRODUCTOS
def agregar_producto():
    print("\n--- AGREGAR PRODUCTO ---")
    
    # Validar nombre
    while True:
        nombre = input("Ingrese el nombre del producto: ").strip()
        if nombre == "":
            print("Error: El nombre no puede estar vacío.")
        else:
            break
    
    # Validar precio
    while True:
        try:
            precio = float(input("Ingrese el precio del producto: "))
            if precio <= 0:
                print("Error: El precio debe ser mayor a 0.")
            else:
                break
        except ValueError:
            print("Error: Debe ingresar un número válido.")
    
    # Validar cantidad
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad del producto: "))
            if cantidad < 0:
                print("Error: La cantidad no puede ser negativa.")
            else:
                break
        except ValueError:
            print("Error: Debe ingresar un número entero.")
    
    # Crear el producto como diccionario
    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    
    # Guardar en la lista
    inventario.append(producto)
    
    print("Producto agregado correctamente ✅")



# FUNCIÓN PARA MOSTRAR INVENTARIO
def mostrar_inventario():
    print("\n--- INVENTARIO ---")
    
    # Verificar si está vacío
    if len(inventario) == 0:
        print("El inventario está vacío.")
    else:
        # Recorrer con for
        for producto in inventario:
            print(f"Producto: {producto['nombre']} | Precio: {producto['precio']} | Cantidad: {producto['cantidad']}")


# FUNCIÓN PARA CALCULAR ESTADÍSTICAS
def calcular_estadisticas():
    print("\n--- ESTADÍSTICAS ---")
    
    # Verificar si hay productos
    if len(inventario) == 0:
        print("No hay productos para calcular.")
        return
    
    total_inventario = 0
    total_productos = 0
    
    # Recorrer productos
    for producto in inventario:
        total_inventario += producto["precio"] * producto["cantidad"]
        total_productos += producto["cantidad"]
    
    print(f"Valor total del inventario: {total_inventario}")
    print(f"Cantidad total de productos: {total_productos}")


# MENÚ PRINCIPAL CON BUCLE WHILE
while True:
    print("\n--- MENÚ ---")
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Calcular estadísticas")
    print("4. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    # Condicionales
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        mostrar_inventario()
    elif opcion == "3":
        calcular_estadisticas()
    elif opcion == "4":
        print("Saliendo del sistema...")
        break
    else:
        print("Error: Opción inválida. Intente nuevamente.")


# Este programa permite gestionar un inventario básico usando listas y diccionarios.
# Se aplican estructuras condicionales, bucles y validaciones para asegurar
# que los datos ingresados sean correctos.
# Además, se calculan estadísticas como el valor total del inventario
# y la cantidad total de productos registrados.
