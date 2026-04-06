package modelo;

/**
 * Representa un empleado de la ferretería.
 * Es quien registra los movimientos de stock.
 */
public class Empleado {

    private String nombre;
    private String legajo;

    public Empleado(String nombre, String legajo) {
        this.nombre = nombre;
        this.legajo = legajo;
    }

    // --- Getters y Setters ---

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getLegajo() { return legajo; }
    public void setLegajo(String legajo) { this.legajo = legajo; }

    @Override
    public String toString() {
        return "Empleado{nombre='" + nombre + "', legajo='" + legajo + "'}";
    }
}
