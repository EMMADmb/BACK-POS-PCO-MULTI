import os
import re

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

pattern = r"async registrarEntradaInventario\(payload: \{ idProducto: number;[\s\S]*?finally \{\s*await queryRunner\.release\(\);\s*\}\s*\}"

new_code = """async registrarEntradaInventario(payload: { idProducto: number; cantidad: number; referencia?: string; tipoMovimiento?: string; costoUnitario?: number; actualizarCosto?: boolean }, idUsuario: number, idSucursal?: number) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      const producto = await queryRunner.manager.findOne(PosProducto, { 
        where: { idProducto: payload.idProducto },
      });
      if (!producto) throw new BadRequestException('Producto no encontrado');

      const usuario = await queryRunner.manager.findOne(PosUsuario, { where: { idUsuario: idUsuario } });
      if (!usuario) throw new BadRequestException('Usuario no encontrado');

      const cantidadNumber = Number(payload.cantidad);
      if (isNaN(cantidadNumber) || cantidadNumber <= 0) {
        throw new BadRequestException('La cantidad debe ser mayor a 0');
      }

      // Crear el movimiento
      const movimiento = queryRunner.manager.create(PosMovimientoInventario, {
        producto,
        usuario,
        sucursal: idSucursal ? { idSucursal } : undefined,
        tipoMovimiento: payload.tipoMovimiento || 'Entrada',
        cantidad: cantidadNumber,
        referencia: payload.referencia || 'Compra General',
        costoUnitario: payload.costoUnitario
      });

      await queryRunner.manager.save(movimiento);

      if (!idSucursal) throw new BadRequestException('Se requiere idSucursal para registrar entrada');
      
      let inv = await queryRunner.manager.findOne(PosInventario, {
        where: { producto: { idProducto: producto.idProducto }, sucursal: { idSucursal } }
      });
      if (!inv) {
        inv = queryRunner.manager.create(PosInventario, {
           producto: { idProducto: producto.idProducto },
           sucursal: { idSucursal },
           stockActual: 0,
           stockMinimo: 0
        });
      }

      // Calcular el nuevo costo promedio ponderado
      const doUpdate = payload.actualizarCosto !== false;
      if (doUpdate && payload.costoUnitario !== undefined && payload.costoUnitario !== null) {
        const stockPrevio = Number(inv.stockActual);
        const costoPrevio = Number(producto.precioCompra) || 0;
        const costoEntrante = Number(payload.costoUnitario);
        
        if (stockPrevio <= 0 || costoEntrante > costoPrevio) {
          producto.precioCompra = calcularCostoPromedioPonderado(
            stockPrevio, 
            costoPrevio, 
            cantidadNumber, 
            costoEntrante
          );
          
          if (producto.utilidad && producto.utilidad > 0) {
             const factor = 1 + (Number(producto.utilidad) / 100);
             producto.precioUnitario = Number((producto.precioCompra * factor).toFixed(2));
             producto.precioPublico = producto.precioUnitario;
          }
          await queryRunner.manager.save(producto);
        }
      }

      inv.stockActual = Number(inv.stockActual) + cantidadNumber;
      await queryRunner.manager.save(inv);

      await queryRunner.commitTransaction();
      return { success: true, movimiento };
    } catch (error) {
      await queryRunner.rollbackTransaction();
      throw error;
    } finally {
      await queryRunner.release();
    }
  }"""

ts = re.sub(pattern, new_code, ts)

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print("REPLACED registrarEntrada")
