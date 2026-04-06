package strategy;

import modelo.Producto;
import java.util.List;

public interface ReporteStrategy {
    void generarReporte(List<Producto> productos);
}