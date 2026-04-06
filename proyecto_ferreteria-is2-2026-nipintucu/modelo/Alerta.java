package modelo;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Representa una alerta generada cuando el stock de un producto
 * cae por debajo del stock mínimo configurado.
 *
 * Es el objeto que el patrón Observer propaga a todos los observadores.
 */
public class Alerta {

    public enum Estado {
        PENDIENTE,
        RESUELTA
    }

    private Producto producto;
    private LocalDateTime fecha;
    private Estado estado;
    private String mensaje;

    public Alerta(Producto producto) {
        this.producto = producto;
        this.fecha = LocalDateTime.now();
        this.estado = Estado.PENDIENTE;
        this.mensaje = generarMensaje(producto);
    }

    private String generarMensaje(Producto p) {
        return "STOCK CRÍTICO: " + p.getNombre()
                + " (" + p.getStockActual() + "/" + p.getStockMinimo() + ")";
    }

    // --- Acciones ---

    /**
     * Marca la alerta como resuelta (por ejemplo, cuando se repone stock).
     */
    public void resolver() {
        this.estado = Estado.RESUELTA;
    }

    public boolean esPendiente() {
        return this.estado == Estado.PENDIENTE;
    }

    // --- Getters ---

    public Producto getProducto() {
        return producto;
    }

    public LocalDateTime getFecha() {
        return fecha;
    }

    public Estado getEstado() {
        return estado;
    }

    public String getMensaje() {
        return mensaje;
    }

    @Override
    public String toString() {
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss");
        return "[ALERTA] " + mensaje
                + " | Estado: " + estado
                + " | Fecha: " + fecha.format(fmt);
    }
}
