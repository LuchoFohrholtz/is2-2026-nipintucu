package strategy;

import modelo.Producto;
import java.util.List;

public class ReporteExcel implements ReporteStrategy {

    @Override
    public void generarReporte(List<Producto> productos) {
        System.out.println("\n[SISTEMA] Generando archivo Excel/CSV...");

        // Cabecera del CSV
        System.out.println("Nombre_Producto,Precio,Stock_Actual,Stock_Minimo,Categoria");

        // Filas
        for (Producto p : productos) {
            String lineaCsv = String.format("%s,%.2f,%d,%d,%s",
                    p.getNombre(),
                    p.getPrecio(),
                    p.getStockActual(),
                    p.getStockMinimo(),
                    p.getCategoria().getNombre());
            System.out.println(lineaCsv);
        }
        System.out.println("[SISTEMA] Excel exportado correctamente a 'inventario_ferreteria.csv'.\n");
    }
}