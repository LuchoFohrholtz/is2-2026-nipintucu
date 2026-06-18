import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('src/index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────
# FIX 1: Replace confirmarVenta() with full state-machine flow
# ─────────────────────────────────────────────────────────────
OLD_CONFIRMAR = '''async function confirmarVenta() {
  if (carrito.length === 0) { toast('El carrito está vacío.', 'warn'); return; }

  const body = {
    usuario:     sesion.usuario,
    metodo_pago: metodoPagoActivo,
    factura:     facturaData || null,
    items: carrito.map(item => ({
      producto_id:     item.producto_id,
      cantidad:        item.cantidad,
      precio_unitario: item.precio_unitario,
    })),
  };

  try {
    const r = await fetch('/api/ventas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await r.json();
    if (!r.ok) { toast(data.error, 'error'); return; }

    const ventaId = data.venta.id;
    toast(`Venta #${ventaId} confirmada — Total: ${moneda(data.total)}`);

    // Guardar snapshot de items para el comprobante
    const itemsSnapshot = [...carrito];
    const facturaSnapshot = facturaData ? {...facturaData} : null;
    const pagoSnapshot = metodoPagoActivo;

    carrito = [];
    facturaData = null;
    renderCarrito();
    resetFacturaBadge();

    cargarProductos();
    cargarMovimientos();

    // Abrir comprobante si hay factura marcada
    if (facturaSnapshot) {
      generarComprobante(ventaId, data.total, itemsSnapshot, pagoSnapshot, facturaSnapshot);
    }

    // Pop-up de alertas si hay
    if (data.notificaciones && data.notificaciones.length > 0) {
      mostrarModalAlerta(data.notificaciones);
      checkAlertasNoLeidas();
      checkBanner();
    }
  } catch(e) {
    toast('Error al procesar la venta.', 'error');
  }
}'''

NEW_CONFIRMAR = '''async function confirmarVenta() {
  if (carrito.length === 0) { toast('El carrito está vacío.', 'warn'); return; }

  const btn    = document.getElementById('btn-confirmar-venta');
  const label  = btn ? btn.querySelector('.btn-label') : null;

  // ── Estado: PROCESANDO ──
  if (btn)   { btn.disabled = true; btn.classList.add('procesando'); }
  if (label) { label.innerHTML = '<span class="spin-icon">⟳</span> Procesando venta…'; }
  ocultarFeedbackCarrito();

  const body = {
    usuario:     sesion.usuario,
    metodo_pago: metodoPagoActivo,
    factura:     facturaData || null,
    items: carrito.map(item => ({
      producto_id:     item.producto_id,
      cantidad:        item.cantidad,
      precio_unitario: item.precio_unitario,
    })),
  };

  let ventaExitosa = false;
  try {
    const r = await fetch('/api/ventas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await r.json();

    if (!r.ok) {
      // Error del servidor (stock insuficiente, etc.)
      mostrarFeedbackCarritoError(data.error || 'Error al procesar la venta.');
      resetBotonConfirmar();
      return;
    }

    ventaExitosa = true;
    const ventaId = data.venta.id;

    // Guardar snapshots antes de limpiar
    const itemsSnapshot    = [...carrito];
    const facturaSnapshot  = facturaData ? {...facturaData} : null;
    const pagoSnapshot     = metodoPagoActivo;

    // ── Estado: ÉXITO ──
    mostrarFeedbackCarritoExito(ventaId, data.total);

    // Limpiar carrito
    carrito     = [];
    facturaData = null;
    renderCarrito();
    resetFacturaBadge();

    cargarProductos();
    cargarMovimientos();
    if (document.getElementById('ventas') && document.getElementById('ventas').classList.contains('active')) {
      cargarVentasHistorial();
    }

    // Comprobante si hay factura
    if (facturaSnapshot) {
      generarComprobante(ventaId, data.total, itemsSnapshot, pagoSnapshot, facturaSnapshot);
    }

    // Alertas de stock bajo
    if (data.notificaciones && data.notificaciones.length > 0) {
      mostrarModalAlerta(data.notificaciones);
      checkAlertasNoLeidas();
      checkBanner();
    }

  } catch(e) {
    // ── Estado: ERROR DE RED ──
    mostrarFeedbackCarritoErrorRed(body);
    resetBotonConfirmar();
  }
}

function resetBotonConfirmar() {
  const btn   = document.getElementById('btn-confirmar-venta');
  const label = btn ? btn.querySelector('.btn-label') : null;
  if (btn)   { btn.disabled = false; btn.classList.remove('procesando'); }
  if (label) { label.innerHTML = '✓ Confirmar venta'; }
}

function ocultarFeedbackCarrito() {
  const fb = document.getElementById('cart-feedback');
  if (fb) { fb.innerHTML = ''; fb.style.display = 'none'; }
  const btnNueva = document.getElementById('btn-nueva-venta');
  if (btnNueva) btnNueva.style.display = 'none';
  const btnConfirmar = document.getElementById('btn-confirmar-venta');
  if (btnConfirmar) btnConfirmar.style.display = 'block';
}

function mostrarFeedbackCarritoExito(ventaId, total) {
  const btn = document.getElementById('btn-confirmar-venta');
  if (btn) btn.style.display = 'none';
  const fb = document.getElementById('cart-feedback');
  if (!fb) return;
  fb.style.display = 'block';
  fb.innerHTML = `
    <div class="cart-fb-exito">
      <div class="cart-fb-icon">✓</div>
      <div>
        <strong>Venta #${String(ventaId).padStart(4,'0')} registrada</strong>
        <div class="cart-fb-sub">Stock actualizado · Comprobante guardado</div>
      </div>
    </div>`;
  const btnNueva = document.getElementById('btn-nueva-venta');
  if (btnNueva) { btnNueva.style.display = 'block'; btnNueva.textContent = 'Nueva venta'; }
}

function mostrarFeedbackCarritoError(mensaje) {
  const fb = document.getElementById('cart-feedback');
  if (!fb) { toast(mensaje, 'error'); return; }
  fb.style.display = 'block';
  fb.innerHTML = `<div class="cart-fb-error"><span>⚠ ${mensaje}</span></div>`;
}

function mostrarFeedbackCarritoErrorRed(bodyGuardado) {
  const btn = document.getElementById('btn-confirmar-venta');
  if (btn) btn.style.display = 'none';
  const fb = document.getElementById('cart-feedback');
  if (!fb) { toast('Sin conexión con el servidor.', 'error'); return; }
  fb.style.display = 'block';
  fb.innerHTML = `
    <div class="cart-fb-error-red">
      <div><strong>⚠ No se pudo guardar</strong></div>
      <div class="cart-fb-sub">Sin conexión con el servidor. La venta queda en borrador local.</div>
      <div class="cart-fb-actions">
        <button class="btn btn-ghost btn-sm" style="width:auto" onclick="ocultarFeedbackCarrito();resetBotonConfirmar()">Cancelar</button>
        <button class="btn btn-primary btn-sm" style="width:auto" onclick="reintentarVenta(${JSON.stringify(JSON.stringify(bodyGuardado))})">↺ Reintentar</button>
      </div>
    </div>`;
}

async function reintentarVenta(bodyJson) {
  ocultarFeedbackCarrito();
  const body = JSON.parse(bodyJson);
  // Restaurar carrito desde el body guardado para poder reenviar
  try {
    const btn    = document.getElementById('btn-confirmar-venta');
    const label  = btn ? btn.querySelector('.btn-label') : null;
    if (btn)   { btn.disabled = true; btn.classList.add('procesando'); btn.style.display = 'block'; }
    if (label) { label.innerHTML = '<span class="spin-icon">⟳</span> Procesando venta…'; }
    const r = await fetch('/api/ventas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: bodyJson,
    });
    const data = await r.json();
    if (!r.ok) { mostrarFeedbackCarritoError(data.error || 'Error al procesar la venta.'); resetBotonConfirmar(); return; }
    mostrarFeedbackCarritoExito(data.venta.id, data.total);
    carrito = []; facturaData = null; renderCarrito(); resetFacturaBadge();
    cargarProductos(); cargarMovimientos();
  } catch(e) {
    mostrarFeedbackCarritoErrorRed(body);
    resetBotonConfirmar();
  }
}'''

if OLD_CONFIRMAR in text:
    text = text.replace(OLD_CONFIRMAR, NEW_CONFIRMAR, 1)
    print('OK: confirmarVenta() reemplazada con flujo completo de estados')
else:
    print('ERROR: No se encontro confirmarVenta() para reemplazar')

# ─────────────────────────────────────────────────────────────
# FIX 2: Add "btn-nueva-venta" and "cart-feedback" div to HTML
# ─────────────────────────────────────────────────────────────
OLD_BTN = '''<button class="btn btn-success" id="btn-confirmar-venta" onclick="confirmarVenta()">
                  <span class="btn-label">✓ Confirmar venta</span>
                </button>
                <button class="btn btn-ghost btn-sm" style="width:100%;margin-top:6px" onclick="vaciarCarrito()">Vaciar carrito</button>'''

NEW_BTN = '''<div id="cart-feedback" style="display:none;margin-bottom:10px"></div>
                <button class="btn btn-success" id="btn-confirmar-venta" onclick="confirmarVenta()">
                  <span class="btn-label">✓ Confirmar venta</span>
                </button>
                <button class="btn btn-success" id="btn-nueva-venta" style="display:none;width:100%;margin-top:6px" onclick="ocultarFeedbackCarrito();resetBotonConfirmar()">Nueva venta</button>
                <button class="btn btn-ghost btn-sm" style="width:100%;margin-top:6px" onclick="vaciarCarrito()">Vaciar carrito</button>'''

if OLD_BTN in text:
    text = text.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: cart-feedback y btn-nueva-venta agregados al HTML')
else:
    print('ERROR: No se encontro el bloque del boton confirmar en HTML')

# ─────────────────────────────────────────────────────────────
# FIX 3: Replace abrirAnularVenta(prompt) with modal anulacion
# ─────────────────────────────────────────────────────────────
OLD_ANULAR = '''function abrirAnularVenta(ventaId) {
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
}'''

NEW_ANULAR = '''function abrirAnularVenta(ventaId) {
  // Mostrar modal de anulacion
  const modal = document.getElementById('modal-anular-venta');
  if (!modal) {
    // Fallback si no existe el modal
    const motivo = window.prompt('Motivo de anulación (mínimo 5 caracteres):');
    if (!motivo || motivo.trim().length < 5) { toast('Motivo inválido o muy corto.', 'error'); return; }
    ejecutarAnulacion(ventaId, motivo.trim());
    return;
  }
  document.getElementById('anular-venta-id').value   = ventaId;
  document.getElementById('anular-venta-num').textContent = String(ventaId).padStart(4, '0');
  document.getElementById('anular-motivo').value      = '';
  document.getElementById('anular-error').textContent = '';
  modal.classList.add('open');
}

function cerrarModalAnular() {
  const modal = document.getElementById('modal-anular-venta');
  if (modal) modal.classList.remove('open');
}

function confirmarAnulacion() {
  const ventaId = parseInt(document.getElementById('anular-venta-id').value);
  const motivo  = (document.getElementById('anular-motivo').value || '').trim();
  const errEl   = document.getElementById('anular-error');
  if (!motivo || motivo.length < 5) {
    errEl.textContent = 'El motivo debe tener al menos 5 caracteres.';
    return;
  }
  errEl.textContent = '';
  const btnOk = document.getElementById('btn-anular-ok');
  if (btnOk) { btnOk.disabled = true; btnOk.textContent = 'Anulando…'; }
  ejecutarAnulacion(ventaId, motivo);
}

function ejecutarAnulacion(ventaId, motivo) {
  fetch('/api/ventas/' + ventaId + '/anular', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({motivo: motivo, usuario: sesion.usuario})
  })
  .then(r => r.json())
  .then(data => {
    const btnOk = document.getElementById('btn-anular-ok');
    if (btnOk) { btnOk.disabled = false; btnOk.textContent = 'Anular venta'; }
    if (data.ok) {
      cerrarModalAnular();
      toast('Venta #' + String(ventaId).padStart(4,'0') + ' anulada correctamente.');
      cargarVentasHistorial();
      cargarStats();
      cargarProductos();
    } else {
      const errEl = document.getElementById('anular-error');
      if (errEl) errEl.textContent = data.error || 'Error al anular.';
      else toast(data.error || 'Error al anular.', 'error');
    }
  })
  .catch(() => {
    const btnOk = document.getElementById('btn-anular-ok');
    if (btnOk) { btnOk.disabled = false; btnOk.textContent = 'Anular venta'; }
    toast('Sin conexión con el servidor.', 'error');
  });
}'''

if OLD_ANULAR in text:
    text = text.replace(OLD_ANULAR, NEW_ANULAR, 1)
    print('OK: abrirAnularVenta() actualizada con modal')
else:
    print('ERROR: No se encontro abrirAnularVenta() para reemplazar')
    # Check what's there
    idx = text.find('function abrirAnularVenta')
    if idx > -1:
        print('Found at:', idx)
        print(repr(text[idx:idx+300]))

# ─────────────────────────────────────────────────────────────
# FIX 4: Add modal HTML + CSS for anular and cart feedback styles
# ─────────────────────────────────────────────────────────────
MODAL_HTML = '''
<!-- ═══════════════ MODAL ANULAR VENTA ═══════════════ -->
<div class="modal-overlay" id="modal-anular-venta" onclick="if(event.target===this)cerrarModalAnular()">
  <div class="modal-box" style="max-width:420px">
    <div class="modal-header">
      <span class="modal-title">Anular venta <strong>#<span id="anular-venta-num">----</span></strong></span>
      <button class="modal-close" onclick="cerrarModalAnular()">✕</button>
    </div>
    <div class="modal-body">
      <input type="hidden" id="anular-venta-id">
      <p style="color:var(--muted2);font-size:.85rem;margin-bottom:14px">
        Esta acción restituye el stock de todos los productos de la venta. La venta quedará marcada como anulada.
      </p>
      <div class="form-group">
        <label>Motivo de anulación <span style="color:var(--rojo)">*</span></label>
        <textarea id="anular-motivo" rows="3" placeholder="Ej: Devolución del cliente, error en el pedido…"
          style="width:100%;resize:vertical;font-family:var(--sans);font-size:.9rem;padding:8px 10px;border:1px solid var(--border2);border-radius:6px;background:var(--surface2);color:var(--fg)"></textarea>
        <span id="anular-error" style="color:var(--rojo);font-size:.8rem;margin-top:4px;display:block"></span>
      </div>
    </div>
    <div class="modal-footer" style="display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-ghost btn-sm" style="width:auto" onclick="cerrarModalAnular()">Cancelar</button>
      <button class="btn btn-sm" id="btn-anular-ok" style="width:auto;background:#dc2626;color:#fff;border-color:#dc2626" onclick="confirmarAnulacion()">Anular venta</button>
    </div>
  </div>
</div>
'''

EXTRA_CSS = '''
/* ── Cart feedback states ── */
.cart-fb-exito {
  display:flex; align-items:center; gap:12px;
  background:var(--verde-l, #dcfce7); color:#15803d;
  border:1px solid #bbf7d0; border-radius:8px;
  padding:12px 14px; font-size:.88rem;
}
.cart-fb-icon { font-size:1.3rem; font-weight:700; color:#16a34a; }
.cart-fb-sub  { font-size:.78rem; color:var(--muted2); margin-top:2px; }
.cart-fb-error {
  background:var(--rojo-l,#fee2e2); color:#dc2626;
  border:1px solid #fca5a5; border-radius:8px;
  padding:10px 14px; font-size:.85rem;
}
.cart-fb-error-red {
  background:var(--rojo-l,#fee2e2); color:#dc2626;
  border:1px solid #fca5a5; border-radius:8px;
  padding:12px 14px; font-size:.85rem;
}
.cart-fb-actions { display:flex; gap:8px; margin-top:10px; }
/* Spin animation for procesando */
@keyframes spin { to { transform: rotate(360deg); } }
.spin-icon { display:inline-block; animation: spin .8s linear infinite; }
/* Procesando state button */
#btn-confirmar-venta.procesando { opacity:.8; cursor:not-allowed; }
'''

# Insert CSS before </style>
close_style = text.rfind('</style>')
if close_style > -1:
    text = text[:close_style] + EXTRA_CSS + text[close_style:]
    print('OK: CSS de feedback y spin agregado')
else:
    print('ERROR: No se encontro </style>')

# Insert modal before </body>
close_body = text.rfind('</body>')
if close_body > -1:
    text = text[:close_body] + MODAL_HTML + text[close_body:]
    print('OK: Modal de anulacion agregado')
else:
    print('ERROR: No se encontro </body>')

# ─────────────────────────────────────────────────────────────
# WRITE BACK
# ─────────────────────────────────────────────────────────────
with open('src/index.html', 'wb') as f:
    f.write(text.encode('utf-8'))
print('DONE: index.html actualizado')
