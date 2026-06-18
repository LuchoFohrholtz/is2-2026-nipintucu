import sys, io

# Read raw bytes
with open('src/index.html', 'rb') as f:
    raw = f.read()

text = raw.decode('utf-8', errors='replace')

# ── FIX 1: Insert <section id="ventas"> after movimientos section ──────────
VENTAS_SECTION = '''

    <!-- ══════════════ VENTAS ══════════════ -->
    <section class="section" id="ventas">
      <div class="page-header">
        <div class="page-title">Historial de Ventas</div>
        <div class="page-sub">Registro de todas las ventas confirmadas</div>
      </div>

      <div id="ventas-loading" style="text-align:center;padding:40px;color:var(--muted2);display:none">Cargando ventas…</div>

      <div class="card" style="overflow:auto">
        <table class="tabla" id="tabla-ventas-hist">
          <thead>
            <tr>
              <th>#</th>
              <th>Fecha</th>
              <th>Usuario</th>
              <th>Método Pago</th>
              <th>Items</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody id="tbody-ventas-hist">
            <tr><td colspan="8" style="text-align:center;color:var(--muted2);padding:30px">
              Sin ventas registradas todavía.
            </td></tr>
          </tbody>
        </table>
      </div>
    </section>

'''

# Insert after the closing </section> of movimientos (position 57720 + len('</section>'))
insert_pos = text.find('</section>\n\n    <!-- ══════════════ ALERTAS')
if insert_pos == -1:
    insert_pos = text.find('</section>', text.find('id="movimientos"'))
    print('Fallback insert_pos:', insert_pos)
else:
    print('Found alertas divider at:', insert_pos)

# Insert after </section>
new_text = text[:insert_pos + len('</section>')] + VENTAS_SECTION + text[insert_pos + len('</section>'):]
print('Ventas section inserted. New size:', len(new_text))

# ── FIX 2: Add cargarVentas() call in ir() function ─────────────────────────
OLD_IR = "  if (id === 'alertas')     { cargarAlertas(); cargarCriticos(); }\n}"
NEW_IR = "  if (id === 'alertas')     { cargarAlertas(); cargarCriticos(); }\n  if (id === 'ventas')      { cargarVentasHistorial(); }\n}"

if OLD_IR in new_text:
    new_text = new_text.replace(OLD_IR, NEW_IR, 1)
    print('ir() function updated.')
else:
    print('WARNING: Could not find ir() pattern to update!')

# ── FIX 3: Add cargarVentasHistorial() function before // MÉTODO DE PAGO ──
VENTAS_FUNC = '''
// ══════════════════════════════════════════════════════════
//  HISTORIAL DE VENTAS
// ══════════════════════════════════════════════════════════
async function cargarVentasHistorial() {
  const tbody = document.getElementById('tbody-ventas-hist');
  const loading = document.getElementById('ventas-loading');
  if (loading) loading.style.display = 'block';
  try {
    const r = await fetch('/api/ventas');
    const ventas = await r.json();
    if (loading) loading.style.display = 'none';
    if (!Array.isArray(ventas) || ventas.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--muted2);padding:30px">Sin ventas registradas todavía.</td></tr>';
      return;
    }
    tbody.innerHTML = ventas.map(v => {
      const anulada = v.anulada;
      const metodoPago = (v.metodo_pago || 'efectivo').charAt(0).toUpperCase() + (v.metodo_pago || 'efectivo').slice(1);
      const fecha = v.created_at ? new Date(v.created_at).toLocaleString('es-AR') : '—';
      const estadoBadge = anulada
        ? '<span class="tag-pill" style="background:var(--rojo-l,#fee2e2);color:#dc2626">Anulada</span>'
        : '<span class="tag-pill" style="background:var(--verde-l,#dcfce7);color:#16a34a">Confirmada</span>';
      const acciones = anulada ? '—' : `<button class="btn-tiny" onclick="abrirAnularVenta(${v.id})">Anular</button>`;
      return `<tr class="${anulada ? 'venta-anulada' : ''}">
        <td class="mono">#${String(v.id).padStart(4,'0')}</td>
        <td>${fecha}</td>
        <td>${v.usuario || '—'}</td>
        <td>${metodoPago}</td>
        <td style="text-align:center">${v.items_count || (v.items ? v.items.length : '—')}</td>
        <td class="mono" style="font-weight:700;color:var(--verde)">${moneda(v.total)}</td>
        <td>${estadoBadge}</td>
        <td>${acciones}</td>
      </tr>`;
    }).join('');
  } catch(e) {
    if (loading) loading.style.display = 'none';
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--rojo,#dc2626);padding:30px">Error al cargar ventas.</td></tr>';
  }
}

function abrirAnularVenta(ventaId) {
  const motivo = prompt('Motivo de anulación (mínimo 5 caracteres):');
  if (!motivo || motivo.trim().length < 5) {
    toast('Motivo inválido o muy corto.', 'error');
    return;
  }
  fetch('/api/ventas/' + ventaId + '/anular', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({motivo: motivo.trim(), usuario: sesion.usuario})
  }).then(r => r.json()).then(data => {
    if (data.ok) {
      toast('Venta anulada correctamente.');
      cargarVentasHistorial();
      cargarStats();
      cargarProductos();
    } else {
      toast(data.error || 'Error al anular.', 'error');
    }
  }).catch(() => toast('Error de conexión al anular.', 'error'));
}

'''

# Insert before "// ══ MÉTODO DE PAGO"
METODO_MARKER = '// ══════════════════════════════════════════════════════════\n//  MÉTODO DE PAGO'
if METODO_MARKER in new_text:
    new_text = new_text.replace(METODO_MARKER, VENTAS_FUNC + METODO_MARKER, 1)
    print('cargarVentasHistorial() function inserted.')
else:
    # Try alternate
    METODO_MARKER2 = 'function seleccionarPago('
    if METODO_MARKER2 in new_text:
        new_text = new_text.replace(METODO_MARKER2, VENTAS_FUNC + METODO_MARKER2, 1)
        print('cargarVentasHistorial() inserted before seleccionarPago()')
    else:
        print('WARNING: Could not find insertion point for cargarVentasHistorial!')

# Write back
with open('src/index.html', 'wb') as f:
    f.write(new_text.encode('utf-8'))

print('Done! index.html updated successfully.')
