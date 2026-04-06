import modelo.*;
import observer.AlertaConsolaObserver;
import servicio.InventarioServicio;
import strategy.*;

import java.util.List;
import java.util.Scanner;

/**
 * Punto de entrada de la aplicación.
 * Menú de consola para probar el sistema completo con patrones Observer y Strategy.
 */
public class Main {

    private static InventarioServicio servicio = new InventarioServicio();
    private static Empleado empleadoActivo;
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {

        // --- Datos de ejemplo ---
        configurarDatosIniciales();

        // --- Registrar observador de consola (Patrón Observer) ---
        servicio.agregarObservadorGlobal(new AlertaConsolaObserver());

        System.out.println("=== SISTEMA DE INVENTARIO - FERRETERÍA ===");
        System.out.println("Empleado activo: " + empleadoActivo.getNombre());

        boolean salir = false;
        while (!salir) {
            mostrarMenu();
            int opcion = leerEntero("Opción: ");

            switch (opcion) {
                case 1 -> registrarSalidaStock();
                case 2 -> registrarEntradaStock();
                case 3 -> listarProductos();
                case 4 -> listarStockBajo();
                case 5 -> listarMovimientos();
                case 6 -> exportarReportes();
                case 0 -> salir = true;
                default -> System.out.println("Opción inválida.");
            }
        }

        System.out.println("Sistema cerrado.");
    }

    // =========================================================
    // MENÚ
    // =========================================================

    private static void mostrarMenu() {
        System.out.println("\n--- MENÚ PRINCIPAL ---");
        System.out.println("1. Registrar salida de stock (venta)");
        System.out.println("2. Registrar entrada de stock (reposición)");
        System.out.println("3. Listar productos");
        System.out.println("4. Ver productos con stock bajo");
        System.out.println("5. Ver historial de movimientos");
        System.out.println("6. Generar reporte de inventario (Strategy)");
        System.out.println("0. Salir");
    }

    // =========================================================
    // IMPLEMENTACIÓN DEL PATRÓN STRATEGY
    // =========================================================

    private static void exportarReportes() {
        System.out.println("\n-- Generar Reporte de Inventario --");
        System.out.println("1. Reporte de Stock Actual");
        System.out.println("2. Reporte de Reposición (Solo faltantes)");
        int opcion = leerEntero("Seleccione opción: ");

        // Uso de la clase de contexto según el informe
        GeneradorDeReportes generador = new GeneradorDeReportes();
        List<Producto> inventarioActual = servicio.getProductos();

        if (opcion == 1) {
            generador.setEstrategia(new ReporteStockActual());
        } else if (opcion == 2) {
            generador.setEstrategia(new ReporteReposicion());
        } else {
            System.out.println("Opción inválida.");
            return;
        }

        // Ejecución del método definido en el diagrama de clases
        generador.ejecutarGeneracion(inventarioActual);
    }

    // =========================================================
    // CASOS DE USO EXISTENTES
    // =========================================================

    private static void registrarSalidaStock() {
        System.out.println("\n-- Registrar Salida de Stock --");
        Producto producto = seleccionarProducto();
        if (producto == null) return;

        System.out.print("Nombre del cliente: ");
        String nombreCliente = scanner.nextLine();
        System.out.print("Teléfono del cliente: ");
        String telefonoCliente = scanner.nextLine();
        Cliente cliente = new Cliente(nombreCliente, telefonoCliente, "");

        int cantidad = leerEntero("Cantidad a retirar: ");
        System.out.print("Motivo: ");
        String motivo = scanner.nextLine();

        try {
            MovimientoStock mov = servicio.registrarSalidaStock(
                    producto, empleadoActivo, cliente, cantidad, motivo
            );
            System.out.println("✓ Movimiento registrado: " + mov);
        } catch (IllegalArgumentException e) {
            System.out.println("✗ Error: " + e.getMessage());
        }
    }

    private static void registrarEntradaStock() {
        System.out.println("\n-- Registrar Entrada de Stock --");
        Producto producto = seleccionarProducto();
        if (producto == null) return;

        System.out.print("Nombre del proveedor: ");
        String nombreProv = scanner.nextLine();
        System.out.print("CUIT del proveedor: ");
        String cuit = scanner.nextLine();
        Proveedor proveedor = new Proveedor(nombreProv, cuit, "");

        int cantidad = leerEntero("Cantidad a ingresar: ");
        System.out.print("Motivo: ");
        String motivo = scanner.nextLine();

        MovimientoStock mov = servicio.registrarEntradaStock(
                producto, empleadoActivo, proveedor, cantidad, motivo
        );
        System.out.println("✓ Movimiento registrado: " + mov);
    }

    private static void listarProductos() {
        System.out.println("\n-- Productos en inventario --");
        List<Producto> lista = servicio.getProductos();
        if (lista.isEmpty()) {
            System.out.println("No hay productos.");
            return;
        }
        for (int i = 0; i < lista.size(); i++) {
            System.out.println((i + 1) + ". " + lista.get(i));
        }
    }

    private static void listarStockBajo() {
        System.out.println("\n-- Productos con stock bajo --");
        List<Producto> lista = servicio.getProductosConStockBajo();
        if (lista.isEmpty()) {
            System.out.println("Todos los productos tienen stock suficiente.");
        } else {
            for (Producto p : lista) {
                System.out.println("⚠️ " + p);
            }
        }
    }

    private static void listarMovimientos() {
        System.out.println("\n-- Historial de movimientos --");
        List<MovimientoStock> lista = servicio.getMovimientos();
        if (lista.isEmpty()) {
            System.out.println("No hay movimientos registrados.");
            return;
        }
        for (MovimientoStock m : lista) {
            System.out.println(m);
        }
    }

    // =========================================================
    // HELPERS
    // =========================================================

    private static Producto seleccionarProducto() {
        listarProductos();
        int idx = leerEntero("Número de producto: ") - 1;
        List<Producto> lista = servicio.getProductos();
        if (idx < 0 || idx >= lista.size()) {
            System.out.println("Producto inválido.");
            return null;
        }
        return lista.get(idx);
    }

    private static int leerEntero(String prompt) {
        System.out.print(prompt);
        while (!scanner.hasNextInt()) {
            scanner.next();
            System.out.print("Ingrese un número válido: ");
        }
        int valor = scanner.nextInt();
        scanner.nextLine();
        return valor;
    }

    private static void configurarDatosIniciales() {
        empleadoActivo = new Empleado("Santiago Gonzalez", "010");

        Categoria electricas = new Categoria(
                "Herramientas Eléctricas",
                "Herramientas de mano con motor"
        );

        Producto amoladora = new Producto(
                "Amoladora Caterpillar 115mm",
                85000.00,
                6,
                5,
                electricas
        );

        Producto taladro = new Producto(
                "Taladro Black&Decker 650W",
                62000.00,
                8,
                3,
                electricas
        );

        servicio.agregarProducto(amoladora);
        servicio.agregarProducto(taladro);
    }
}