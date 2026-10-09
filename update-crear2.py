import os

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

# I will find the start and end of crearProducto
start_idx = ts.find("async crearProducto(data: {")
if start_idx == -1:
    print("NO SE ENCONTRÓ crearProducto")
    exit(1)

end_str = "return this.productoRepo.save(producto);\n  }"
end_idx = ts.find(end_str, start_idx)

if end_idx == -1:
    print("NO SE ENCONTRÓ EL FINAL DE crearProducto")
    exit(1)

end_idx += len(end_str)

old_code = ts[start_idx:end_idx]

new_code = """async crearProducto(data: any) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();
    try {
      let idEmpresa = data.idEmpresa;
      if (!idEmpresa && data.idSucursal) {
        const suc = await queryRunner.manager.findOne(PosSucursal, { where: { idSucursal: data.idSucursal }, relations: { empresa: true } });
        if (suc?.empresa) idEmpresa = suc.empresa.idEmpresa;
      }

      if (idEmpresa) {
        if (data.nombre) {
          const dupNombre = await queryRunner.manager.findOne(PosProducto, {
            where: { empresa: { idEmpresa }, nombre: data.nombre.trim().toUpperCase() }
          });
          if (dupNombre) throw new BadRequestException(`Ya existe otro producto con el nombre "${data.nombre.trim().toUpperCase()}" en esta empresa.`);
        }
        if (data.codigoBarras) {
          const dupCodigo = await queryRunner.manager.findOne(PosProducto, {
            where: { empresa: { idEmpresa }, codigoBarras: data.codigoBarras }
          });
          if (dupCodigo) throw new BadRequestException(`Ya existe otro producto con el código de barras "${data.codigoBarras}" en esta empresa.`);
        }
      }

      const payload: any = {
        nombre: data.nombre.trim().toUpperCase(),
        codigoBarras: data.codigoBarras || null,
        precioUnitario: data.precioUnitario || 0,
        precioPublico: data.precioPublico || data.precioUnitario || 0,
        precioCompra: data.precioCompra || 0,
        utilidad: data.utilidad || 18.0,
        aplicaDescuento: data.aplicaDescuento || false,
        tipoDescuento: data.tipoDescuento || 'porcentaje',
        aplicaIva: data.aplicaIva || false,
        precioVenta: data.precioVenta || 0,
        precioMayoreo: data.precioMayoreo || null,
        descuento: data.descuento || 0,
        minimoMayoreo: data.minimoMayoreo || 0,
        tipoArticulo: data.tipoArticulo || 'Terminado',
        unidadMedida: data.unidadMedida || 'Pza',
        iva: data.iva || 0,
        imagenUrl: data.imagenUrl || null,
        claveProdServ: data.claveProdServ || '01010101',
        claveUnidad: data.claveUnidad || 'H87',
        activo: true,
        empresa: idEmpresa ? { idEmpresa } : undefined,
        categoria: data.idCategoria ? { idCategoria: data.idCategoria } : undefined,
      };

      const producto = queryRunner.manager.create(PosProducto, payload);
      const savedProducto = await queryRunner.manager.save(producto);

      let inv;
      if (data.idSucursal) {
        inv = queryRunner.manager.create(PosInventario, {
          producto: { idProducto: savedProducto.idProducto },
          sucursal: { idSucursal: data.idSucursal },
          stockActual: data.stockActual || 0,
          stockMinimo: data.stockMinimo || 0,
        });
        await queryRunner.manager.save(inv);
      }
      
      await queryRunner.commitTransaction();
      
      return { ...savedProducto, stockActual: inv?.stockActual || 0, stockMinimo: inv?.stockMinimo || 0 };
    } catch (e) {
      await queryRunner.rollbackTransaction();
      throw e;
    } finally {
      await queryRunner.release();
    }
  }"""

ts = ts[:start_idx] + new_code + ts[end_idx:]

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print("REPLACED crearProducto")
