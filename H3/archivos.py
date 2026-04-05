"""
archivos.py
Módulo para guardar y cargar el inventario en archivos CSV.
"""

import csv
import os


# Encabezado estándar del CSV
ENCABEZADO = ["nombre", "precio", "cantidad"]


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        ruta (str): Ruta del archivo CSV de destino.
        incluir_header (bool): Si True, escribe la fila de encabezado.

    Retorno:
        bool: True si se guardó correctamente, False en caso de error.
    """
    # Validar que el inventario no esté vacío
    if not inventario:
        print("  ⚠  El inventario está vacío. No hay datos para guardar.")
        return False

    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=ENCABEZADO)

            if incluir_header:
                writer.writeheader()  # Escribe: nombre,precio,cantidad

            for producto in inventario:
                writer.writerow({
                    "nombre": producto["nombre"],
                    "precio": producto["precio"],
                    "cantidad": producto["cantidad"]
                })

        print(f"  ✔  Inventario guardado en: {os.path.abspath(ruta)}")
        return True

    except PermissionError:
        print(f"  ✘  Sin permisos para escribir en '{ruta}'. Elija otra ubicación.")
    except OSError as e:
        print(f"  ✘  Error al guardar el archivo: {e}")

    return False


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV y los valida.

    Parámetros:
        ruta (str): Ruta del archivo CSV a leer.

    Retorno:
        tuple: (lista_productos, filas_invalidas)
            - lista_productos (list): Productos válidos con estructura {'nombre', 'precio', 'cantidad'}.
            - filas_invalidas (int): Número de filas omitidas por ser inválidas.
        (None, 0) si ocurre un error crítico (archivo no encontrado, etc.).
    """
    productos = []
    filas_invalidas = 0

    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            reader = csv.reader(archivo)

            # Leer y validar el encabezado
            try:
                encabezado = next(reader)
            except StopIteration:
                print("  ✘  El archivo está vacío.")
                return None, 0

            # Normalizar encabezado (quitar espacios y pasar a minúsculas)
            encabezado_norm = [col.strip().lower() for col in encabezado]
            if encabezado_norm != ENCABEZADO:
                print(
                    f"  ✘  Encabezado inválido: {encabezado}. "
                    f"Se esperaba: {ENCABEZADO}"
                )
                return None, 0

            # Procesar cada fila de datos
            for num_fila, fila in enumerate(reader, start=2):

                # Validar número de columnas
                if len(fila) != 3:
                    print(f"  ⚠  Fila {num_fila} ignorada (columnas incorrectas): {fila}")
                    filas_invalidas += 1
                    continue

                nombre, precio_str, cantidad_str = fila

                # Validar nombre no vacío
                nombre = nombre.strip()
                if not nombre:
                    print(f"  ⚠  Fila {num_fila} ignorada (nombre vacío).")
                    filas_invalidas += 1
                    continue

                # Convertir y validar precio
                try:
                    precio = float(precio_str)
                    if precio < 0:
                        raise ValueError("precio negativo")
                except ValueError:
                    print(f"  ⚠  Fila {num_fila} ignorada (precio inválido: '{precio_str}').")
                    filas_invalidas += 1
                    continue

                # Convertir y validar cantidad
                try:
                    cantidad = int(cantidad_str)
                    if cantidad < 0:
                        raise ValueError("cantidad negativa")
                except ValueError:
                    print(f"  ⚠  Fila {num_fila} ignorada (cantidad inválida: '{cantidad_str}').")
                    filas_invalidas += 1
                    continue

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "cantidad": cantidad
                })

    except FileNotFoundError:
        print(f"  ✘  Archivo no encontrado: '{ruta}'.")
        return None, 0
    except UnicodeDecodeError:
        print(f"  ✘  Error de codificación al leer '{ruta}'. Asegúrese de que sea UTF-8.")
        return None, 0
    except Exception as e:
        print(f"  ✘  Error inesperado al leer el archivo: {e}")
        return None, 0

    return productos, filas_invalidas


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """
    Fusiona los productos_nuevos al inventario_actual sin reemplazarlo.

    Política de fusión:
      - Si el nombre ya existe → suma las cantidades y actualiza al nuevo precio.
      - Si el nombre no existe → agrega el producto.

    Parámetros:
        inventario_actual (list): Inventario en memoria.
        productos_nuevos (list): Productos cargados del CSV.

    Retorno:
        int: Número de productos nuevos agregados (no fusionados).
    """
    print("\n  Política de fusión: si el producto ya existe,")
    print("  se suma la cantidad y se actualiza el precio al del archivo.")

    nuevos_agregados = 0

    for nuevo in productos_nuevos:
        # Buscar manualmente para reutilizar la lógica sin importar servicios (evitar circular)
        existente = next(
            (p for p in inventario_actual if p["nombre"].lower() == nuevo["nombre"].lower()),
            None
        )

        if existente:
            # Fusión: sumar cantidad y actualizar precio
            existente["cantidad"] += nuevo["cantidad"]
            existente["precio"] = nuevo["precio"]
        else:
            inventario_actual.append(nuevo)
            nuevos_agregados += 1

    return nuevos_agregados
