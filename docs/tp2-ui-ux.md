# TP2 — Diseño de Interfaz Centrado en el Usuario
**Materia:** Ingeniería de Software II · UCP · 2026  
**Sistema:** FerreRAP — Gestión de Stock para Ferretería  
**Equipo:** Santiago Gonzalez · Luciano Fohrholtz · Juan Carlos Abente · Mariano Acosta  
**Parte:** A — Eje 3: HCI

---

## Índice

1. [A1 — Prototipo en Figma](#a1--prototipo-en-figma)
2. [A2 — Análisis de usuario, tarea y contexto](#a2--análisis-de-usuario-tarea-y-contexto)
3. [A3 — Auditoría de usabilidad ISO 9241-11](#a3--auditoría-de-usabilidad-iso-9241-11)

---

## A1 — Prototipo en Figma

(https://www.figma.com/make/CicSoOUwMEUprpSG9INYkZ/FerreRAP-Stock-Management-Prototype?t=ufxEOo6hIVvvNYoi-1)

**Pantallas incluidas:**
1. Listado de productos con buscador y estados de stock
2. Alta de producto nuevo (formulario completo)
3. Confirmación de stock actualizado con feedback visual

**Capturas:** 
<img width="1320" height="878" alt="image" src="https://github.com/user-attachments/assets/922959d8-6f70-4b5a-ab0d-a1cdf05d0561" />
<img width="1325" height="871" alt="image" src="https://github.com/user-attachments/assets/557d614b-df74-41a3-af4e-7124a088d188" />
<img width="1310" height="869" alt="image" src="https://github.com/user-attachments/assets/92e6016b-0b7c-48c0-822e-772aff5f0a83" />

---

## A2 — Análisis de usuario, tarea y contexto

### Usuarios objetivo

FerreRAP está pensado para dos tipos de usuarios bien distintos dentro de una ferretería mediana. Por un lado está el **empleado de mostrador**, que es quien más interactúa con el sistema en el día a día. Es una persona que no necesariamente tiene experiencia con software de gestión, y que trabaja bajo presión cuando hay clientes esperando. Por eso necesita que el sistema sea directo: entrar, registrar la venta, seguir atendiendo. No tiene tiempo para leer instrucciones ni recordar rutas complicadas dentro de una interfaz.

El segundo usuario es el **encargado de compras o administrador**, que usa el sistema de forma menos frecuente pero con mayor profundidad. Su foco está en revisar el estado del stock, analizar qué productos están por agotarse, generar reportes y decidir qué reponer. A diferencia del empleado, este usuario sí puede tomarse más tiempo para explorar el sistema, pero igual espera que la información esté organizada y sea fácil de interpretar de un vistazo.

### Tareas principales

Las tareas que más se repiten en el sistema son: registrar una venta (salida de stock), consultar el inventario actual, revisar las alertas de productos con stock bajo, y generar un reporte de reposición. De estas, la más crítica en términos de frecuencia y riesgo de error es el registro de ventas, porque ocurre varias veces por hora y cualquier equivocación afecta directamente el stock real de la ferretería.

El encargado, en cambio, realiza tareas más espaciadas: revisar las órdenes de reposición generadas automáticamente por el sistema, consultar el historial de movimientos, y eventualmente agregar productos nuevos o modificar el stock mínimo de alguno.

### Contexto de uso

El sistema se usa desde una computadora de escritorio en el mostrador de la ferretería, en un entorno con bastante actividad alrededor: clientes, ruido, consultas en paralelo. Esto significa que la interfaz no puede requerir demasiada concentración para operar, y los elementos importantes como el estado del stock o los botones de acción tienen que ser visibles de forma inmediata sin necesidad de buscarlos.

Una restricción real que encontramos al diseñar es que el empleado de mostrador probablemente no tenga los dos ojos fijos en la pantalla mientras atiende. Por eso el sistema prioriza el feedback visual claro — colores, mensajes de confirmación — por encima de cualquier otro mecanismo de respuesta. Si el sistema hace algo, el usuario tiene que poder verlo aunque esté mirando para otro lado por un segundo.

---

## A3 — Auditoría de usabilidad ISO 9241-11

La norma ISO 9241-11 define usabilidad como el grado en que un sistema
puede ser usado por usuarios específicos para alcanzar objetivos
específicos con eficacia, eficiencia y satisfacción, en un contexto
de uso determinado. Para esta auditoría evaluamos dos de esos tres
criterios sobre el prototipo actual de FerreRAP.

---

### Criterio 1 — Eficacia

**Definición:** Grado en que el usuario logra completar la tarea
correctamente, sin errores ni pasos incorrectos.

**Métrica definida:** Porcentaje de tareas completadas en el primer
intento sin cometer errores de navegación ni de carga de datos.

**Tarea evaluada:** Registrar un producto nuevo en el sistema
(flujo: Pantalla 1 → Pantalla 2 → Pantalla 3).

**Simulación sobre el prototipo:**

Al recorrer el flujo en Figma, el camino es claro: desde el
inventario hay un botón visible "+ Nuevo producto" en la esquina
superior derecha (Pantalla 1). Al hacer clic lleva directamente
al formulario (Pantalla 2), donde todos los campos obligatorios
están marcados con asterisco (*). Al guardar, el sistema vuelve
al inventario y muestra una notificación verde de confirmación
con el mensaje "Producto creado correctamente" y el nombre del
producto agregado (Pantalla 3). El contador de productos también
se actualiza de 8 a 10 en tiempo real.

**Resultado de la evaluación:** El flujo cumple con eficacia.
El usuario puede completar la tarea sin ambigüedades porque
cada pantalla tiene un único camino posible hacia adelante.

**Problema identificado:** El botón "Guardar producto" aparece
deshabilitado visualmente (color gris) cuando el formulario
está vacío, pero el prototipo no indica al usuario qué campos
faltan completar para habilitarlo. Un usuario nuevo podría no
entender por qué el botón no responde.

**Mejora concreta:** Agregar un mensaje debajo del botón que
indique los campos obligatorios pendientes cuando el usuario
intenta guardar sin completar el formulario. Por ejemplo:
"Completá nombre, categoría y stock para continuar."

---

### Criterio 2 — Eficiencia

**Definición:** Recursos utilizados en relación con la precisión
con que se logra el objetivo. En interfaces, se mide típicamente
por la cantidad de pasos o tiempo necesario para completar la tarea.

**Métrica definida:** Cantidad de clics y campos necesarios para
completar el caso de uso principal desde la pantalla inicial.

**Tarea evaluada:** Agregar un producto nuevo al inventario.

**Simulación sobre el prototipo:**

Contando los pasos sobre el prototipo de Figma:

| Paso | Acción | Tipo |
|------|--------|------|
| 1 | Clic en "+ Nuevo producto" | 1 clic |
| 2 | Completar campo Nombre | 1 campo |
| 3 | Completar campo Descripción | 1 campo (opcional) |
| 4 | Seleccionar Categoría | 1 campo |
| 5 | Completar Precio | 1 campo |
| 6 | Completar Stock actual | 1 campo |
| 7 | Completar Stock mínimo | 1 campo |
| 8 | Clic en "Guardar producto" | 1 clic |

**Total:** 2 clics + 5 campos obligatorios + 1 opcional.
El flujo es eficiente para la tarea que realiza.

**Resultado de la evaluación:** El flujo es eficiente.
No hay pantallas intermedias innecesarias ni confirmaciones
redundantes. El usuario completa la tarea en una sola pantalla
de formulario.

**Problema identificado:** El campo "Descripción" está ubicado
antes de Categoría y Precio, pero es el único campo opcional.
Visualmente rompe el orden esperado (datos principales primero,
datos secundarios después), lo que puede llevar al usuario a
completar un campo que no es obligatorio antes de los que sí lo son.

**Mejora concreta:** Reordenar el formulario colocando Descripción
al final, después de todos los campos obligatorios. Así el usuario
sigue un flujo lógico de arriba hacia abajo completando primero
lo necesario.

---

### Alineación con ISO 13407

ISO 13407 (actualmente reemplazada por ISO 9241-210) define un
proceso de diseño centrado en el humano compuesto por 4 pasos
iterativos que se repiten hasta que el sistema sea aceptable
para sus usuarios.

El desarrollo de FerreRAP siguió este proceso de forma implícita
a lo largo del cuatrimestre:

**Paso 1 — Entender y especificar el contexto de uso:**
Realizado en el Sprint 0, cuando se definieron los actores
del sistema (empleado de mostrador y encargado de compras),
sus tareas principales y el entorno de trabajo (mostrador
de ferretería, bajo presión, múltiples distracciones).

**Paso 2 — Especificar los requisitos del usuario:**
Realizado durante el TP1, al definir las funcionalidades
mínimas del sistema: registrar entradas y salidas, generar
alertas automáticas, y producir reportes de reposición.

**Paso 3 — Producir soluciones de diseño:**
El prototipo de Figma representa esta etapa. Las tres
pantallas diseñadas por el UX Lead responden directamente
a los requisitos identificados en los pasos anteriores.

**Paso 4 — Evaluar el diseño contra los requisitos:**
Esta auditoría ISO 9241-11 es exactamente este paso.
Al evaluar eficacia y eficiencia sobre el prototipo,
identificamos dos problemas concretos y propusimos mejoras
que deberían incorporarse en la próxima iteración del diseño.

El ciclo no termina acá — las mejoras propuestas en esta
auditoría alimentan una nueva iteración del prototipo, que
luego volvería a evaluarse. Eso es exactamente lo que
ISO 13407 plantea como proceso.

*IS II · UCP Inc. · FerreRAP · 2026*
