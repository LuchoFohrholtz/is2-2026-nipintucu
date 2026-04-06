package strategy;

import modelo.Producto;
import java.util.List;

public class ReportePDF implements ReporteStrategy {

    @Override
    public void generarReporte(List<Producto> productos) {
        System.out.println("\n[SISTEMA] Generando documento PDF...");
        System.out.println("=====================================================");
        System.out.println("           REPORTE DE INVENTARIO - FERRETERÍA        ");
        System.out.println("=====================================================");

        for (Producto p : productos) {
            System.out.printf("- %-30s | Stock: %3d | Precio: $%8.2f\n",
                    p.getNombre(), p.getStockActual(), p.getPrecio());
        }

        System.out.println("=====================================================");
        System.out.println("[SISTEMA] PDF guardado correctamente como 'reporte_inventario.pdf'.\n");
    }
}