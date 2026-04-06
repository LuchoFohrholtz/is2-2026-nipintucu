package strategy;

import modelo.Producto;
import java.util.List;

public class GeneradorReportes {

    private ReporteStrategy estrategia;

    // Permite cambiar la estrategia dinámicamente
    public void setEstrategia(ReporteStrategy estrategia) {
        this.estrategia = estrategia;
    }

    public void exportarInventario(List<Producto> productos) {
        if (estrategia == null) {
            System.out.println("Error: No se seleccionó ningún formato para el reporte.");
            return;
        }
        estrategia.generarReporte(productos);
    }
}