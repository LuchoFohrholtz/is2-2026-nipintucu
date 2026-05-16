
## Verificación y Validación

### 1. Verificación vs Validación

La verificación es comprobar que estamos construyendo el sistema *correctamente*, y la validación es comprobar que estamos construyendo *el sistema correcto*.

**Verificación en nuestro proyecto:**revisar que `registrar_salida()` en `models.py` descuenta el stock y llama a `_notificar()` cuando `stock_actual < stock_minimo`, siguiendo el diseño del patrón Observer definido en el TP1.  
**Validación en nuestro proyecto:** que un empleado real de ferretería pruebe el sistema y confirme que las alertas de stock le resultan útiles en su trabajo diario.

---

### 2. Planificación de V&V para el próximo sprint

Para un sprint de una semana incluiríamos:

- Hacer una walkthrough del flujo principal: registrar salida de stock → Observer dispara alerta → OrdenReposicion genera orden pendiente, verificando cada paso contra lo especificado en el TP1.
  
- Realizar pruebas exploratorias sin guión fijo: intentar registrar una salida con stock 0, generar un reporte sin productos cargados, o acceder a endpoints sin autenticación, buscando comportamientos inesperados no cubiertos por los tests unitarios del B1.

---

### 3. Inspección de código vs prueba automática

La inspección es una revisión humana del código fuente sin ejecutarlo. La prueba automática ejecuta el código con datos concretos y verifica el resultado.

Conviene la **inspección** cuando querés detectar problemas de diseño, como verificar que el patrón Observer en `models.py` no está acoplando a `Producto` con los detalles internos de `Alerta` u `OrdenReposicion`. 
Conviene la **prueba automática** para comportamientos repetibles y rápidos, como verificar que `registrar_salida(5)` con stock 3 lanza siempre un `ValueError("Stock insuficiente")`.

---

### 4. Análisis estático automatizado

**Pylint.** Sin ejecutar el código, podría detectar en nuestro `app.py` cosas como variables no usadas, funciones demasiado largas, bloques `except` vacíos (que tenemos al parsear datos del request), o imports innecesarios. También avisaría si alguna clase no sigue las convenciones de nombrado de Python, algo relevante dado que models.py tiene una jerarquía de herencia (Observador → Alerta, OrdenReposicion) que debe mantenerse consistente.

---

### 5. Métodos formales de verificación

Son imprescindibles en sistemas donde un fallo tiene consecuencias críticas: software médico, aeronáutico, control de reactores nucleares, sistemas de frenado en autos. Se usan porque permiten demostrar matemáticamente que el sistema cumple su especificación.

No se usan siempre porque son muy costosos en tiempo y requieren conocimiento especializado en lógica matemática. Para un sistema como el nuestro, ese nivel de rigor no se justifica: un bug en el stock de una ferretería no pone vidas en riesgo y el costo de aplicarlos superaría con creces el beneficio. 

---

### 6. Reuniones de validación en Scrum — rol del Product Owner

En la *Sprint Review*, el Product Owner valida que lo entregado cumple con los criterios de aceptación que él mismo definió al inicio del sprint. No es solo "ver si funciona", sino decidir si eso es lo que realmente se necesitaba.

Se relaciona con las pruebas automáticas porque éstas le dan confianza de que el sistema no rompió lo que ya funcionaba. En nuestro sistema, si el pipeline de GitHub Actions muestra todos los tests en verde, el PO puede enfocarse en validar la funcionalidad nueva sin preocuparse por regresiones.
