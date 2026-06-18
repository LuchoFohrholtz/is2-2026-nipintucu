"""
FerreRAP — Pruebas unitarias
TP2 · IS2 · UCP · 2026
Responsable: Juan Carlos Abente — QA Lead

Ejecutar con:
    pytest tests/unit/test_models.py -v
"""

import pytest
from models import Producto, Alerta, OrdenReposicion, StockMovimiento


# ─────────────────────────────────────────────────────────────
#  FIXTURES — objetos reutilizables entre tests
# ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def resetear_contadores():
    """Resetea los contadores de ID antes de cada test para evitar interferencias."""
    Producto._contador = 1
    StockMovimiento._contador = 1


@pytest.fixture
def producto_normal():
    """Producto con stock holgado: stock_actual=10, stock_minimo=5."""
    return Producto("Martillo 500g", "Martillo de carpintero", 1500, 10, 5, "Herramientas")


@pytest.fixture
def producto_bajo():
    """Producto con stock exactamente en el límite: stock_actual=5, stock_minimo=5."""
    return Producto("Destornillador Ph", "Phillips #2", 800, 5, 5, "Herramientas")


@pytest.fixture
def producto_critico():
    """Producto con stock ya bajo mínimo: stock_actual=2, stock_minimo=5."""
    return Producto("Llave de paso 1/2", "Bronce media pulgada", 2200, 2, 5, "Plomería")


# ─────────────────────────────────────────────────────────────
#  TC01 — Salida válida: el stock se decrementa correctamente
#  Técnica: Partición de equivalencia — clase válida (CE1)
# ─────────────────────────────────────────────────────────────

def test_TC01_salida_valida_decrementa_stock(producto_normal):
    mov = producto_normal.registrar_salida(3, "Venta mostrador")

    assert producto_normal.stock_actual == 7
    assert mov.tipo == "salida"
    assert mov.cantidad == 3
    assert mov.motivo == "Venta mostrador"
    assert mov.producto_nombre == "Martillo 500g"


# ─────────────────────────────────────────────────────────────
#  TC02 — Salida con cantidad cero: debe lanzar ValueError
#  Técnica: Valor límite inferior inválido (CE2: cantidad = 0)
# ─────────────────────────────────────────────────────────────

def test_TC02_salida_cantidad_cero_lanza_error(producto_normal):
    with pytest.raises(ValueError, match="La cantidad debe ser mayor a cero"):
        producto_normal.registrar_salida(0, "Test")

    # El stock no debe haberse modificado
    assert producto_normal.stock_actual == 10


# ─────────────────────────────────────────────────────────────
#  TC03 — Salida mayor al stock disponible: debe lanzar ValueError
#  Técnica: Valor límite superior inválido (CE3: cantidad = stock_actual + 1)
# ─────────────────────────────────────────────────────────────

def test_TC03_salida_supera_stock_lanza_error(producto_normal):
    with pytest.raises(ValueError, match="Stock insuficiente"):
        producto_normal.registrar_salida(11, "Test")

    # El stock no debe haberse modificado
    assert producto_normal.stock_actual == 10


# ─────────────────────────────────────────────────────────────
#  TC04 — Salida que deja stock bajo mínimo activa el Observer
#  Técnica: Valor límite superior válido (CE1) + verificación Observer
# ─────────────────────────────────────────────────────────────

def test_TC04_salida_bajo_minimo_dispara_observer(producto_bajo):
    alerta = Alerta()
    producto_bajo.agregar_observador(alerta)

    producto_bajo.registrar_salida(1, "Venta")

    assert producto_bajo.stock_actual == 4
    assert producto_bajo.bajo_stock is True
    assert len(alerta.historial) == 1
    assert alerta.historial[0]["tipo"] == "alerta"
    assert alerta.historial[0]["producto"] == "Destornillador Ph"


# ─────────────────────────────────────────────────────────────
#  TC05 — Entrada válida: el stock se incrementa correctamente
#  Técnica: Partición de equivalencia — clase válida
# ─────────────────────────────────────────────────────────────

def test_TC05_entrada_valida_incrementa_stock(producto_critico):
    mov = producto_critico.registrar_entrada(10, "Reposición proveedor")

    assert producto_critico.stock_actual == 12
    assert mov.tipo == "entrada"
    assert mov.cantidad == 10
    assert mov.motivo == "Reposición proveedor"


# ─────────────────────────────────────────────────────────────
#  TC06 — Entrada que normaliza el stock cierra órdenes pendientes
#  Técnica: Partición de equivalencia + Observer inverso (resolver)
# ─────────────────────────────────────────────────────────────

def test_TC06_entrada_normaliza_stock_cierra_ordenes(producto_critico):
    orden_obs = OrdenReposicion()
    producto_critico.agregar_observador(orden_obs)

    # Simular una orden pendiente preexistente
    orden_obs.ordenes.append({
        "tipo": "orden",
        "producto": "Llave de paso 1/2",
        "mensaje": "Reponer 'Llave de paso 1/2'",
        "cantidad_sugerida": 10,
        "fecha": "01/05/2026 10:00",
        "estado": "pendiente"
    })

    producto_critico.registrar_entrada(10, "Reposición proveedor")

    assert producto_critico.stock_actual == 12
    assert producto_critico.bajo_stock is False
    assert orden_obs.ordenes[0]["estado"] == "resuelta"
    assert "fecha_resolucion" in orden_obs.ordenes[0]
