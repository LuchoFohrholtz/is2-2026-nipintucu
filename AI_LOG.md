**ejemplo**
## Entrada 001 — Semana 3

**Herramienta:** GitHub Copilot
**Responsable:** Dev Lead (Matías Ruiz)
**¿Para qué se usó?**
Generar el esqueleto de la clase TurnoService con el patrón Strategy.

**¿Qué generó la IA?**
Un esqueleto con los métodos calcularPrioridad() y asignarTurno().

**¿Qué modificamos y por qué?**
- Renombramos calcularPrioridad() a calcularNivel() para que coincida
  con el vocabulario del dominio definido en el diagrama de clases.
- Agregamos validación de null en asignarTurno() que la IA no incluyó.
- Eliminamos un método getAll() que no corresponde al patrón Strategy.
