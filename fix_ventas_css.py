import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('src/index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

# ── Replace ALL ventas-split CSS with corrected version ──────────────
OLD_CSS = '''/* ── Ventas split layout ── */
.ventas-split { display:flex; gap:0; height:calc(100vh - 220px); min-height:400px; }
.ventas-lista { flex:1; overflow:hidden; display:flex; flex-direction:column; gap:12px; }
.ventas-lista .card { flex:1; overflow:auto; margin:0; }
.ventas-fila { cursor:pointer; transition:background .15s; }
.ventas-fila:hover td { background:var(--surface2) !important; }
.ventas-fila.vd-row-active td { background:var(--azul-btn) !important; color:#fff !important; }
.ventas-fila.vd-row-active .tag-pill { background:rgba(255,255,255,.2) !important; color:#fff !important; }
/* Panel derecho */
.ventas-detalle {
  width:340px; min-width:300px; flex-shrink:0;
  margin-left:16px;
  background:var(--surface); border:1px solid var(--border2); border-radius:10px;
  display:flex; flex-direction:column; overflow:hidden;
}
.vd-header {
  background:var(--azul-btn); color:#fff;
  padding:12px 16px; display:flex; justify-content:space-between; align-items:center;
  flex-shrink:0;
}
.vd-title { font-size:.9rem; font-weight:700; letter-spacing:.04em; }
.vd-actions { display:flex; gap:6px; }
.vd-actions .btn-tiny { background:rgba(255,255,255,.15); color:#fff; border-color:rgba(255,255,255,.3); }
.vd-actions .btn-tiny:hover { background:rgba(255,255,255,.25); }
.vd-body { flex:1; overflow-y:auto; padding:14px 16px; display:flex; flex-direction:column; gap:6px; }
.vd-section { display:flex; justify-content:space-between; align-items:center; padding:4px 0; border-bottom:1px solid var(--border); }
.vd-label { font-size:.75rem; color:var(--muted2); font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
.vd-value { font-size:.85rem; color:var(--fg); font-weight:500; text-align:right; }
.vd-sep { font-size:.7rem; font-weight:800; color:var(--muted2); text-transform:uppercase; letter-spacing:.08em; margin-top:10px; margin-bottom:4px; padding-bottom:4px; border-bottom:2px solid var(--border2); }
.vd-tabla-items { font-size:.8rem; }
.vd-tabla-items th, .vd-tabla-items td { padding:6px 8px; }
.vd-total-row { display:flex; justify-content:space-between; align-items:center; padding:10px 8px; margin-top:8px; border-top:2px solid var(--border2); font-weight:700; }
.vd-total-val { font-size:1.1rem; color:var(--verde); }
.vd-anulada-box { background:#fee2e2; color:#dc2626; border-radius:6px; padding:8px 10px; font-size:.8rem; display:flex; flex-direction:column; gap:4px; }
@media(max-width:768px) {
  .ventas-split { flex-direction:column; height:auto; }
  .ventas-detalle { width:100%; margin-left:0; margin-top:12px; }
}'''

NEW_CSS = '''/* ── Ventas split layout ── */
.ventas-split {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 16px;
  align-items: start;
  min-height: 500px;
}
/* Lista */
.ventas-lista { overflow: hidden; }
.ventas-lista .card { margin: 0; overflow: auto; max-height: calc(100vh - 230px); }
/* Filas compactas */
#tabla-ventas-hist thead th {
  padding: 6px 10px;
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .04em;
  white-space: nowrap;
}
.ventas-fila td {
  padding: 5px 10px !important;
  font-size: .82rem;
  white-space: nowrap;
  cursor: pointer;
}
.ventas-fila { cursor: pointer; transition: background .12s; }
.ventas-fila:hover td { background: var(--surface2) !important; }
.ventas-fila.vd-row-active td {
  background: var(--azul-btn) !important;
  color: #fff !important;
}
.ventas-fila.vd-row-active .tag-pill {
  background: rgba(255,255,255,.25) !important;
  color: #fff !important;
}
/* Panel derecho */
.ventas-detalle {
  position: sticky;
  top: 70px;
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  max-height: calc(100vh - 180px);
}
.vd-header {
  background: var(--azul-btn);
  color: #fff;
  padding: 10px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}
.vd-title { font-size: .85rem; font-weight: 700; letter-spacing: .05em; }
.vd-actions { display: flex; gap: 5px; }
.vd-actions .btn-tiny {
  background: rgba(255,255,255,.15);
  color: #fff;
  border-color: rgba(255,255,255,.3);
  font-size: .7rem;
  padding: 2px 8px;
}
.vd-actions .btn-tiny:hover { background: rgba(255,255,255,.28); }
.vd-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 0;
}
/* Info rows */
.vd-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 5px 0;
  border-bottom: 1px solid var(--border);
  gap: 8px;
}
.vd-row:last-of-type { border-bottom: none; }
.vd-label {
  font-size: .7rem;
  color: var(--muted2);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .05em;
  white-space: nowrap;
  flex-shrink: 0;
}
.vd-value {
  font-size: .82rem;
  color: var(--fg);
  font-weight: 500;
  text-align: right;
}
/* Section divider */
.vd-sep {
  font-size: .65rem;
  font-weight: 800;
  color: var(--muted2);
  text-transform: uppercase;
  letter-spacing: .08em;
  margin: 10px 0 4px;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--border2);
}
/* Items table */
.vd-tabla-items {
  font-size: .78rem;
  width: 100%;
  border-collapse: collapse;
}
.vd-tabla-items th {
  padding: 4px 6px;
  font-size: .65rem;
  text-transform: uppercase;
  letter-spacing: .05em;
  color: var(--muted2);
  border-bottom: 1px solid var(--border2);
  font-weight: 700;
}
.vd-tabla-items td {
  padding: 5px 6px;
  border-bottom: 1px solid var(--border);
  color: var(--fg);
}
.vd-tabla-items tbody tr:last-child td { border-bottom: none; }
/* Total */
.vd-total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0 0;
  margin-top: 6px;
  border-top: 2px solid var(--border2);
  font-weight: 700;
  font-size: .88rem;
}
.vd-total-val { font-size: 1rem; color: var(--verde); }
/* Anulada box */
.vd-anulada-box {
  background: #fee2e2;
  color: #dc2626;
  border-radius: 6px;
  padding: 7px 10px;
  font-size: .78rem;
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin: 6px 0;
}
/* Placeholder */
.vd-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: var(--muted2);
  font-size: .82rem;
  gap: 8px;
  padding: 30px 16px;
  text-align: center;
}
.vd-placeholder-icon { font-size: 2rem; opacity: .4; }
@media(max-width: 900px) {
  .ventas-split { grid-template-columns: 1fr; }
  .ventas-detalle { position: static; max-height: 500px; }
}'''

if OLD_CSS in text:
    text = text.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: CSS ventas-split reemplazado')
else:
    # Try finding and replacing the block by markers
    s = text.find('/* ── Ventas split layout ── */')
    e = text.find('\n}', text.find('@media(max-width:768px)', s)) + 2
    if s > -1 and e > -1:
        text = text[:s] + NEW_CSS + text[e:]
        print('OK: CSS reemplazado por posicion')
    else:
        print('ERROR: no se encontro el bloque CSS')

# ── Also update the HTML section — replace .vd-section with .vd-row ──
# The panel HTML uses vd-section class, update to vd-row
text = text.replace('class="vd-section"', 'class="vd-row"')
print('OK: vd-section -> vd-row')

# ── Add placeholder to the panel when no sale is selected ────────────
OLD_VD_BODY_START = '''          <div class="vd-body">
            <div class="vd-row"><div class="vd-label">Fecha</div><div class="vd-value" id="vd-fecha">—</div></div>'''
NEW_VD_BODY_START = '''          <div class="vd-body">
            <div id="vd-placeholder" class="vd-placeholder">
              <div class="vd-placeholder-icon">🧾</div>
              <div>Seleccioná una venta<br>para ver su detalle</div>
            </div>
            <div id="vd-content" style="display:none;flex-direction:column;gap:0;flex:1">
            <div class="vd-row"><div class="vd-label">Fecha</div><div class="vd-value" id="vd-fecha">—</div></div>'''

OLD_VD_BODY_END = '''            <div class="vd-total-row">
              <span>Total</span>
              <span class="vd-total-val" id="vd-total">$0</span>
            </div>
          </div>'''
NEW_VD_BODY_END = '''            <div class="vd-total-row">
              <span>Total</span>
              <span class="vd-total-val" id="vd-total">$0</span>
            </div>
            </div><!-- /vd-content -->
          </div>'''

if OLD_VD_BODY_START in text:
    text = text.replace(OLD_VD_BODY_START, NEW_VD_BODY_START, 1)
    print('OK: placeholder agregado')
else:
    print('WARN: no se encontro el inicio del vd-body para agregar placeholder')

if OLD_VD_BODY_END in text:
    text = text.replace(OLD_VD_BODY_END, NEW_VD_BODY_END, 1)
    print('OK: cierre vd-content agregado')
else:
    print('WARN: no se encontro el fin del vd-body')

# ── Make panel always visible (remove style="display:none") ──────────
text = text.replace(
    '<div class="ventas-detalle" id="ventas-detalle" style="display:none">',
    '<div class="ventas-detalle" id="ventas-detalle">'
)
print('OK: panel siempre visible')

# ── Update verDetalleVenta to show/hide content div ──────────────────
OLD_SHOW = "  // Mostrar panel\n  const panel = document.getElementById('ventas-detalle');\n  panel.style.display = 'flex';"
NEW_SHOW = "  // Mostrar contenido del panel (ocultar placeholder)\n  const placeholder = document.getElementById('vd-placeholder');\n  const content = document.getElementById('vd-content');\n  if (placeholder) placeholder.style.display = 'none';\n  if (content) content.style.display = 'flex';"
if OLD_SHOW in text:
    text = text.replace(OLD_SHOW, NEW_SHOW, 1)
    print('OK: verDetalleVenta actualizado')
else:
    print('WARN: no se encontro el bloque show panel en verDetalleVenta')

OLD_CLOSE = """function cerrarDetalleVenta() {
  document.getElementById('ventas-detalle').style.display = 'none';
  document.querySelectorAll('.ventas-fila').forEach(r => r.classList.remove('vd-row-active'));
  _ventaDetalleActual = null;
}"""
NEW_CLOSE = """function cerrarDetalleVenta() {
  const placeholder = document.getElementById('vd-placeholder');
  const content = document.getElementById('vd-content');
  if (placeholder) placeholder.style.display = 'flex';
  if (content) content.style.display = 'none';
  document.querySelectorAll('.ventas-fila').forEach(r => r.classList.remove('vd-row-active'));
  _ventaDetalleActual = null;
}"""
if OLD_CLOSE in text:
    text = text.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: cerrarDetalleVenta actualizado')
else:
    print('WARN: no se encontro cerrarDetalleVenta')

with open('src/index.html', 'wb') as f:
    f.write(text.encode('utf-8'))
print('DONE: index.html guardado')
