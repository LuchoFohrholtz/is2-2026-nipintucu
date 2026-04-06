package strategy;

import modelo.Producto;
import java.util.List;

public class ReporteStockActual implements ReporteStrategy {
    @Override
    public void generar(List<Producto> productos) {
        System.out.println("\n--- REPORTE DE STOCK ACTUAL ---");
        for (Producto p : productos) {
            System.out.println("Producto: " + p.getNombre() + " | Stock: " + p.getStockActual());
        }
    }
}