package strategy;

import modelo.Producto;
import java.util.List;

public class GeneradorDeReportes {
    private ReporteStrategy estrategia;

    public void setEstrategia(ReporteStrategy estrategia) {
        this.estrategia = estrategia;
    }

    public void ejecutarGeneracion(List<Producto> productos) {
        if (estrategia != null) {
            estrategia.generar(productos);
        } else {
            System.out.println("No se ha seleccionado una estrategia de reporte.");
        }
    }
}