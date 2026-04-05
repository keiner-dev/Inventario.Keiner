"""
servicios.py
Módulo con funciones CRUD y estadísticas para el inventario.
"""


def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto.
        precio (float): Precio unitario del producto.
        cantidad (int): Cantidad en stock.

    Retorno:
        bool: True si se agregó, False si el producto ya existe.
    """
    # Verificar si el producto ya existe (búsqueda insensible a mayúsculas)
    if buscar_producto(inventario, nombre) is not None:
        print(f"  ⚠  El producto '{nombre}' ya existe. Use 'Actualizar' para modificarlo.")
        return False

    inventario.append({
        "nombre": nombre,
        "precio": float(precio),
        "cantidad": int(cantidad)
    })
    print(f"  ✔  Producto '{nombre}' agregado correctamente.")
    return True


def mostrar_inventario(inventario):
    """
    Imprime todos los productos del inventario en formato tabular.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorno:
        None
    """
    if not inventario:
        print("  ℹ  El inventario está vacío.")
        return

    # Encabezado de tabla
    print("\n" + "─" * 55)
    print(f"  {'#':<4} {'Nombre':<20} {'Precio':>10} {'Cantidad':>10}")
    print("─" * 55)

    for i, producto in enumerate(inventario, start=1):
        print(
            f"  {i:<4} {producto['nombre']:<20} "
            f"${producto['precio']:>9.2f} {producto['cantidad']:>10}"
        )

    print("─" * 55)
    print(f"  Total de productos: {len(inventario)}\n")


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre (insensible a mayúsculas).

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a buscar.

    Retorno:
        dict | None: El diccionario del producto si se encuentra, None en caso contrario.
    """
    nombre_lower = nombre.strip().lower()
    for producto in inventario:
        if producto["nombre"].lower() == nombre_lower:
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o cantidad de un producto existente.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a actualizar.
        nuevo_precio (float | None): Nuevo precio; None para no modificar.
        nueva_cantidad (int | None): Nueva cantidad; None para no modificar.

    Retorno:
        bool: True si se actualizó, False si el producto no existe.
    """
    producto = buscar_producto(inventario, nombre)

    if producto is None:
        print(f"  ✘  Producto '{nombre}' no encontrado.")
        return False

    # Actualizar solo los campos proporcionados
    if nuevo_precio is not None:
        producto["precio"] = float(nuevo_precio)
    if nueva_cantidad is not None:
        producto["cantidad"] = int(nueva_cantidad)

    print(f"  ✔  Producto '{nombre}' actualizado correctamente.")
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a eliminar.

    Retorno:
        bool: True si se eliminó, False si no se encontró.
    """
    producto = buscar_producto(inventario, nombre)

    if producto is None:
        print(f"  ✘  Producto '{nombre}' no encontrado.")
        return False

    inventario.remove(producto)
    print(f"  ✔  Producto '{nombre}' eliminado correctamente.")
    return True


def calcular_estadisticas(inventario):
    """
    Calcula métricas del inventario.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorno:
        dict: Diccionario con las siguientes métricas:
            - unidades_totales (int)
            - valor_total (float)
            - producto_mas_caro (dict con 'nombre' y 'precio')
            - producto_mayor_stock (dict con 'nombre' y 'cantidad')
        None: Si el inventario está vacío.
    """
    if not inventario:
        return None

    # Lambda para calcular el subtotal de cada producto
    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)

    # Producto más caro y el de mayor stock
    mas_caro = max(inventario, key=lambda p: p["precio"])
    mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": {"nombre": mas_caro["nombre"], "precio": mas_caro["precio"]},
        "producto_mayor_stock": {"nombre": mayor_stock["nombre"], "cantidad": mayor_stock["cantidad"]},
    }


def mostrar_estadisticas(inventario):
    """
    Imprime las estadísticas del inventario de forma legible.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorno:
        None
    """
    stats = calcular_estadisticas(inventario)

    if stats is None:
        print("  ℹ  El inventario está vacío; no hay estadísticas que mostrar.")
        return

    print("\n" + "─" * 45)
    print("  📊  ESTADÍSTICAS DEL INVENTARIO")
    print("─" * 45)
    print(f"  Unidades totales en stock : {stats['unidades_totales']}")
    print(f"  Valor total del inventario: ${stats['valor_total']:,.2f}")
    print(f"  Producto más caro         : {stats['producto_mas_caro']['nombre']}"
          f" (${stats['producto_mas_caro']['precio']:.2f})")
    print(f"  Mayor stock               : {stats['producto_mayor_stock']['nombre']}"
          f" ({stats['producto_mayor_stock']['cantidad']} unidades)")
    print("─" * 45 + "\n")
