import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('src/index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

# Exact boundaries from previous inspection
SEC_COMMENT = '<!-- ══════════════ VENTAS ══════════════ -->'
s_comment = text.find(SEC_COMMENT)
sec_start = 58067  # <section class="section" id="ventas">
sec_end   = 59080  # end of </section>
# Include the comment before the section
# We'll replace from the comment to end of </section>
old_block = text[s_comment : sec_end + len('</section>')]
print('Old block length:', len(old_block))
print('First 100:', old_block[:100])
print('Last 100:', old_block[-100:])

NEW_SECTION = '''<!-- ══════════════ VENTAS ══════════════ -->
    <section class="section" id="ventas">
      <div class="page-header">
        <div class="page-title">Historial de Ventas</div>
        <div class="page-sub">Hacé click en una fila para ver el detalle completo</div>
      </div>
      <div class="ventas-split">
        <!-- LISTA -->
        <div class="ventas-lista">
          <div id="ventas-loading" style="text-align:center;padding:40px;color:var(--muted2);display:none">Cargando…</div>
          <div class="card" style="overflow:auto">
            <table class="tabla" id="tabla-ventas-hist">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Fecha</th>
                  <th>Usuario</th>
                  <th>Pago</th>
                  <th style="text-align:center">Items</th>
                  <th style="text-align:right">Total</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody id="tbody-ventas-hist">
                <tr><td colspan="7" style="text-align:center;color:var(--muted2);padding:30px">Sin ventas registradas.</td></tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- PANEL DETALLE -->
        <div class="ventas-detalle" id="ventas-detalle" style="display:none">
          <div class="vd-header">
            <div class="vd-title">VENTA <strong id="vd-num">#----</strong></div>
            <div class="vd-actions">
              <button class="btn-tiny" id="vd-btn-anular" onclick="abrirAnularVentaActual()">✕ Anular</button>
              <button class="btn-tiny" onclick="cerrarDetalleVenta()">✕ Cerrar</button>
            </div>
          </div>
          <div class="vd-body">
            <div class="vd-section"><div class="vd-label">Fecha</div><div class="vd-value" id="vd-fecha">—</div></div>
            <div class="vd-section"><div class="vd-label">Usuario</div><div class="vd-value" id="vd-usuario">—</div></div>
            <div class="vd-section"><div class="vd-label">Pago</div><div class="vd-value" id="vd-pago">—</div></div>
            <div class="vd-section"><div class="vd-label">Estado</div><div class="vd-value" id="vd-estado">—</div></div>
            <div id="vd-anulada-info" style="display:none" class="vd-anulada-box">
              <div><strong>Motivo:</strong> <span id="vd-anulada-motivo">—</span></div>
              <div><strong>Por:</strong> <span id="vd-anulada-por">—</span></div>
            </div>
            <div id="vd-factura-block" style="display:none">
              <div class="vd-sep">FACTURACIÓN</div>
              <div class="vd-section"><div class="vd-label">Tipo</div><div class="vd-value" id="vd-fact-tipo">—</div></div>
              <div class="vd-section"><div class="vd-label">Cliente</div><div class="vd-value" id="vd-fact-nombre">—</div></div>
              <div class="vd-section"><div class="vd-label">DNI/CUIT</div><div class="vd-value" id="vd-fact-doc">—</div></div>
            </div>
            <div class="vd-sep">ARTÍCULOS</div>
            <div id="vd-items-loading" style="text-align:center;padding:12px;color:var(--muted2);font-size:.8rem">Cargando…</div>
            <table class="tabla vd-tabla-items" id="vd-tabla-items" style="display:none;font-size:.8rem">
              <thead><tr><th>Producto</th><th style="text-align:center">Cant.</th><th style="text-align:right">P.Unit</th><th style="text-align:right">Subtotal</th></tr></thead>
              <tbody id="vd-tbody-items"></tbody>
            </table>
            <div class="vd-total-row">
              <span>Total</span>
              <span class="vd-total-val" id="vd-total">$0</span>
            </div>
          </div>
        </div>
      </div>
    </section>'''

text = text[:s_comment] + NEW_SECTION + text[sec_end + len('</section>'):]
print('OK: seccion ventas reemplazada')

with open('src/index.html', 'wb') as f:
    f.write(text.encode('utf-8'))
print('DONE: guardado')
