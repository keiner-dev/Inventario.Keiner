# 🧾 Sistema de Inventario en Python

Este proyecto es un sistema básico de inventario desarrollado en Python.  
Permite gestionar productos mediante un menú interactivo en consola.

---

## 🚀 Funcionalidades

- ✅ Agregar productos (nombre, precio y cantidad)
- ✅ Mostrar todos los productos del inventario
- ✅ Calcular estadísticas:
  - Valor total del inventario
  - Cantidad total de productos
- ✅ Validación de datos (evita errores del usuario)
- ✅ Menú interactivo con múltiples opciones

---

## 🧠 Tecnologías utilizadas

- Python
- Estructuras de datos:
  - Listas
  - Diccionarios
- Estructuras de control:
  - if / elif / else
  - while / for
- Manejo de errores con `try/except`

---

## 📦 Estructura del producto

Cada producto se guarda como un diccionario:

```python
producto = {
    "nombre": "Lápiz",
    "precio": 500,
    "cantidad": 3
}