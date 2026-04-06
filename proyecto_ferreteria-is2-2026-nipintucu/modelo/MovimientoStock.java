package modelo;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Representa un movimiento de stock (entrada o salida).
 *
 * Cada movimiento queda registrado con:
 * - Tipo: ENTRADA o SALIDA
 * - Producto afectado
 * - Empleado que lo registró
 * - Cliente que lo solicitó (opcional, solo en ventas)
 * - Cantidad y motivo
 */
public class MovimientoStock {

    public enum Tipo {
        ENTRADA,
        SALIDA
    }

    private Tipo tipo;
    private Producto producto;
    private Empleado empleado;
    private Cliente cliente;       // puede ser null en reposiciones
    private Proveedor proveedor;   // puede ser null en ventas
    private int cantidad;
    private String motivo;
    private LocalDateTime fecha;

    // Constructor para SALIDA (venta a cliente)
    public MovimientoStock(Producto producto, Empleado empleado, Cliente cliente,
                           int cantidad, String motivo) {
        this.tipo = Tipo.SALIDA;
        this.producto = producto;
        this.empleado = empleado;
        this.cliente = cliente;
        this.cantidad = cantidad;
        this.motivo = motivo;
        this.fecha = LocalDateTime.now();
    }

    // Constructor para ENTRADA (reposición de proveedor)
    public MovimientoStock(Producto producto, Empleado empleado, Proveedor proveedor,
                           int cantidad, String motivo) {
        this.tipo = Tipo.ENTRADA;
        this.producto = producto;
        this.empleado = empleado;
        this.proveedor = proveedor;
        this.cantidad = cantidad;
        this.motivo = motivo;
        this.fecha = LocalDateTime.now();
    }

    // --- Getters ---

    public Tipo getTipo() { return tipo; }
    public Producto getProducto() { return producto; }
    public Empleado getEmpleado() { return empleado; }
    public Cliente getCliente() { return cliente; }
    public Proveedor getProveedor() { return proveedor; }
    public int getCantidad() { return cantidad; }
    public String getMotivo() { return motivo; }
    public LocalDateTime getFecha() { return fecha; }

    @Override
    public String toString() {
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm");
        String origen = (tipo == Tipo.SALIDA)
                ? (cliente != null ? "Cliente: " + cliente.getNombre() : "-")
                : (proveedor != null ? "Proveedor: " + proveedor.getNombre() : "-");

        return "[" + tipo + "] "
                + producto.getNombre()
                + " x" + cantidad
                + " | " + motivo
                + " | " + origen
                + " | Empleado: " + empleado.getNombre()
                + " | " + fecha.format(fmt);
    }
}
