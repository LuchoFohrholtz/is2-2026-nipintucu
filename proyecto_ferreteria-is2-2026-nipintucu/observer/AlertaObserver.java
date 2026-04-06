package observer;

import modelo.Alerta;  // ← agregá esta línea

public interface AlertaObserver {
    void onAlertaGenerada(Alerta alerta);
}
