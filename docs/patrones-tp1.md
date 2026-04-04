# Documentación de Patrones de Diseño — TP1

**Materia:** Ingeniería de Software II · UCP · 2026  
**Sistema:** Gestión de Stock — Ferretería  
**Empresa:** UCP Inc.

| Integrante | Rol | GitHub |
|---|---|---|
| Santiago Gonzalez | Scrum Master | @santi-ngonzalez |
| Luciano Fohrholtz | Dev Lead | @luchofohrholtz |
| Juan Carlos Abente | QA Lead | @juankiabente |
| Mariano Acosta | UX Lead | @mittax6 |

## 1. Introducción

Este documento forma parte de la entrega del Trabajo Práctico N°1 de la materia Ingeniería de Software II (IS2), correspondiente al ciclo lectivo 2026 de la Universidad de la Cuenca del Plata (UCP). El trabajo fue desarrollado en el marco de la empresa ficticia UCP Inc., adoptando el rol de equipo de desarrollo de software.

El sistema desarrollado corresponde a la **Opción B** de la consigna: un sistema de gestión de stock para una ferretería mediana. Permite registrar productos, gestionar entradas y salidas de stock, generar alertas automáticas cuando el stock cae por debajo del mínimo configurado, y producir distintos tipos de reportes.

El objetivo principal de este TP es la aplicación de **patrones de diseño del catálogo GoF** dentro de funcionalidades reales del sistema, integrándolos de forma que resuelvan problemas concretos de diseño.

### 1.1 Contexto del sistema

> **Problema:** Una ferretería mediana necesita controlar su stock. Hoy no saben qué tienen ni cuándo pedir más. Quieren una solución que les avise cuando un producto está por agotarse.

> **Usuarios principales:** Empleado de mostrador (registra entradas y salidas) · Encargado de compras (consulta reportes y órdenes de reposición)

### 1.2 Clases principales del dominio

| Clase | Descripción |
|---|---|
| `Producto` | Entidad central. Contiene `nombre`, `descripcion`, `precio`, `stock_actual` y `stock_minimo`. Es el sujeto observado en el patrón Observer. |
| `Categoria` | Agrupa productos por rubro. Relación de agregación con `Producto`. |
| `StockMovimiento` | Registra cada entrada o salida con cantidad, tipo, fecha y motivo. |
| `Alerta` | Observador concreto que se activa cuando el stock cae por debajo del mínimo. Composición con `Producto`. |
| `OrdenReposicion` | Observador concreto que genera una orden de reposición automática. |
| `Empleado` | Actor del sistema con nombre, legajo y rol. Registra los movimientos de stock. |

---

## 2. Patrón 1 — Observer

### 2.1 Nombre del patrón

**Observer** · Categoría: Comportamental · Catálogo GoF  
*También conocido como: Publish-Subscribe, Event Listener*

### 2.2 Intención

Según el catálogo GoF:

> *"Definir una dependencia de uno a muchos entre objetos, de manera que cuando un objeto cambia de estado, todos sus dependientes son notificados y actualizados automáticamente."*

En términos prácticos, el Observer permite que un objeto (el **sujeto**) mantenga una lista de dependientes (**observadores**) y los notifique automáticamente ante cualquier cambio de estado relevante, sin conocer qué hacen esos dependientes con la información. Esto logra un desacoplamiento fuerte entre el sujeto y sus observadores.

### 2.3 Problema que resuelve en el sistema

Cuando el stock de un `Producto` cae por debajo del `stock_minimo`, el sistema debe generar automáticamente una `Alerta` y una `OrdenReposicion`. Sin Observer, la clase `Producto` tendría que conocer y llamar directamente a `Alerta` y `OrdenReposicion`, generando los siguientes problemas concretos:

- `Producto` acumularía responsabilidades que no le corresponden, violando el **Principio de Responsabilidad Única (SRP)**.
- Agregar un nuevo tipo de notificación (por ejemplo, un módulo de email) requeriría modificar `Producto`, violando el **Principio Open/Closed (OCP)**.
- Los tests de `Producto` se volverían dependientes de `Alerta` y `OrdenReposicion`, dificultando las pruebas unitarias.

### 2.4 Justificación de la elección

El patrón Observer fue elegido porque resuelve directamente los tres problemas identificados:

- **Desacoplamiento:** `Producto` solo conoce la interfaz abstracta `Observador`. No sabe qué hace cada observador concreto cuando es notificado.
- **Extensibilidad (OCP):** Para agregar un nuevo observador (email, SMS, log) basta con crear una nueva clase que implemente `Observador` y registrarla en `Producto`. `Producto` no cambia.
- **Testeabilidad:** `Producto` puede testearse de forma aislada con observadores mock sin depender de `Alerta` ni `OrdenReposicion`.
- **Responsabilidad única (SRP):** Cada clase tiene una sola responsabilidad — `Producto` gestiona stock, `Alerta` gestiona notificaciones, `OrdenReposicion` gestiona órdenes.

**Alternativa descartada:** se consideró usar un método estático en una clase utilitaria (`NotificadorStock`) que `Producto` llamara directamente. Esta alternativa fue descartada porque seguía acoplando `Producto` a una implementación específica y no permitía agregar nuevos tipos de notificación sin modificar el código existente.

### 2.5 Estructura del patrón en el sistema

| Rol | Clase |
|---|---|
| Interfaz | `Observador` — define el método abstracto `actualizar(producto)` |
| Sujeto | `Producto` — mantiene la lista de observadores y llama a `_notificar()` cuando `stock_actual < stock_minimo` |
| Observador concreto 1 | `Alerta` — implementa `actualizar()`, registra la alerta en su historial |
| Observador concreto 2 | `OrdenReposicion` — implementa `actualizar()`, genera una orden de reposición |
| Trigger | `Producto.registrar_salida()` — descuenta stock y llama a `_notificar()` si corresponde |

### 2.6 Implementación en el código

**Interfaz abstracta del observador**

```python
from abc import ABC, abstractmethod

class Observador(ABC):
    @abstractmethod
    def actualizar(self, producto):
        pass
```

**Sujeto: clase Producto**

```python
class Producto:
    def __init__(self, nombre, stock_actual, stock_minimo, ...):
        self.nombre = nombre
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self._observadores = []   # lista de observadores registrados

    def agregar_observador(self, obs: Observador):
        self._observadores.append(obs)

    def _notificar(self):
        # recorre la lista y notifica a cada observador
        for obs in self._observadores:
            obs.actualizar(self)

    def registrar_salida(self, cantidad, motivo):
        self.stock_actual -= cantidad
        if self.stock_actual < self.stock_minimo:  # trigger del patrón
            self._notificar()
```

**Observadores concretos**

```python
class Alerta(Observador):
    def __init__(self):
        self.historial = []

    def actualizar(self, producto):
        self.historial.append({
            'mensaje': f"Stock bajo en '{producto.nombre}'",
            'stock_actual': producto.stock_actual,
            'stock_minimo': producto.stock_minimo,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
        })


class OrdenReposicion(Observador):
    def __init__(self):
        self.ordenes = []

    def actualizar(self, producto):
        self.ordenes.append({
            'mensaje': f"Reponer '{producto.nombre}'",
            'cantidad_sugerida': producto.stock_minimo * 2,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
```

**Uso en el sistema**

```python
# Registro de observadores al crear el producto
p = Producto('Martillo 500g', stock_actual=8, stock_minimo=5, ...)
p.agregar_observador(Alerta())
p.agregar_observador(OrdenReposicion())

# Cuando el stock baja de 5, se notifica automáticamente a ambos observadores
p.registrar_salida(5, motivo='venta mostrador')
# → Alerta y OrdenReposicion son notificados sin que Producto los conozca
```

### 2.7 Mejoras que aporta al sistema

- **Desacoplamiento:** `Producto` desconoce completamente qué hacen `Alerta` y `OrdenReposicion`.
- **Mantenibilidad:** Nuevos observadores se agregan sin tocar código existente.
- **Claridad:** La lógica de notificación está centralizada en el método `_notificar()`.
- **Testeabilidad:** Se puede probar `Producto` con observadores mock sin dependencias externas.

---

## 3. Patrón 2 — Strategy

### 3.1 Nombre del patrón

**Strategy** · Categoría: Comportamental · Catálogo GoF  
*También conocido como: Policy, Algorithm Family*

### 3.2 Intención

Según el catálogo GoF:

> *"Definir una familia de algoritmos, encapsular cada uno de ellos y hacerlos intercambiables. Strategy permite que el algoritmo varíe independientemente de los clientes que lo usan."*

En términos prácticos, Strategy permite seleccionar el comportamiento de un objeto en tiempo de ejecución, encapsulando cada variante en una clase separada y haciéndolas intercambiables a través de una interfaz común.

### 3.3 Problema que resuelve en el sistema

El sistema necesita generar distintos tipos de reportes: productos a reponer, stock completo, y eventualmente más en el TP2. Sin Strategy, toda la lógica de reportes estaría en una sola clase con múltiples `if/else`, lo que generaría los siguientes problemas:

- Una clase `GeneradorReporte` con un bloque `if/else` que crece con cada nuevo tipo de reporte.
- Cada modificación de un tipo de reporte implica abrir y modificar `GeneradorReporte` completa, violando el **Principio Open/Closed (OCP)**.
- Los tests deben cubrir todos los casos dentro de la misma clase, aumentando la complejidad innecesariamente.

### 3.4 Justificación de la elección

El patrón Strategy fue elegido porque:

- **Interfaz uniforme:** Cada estrategia de reporte tiene exactamente la misma firma — recibe una lista de productos y devuelve un resultado estructurado. Esto se mapea perfectamente a la interfaz común `EstrategiaReporte`.
- **Open/Closed:** Agregar un nuevo tipo de reporte en TP2 requiere crear una nueva clase sin modificar `GeneradorReporte` ni las estrategias existentes.
- **Intercambiabilidad en runtime:** El tipo de reporte se selecciona en tiempo de ejecución según la acción del usuario en la interfaz, sin reiniciar ni reconfigurar el sistema.
- **Separación de responsabilidades:** Cada estrategia puede testearse de forma completamente independiente.

**Alternativa descartada:** se consideró implementar los reportes como métodos distintos dentro de una única clase (`generar_reposicion()`, `generar_stock_actual()`, etc.). Esta alternativa fue descartada porque viola el SRP (la clase tiene múltiples razones para cambiar) y el OCP (agregar un reporte requiere modificar la clase).

### 3.5 Estructura del patrón en el sistema

| Rol | Clase |
|---|---|
| Interfaz | `EstrategiaReporte` — define el método abstracto `generar(productos)` |
| Estrategia concreta 1 | `ReporteReposicion` — filtra y devuelve solo los productos con `stock_actual < stock_minimo` |
| Estrategia concreta 2 | `ReporteStockActual` — devuelve todos los productos con su estado de stock completo |
| Contexto | `GeneradorReporte` — recibe una estrategia y delega en ella la generación del reporte |
| Extensión TP2 | `ReporteMovimientosDiarios` — nueva estrategia a agregar sin modificar código existente |

### 3.6 Implementación en el código

**Interfaz abstracta de la estrategia**

```python
from abc import ABC, abstractmethod

class EstrategiaReporte(ABC):
    @abstractmethod
    def generar(self, productos):
        pass
```

**Estrategias concretas**

```python
class ReporteReposicion(EstrategiaReporte):
    def generar(self, productos):
        # filtra solo los productos con stock bajo mínimo
        return [
            {
                'nombre': p.nombre,
                'stock_actual': p.stock_actual,
                'stock_minimo': p.stock_minimo,
                'categoria': p.categoria
            }
            for p in productos if p.stock_actual < p.stock_minimo
        ]


class ReporteStockActual(EstrategiaReporte):
    def generar(self, productos):
        # devuelve todos los productos con su estado completo
        return [
            {
                'nombre': p.nombre,
                'stock_actual': p.stock_actual,
                'stock_minimo': p.stock_minimo,
                'precio': p.precio,
                'categoria': p.categoria
            }
            for p in productos
        ]
```

**Contexto: GeneradorReporte**

```python
class GeneradorReporte:
    def __init__(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia   # intercambio en tiempo de ejecución

    def ejecutar(self, productos):
        return self._estrategia.generar(productos)   # delega en la estrategia
```

**Uso en el sistema (intercambio en runtime)**

```python
# El usuario selecciona 'reporte de reposición' en la interfaz
gen = GeneradorReporte(ReporteReposicion())
resultado = gen.ejecutar(productos)   # solo productos con stock bajo

# El usuario cambia a 'stock completo' sin reiniciar el sistema
gen.cambiar_estrategia(ReporteStockActual())
resultado = gen.ejecutar(productos)   # todos los productos

# En TP2: agregar nuevo tipo sin tocar código existente
# gen.cambiar_estrategia(ReporteMovimientosDiarios())
```

### 3.7 Mejoras que aporta al sistema

- **Encapsulamiento:** Cada estrategia encapsula un algoritmo completo e independiente.
- **Mantenibilidad (OCP):** Nuevas estrategias se agregan sin modificar `GeneradorReporte` ni las existentes.
- **Flexibilidad en runtime:** El tipo de reporte se selecciona según la acción del usuario.
- **Testeabilidad:** Cada estrategia se prueba de forma completamente independiente.

---

## 4. Comparación entre patrones

| Dimensión | Observer | Strategy |
|---|---|---|
| Categoría GoF | Comportamental | Comportamental |
| Problema que resuelve | Notificación automática ante cambio de estado | Selección de algoritmo en tiempo de ejecución |
| Relación clave | Sujeto → Observadores (1 a muchos) | Contexto → Estrategia (1 a 1 intercambiable) |
| Principios aplicados | OCP, SRP, bajo acoplamiento | OCP, SRP, encapsulamiento de algoritmo |
| Clases involucradas | `Producto` → `Alerta`, `OrdenReposicion` | `GeneradorReporte` → `ReporteX` |
| Trigger | Cambio de `stock_actual` | Selección del usuario en la interfaz |

---

## 5. Conclusión

Los dos patrones seleccionados — Observer y Strategy — fueron elegidos porque resuelven problemas reales e identificados del sistema, no porque sean los más conocidos del catálogo GoF.

**Observer** resuelve el desacoplamiento entre el estado de un producto y las acciones que se disparan cuando ese estado cambia. **Strategy** resuelve la variabilidad de algoritmos de reporte sin comprometer la estabilidad de la clase que los ejecuta.

Ambos patrones están integrados en funcionalidades reales del sistema, pueden identificarse claramente en el código, y sientan las bases para las extensiones que se desarrollarán en el TP2 — pruebas automatizadas, nuevas estrategias de reporte, nuevos observadores.

> ⚠️ Todos los integrantes del equipo deben poder responder en el coloquio: **¿Por qué usamos este patrón y no otro?**



*IS II · UCP Inc. · Documentación de Patrones de Diseño · TP1 · 2026*
