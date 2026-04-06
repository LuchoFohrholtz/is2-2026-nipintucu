package strategy;

import modelo.Producto;
import java.util.List;

public interface ReporteStrategy {
    void generar(List<Producto> productos);
}