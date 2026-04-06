package servicio;

import modelo.*;
import observer.AlertaObserver;

import java.util.ArrayList;
import java.util.List;

/**
 * Servicio principal del sistema de inventario.
 *
 * Encapsula los casos de uso del negocio:
 * - Registrar salida de stock (venta)
 * - Registrar entrada de stock (reposición)
 * - Consultar productos con stock bajo
 * - Consultar historial de movimientos
 *
 * Esta clase es la que la interfaz gráfica (u otro componente) debe usar.
 * Nunca interactúa directamente con las clases del modelo desde la UI.
 */
public class InventarioServicio {

    private List<Producto> productos = new ArrayList<>();
    private List<MovimientoStock> movimientos = new ArrayList<>();
    private List<AlertaObserver> observadoresGlobales = new ArrayList<>();

    // =========================================================
    // GESTIÓN DE OBSERVADORES GLOBALES
    // =========================================================

    /**
     * Agrega un observador que recibirá alertas de TODOS los productos.
     * Útil para que la UI registre un solo observer en lugar de uno por producto.
     */
    public void agregarObservadorGlobal(AlertaObserver observador) {
        observadoresGlobales.add(observador);
        // Registrar en todos los productos existentes
        for (Producto p : productos) {
            p.agregarObservador(observador);
        }
    }

    // =========================================================
    // GESTIÓN DE PRODUCTOS
    // =========================================================

    public void agregarProducto(Producto producto) {
        // Registrar observadores globales ya existentes en el nuevo producto
        for (AlertaObserver obs : observadoresGlobales) {
            producto.agregarObservador(obs);
        }
        productos.add(producto);
    }

    public List<Producto> getProductos() {
        return productos;
    }

    public Producto buscarProductoPorNombre(String nombre) {
        for (Producto p : productos) {
            if (p.getNombre().equalsIgnoreCase(nombre)) {
                return p;
            }
        }
        return null;
    }

    // =========================================================
    // CASO DE USO: REGISTRAR SALIDA DE STOCK (VENTA)
    // =========================================================

    /**
     * Registra una salida de stock por venta a un cliente.
     *
     * @return el movimiento generado
     * @throws IllegalArgumentException si no hay stock suficiente
     */
    public MovimientoStock registrarSalidaStock(Producto producto, Empleado empleado,
                                                 Cliente cliente, int cantidad, String motivo) {
        // Descontar stock (puede generar alerta si baja del mínimo)
        producto.descontarStock(cantidad);

        // Registrar el movimiento
        MovimientoStock mov = new MovimientoStock(producto, empleado, cliente, cantidad, motivo);
        movimientos.add(mov);
        return mov;
    }

    // =========================================================
    // CASO DE USO: REGISTRAR ENTRADA DE STOCK (REPOSICIÓN)
    // =========================================================

    /**
     * Registra una entrada de stock por recepción de proveedor.
     *
     * @return el movimiento generado
     */
    public MovimientoStock registrarEntradaStock(Producto producto, Empleado empleado,
                                                  Proveedor proveedor, int cantidad, String motivo) {
        // Agregar stock (resuelve alertas automáticamente si supera el mínimo)
        producto.agregarStock(cantidad);

        // Registrar el movimiento
        MovimientoStock mov = new MovimientoStock(producto, empleado, proveedor, cantidad, motivo);
        movimientos.add(mov);
        return mov;
    }

    // =========================================================
    // CONSULTAS
    // =========================================================

    /**
     * Retorna todos los productos con stock por debajo del mínimo.
     */
    public List<Producto> getProductosConStockBajo() {
        List<Producto> resultado = new ArrayList<>();
        for (Producto p : productos) {
            if (p.tieneStockBajo()) {
                resultado.add(p);
            }
        }
        return resultado;
    }

    /**
     * Retorna el historial completo de movimientos.
     */
    public List<MovimientoStock> getMovimientos() {
        return movimientos;
    }
}
