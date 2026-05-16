# FerreRAP — Sistema de Gestión de Inventario
> IS2 · Universidad de la Cuenca del Plata · 2026 · Equipo nipintucu

Sistema web de gestión de inventario para ferretería. Permite registrar productos, controlar stock en tiempo real, gestionar ventas con carrito, generar reportes y recibir alertas automáticas por bajo stock.

---

## Equipo de Trabajo

| Nombre             | Rol          | GitHub                                               |
|--------------------|--------------|------------------------------------------------------|
| Santiago Gonzalez  | Scrum Master | [@santi-ngonzalez](https://github.com/santi-ngonzalez) |
| Luciano Fohrholtz  | Dev Lead     | [@luchofohrholz](https://github.com/luchofohrholtz)  |
| Juan Carlos Abente | QA Lead      | [@juankiabente](https://github.com/juankiabente)     |
| Mariano Acosta     | UX Lead      | [@mittax6](https://github.com/mittax6)               |

---

## Enlaces Rápidos

* [Tablero Kanban (GitHub Projects)](https://github.com/users/LuchoFohrholtz/projects/1)
* [Matriz de Riesgos](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/matriz-de-riesgos.md)
* [AI Log](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/AI_LOG.md)
* [Informe TP1](https://docs.google.com/document/d/1C3rg_HAe2fNjk1P0o_SO_F86wyOYUDYX/edit?usp=sharing&ouid=105019262908114217359&rtpof=true&sd=true)
* [Documentación de Patrones de Diseño](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/patrones-tp1.md)
* [Prototipo en Figma (3 pantallas)](https://www.figma.com/make/CicSoOUwMEUprpSG9INYkZ/FerreRAP-Stock-Management-Prototype?t=ufxEOo6hIVvvNYoi-1)

---

## Tecnologías utilizadas

### Backend

| Tecnología       | Versión  | Uso                                              |
|------------------|----------|--------------------------------------------------|
| Python           | 3.12+    | Lenguaje principal del backend                   |
| Flask            | 3.0.0    | Framework API REST                               |
| Flask-CORS       | 4.0.0    | Habilitación de CORS para el frontend            |
| postgrest-py     | —        | Cliente HTTP liviano para la API REST de Supabase |
| httpx            | —        | Cliente HTTP con soporte de timeout y conexión   |
| python-dotenv    | —        | Carga de variables de entorno desde `.env`       |
| ReportLab        | 4.2.0    | Generación de reportes en PDF                    |
| openpyxl         | 3.1.2    | Exportación de reportes a Excel (.xlsx)          |

### Base de Datos

| Tecnología  | Uso                                                                 |
|-------------|---------------------------------------------------------------------|
| **Supabase** | Base de datos PostgreSQL en la nube con API REST automática (PostgREST) |
| PostgreSQL  | Motor relacional subyacente de Supabase                             |
| Row Level Security (RLS) | Políticas de acceso a nivel de fila en Supabase        |

> La conexión a Supabase se gestiona en `src/database.py`. Las credenciales se configuran en el archivo `.env` (ver sección de instalación).

**Tablas en Supabase:**

| Tabla               | Descripción                                           |
|---------------------|-------------------------------------------------------|
| `productos`         | Catálogo con precio_costo, precio_venta, stock, categoría |
| `movimientos`       | Historial de entradas y salidas de stock              |
| `alertas`           | Notificaciones de bajo stock (patrón Observer)        |
| `ordenes_reposicion`| Órdenes generadas automáticamente (patrón Observer)   |
| `ventas`            | Cabecera de ventas confirmadas desde el carrito       |
| `venta_items`       | Líneas de detalle de cada venta                       |

### Frontend

| Tecnología    | Uso                                                   |
|---------------|-------------------------------------------------------|
| HTML5 / CSS3  | Interfaz web single-page con modo oscuro              |
| JavaScript (Vanilla) | Lógica del cliente, carrito, alertas en tiempo real |
| Google Fonts (DM Sans, DM Mono) | Tipografía del sistema               |

### Herramientas y gestión

| Herramienta    | Uso                         |
|----------------|-----------------------------|
| GitHub Projects | Tablero Kanban             |
| Figma          | Prototipo de interfaz       |
| Git            | Control de versiones        |

---

## Instalación y puesta en marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/LuchoFohrholtz/is2-2026-nipintucu.git
cd is2-2026-nipintucu
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r src/requirements.txt
```

### 4. Configurar variables de entorno
Crear el archivo `.env` en la raíz del proyecto:
```env
SUPABASE_URL=https://<tu-proyecto>.supabase.co
SUPABASE_KEY=<tu-anon-key>
MARGEN_GANANCIA=50
```

### 5. Inicializar la base de datos
Ejecutar el script `setup_db.sql` en el **SQL Editor** de Supabase Dashboard. Crea todas las tablas y habilita las políticas RLS.

### 6. Ejecutar el servidor
```bash
python src/app.py
```
Abrir en el navegador: `http://localhost:5000`

> **Credenciales por defecto:** `admin / admin123` · `empleado / empleado123`

---

## Funcionalidades principales

- 📦 **Gestión de productos** — Alta, baja y modificación con precio de costo y precio de venta separados
- 📉 **Control de stock** — Registro de entradas y salidas con motivo y trazabilidad completa
- 🔔 **Alertas automáticas** — Notificaciones por bajo stock via patrón Observer (campana en el header con dropdown)
- 🛒 **Carrito de ventas** — Venta de productos con confirmación y registro en base de datos
- 📊 **Reportes** — Exportación de stock e inventario en PDF y Excel (con precio costo + venta)
- 💰 **Margen de ganancia configurable** — Configurable vía variable de entorno `MARGEN_GANANCIA`
- 🌙 **Modo oscuro / claro** — Tema persistente con CSS custom properties
- 👤 **Roles de usuario** — Vistas diferenciadas para administrador y empleado

---

## Patrones de diseño implementados

### Observer — Comportamental
Aplicado en `src/models.py` entre el sistema de movimientos de stock y los observadores `AlertaObserver` y `OrdenReposicionObserver`.
Cuando el stock de un producto cae por debajo del mínimo configurado, el sistema persiste automáticamente alertas y órdenes de reposición en Supabase sin acoplamiento directo.

### Strategy — Comportamental
Aplicado en el módulo de reportes a través de `GeneradorReporte` y las estrategias `ReporteReposicion` y `ReporteStockActual`.
Permite intercambiar el algoritmo de generación de reportes en tiempo de ejecución sin modificar el código del contexto.

---

## Diagrama de clases

<img width="6272" height="3235" alt="Diagrama de clases del sistema" src="https://github.com/user-attachments/assets/4464cde6-9036-492d-a27b-fdf38a3fd215" />
<img width="5389" height="3235" alt="Diagrama de movimientos" src="https://github.com/user-attachments/assets/ab07e319-33f1-48cd-bc08-a98e513f6fe5" />

---

## Caso de uso principal

**Registrar una salida de stock y generar alerta si el stock queda bajo mínimo**

1. El empleado registra una salida de stock con producto, cantidad y motivo.
2. El sistema descuenta el stock actual en Supabase.
3. Si `stock_actual < stock_minimo` → el patrón Observer persiste una alerta y una orden de reposición.
4. La campana del header muestra el badge con la cantidad de alertas pendientes.
5. El administrador puede ver y gestionar las alertas desde el panel correspondiente.

---

## Uso de IA

El equipo utilizó herramientas de IA (ChatGPT, Claude, Gemini, Antigravity) durante el desarrollo.
Todo el uso está documentado con detalle en: [AI Log](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/AI_LOG.md).


## Verificación y Validación

### 1. Verificación vs Validación

La verificación es comprobar que estamos construyendo el sistema *correctamente*, y la validación es comprobar que estamos construyendo *el sistema correcto*.

**Verificación en nuestro proyecto:** revisar que `registrar_salida()` en `models.py` descuenta el stock y llama a `_notificar()` cuando corresponde, siguiendo el diseño definido.  
**Validación en nuestro proyecto:** que un empleado real de ferretería pruebe el sistema y confirme que las alertas de stock le resultan útiles en su trabajo diario.

---

### 2. Planificación de V&V para el próximo sprint

Para un sprint de una semana incluiríamos:

- Escribir pruebas unitarias con **pytest** sobre `registrar_salida()` y `registrar_entrada()` usando clases de equivalencia (cantidad válida, cantidad negativa, cantidad mayor al stock disponible).
- Hacer una **revisión de código en pull request** antes de mergear, donde otro integrante del equipo verifique que los patrones Observer y Strategy siguen aplicados correctamente.

---

### 3. Inspección de código vs prueba automática

La inspección es una revisión humana del código fuente sin ejecutarlo. La prueba automática ejecuta el código con datos concretos y verifica el resultado.

Conviene la **inspección** cuando querés detectar problemas de diseño o acoplamiento, como revisar si el patrón Observer está bien estructurado en `models.py`.  
Conviene la **prueba automática** para verificar comportamientos repetibles y rápidos, como que el stock se descuenta correctamente en cada movimiento registrado.

---

### 4. Análisis estático automatizado

**Pylint.** Sin ejecutar el código, podría detectar en nuestro `app.py` cosas como variables no usadas, funciones demasiado largas, bloques `except` vacíos (que tenemos al parsear datos del request), o imports innecesarios. También avisaría si alguna clase no sigue las convenciones de nombrado de Python.

---

### 5. Métodos formales de verificación

Son imprescindibles en sistemas donde un fallo tiene consecuencias críticas: software médico, aeronáutico, control de reactores nucleares o sistemas de frenado. Permiten demostrar matemáticamente que el sistema cumple su especificación.

No se usan siempre porque son muy costosos en tiempo y requieren conocimiento especializado en lógica matemática. Para un sistema como FerreRAP ese nivel de rigor no se justifica: un bug en el stock de una ferretería no pone vidas en riesgo.

---

### 6. Reuniones de validación en Scrum — rol del Product Owner

En la **Sprint Review**, el Product Owner valida que lo entregado cumple con los criterios de aceptación que él mismo definió al inicio del sprint. No es solo ver si funciona, sino decidir si eso es lo que realmente se necesitaba.

Se relaciona con las pruebas automáticas porque éstas le dan confianza de que el sistema no rompió lo que ya funcionaba. En nuestro sistema, si el pipeline de GitHub Actions muestra todos los tests en verde, el PO puede enfocarse en validar la funcionalidad nueva sin preocuparse por regresiones.
