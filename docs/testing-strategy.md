# Testing Strategy — FerreRAP
**Materia:** Ingeniería de Software II · UCP · 2026
**Sistema:** FerreRAP — Gestión de Stock para Ferretería
**Equipo:** Santiago Gonzalez · Luciano Fohrholtz · Juan Carlos Abente · Mariano Acosta

---

## 1. Tipos de pruebas seleccionadas

| Tipo de prueba | ¿Aplica en este proyecto? | Justificación |
| :--- | :---: | :--- |
| Unitarias | ✅ | Verificar la lógica de `registrar_salida()`, el disparo del patrón Observer cuando el stock cae bajo el mínimo, y las validaciones de entrada en la clase `Producto`. |
| Integración | ✅ | Verificar la comunicación entre los endpoints Flask y Supabase mockeado, y que el Observer registra correctamente las alertas en la base de datos. |
| Componentes | ✅ (futuro) | Probar el módulo de ventas completo de forma aislada: carrito → descuento de stock → Observer → registro en Supabase. |
| Sistema (E2E) | ✅ | Flujo completo: login → registrar venta → verificar que el Observer disparó → verificar alerta generada en el panel. |
| Regresión | ✅ | Se automatiza con GitHub Actions en cada push y pull request hacia main. |
| Estrés | 🔜 Planificado | Se implementará en la fase 2 con Locust: 50 usuarios simultáneos registrando ventas durante 2 minutos. |

---

## 2. Herramientas gratuitas elegidas (stack de automatización)

| Nivel de prueba | Herramienta | ¿Qué automatiza en este proyecto? | Justificación |
| :--- | :--- | :--- | :--- |
| Unitarias | pytest + unittest.mock | Lógica de `Producto`, patrón Observer, patrón Strategy, validaciones de stock mínimo. | Nativo de Python, sintaxis simple, sin necesidad de estructura de clases obligatoria. Integración directa con GitHub Actions. |
| Integración | pytest + unittest.mock + Flask test client | Endpoints Flask con Supabase mockeado, flujo Observer → Supabase, respuestas HTTP de la API. | No requiere instalación extra. `unittest.mock` permite simular el cliente de Supabase completamente sin conexión real. |
| Sistema / E2E | Playwright (Python) | Flujo completo: login → inventario → venta → alerta → reporte. | Soporte nativo para Python, manejo de llamadas asíncronas a APIs externas como Supabase, más rápido que Selenium. |
| Estrés | Locust | 50 usuarios simultáneos registrando ventas y consultando reportes en paralelo. | Scripts en Python puro, interfaz web en tiempo real, completamente gratuito, fácil integración con GitHub Actions. |

---

## 3. Ejemplos de casos de prueba unitaria (clases de equivalencia y valores límite)

> **Funcionalidad elegida:** `registrar_salida(cantidad, motivo)` — método de la clase `Producto` en `src/models.py`

### Clases de equivalencia identificadas

- **Válidas:** 1 ≤ cantidad ≤ stock_actual — el método descuenta el stock correctamente.
- **Inválidas (por debajo del rango):** cantidad ≤ 0 — debe lanzar `ValueError`.
- **Inválidas (por encima del rango):** cantidad > stock_actual — debe lanzar `ValueError` con mensaje "Stock insuficiente".
- **Límite inferior válido:** cantidad = 1 — descuenta 1 unidad sin error.
- **Límite superior válido:** cantidad = stock_actual — deja el stock en 0 sin error.
- **Límite cruce mínimo:** la salida deja stock_actual < stock_minimo — dispara el Observer.

### Tres casos de prueba representativos

1. **Caso 1 (válido — sin alerta):**
   Entrada = Producto con stock_actual=10, stock_minimo=5 → registrar_salida(3)
   Resultado esperado = stock_actual=7, Observer NO notificado.

2. **Caso 2 (límite cruce mínimo — Observer se dispara):**
   Entrada = Producto con stock_actual=6, stock_minimo=5 → registrar_salida(2)
   Resultado esperado = stock_actual=4, Observer notificado exactamente una vez.

3. **Caso 3 (inválido — stock insuficiente):**
   Entrada = Producto con stock_actual=3 → registrar_salida(5)
   Resultado esperado = ValueError con mensaje "Stock insuficiente. Stock actual: 3".

### Código de los tres casos en pytest

```python
import pytest
from unittest.mock import MagicMock
from models import Producto

def test_salida_normal_no_dispara_observer():
    p = Producto("Martillo", "desc", 1500, 10, 5, "Herramientas")
    obs = MagicMock()
    p.agregar_observador(obs)
    p.registrar_salida(3, "venta mostrador")
    assert p.stock_actual == 7
    obs.actualizar.assert_not_called()

def test_salida_cruce_minimo_dispara_observer():
    p = Producto("Martillo", "desc", 1500, 6, 5, "Herramientas")
    obs = MagicMock()
    p.agregar_observador(obs)
    p.registrar_salida(2, "venta mostrador")
    assert p.stock_actual == 4
    obs.actualizar.assert_called_once_with(p)

def test_salida_stock_insuficiente_lanza_error():
    p = Producto("Martillo", "desc", 1500, 3, 5, "Herramientas")
    with pytest.raises(ValueError, match="Stock insuficiente"):
        p.registrar_salida(5, "venta")
```

*Casos implementados en: `tests/unit/test_producto.py`*

---

## 4. Plan de mocks / stubs para pruebas de integración

- **Dependencias externas a simular:**
  1. Supabase (base de datos en la nube) — todas las operaciones de lectura y escritura de productos, ventas y alertas.
  2. Flask (servidor HTTP) — los endpoints de la API que el frontend consume.

- **Estrategia de dobles:**
  - Usaremos `unittest.mock.patch` para crear stubs del cliente de Supabase que devuelvan datos predefinidos sin conexión real.
  - Usaremos `app.test_client()` de Flask para hacer llamadas HTTP reales al servidor en modo test.

  - **Ejemplo de prueba de integración:**
    - *Flujo:* POST /api/movimientos → stub de Supabase devuelve producto con stock=10 → sistema descuenta 3 → stub de UPDATE acepta el cambio → endpoint devuelve 201 con el movimiento registrado.
    - *Pseudocódigo:*

```python
def test_registrar_movimiento_salida_exitosa(cliente):
    with patch("app.supabase.table") as mock_tabla:
        # Stub SELECT — devuelve producto simulado
        mock_tabla.return_value.select.return_value \
            .eq.return_value.execute.return_value \
            .data = [{"id":1,"nombre":"Martillo","stock_actual":10,"stock_minimo":5}]

        # Stub UPDATE — simula escritura exitosa
        mock_tabla.return_value.update.return_value \
            .eq.return_value.execute.return_value \
            .data = [{"stock_actual": 7}]

        respuesta = cliente.post("/api/movimientos", json={
            "producto_id": 1, "cantidad": 3,
            "tipo": "salida", "motivo": "venta mostrador"
        })

    assert respuesta.status_code == 201
    assert respuesta.get_json()["movimiento"]["cantidad"] == 3
```

- **Ubicación en el repo:** `tests/integration/test_endpoints.py` y `tests/integration/test_observer_supabase.py`

---

## 5. Pruebas de sistema (E2E) — flujo crítico actual

**Flujo: "Registrar venta que dispara Observer"**

1. Abrir `http://localhost:5000`.
2. Ingresar usuario `empleado` y contraseña `empleado123` → clic en "Ingresar".
3. **Validar** que la pantalla de login desaparece y aparece el sistema con el inventario cargado.
4. Ir a la sección "Movimientos".
5. Seleccionar el producto "Martillo 500g" (stock_actual=6, stock_minimo=5).
6. Seleccionar tipo "Salida", cantidad=2, motivo="venta mostrador" → clic en "Registrar movimiento".
7. **Validar** que aparece el mensaje "Observer disparado — stock bajo mínimo".
8. **Validar** que el stock del producto se actualizó a 4 en la tabla de inventario.
9. Ir a la sección "Alertas".
10. **Validar** que aparece una alerta no leída con el mensaje "Stock bajo en Martillo 500g".

```python
# tests/e2e/test_flujo_venta.py
from playwright.sync_api import sync_playwright

def test_flujo_venta_dispara_observer():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("http://localhost:5000")
        pagina.fill("#l-usuario", "empleado")
        pagina.fill("#l-password", "empleado123")
        pagina.click("button:has-text('Ingresar')")
        pagina.wait_for_selector("#pantalla-app")
        pagina.click("button:has-text('Movimientos')")
        pagina.select_option("#mov-tipo", "salida")
        pagina.fill("#mov-cantidad", "2")
        pagina.fill("#mov-motivo", "venta mostrador")
        pagina.click("button:has-text('Registrar movimiento')")
        pagina.wait_for_selector("#resultado-mov")
        assert "Observer disparado" in pagina.inner_text("#resultado-mov")
        navegador.close()
```

*Script E2E implementado en: `tests/e2e/test_flujo_venta.py`*

**Futuros flujos E2E:**
- Flujo de alta de producto nuevo (solo Administrador).
- Flujo de generación de reporte Strategy con cambio de estrategia en runtime.
- Flujo de resolución de orden de reposición.

---

## 6. Estrategia de regresión automatizada (CI/CD)

- **Herramienta de CI/CD:** GitHub Actions (gratuito en repositorios públicos)
- **Workflow:** `.github/workflows/tests.yml`
- **Activación:** Se ejecuta en cada `push` a cualquier rama y en cada `pull_request` hacia `main`.
- **Qué pruebas ejecuta actualmente:**
  - Tests unitarios (`pytest tests/unit/`)
  - Tests de integración con Supabase mockeado (`pytest tests/integration/`)
  - Verificación de cobertura mínima del 70% en módulos críticos.
- **Reporting:** Los resultados aparecen en la pestaña Actions de GitHub con tilde verde o cruz roja por commit.

```yaml
# .github/workflows/tests.yml
name: Tests FerreRAP
on:
  push:
    branches: ["*"]
  pull_request:
    branches: ["main"]
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - name: Instalar dependencias
        run: pip install pytest pytest-cov flask flask-cors python-dotenv postgrest httpx
      - name: Crear .env de prueba
        run: |
          echo "SUPABASE_URL=http://mock" >> src/.env
          echo "SUPABASE_KEY=mock_key" >> src/.env
          echo "MARGEN_GANANCIA=50" >> src/.env
      - name: Ejecutar tests
        run: cd src && pytest ../tests/ -v --cov=. --cov-fail-under=70
```

---

## 7. Pruebas de estrés — planificación futura

- **Herramienta elegida:** Locust
- **Escenario de carga extrema propuesto:** 50 usuarios simultáneos realizando ventas durante 2 minutos, con picos de 10 ventas por segundo, mientras 10 usuarios consultan reportes en paralelo. El sistema debe responder en menos de 2 segundos por operación sin perder transacciones.
- **Estado actual:** Script base disponible en `tests/stress/locustfile.py`.
- **Hito de implementación:** Mes 5 del plan de implementación, cuando el backend tenga todos los endpoints de ventas y reportes estables.

```python
# tests/stress/locustfile.py
from locust import HttpUser, task, between

class EmpleadoFerreteria(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/api/login", json={
            "usuario": "empleado", "password": "empleado123"
        })

    @task(3)
    def registrar_venta(self):
        self.client.post("/api/movimientos", json={
            "producto_id": 1, "cantidad": 1,
            "tipo": "salida", "motivo": "test estrés"
        })

    @task(2)
    def consultar_inventario(self):
        self.client.get("/api/productos")

    @task(1)
    def consultar_alertas(self):
        self.client.get("/api/alertas")
```

---

## 8. Hoja de ruta de implementación (6 meses)

| Mes | Hito | Responsable |
|---|---|---|
| Mes 1 | Tests unitarios para `models.py`: Observer, Strategy, validaciones de stock. | QA Lead |
| Mes 2 | CI/CD con GitHub Actions: tests unitarios automáticos en cada push. | QA Lead + Dev Lead |
| Mes 3 | Tests de integración para endpoints críticos: ventas, movimientos, alertas. | Dev Lead + QA Lead |
| Mes 4 | Tests E2E con Playwright: flujo completo login → venta → Observer → alerta. | QA Lead + UX Lead |
| Mes 5 | Tests de estrés con Locust: 50 usuarios simultáneos sobre endpoints de ventas. | Dev Lead |
| Mes 6 | Cobertura mínima 80% en módulos críticos, revisión final y documentación. | Todo el equipo |

---

*IS II · UCP Inc. · FerreRAP · 2026*
