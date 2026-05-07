# Pruebas Unitarias — TP2 · FerreRAP

**Materia:** Ingeniería de Software II  
**Institución:** Universidad de la Cuenca del Plata · 2026  
**Entrega:** Trabajo Práctico N°2 — Parte B  
**Responsable:** Juan Carlos Abente · QA Lead

---

## B0 — Investigación previa: técnicas de diseño de casos de prueba

### ¿Qué es una clase de equivalencia y cómo se aplica?

Una **clase de equivalencia** (o partición de equivalencia) es una técnica de diseño de pruebas de caja negra que divide el dominio de entrada de una función en grupos (*clases*) de valores que, desde el punto de vista del sistema, deben producir el mismo comportamiento. La premisa es que si una prueba con cualquier valor de la clase detecta un defecto, cualquier otro valor de esa misma clase también lo detectaría; y si no lo detecta, ningún otro valor de la clase lo hará. Esto permite reducir la cantidad de casos de prueba necesarios sin perder cobertura.

Las clases se clasifican en:

- **Clases válidas:** entradas que el sistema debería aceptar y procesar correctamente.
- **Clases inválidas:** entradas que el sistema debería rechazar con un error controlado.

**Ejemplo concreto aplicado a `registrar_salida(cantidad, motivo)` de `Producto`:**

El parámetro `cantidad` tiene las siguientes reglas según el código:
- Debe ser mayor a cero (`cantidad > 0`)
- No puede superar el stock disponible (`cantidad ≤ stock_actual`)

Esto genera tres clases de equivalencia:

| Clase | Rango | Tipo | Comportamiento esperado |
|-------|-------|------|-------------------------|
| CE1 | `1 ≤ cantidad ≤ stock_actual` | Válida | Stock decrementado, movimiento registrado |
| CE2 | `cantidad ≤ 0` | Inválida | `ValueError`: "La cantidad debe ser mayor a cero." |
| CE3 | `cantidad > stock_actual` | Inválida | `ValueError`: "Stock insuficiente. Stock actual: X" |

Con tres clases identificadas, bastan tres casos de prueba para cubrir todos los escenarios posibles. Sin esta técnica, un programador podría probar docenas de valores sin mayor cobertura real.

---

### ¿Qué es un valor límite y cómo se usa para encontrar defectos?

El **análisis de valores límite** (BVA, *Boundary Value Analysis*) complementa la partición de equivalencia. La experiencia empírica en pruebas de software muestra que los defectos se concentran en los bordes de las clases de equivalencia: un `>` codificado como `>=`, un índice fuera de rango, un off-by-one. La técnica indica probar los valores exactamente en el límite de cada clase y los adyacentes inmediatos.

Para una partición `[mín, máx]` se prueban típicamente: `mín - 1`, `mín`, `máx`, `máx + 1`.

**Ejemplo concreto aplicado a `registrar_salida(cantidad, motivo)`** con un producto de `stock_actual = 5`:

| Valor | Posición | Clase | Resultado esperado |
|-------|----------|-------|--------------------|
| `0` | Límite inferior de CE2 | Inválida | `ValueError` |
| `1` | Límite inferior de CE1 | Válida | Stock decrementado a 4 |
| `5` | Límite superior de CE1 | Válida | Stock decrementado a 0 |
| `6` | Límite inferior de CE3 | Inválida | `ValueError` |

Si el código tuviera un bug usando `cantidad < 0` en vez de `cantidad <= 0`, solo el análisis de valores límite (testeando `cantidad = 0`) lo detectaría. Sin esta técnica, ese defecto pasaría inadvertido.

---

## B1 — Casos de prueba unitaria

Los siguientes casos de prueba cubren los métodos más críticos del dominio (`models.py`). El código correspondiente se encuentra en `tests/unit/`. Cada caso especifica el método bajo prueba, la técnica aplicada, los datos de entrada y el resultado esperado.

### Resumen de cobertura

| # | Método bajo prueba | Técnica | Tipo |
|---|-------------------|---------|------|
| TC01 | `Producto.registrar_salida()` | Clase válida (CE1) | Funcional positivo |
| TC02 | `Producto.registrar_salida()` | Valor límite inferior inválido (CE2) | Error esperado |
| TC03 | `Producto.registrar_salida()` | Valor límite superior inválido (CE3) | Error esperado |
| TC04 | `Producto.registrar_salida()` | Valor límite superior válido (CE1) | Observer + funcional |
| TC05 | `Producto.registrar_entrada()` | Clase válida | Funcional positivo |
| TC06 | `Producto.registrar_entrada()` | Observer inverso (reposición) | Integración de Observer |

---

### TC01 — Salida válida: stock se decrementa correctamente

| Campo | Detalle |
|-------|---------|
| **Método bajo prueba** | `Producto.registrar_salida(cantidad, motivo)` |
| **Técnica aplicada** | Partición de equivalencia — clase válida (CE1) |
| **Precondición** | Producto con `stock_actual = 10`, `stock_minimo = 5` |
| **Datos de entrada** | `cantidad = 3`, `motivo = "Venta mostrador"` |
| **Resultado esperado** | `stock_actual` pasa a `7`; el método retorna un objeto `StockMovimiento` con `tipo = "salida"` y `cantidad = 3`; no se generan notificaciones de alerta |
| **Criterio de pasar** | `p.stock_actual == 7` y `mov.tipo == "salida"` |

```python
def test_TC01_salida_valida_decrementa_stock():
    p = Producto("Martillo", "desc", 1500, 10, 5, "Herramientas")
    mov = p.registrar_salida(3, "Venta mostrador")
    assert p.stock_actual == 7
    assert mov.tipo == "salida"
    assert mov.cantidad == 3
```

---

### TC02 — Salida con cantidad cero: debe lanzar ValueError

| Campo | Detalle |
|-------|---------|
| **Método bajo prueba** | `Producto.registrar_salida(cantidad, motivo)` |
| **Técnica aplicada** | Valor límite inferior inválido (límite de CE2: `cantidad = 0`) |
| **Precondición** | Producto con `stock_actual = 10` |
| **Datos de entrada** | `cantidad = 0`, `motivo = "Test"` |
| **Resultado esperado** | Se lanza `ValueError` con el mensaje `"La cantidad debe ser mayor a cero."` |
| **Criterio de pasar** | La excepción es capturada correctamente; el stock no se modifica |

```python
def test_TC02_salida_cantidad_cero_lanza_error():
    p = Producto("Martillo", "desc", 1500, 10, 5, "Herramientas")
    with pytest.raises(ValueError, match="La cantidad debe ser mayor a cero"):
        p.registrar_salida(0, "Test")
    assert p.stock_actual == 10  # stock no modificado
```

---

### TC03 — Salida con cantidad mayor al stock: debe lanzar ValueError

| Campo | Detalle |
|-------|---------|
| **Método bajo prueba** | `Producto.registrar_salida(cantidad, motivo)` |
| **Técnica aplicada** | Valor límite superior inválido (límite de CE3: `cantidad = stock_actual + 1`) |
| **Precondición** | Producto con `stock_actual = 5` |
| **Datos de entrada** | `cantidad = 6`, `motivo = "Test"` |
| **Resultado esperado** | Se lanza `ValueError` con el mensaje `"Stock insuficiente. Stock actual: 5"` |
| **Criterio de pasar** | La excepción es capturada; el stock permanece en `5` |

```python
def test_TC03_salida_supera_stock_lanza_error():
    p = Producto("Martillo", "desc", 1500, 5, 3, "Herramientas")
    with pytest.raises(ValueError, match="Stock insuficiente"):
        p.registrar_salida(6, "Test")
    assert p.stock_actual == 5
```

---

### TC04 — Salida que deja stock bajo mínimo activa el Observer

| Campo | Detalle |
|-------|---------|
| **Método bajo prueba** | `Producto.registrar_salida()` + `Alerta.actualizar()` |
| **Técnica aplicada** | Valor límite superior válido (CE1) + verificación del patrón Observer |
| **Precondición** | Producto con `stock_actual = 5`, `stock_minimo = 5`; observador `Alerta` registrado |
| **Datos de entrada** | `cantidad = 1`, `motivo = "Venta"` |
| **Resultado esperado** | `stock_actual` pasa a `4`; como `4 < 5`, el Observer notifica; `alerta.historial` tiene exactamente una entrada con `tipo = "alerta"` |
| **Criterio de pasar** | `len(alerta.historial) == 1` y `alerta.historial[0]["tipo"] == "alerta"` |

```python
def test_TC04_salida_bajo_minimo_dispara_observer():
    p = Producto("Destornillador", "desc", 800, 5, 5, "Herramientas")
    alerta = Alerta()
    p.agregar_observador(alerta)
    p.registrar_salida(1, "Venta")
    assert p.stock_actual == 4
    assert p.bajo_stock is True
    assert len(alerta.historial) == 1
    assert alerta.historial[0]["tipo"] == "alerta"
```

---

### TC05 — Entrada válida: stock se incrementa correctamente

| Campo | Detalle |
|-------|---------|
| **Método bajo prueba** | `Producto.registrar_entrada(cantidad, motivo)` |
| **Técnica aplicada** | Partición de equivalencia — clase válida |
| **Precondición** | Producto con `stock_actual = 3` |
| **Datos de entrada** | `cantidad = 10`, `motivo = "Reposición"` |
| **Resultado esperado** | `stock_actual` pasa a `13`; el método retorna un `StockMovimiento` con `tipo = "entrada"` |
| **Criterio de pasar** | `p.stock_actual == 13` y `mov.tipo == "entrada"` |

```python
def test_TC05_entrada_valida_incrementa_stock():
    p = Producto("Cable", "desc", 350, 3, 10, "Electricidad")
    mov = p.registrar_entrada(10, "Reposición")
    assert p.stock_actual == 13
    assert mov.tipo == "entrada"
```

---

### TC06 — Entrada que normaliza el stock cierra las órdenes pendientes (Observer inverso)

| Campo | Detalle |
|-------|---------|
| **Método bajo prueba** | `Producto.registrar_entrada()` + `OrdenReposicion.resolver()` |
| **Técnica aplicada** | Partición de equivalencia + verificación del patrón Observer (flujo de reposición) |
| **Precondición** | Producto con `stock_actual = 2`, `stock_minimo = 5`; observador `OrdenReposicion` con una orden pendiente preexistente |
| **Datos de entrada** | `cantidad = 10`, `motivo = "Reposición proveedor"` |
| **Resultado esperado** | `stock_actual` pasa a `12`; como `12 ≥ 5`, se llama a `resolver()` en el Observer; la orden preexistente queda con `estado = "resuelta"` |
| **Criterio de pasar** | `p.bajo_stock is False` y `orden_obs.ordenes[0]["estado"] == "resuelta"` |

```python
def test_TC06_entrada_normaliza_stock_cierra_ordenes():
    p = Producto("Llave", "desc", 2200, 2, 5, "Plomería")
    orden_obs = OrdenReposicion()
    p.agregar_observador(orden_obs)
    # Simular que ya había una orden pendiente
    orden_obs.ordenes.append({
        "tipo": "orden",
        "producto": "Llave",
        "mensaje": "Reponer 'Llave'",
        "cantidad_sugerida": 10,
        "fecha": "01/05/2026 10:00",
        "estado": "pendiente"
    })
    p.registrar_entrada(10, "Reposición proveedor")
    assert p.stock_actual == 12
    assert p.bajo_stock is False
    assert orden_obs.ordenes[0]["estado"] == "resuelta"
```

---

## B2 — Framework de pruebas y automatización CI/CD

### Framework elegido: pytest

Se eligió **pytest** como framework de pruebas unitarias por las siguientes razones:

- **Compatibilidad con el stack:** el proyecto está desarrollado en Python 3.12, y pytest es el framework de pruebas más utilizado y mantenido del ecosistema Python.
- **Sintaxis simple:** no requiere clases ni boilerplate. Cada test es una función simple que comienza con `test_`, lo que facilita la lectura y el mantenimiento.
- **Aserciones nativas:** usa el `assert` estándar de Python con introspección automática, mostrando el detalle del valor real vs el esperado cuando un test falla.
- **Integración directa con GitHub Actions:** existen acciones oficiales y comunidad amplia que documentan workflows con pytest, lo que simplifica la configuración del pipeline CI/CD.
- **Sin dependencias adicionales:** se instala con `pip install pytest` y no requiere configuración previa para empezar a escribir tests.

### Pipeline CI/CD configurado

Se configuró un pipeline en **GitHub Actions** mediante el archivo `.github/workflows/test.yml`. El workflow se ejecuta automáticamente en cada `push` y `pull request` hacia la rama principal, mostrando los resultados en la pestaña **Actions** del repositorio.

El pipeline realiza los siguientes pasos:

1. Hace checkout del código del repositorio.
2. Configura Python 3.12 en el entorno.
3. Instala las dependencias necesarias (`pytest`, dependencias de `requirements.txt`).
4. Ejecuta los 6 casos de prueba unitaria con `pytest tests/unit/ -v`.
5. Reporta el resultado final (verde si pasan todos, rojo si alguno falla).

### Evidencia de ejecución exitosa

**Captura 1 — Workflow ejecutado correctamente (Success):**

<img width="739" height="353" alt="1" src="https://github.com/user-attachments/assets/1acd4863-b902-48f6-9fb3-959a5e1d927f" />


**Captura 2 — Detalle del job con todos los pasos aprobados:**

<img width="430" height="412" alt="2" src="https://github.com/user-attachments/assets/bee207d7-9f5c-49de-87b5-ad609f13de65" />

### Video de evidencia

Se grabó un video corto mostrando los tests ejecutándose localmente y pasando en verde.

🎥 **Link al video (YouTube — no listado):** https://youtu.be/z-QnhYLdQRQ

---

## B3 — Diseño conceptual de pruebas de integración

> **Aclaración:** Esta sección es un diseño conceptual. Las pruebas de integración no se implementan en el TP2 sino que se planifican para etapas futuras del proyecto.

### Identificación de dependencias externas

El sistema FerreRAP tiene dos dependencias externas principales que dificultan las pruebas unitarias puras y requieren estrategias de dobles de prueba:

---

### Dependencia 1 — Flask y el cliente HTTP

**Descripción:** Los endpoints en `app.py` (`/api/movimientos`, `/api/productos`, etc.) dependen del framework Flask para recibir requests HTTP, parsear JSON y devolver respuestas. En una prueba unitaria no se puede (ni debe) levantar un servidor real.

**Estrategia de mock:** Flask provee `app.test_client()`, un cliente de prueba que simula requests HTTP internamente sin abrir sockets de red. Se configura la aplicación en modo `TESTING = True` y se instancia el cliente. No se necesita ninguna biblioteca de terceros.

**Pseudocódigo de la prueba de integración:**

```
FUNCIÓN test_registrar_movimiento_endpoint():
    # Arrange
    cliente = app.test_client()
    app.config["TESTING"] = True
    limpiar_productos_globales()
    agregar_producto_de_prueba(id=1, stock_actual=10, stock_minimo=5)

    payload = {
        "producto_id": 1,
        "cantidad": 3,
        "tipo": "salida",
        "motivo": "Test integración"
    }

    # Act
    respuesta = cliente.POST("/api/movimientos", json=payload)

    # Assert
    VERIFICAR respuesta.status_code == 201
    VERIFICAR respuesta.json["movimiento"]["tipo"] == "salida"
    VERIFICAR respuesta.json["producto"]["stock_actual"] == 7
    VERIFICAR respuesta.json["notificaciones"] == []  # stock no bajó del mínimo
FIN FUNCIÓN
```

---

### Dependencia 2 — Generación de archivos PDF y Excel (sistema de archivos / buffer en memoria)

**Descripción:** Los endpoints `/api/reportes/<tipo>/pdf` y `/api/reportes/<tipo>/excel` utilizan las bibliotecas `reportlab` y `openpyxl` para generar archivos binarios y devolverlos como descarga. En una prueba unitaria del endpoint, no se puede verificar fácilmente el contenido del archivo generado sin instrumentar la respuesta.

**Estrategia de mock:** Se utiliza `unittest.mock.patch` para reemplazar la función `send_file` de Flask por un stub que intercepta el buffer generado. De esta forma la prueba verifica que el buffer tiene contenido válido (tamaño > 0, magic bytes correctos) sin depender del filesystem ni de un browser real.

**Pseudocódigo de la prueba de integración:**

```
FUNCIÓN test_exportar_pdf_genera_archivo_valido():
    # Arrange
    cliente = app.test_client()
    agregar_productos_de_prueba()

    # Act
    respuesta = cliente.GET("/api/reportes/stock/pdf")

    # Assert
    VERIFICAR respuesta.status_code == 200
    VERIFICAR respuesta.content_type == "application/pdf"
    VERIFICAR len(respuesta.data) > 0
    VERIFICAR respuesta.data[0:4] == b"%PDF"  # magic bytes del formato PDF
    VERIFICAR "ferrerap_stock_" en respuesta.headers["Content-Disposition"]
FIN FUNCIÓN

FUNCIÓN test_exportar_excel_genera_archivo_valido():
    # Arrange
    cliente = app.test_client()
    agregar_productos_de_prueba()

    # Act
    respuesta = cliente.GET("/api/reportes/reposicion/excel")

    # Assert
    VERIFICAR respuesta.status_code == 200
    VERIFICAR "spreadsheetml" en respuesta.content_type
    VERIFICAR len(respuesta.data) > 0
FIN FUNCIÓN
```

---

### Herramienta recomendada para crear dobles de prueba

**Herramienta recomendada:** `unittest.mock` (módulo estándar de Python)

**Justificación:**

`unittest.mock` forma parte de la biblioteca estándar de Python desde la versión 3.3, por lo que no requiere instalación adicional ni añade dependencias al proyecto. Provee `MagicMock`, `patch` y `patch.object` que permiten reemplazar funciones, métodos o clases enteras por objetos controlables que registran cada llamada recibida.

Para las necesidades de FerreRAP es suficiente porque:

1. **Stubbing de `send_file`:** con `@patch("app.send_file")` se puede verificar que el endpoint invoca la función con el buffer correcto y el `mimetype` esperado, sin que el archivo salga del proceso.
2. **Espionaje del Observer:** con `MagicMock()` se puede registrar un observador falso y verificar que `actualizar()` fue llamado exactamente una vez con el producto correcto.
3. **Sin overhead:** al no necesitar servidores externos ni contenedores, los tests se ejecutan en milisegundos, lo que es compatible con el pipeline de GitHub Actions configurado en B2.

Si en el futuro se necesitara mockear servicios externos reales (base de datos, email SMTP, APIs de terceros), se recomienda evaluar `responses` (para HTTP) o `pytest-mock` (wrapper ergonómico sobre `unittest.mock`).

---

*FerreRAP · IS2 · UCP · 2026 · Juan Carlos Abente — QA Lead*
