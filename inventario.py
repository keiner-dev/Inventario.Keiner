print("INVENTARIO EN PYTHON")
# Inicia un ciclo infinito para pedir el nombre hasta que el usuario escriba uno válido
while True:
    # Pide al usuario el nombre del producto y elimina espacios al inicio y al final
    nombre = input("Ingrese el nombre del producto: ").strip()
    # Verifica si el usuario no escribió nada
    if nombre == "":
        # Muestra un mensaje de error si el nombre está vacío
        print("Error: Debe ingresar un nombre para el producto.")
    else:
        # Si el nombre es válido, rompe el ciclo y continúa el programa
        break

# Inicia otro ciclo infinito para pedir el precio hasta que sea válido
while True:
    # Intenta ejecutar el siguiente bloque de código
    try:
        # Pide el precio del producto y lo convierte a número decimal (float)
        precio = float(input("Ingrese el precio del producto: "))
        # Si no ocurre ningún error, sale del ciclo
        break
    # Si ocurre un error al convertir el dato (por ejemplo si escriben texto)
    except ValueError:
        # Muestra un mensaje indicando que el dato ingresado no es válido
        print("Error: Debe ingresar un número válido para el precio.")

# Inicia otro ciclo infinito para pedir la cantidad hasta que sea válida
while True:
    # Intenta ejecutar el siguiente bloque
    try:
        # Pide la cantidad del producto y la convierte a número entero
        cantidad = int(input("Ingrese la cantidad del producto: "))
        # Si el número es válido, sale del ciclo
        break
    # Si el usuario escribe algo que no es un número entero
    except ValueError:
        print("Error: Debe ingresar un número entero válido para la cantidad.")

# Calcula el costo total multiplicando el precio por la cantidad
costo_total = precio * cantidad

# Muestra en consola toda la información del producto y el total calculado
print(f"Producto: {nombre} | Precio: {precio} | Cantidad: {cantidad} | Total: {costo_total}")

