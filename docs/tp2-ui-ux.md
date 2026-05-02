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

> 🔄 *En progreso — Scrum Master + UX Lead*

*(Se completará cuando el prototipo de Figma esté disponible para evaluar)*

### Criterio 1 — Eficacia

**Métrica:** Porcentaje de tareas completadas sin errores en el primer intento.  
**Tarea evaluada:** Registrar una salida de stock desde el módulo de movimientos.  
**Simulación:** *(pendiente — se evaluará sobre el prototipo Figma)*  
**Mejora propuesta:** *(pendiente)*

### Criterio 2 — Eficiencia

**Métrica:** Cantidad de pasos necesarios para completar la tarea principal.  
**Tarea evaluada:** Registrar una venta desde que el usuario abre el sistema hasta que el stock queda actualizado.  
**Simulación:** *(pendiente — se evaluará sobre el prototipo Figma)*  
**Mejora propuesta:** *(pendiente)*

### Alineación con ISO 13407

*(Se completará junto con el análisis de los criterios anteriores)*

---

*IS II · UCP Inc. · FerreRAP · 2026*
