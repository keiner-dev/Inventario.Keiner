"""
app.py
Punto de entrada del sistema de inventario.
Integra el menú principal y conecta los módulos servicios.py y archivos.py.
"""

from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    mostrar_estadisticas,
)
from archivos import guardar_csv, cargar_csv, fusionar_inventarios


# ─────────────────────────────────────────
#  Inventario en memoria (lista de dicts)
# ─────────────────────────────────────────
inventario = []


# ══════════════════════════════════════════
#  Funciones auxiliares de entrada de datos
# ══════════════════════════════════════════

def pedir_texto(mensaje):
    """Solicita una cadena de texto no vacía al usuario."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  ⚠  El campo no puede estar vacío. Intente de nuevo.")


def pedir_float(mensaje):
    """Solicita un número decimal no negativo al usuario."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("  ⚠  El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Ingrese un número válido (ej: 12.50).")


def pedir_int(mensaje):
    """Solicita un número entero no negativo al usuario."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("  ⚠  El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Ingrese un número entero válido (ej: 10).")


def pedir_confirmacion(mensaje):
    """Solicita S o N al usuario. Retorna True si elige S."""
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("  ⚠  Responda con S (sí) o N (no).")


# ══════════════════════════════════════════
#  Handlers de cada opción del menú
# ══════════════════════════════════════════

def opcion_agregar():
    """Maneja el flujo para agregar un nuevo producto."""
    print("\n  ── Agregar producto ──")
    nombre   = pedir_texto("  Nombre   : ")
    precio   = pedir_float("  Precio   : $")
    cantidad = pedir_int(  "  Cantidad : ")
    agregar_producto(inventario, nombre, precio, cantidad)


def opcion_mostrar():
    """Muestra todos los productos del inventario."""
    print("\n  ── Inventario actual ──")
    mostrar_inventario(inventario)


def opcion_buscar():
    """Busca y muestra un producto por nombre."""
    print("\n  ── Buscar producto ──")
    nombre   = pedir_texto("  Nombre a buscar: ")
    producto = buscar_producto(inventario, nombre)

    if producto:
        print(f"\n  ✔  Producto encontrado:")
        print(f"     Nombre   : {producto['nombre']}")
        print(f"     Precio   : ${producto['precio']:.2f}")
        print(f"     Cantidad : {producto['cantidad']}")
    else:
        print(f"  ✘  Producto '{nombre}' no encontrado en el inventario.")


def opcion_actualizar():
    """Actualiza precio y/o cantidad de un producto existente."""
    print("\n  ── Actualizar producto ──")
    nombre = pedir_texto("  Nombre del producto a actualizar: ")

    if buscar_producto(inventario, nombre) is None:
        print(f"  ✘  Producto '{nombre}' no encontrado.")
        return

    print("  (Deje en blanco para no modificar ese campo)")

    # Nuevo precio (opcional)
    nuevo_precio = None
    entrada_precio = input("  Nuevo precio   : $").strip()
    if entrada_precio:
        try:
            nuevo_precio = float(entrada_precio)
            if nuevo_precio < 0:
                print("  ⚠  Precio negativo ignorado.")
                nuevo_precio = None
        except ValueError:
            print("  ⚠  Precio inválido ignorado.")

    # Nueva cantidad (opcional)
    nueva_cantidad = None
    entrada_cantidad = input("  Nueva cantidad : ").strip()
    if entrada_cantidad:
        try:
            nueva_cantidad = int(entrada_cantidad)
            if nueva_cantidad < 0:
                print("  ⚠  Cantidad negativa ignorada.")
                nueva_cantidad = None
        except ValueError:
            print("  ⚠  Cantidad inválida ignorada.")

    if nuevo_precio is None and nueva_cantidad is None:
        print("  ℹ  No se realizaron cambios.")
        return

    actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)


def opcion_eliminar():
    """Elimina un producto del inventario."""
    print("\n  ── Eliminar producto ──")
    nombre = pedir_texto("  Nombre del producto a eliminar: ")

    # Pedir confirmación antes de eliminar
    if pedir_confirmacion(f"  ¿Confirma eliminar '{nombre}'? (S/N): "):
        eliminar_producto(inventario, nombre)
    else:
        print("  ℹ  Operación cancelada.")


def opcion_estadisticas():
    """Muestra las estadísticas del inventario."""
    mostrar_estadisticas(inventario)


def opcion_guardar_csv():
    """Guarda el inventario en un archivo CSV."""
    print("\n  ── Guardar CSV ──")
    ruta = pedir_texto("  Ruta del archivo (ej: inventario.csv): ")
    guardar_csv(inventario, ruta)


def opcion_cargar_csv():
    """Carga productos desde un CSV con opción de sobrescribir o fusionar."""
    global inventario

    print("\n  ── Cargar CSV ──")
    ruta = pedir_texto("  Ruta del archivo CSV a cargar: ")

    # Intentar cargar el archivo
    productos_cargados, filas_invalidas = cargar_csv(ruta)

    if productos_cargados is None:
        # Error crítico ya fue reportado dentro de cargar_csv
        return

    if not productos_cargados:
        print("  ⚠  No se encontraron productos válidos en el archivo.")
        if filas_invalidas:
            print(f"  ℹ  {filas_invalidas} filas inválidas omitidas.")
        return

    # Preguntar acción: sobrescribir o fusionar
    sobrescribir = pedir_confirmacion(
        "\n  ¿Sobrescribir el inventario actual? (S = reemplazar / N = fusionar): "
    )

    if sobrescribir:
        inventario = productos_cargados
        accion = "reemplazo completo"
    else:
        nuevos = fusionar_inventarios(inventario, productos_cargados)
        accion = f"fusión ({nuevos} productos nuevos añadidos)"

    # Resumen final
    print("\n  ─── Resumen de carga ───────────────────")
    print(f"  Productos cargados  : {len(productos_cargados)}")
    print(f"  Filas inválidas     : {filas_invalidas}")
    print(f"  Acción realizada    : {accion}")
    print("  ────────────────────────────────────────")

    # Mostrar inventario actualizado
    mostrar_inventario(inventario)


# ══════════════════════════════════════════
#  Menú principal
# ══════════════════════════════════════════

OPCIONES = {
    "1": ("Agregar producto",   opcion_agregar),
    "2": ("Mostrar inventario", opcion_mostrar),
    "3": ("Buscar producto",    opcion_buscar),
    "4": ("Actualizar producto",opcion_actualizar),
    "5": ("Eliminar producto",  opcion_eliminar),
    "6": ("Estadísticas",       opcion_estadisticas),
    "7": ("Guardar CSV",        opcion_guardar_csv),
    "8": ("Cargar CSV",         opcion_cargar_csv),
    "9": ("Salir",              None),
}


def mostrar_menu():
    """Imprime el menú principal en consola."""
    print("\n" + "═" * 40)
    print("   🗃  SISTEMA DE INVENTARIO")
    print("═" * 40)
    for clave, (nombre, _) in OPCIONES.items():
        print(f"   {clave}. {nombre}")
    print("═" * 40)


def ejecutar_menu():
    """
    Bucle principal del programa.
    Mantiene la aplicación activa hasta que el usuario elige 'Salir'.
    """
    print("\n  Bienvenido al Sistema de Inventario.")

    while True:
        mostrar_menu()

        opcion = input("  Seleccione una opción (1-9): ").strip()

        if opcion not in OPCIONES:
            print("  ⚠  Opción inválida. Ingrese un número entre 1 y 9.")
            continue

        nombre_opcion, handler = OPCIONES[opcion]

        # Opción salir
        if opcion == "9":
            print("\n  Hasta luego. ¡Que tenga un buen día! 👋\n")
            break

        # Ejecutar la opción seleccionada con manejo de errores
        try:
            handler()
        except KeyboardInterrupt:
            print("\n  ℹ  Operación interrumpida. Volviendo al menú...")
        except Exception as e:
            # Captura cualquier error inesperado para no cerrar la app
            print(f"\n  ✘  Error inesperado en '{nombre_opcion}': {e}")
            print("  ℹ  Volviendo al menú principal...")


# ══════════════════════════════════════════
#  Punto de entrada
# ══════════════════════════════════════════

if __name__ == "__main__":
    ejecutar_menu()
