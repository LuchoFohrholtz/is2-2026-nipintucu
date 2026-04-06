package observer;

import modelo.Alerta;

/**
 * Observador concreto que imprime las alertas en consola.
 *
 * La persona que haga la interfaz gráfica puede crear otro observador
 * (ej: AlertaUIObserver) que muestre un popup o actualice un panel,
 * sin tocar nada del dominio.
 *
 * Ejemplo de cómo agregar un observador de UI en el futuro:
 *
 *   producto.agregarObservador(alerta -> {
 *       // mostrar alerta en un JLabel, JDialog, etc.
 *   });
 */
public class AlertaConsolaObserver implements AlertaObserver {

    @Override
    public void onAlertaGenerada(Alerta alerta) {
        System.out.println("========================================");
        System.out.println("⚠️  " + alerta);
        System.out.println("========================================");
    }
}
