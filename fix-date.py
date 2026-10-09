import os

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

ts = ts.replace("DATE_FORMAT(v.fechaVenta, '%Y-%m-%d')", "TO_CHAR(v.fechaVenta, 'YYYY-MM-DD')")

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print('Fixed DATE_FORMAT to TO_CHAR')
