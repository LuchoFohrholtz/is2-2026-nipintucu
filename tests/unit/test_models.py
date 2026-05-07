"""
FerreRAP — Pruebas unitarias con pytest
IS2 · UCP · 2026

Estas pruebas verifican el funcionamiento de las estrategias de reportes
implementadas en src/models.py.
"""

from models import GeneradorReporte, ReporteReposicion, ReporteStockActual


def productos_de_prueba():
    return [
        {
            "nombre": "Martillo 500g",
            "descripcion": "Martillo de carpintero",
            "categoria": "Herramientas",
            "stock_actual": 8,
            "stock_minimo": 5,
            "precio_costo": 1000,
            "precio_venta": 1500,
        },
        {
            "nombre": "Destornillador Ph",
            "descripcion": "Phillips punta fina #2",
            "categoria": "Herramientas",
            "stock_actual": 3,
            "stock_minimo": 5,
            "precio_costo": 530,
            "precio_venta": 800,
        },
        {
            "nombre": "Llave de paso 1/2",
            "descripcion": "Bronce, media pulgada",
            "categoria": "Plomeria",
            "stock_actual": 2,
            "stock_minimo": 4,
            "precio_costo": 1470,
            "precio_venta": 2200,
        },
    ]


def test_reporte_reposicion_devuelve_solo_productos_con_stock_bajo():
    productos = productos_de_prueba()

    generador = GeneradorReporte(ReporteReposicion())
    resultado = generador.ejecutar(productos)

    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Destornillador Ph"
    assert resultado[1]["nombre"] == "Llave de paso 1/2"


def test_reporte_reposicion_no_incluye_productos_con_stock_suficiente():
    productos = productos_de_prueba()

    generador = GeneradorReporte(ReporteReposicion())
    resultado = generador.ejecutar(productos)

    nombres = [producto["nombre"] for producto in resultado]

    assert "Martillo 500g" not in nombres


def test_reporte_stock_actual_devuelve_todos_los_productos():
    productos = productos_de_prueba()

    generador = GeneradorReporte(ReporteStockActual())
    resultado = generador.ejecutar(productos)

    assert len(resultado) == 3


def test_reporte_stock_actual_marca_correctamente_bajo_stock():
    productos = productos_de_prueba()

    generador = GeneradorReporte(ReporteStockActual())
    resultado = generador.ejecutar(productos)

    martillo = resultado[0]
    destornillador = resultado[1]
    llave = resultado[2]

    assert martillo["bajo_stock"] is False
    assert destornillador["bajo_stock"] is True
    assert llave["bajo_stock"] is True


def test_generador_reporte_permite_cambiar_estrategia():
    productos = productos_de_prueba()

    generador = GeneradorReporte(ReporteReposicion())
    resultado_reposicion = generador.ejecutar(productos)

    generador.cambiar_estrategia(ReporteStockActual())
    resultado_stock = generador.ejecutar(productos)

    assert len(resultado_reposicion) == 2
    assert len(resultado_stock) == 3
