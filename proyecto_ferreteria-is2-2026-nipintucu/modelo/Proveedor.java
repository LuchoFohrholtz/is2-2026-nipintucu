package modelo;

/**
 * Representa un proveedor que entrega mercadería a la ferretería.
 */
public class Proveedor {

    private String nombre;
    private String cuit;
    private String contacto;

    public Proveedor(String nombre, String cuit, String contacto) {
        this.nombre = nombre;
        this.cuit = cuit;
        this.contacto = contacto;
    }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getCuit() { return cuit; }
    public void setCuit(String cuit) { this.cuit = cuit; }

    public String getContacto() { return contacto; }
    public void setContacto(String contacto) { this.contacto = contacto; }

    @Override
    public String toString() {
        return "Proveedor{nombre='" + nombre + "', cuit='" + cuit + "'}";
    }
}
