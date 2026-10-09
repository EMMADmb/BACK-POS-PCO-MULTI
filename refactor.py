import sys
import re

file_path = 'src/pos/pos.service.ts'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace actualizarProductoCompleto
match = re.search(r'async actualizarProductoCompleto\(.*?\)\s*\{', content, re.DOTALL)
if match:
    start_body = match.end() - 1
    braces = 0
    started = False
    for i in range(start_body, len(content)):
        if content[i] == '{': braces += 1; started = True
        elif content[i] == '}': braces -= 1
        if started and braces == 0:
            act_start = match.start()
            act_end = i + 1
            new_act = """async actualizarProductoCompleto(id: number, data: any, idSucursalUsuario?: number, rol?: string) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();
    try {
      const productoExistente = await queryRunner.manager.findOne(PosProducto, { where: { idProducto: id }, relations: { empresa: true } });
      if (!productoExistente) throw new BadRequestException('Producto no encontrado');

      const idEmpresa = productoExistente.empresa?.idEmpresa;

      if (idEmpresa) {
        if (data.nombre && data.nombre.trim().toUpperCase() !== productoExistente.nombre) {
          const dupNombre = await queryRunner.manager.findOne(PosProducto, {
            where: { empresa: { idEmpresa }, nombre: data.nombre.trim().toUpperCase(), idProducto: Not(id) }
          });
          if (dupNombre) throw new BadRequestException(`Ya existe otro producto con el nombre "${data.nombre.trim().toUpperCase()}" en esta empresa.`);
        }
        if (data.codigoBarras && data.codigoBarras !== productoExistente.codigoBarras) {
          const dupCodigo = await queryRunner.manager.findOne(PosProducto, {
            where: { empresa: { idEmpresa }, codigoBarras: data.codigoBarras, idProducto: Not(id) }
          });
          if (dupCodigo) throw new BadRequestException(`Ya existe otro producto con el código de barras "${data.codigoBarras}" en esta empresa.`);
        }
      }

      const updates: any = {};
      const fields = ['nombre', 'codigoBarras', 'tipoArticulo', 'unidadMedida', 'precioUnitario', 'precioPublico', 'precioCompra', 'utilidad', 'aplicaDescuento', 'tipoDescuento', 'aplicaIva', 'precioVenta', 'precioMayoreo', 'descuento', 'minimoMayoreo', 'iva', 'imagenUrl', 'claveProdServ', 'claveUnidad'];
      for (const field of fields) {
        if (data[field] !== undefined) updates[field] = data[field];
      }
      if (data.idCategoria !== undefined) updates.categoria = data.idCategoria ? { idCategoria: data.idCategoria } : null;
      if (data.aplicaDescuento === false) updates.descuento = 0;
      if (data.aplicaIva === false) updates.iva = 0;

      if (Object.keys(updates).length > 0) {
        await queryRunner.manager.update(PosProducto, id, updates);
      }

      if (idSucursalUsuario) {
        let inv = await queryRunner.manager.findOne(PosInventario, {
          where: { producto: { idProducto: id }, sucursal: { idSucursal: idSucursalUsuario } }
        });
        
        if (!inv) {
          inv = queryRunner.manager.create(PosInventario, {
            producto: { idProducto: id },
            sucursal: { idSucursal: idSucursalUsuario },
            stockActual: 0,
            stockMinimo: data.stockMinimo !== undefined ? data.stockMinimo : 0
          });
          await queryRunner.manager.save(PosInventario, inv);
        } else {
          let invUpdates = false;
          if (data.sumarStock !== undefined && data.sumarStock !== 0) {
            inv.stockActual = Number(inv.stockActual) + data.sumarStock;
            invUpdates = true;
          }
          if (data.stockMinimo !== undefined) {
            inv.stockMinimo = data.stockMinimo;
            invUpdates = true;
          }
          if (invUpdates) {
             await queryRunner.manager.save(PosInventario, inv);
          }
        }
      }

      await queryRunner.commitTransaction();
      return this.productoRepo.findOne({ where: { idProducto: id }, relations: { categoria: true, codigosAdicionales: true } });
    } catch (e) {
      await queryRunner.rollbackTransaction();
      throw e;
    } finally {
      await queryRunner.release();
    }
  }"""
            content = content[:act_start] + new_act + content[act_end:]
            break

match_ajustar = re.search(r'async ajustarStock\(.*?\)\s*\{', content)
if match_ajustar:
    start_body = match_ajustar.end() - 1
    braces = 0
    started = False
    for i in range(start_body, len(content)):
        if content[i] == '{': braces += 1; started = True
        elif content[i] == '}': braces -= 1
        if started and braces == 0:
            ajust_start = match_ajustar.start()
            ajust_end = i + 1
            new_ajustar = """async ajustarStock(idProducto: number, stockReal: number, motivo: string, idUsuario: number, idSucursal?: number) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();
    try {
      if (stockReal < 0) throw new BadRequestException('El stock no puede ser negativo');

      const producto = await queryRunner.manager.findOne(PosProducto, { where: { idProducto } });
      if (!producto) throw new BadRequestException('Producto no encontrado');
      
      if (!idSucursal) throw new BadRequestException('Sucursal es requerida para ajustar stock');

      let inv = await queryRunner.manager.findOne(PosInventario, {
        where: { producto: { idProducto }, sucursal: { idSucursal } }
      });
      if (!inv) {
         inv = queryRunner.manager.create(PosInventario, {
           producto: { idProducto },
           sucursal: { idSucursal },
           stockActual: 0,
           stockMinimo: 0
         });
         inv = await queryRunner.manager.save(PosInventario, inv);
      }

      const diferencia = stockReal - Number(inv.stockActual);
      const tipoMovimiento = diferencia >= 0 ? 'Entrada' : 'Salida';

      inv.stockActual = stockReal;
      await queryRunner.manager.save(PosInventario, inv);

      const mov = queryRunner.manager.create(PosMovimientoInventario, {
        producto: { idProducto },
        usuario: { idUsuario },
        sucursal: { idSucursal },
        tipoMovimiento: `Ajuste (${tipoMovimiento})`,
        cantidad: Math.abs(diferencia),
        referencia: motivo || 'Ajuste Manual de Inventario',
      });
      await queryRunner.manager.save(PosMovimientoInventario, mov);
      await queryRunner.commitTransaction();

      return { success: true, stockAnterior: Number(inv.stockActual) - diferencia, stockNuevo: stockReal, diferencia };
    } catch (error) {
      await queryRunner.rollbackTransaction();
      throw error;
    } finally {
      await queryRunner.release();
    }
  }"""
            content = content[:ajust_start] + new_ajustar + content[ajust_end:]
            break

match_merma = re.search(r'async registrarMerma\(.*?\)\s*\{', content)
if match_merma:
    start_body = match_merma.end() - 1
    braces = 0
    started = False
    for i in range(start_body, len(content)):
        if content[i] == '{': braces += 1; started = True
        elif content[i] == '}': braces -= 1
        if started and braces == 0:
            merma_start = match_merma.start()
            merma_end = i + 1
            new_merma = """async registrarMerma(idProducto: number, cantidad: number, motivo: string, idUsuario: number, idSucursal?: number) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();
    try {
      const producto = await queryRunner.manager.findOne(PosProducto, { where: { idProducto } });
      if (!producto) throw new BadRequestException('Producto no encontrado');
      
      if (!idSucursal) throw new BadRequestException('Sucursal es requerida para registrar merma');

      let inv = await queryRunner.manager.findOne(PosInventario, {
        where: { producto: { idProducto }, sucursal: { idSucursal } }
      });
      if (!inv) {
         inv = queryRunner.manager.create(PosInventario, {
           producto: { idProducto },
           sucursal: { idSucursal },
           stockActual: 0,
           stockMinimo: 0
         });
         inv = await queryRunner.manager.save(PosInventario, inv);
      }

      if (Number(inv.stockActual) < cantidad) {
        throw new BadRequestException('La cantidad de merma es mayor al stock disponible');
      }

      inv.stockActual = Number(inv.stockActual) - cantidad;
      await queryRunner.manager.save(PosInventario, inv);

      const mov = queryRunner.manager.create(PosMovimientoInventario, {
        producto: { idProducto },
        usuario: { idUsuario },
        sucursal: { idSucursal },
        tipoMovimiento: 'Merma',
        cantidad: cantidad,
        costoUnitario: producto.precioUnitario,
        referencia: `Merma - ${motivo}`,
      });
      await queryRunner.manager.save(PosMovimientoInventario, mov);
      await queryRunner.commitTransaction();

      return { success: true, stockAnterior: Number(inv.stockActual) + cantidad, stockNuevo: Number(inv.stockActual), costoPerdido: cantidad * Number(producto.precioUnitario || 0) };
    } catch (error) {
      await queryRunner.rollbackTransaction();
      throw error;
    } finally {
      await queryRunner.release();
    }
  }"""
            content = content[:merma_start] + new_merma + content[merma_end:]
            break

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
