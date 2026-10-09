import os

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

ts = ts.replace(".groupBy('d.id_producto')", ".groupBy('d.id_producto, p.nombre')")

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print('Fixed groupBy')
