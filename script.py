import sys
import re

file_path = '../src/pos/pos.service.ts'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_actualizar = """  async actualizarProductoCompleto(id: number, data: {
      nombre?: string;
      codigoBarras?: string;
      idCategoria?: number | null;
      precioUnitario?: number;
    precioPublico?: number;
    precioCompra?: number;
    utilidad?: number;
    aplicaDescuento?: boolean;
    tipoDescuento?: string;
    aplicaIva?: boolean;
    precioVenta?: number;
    precioMayoreo?: number;
    descuento?: number;
    minimoMayoreo?: number;
    iva?: number;
    stockMinimo?: number;
    imagenUrl?: string;
    claveProdServ?: string;
    claveUnidad?: string;
    sumarStock?: number;
    tipoArticulo?: string;
    unidadMedida?: string;
  }, idSucursalUsuario?: number, rol?: string) {
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
      if (data.nombre !== undefined) updates.nombre = data.nombre;
      if (data.codigoBarras !== undefined) updates.codigoBarras = data.codigoBarras;
      if (data.idCategoria !== undefined) updates.categoria = data.idCategoria ? { idCategoria: data.idCategoria } : null;
      if (data.tipoArticulo !== undefined) updates.tipoArticulo = data.tipoArticulo;
      if (data.unidadMedida !== undefined) updates.unidadMedida = data.unidadMedida;
      if (data.precioUnitario !== undefined) updates.precioUnitario = data.precioUnitario;
      if (data.precioPublico !== undefined) updates.precioPublico = data.precioPublico;
      if (data.precioCompra !== undefined) updates.precioCompra = data.precioCompra;
      if (data.utilidad !== undefined) updates.utilidad = data.utilidad;
      if (data.aplicaDescuento !== undefined) {
        updates.aplicaDescuento = data.aplicaDescuento;
        if (!data.aplicaDescuento) {
          updates.descuento = 0;
        }
      }
      if (data.tipoDescuento !== undefined) updates.tipoDescuento = data.tipoDescuento;
      if (data.aplicaIva !== undefined) {
        updates.aplicaIva = data.aplicaIva;
        if (!data.aplicaIva) {
          updates.iva = 0;
        }
      }
      if (data.precioVenta !== undefined) updates.precioVenta = data.precioVenta;
      if (data.precioMayoreo !== undefined) updates.precioMayoreo = data.precioMayoreo;
      if (data.descuento !== undefined && updates.descuento === undefined) updates.descuento = data.descuento;
      if (data.minimoMayoreo !== undefined) updates.minimoMayoreo = data.minimoMayoreo;
      if (data.iva !== undefined && updates.iva === undefined) updates.iva = data.iva;
      if (data.imagenUrl !== undefined) updates.imagenUrl = data.imagenUrl;
      if (data.claveProdServ !== undefined) updates.claveProdServ = data.claveProdServ;
      if (data.claveUnidad !== undefined) updates.claveUnidad = data.claveUnidad;

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
          let invUpdates = False;
          if (data.sumarStock !== undefined && data.sumarStock !== 0) {
            inv.stockActual = Number(inv.stockActual) + data.sumarStock;
            invUpdates = True;
          }
          if (data.stockMinimo !== undefined) {
            inv.stockMinimo = data.stockMinimo;
            invUpdates = True;
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
  }\n"""

new_ajustar = """  async ajustarStock(idProducto: number, stockReal: number, motivo: string, idUsuario: number, idSucursal?: number) {
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
  }\n"""

new_merma = """  async registrarMerma(idProducto: number, cantidad: number, motivo: string, idUsuario: number, idSucursal?: number) {
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
  }\n"""

lines[307:403] = [new_actualizar]
def get_block(start_str, cur_lines):
    start = -1
    for i, line in enumerate(cur_lines):
        if start_str in line:
            start = i
            break
    if start == -1: return -1, -1
    braces = 0
    started = False
    for i in range(start, len(cur_lines)):
        braces += cur_lines[i].count('{')
        braces -= cur_lines[i].count('}')
        if '{' in cur_lines[i]: started = True
        if started and braces == 0: return start, i + 1

s, e = get_block('async ajustarStock(', lines)
lines[s:e] = [new_ajustar]

s, e = get_block('async registrarMerma(', lines)
lines[s:e] = [new_merma]

new_content = ''.join(lines).replace('False;', 'false;').replace('True;', 'true;')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('File updated successfully.')
