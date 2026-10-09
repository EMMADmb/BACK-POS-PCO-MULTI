import os

with open('src/pos/pos.module.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

ts = ts.replace("import { PosProductoCodigo } from './entities/pos-producto-codigo.entity';", "import { PosProductoCodigo } from './entities/pos-producto-codigo.entity';\nimport { PosInventario } from './entities/pos-inventario.entity';")
ts = ts.replace("      PosProducto,", "      PosProducto,\n      PosInventario,")

with open('src/pos/pos.module.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
