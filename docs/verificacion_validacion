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
