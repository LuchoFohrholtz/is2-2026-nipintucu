package strategy;

import modelo.Producto;
import java.util.List;

public class ReporteReposicion implements ReporteStrategy {
    @Override
    public void generar(List<Producto> productos) {
        System.out.println("\n--- REPORTE DE REPOSICIÓN (STOCK BAJO) ---");
        for (Producto p : productos) {
            if (p.getStockActual() <= p.getStockMinimo()) {
                System.out.println("REPONER: " + p.getNombre() + " (Actual: " + p.getStockActual() + " - Min: " + p.getStockMinimo() + ")");
            }
        }
    }
}