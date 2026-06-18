import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('src/index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

checks = [
    'id="ventas-detalle"',
    'ventas-split',
    'ventas-fila',
    'vd-row-active',
    'async function verDetalleVenta(',
    'function cerrarDetalleVenta(',
    'function abrirAnularVentaActual(',
    'vd-total-row',
    'vd-tabla-items',
]
for c in checks:
    found = c in text
    print(f"{'OK' if found else 'MISSING'}: {c}")
