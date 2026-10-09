import os
import re

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

# Replace stock update in checkout
pattern = r"producto\.stockActual = Number\(producto\.stockActual\) - Number\(item\.cantidad\);\s*await queryRunner\.manager\.save\(producto\);"

new_checkout_stock = """let inv = await queryRunner.manager.findOne(PosInventario, {
          where: { producto: { idProducto: producto.idProducto }, sucursal: { idSucursal: usuario.sucursal.idSucursal } }
        });
        
        if (!inv) {
          inv = queryRunner.manager.create(PosInventario, {
            producto: { idProducto: producto.idProducto },
            sucursal: { idSucursal: usuario.sucursal.idSucursal },
            stockActual: 0,
            stockMinimo: 0
          });
        }

        inv.stockActual = Number(inv.stockActual) - Number(item.cantidad);
        await queryRunner.manager.save(inv);"""

ts = re.sub(pattern, new_checkout_stock, ts, flags=re.DOTALL)

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
