package modelo;

import observer.AlertaObserver;
import java.util.ArrayList;
import java.util.List;

/**
 * Representa un producto de la ferretería.
 *
 * Actúa como SUBJECT en el patrón Observer:
 * cuando el stock baja del mínimo, notifica a todos los observadores registrados.
 *
 * La lógica de negocio (actualizar stock, verificar mínimo, notificar)
 * está completamente separada de cualquier interfaz gráfica.
 */
public class Producto {

    private String nombre;
    private double precio;
    private int stockActual;
    private int stockMinimo;
    private Categoria categoria;

    // Lista de observadores (consola, UI, email, etc.)
    private List<AlertaObserver> observadores = new ArrayList<>();

    // Alertas generadas por este producto
    private List<Alerta> alertas = new ArrayList<>();

    public Producto(String nombre, double precio, int stockActual, int stockMinimo, Categoria categoria) {
        this.nombre = nombre;
        this.precio = precio;
        this.stockActual = stockActual;
        this.stockMinimo = stockMinimo;
        this.categoria = categoria;
    }

    // =========================================================
    // PATRÓN OBSERVER — gestión de observadores
    // =========================================================

    public void agregarObservador(AlertaObserver observador) {
        observadores.add(observador);
    }

    public void quitarObservador(AlertaObserver observador) {
        observadores.remove(observador);
    }

    private void notificarObservadores(Alerta alerta) {
        for (AlertaObserver obs : observadores) {
            obs.onAlertaGenerada(alerta);
        }
    }

    // =========================================================
    // LÓGICA DE NEGOCIO
    // =========================================================

    /**
     * Verifica si el stock actual está por debajo del mínimo.
     */
    public boolean tieneStockBajo() {
        return stockActual < stockMinimo;
    }

    /**
     * Reduce el stock según la cantidad vendida/salida.
     * Si el stock resultante queda bajo el mínimo, genera y propaga una alerta.
     *
     * @param cantidad unidades a descontar
     * @throws IllegalArgumentException si no hay stock suficiente
     */
    public void descontarStock(int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("La cantidad debe ser mayor a 0.");
        }
        if (cantidad > stockActual) {
            throw new IllegalArgumentException(
                "Stock insuficiente. Disponible: " + stockActual + ", solicitado: " + cantidad
            );
        }

        this.stockActual -= cantidad;

        if (tieneStockBajo()) {
            Alerta alerta = new Alerta(this);
            alertas.add(alerta);
            notificarObservadores(alerta);  // ← Observer en acción
        }
    }

    /**
     * Incrementa el stock (entrada de mercadería / reposición).
     * Si había alertas pendientes, las resuelve automáticamente.
     *
     * @param cantidad unidades a agregar
     */
    public void agregarStock(int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("La cantidad debe ser mayor a 0.");
        }

        this.stockActual += cantidad;

        // Si el stock ya superó el mínimo, resolver alertas pendientes
        if (!tieneStockBajo()) {
            resolverAlertasPendientes();
        }
    }

    /**
     * Resuelve todas las alertas pendientes de este producto.
     */
    private void resolverAlertasPendientes() {
        for (Alerta alerta : alertas) {
            if (alerta.esPendiente()) {
                alerta.resolver();
            }
        }
    }

    // =========================================================
    // GETTERS Y SETTERS
    // =========================================================

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public double getPrecio() { return precio; }
    public void setPrecio(double precio) { this.precio = precio; }

    public int getStockActual() { return stockActual; }

    public int getStockMinimo() { return stockMinimo; }
    public void setStockMinimo(int stockMinimo) { this.stockMinimo = stockMinimo; }

    public Categoria getCategoria() { return categoria; }
    public void setCategoria(Categoria categoria) { this.categoria = categoria; }

    public List<Alerta> getAlertas() { return alertas; }

    @Override
    public String toString() {
        return "Producto{nombre='" + nombre + "'"
                + ", precio=$" + String.format("%.2f", precio)
                + ", stock=" + stockActual + "/" + stockMinimo
                + ", categoria='" + categoria.getNombre() + "'}";
    }
}
