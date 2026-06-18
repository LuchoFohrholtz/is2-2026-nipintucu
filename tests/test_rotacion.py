"""
Prueba unitaria del Reporte de Rotacion de Inventario (mejora integradora).
Valida el calculo de la estrategia ReporteRotacion con datos conocidos,
de forma independiente de la base de datos (Supabase).

Ejecutar desde la raiz del proyecto con:
    pytest tests/test_rotacion.py -v
"""

import sys, os
# Permite importar models.py desde la carpeta src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models import ReporteRotacion


# Datos de prueba con valores fijos y conocidos
PRODUCTOS = [
    {"nombre": "Martillo",  "categoria": "Herramientas", "stock_actual": 10,
     "precio_costo": 1000, "precio_venta": 1500, "stock_minimo": 5},
    {"nombre": "Cable",     "categoria": "Electricidad", "stock_actual": 20,
     "precio_costo": 200,  "precio_venta": 300,  "stock_minimo": 10},
    {"nombre": "Sin ventas","categoria": "Otra",         "stock_actual": 7,
     "precio_costo": 50,   "precio_venta": 80,   "stock_minimo": 3},
]

MOVIMIENTOS = [
    # Martillo: dos salidas (4 + 6 = 10 unidades, 2 eventos -> promedio 5)
    {"producto_nombre": "Martillo", "tipo": "salida", "cantidad": 4},
    {"producto_nombre": "Martillo", "tipo": "salida", "cantidad": 6},
    # Cable: una salida de 5 unidades (1 evento -> promedio 5)
    {"producto_nombre": "Cable", "tipo": "salida", "cantidad": 5},
    # Una entrada que NO debe contarse como salida
    {"producto_nombre": "Cable", "tipo": "entrada", "cantidad": 100},
    # "Sin ventas" no tiene ningun movimiento
]


def _fila(resultado, nombre):
    """Devuelve la fila del resultado correspondiente a un producto."""
    return next(f for f in resultado if f["nombre"] == nombre)


def test_total_salidas():
    """total_salidas debe sumar solo los movimientos de tipo 'salida'."""
    r = ReporteRotacion(MOVIMIENTOS).generar(PRODUCTOS)
    assert _fila(r, "Martillo")["total_salidas"] == 10
    assert _fila(r, "Cable")["total_salidas"] == 5   # la entrada de 100 no cuenta


def test_promedio_salida():
    """promedio_salida = total de unidades / cantidad de eventos de salida."""
    r = ReporteRotacion(MOVIMIENTOS).generar(PRODUCTOS)
    assert _fila(r, "Martillo")["promedio_salida"] == 5.0   # 10 / 2 eventos
    assert _fila(r, "Cable")["promedio_salida"] == 5.0      # 5 / 1 evento


def test_dias_hasta_quiebre():
    """dias_hasta_quiebre = int(stock_actual / promedio_salida)."""
    r = ReporteRotacion(MOVIMIENTOS).generar(PRODUCTOS)
    assert _fila(r, "Martillo")["dias_hasta_quiebre"] == 2   # int(10 / 5)
    assert _fila(r, "Cable")["dias_hasta_quiebre"] == 4      # int(20 / 5)


def test_producto_sin_movimientos():
    """Un producto sin salidas: total 0 y dias_hasta_quiebre nulo (sin datos)."""
    r = ReporteRotacion(MOVIMIENTOS).generar(PRODUCTOS)
    fila = _fila(r, "Sin ventas")
    assert fila["total_salidas"] == 0
    assert fila["promedio_salida"] == 0
    assert fila["dias_hasta_quiebre"] is None


def test_orden_por_rotacion():
    """El resultado se ordena de mayor a menor total_salidas."""
    r = ReporteRotacion(MOVIMIENTOS).generar(PRODUCTOS)
    totales = [f["total_salidas"] for f in r]
    assert totales == sorted(totales, reverse=True)
