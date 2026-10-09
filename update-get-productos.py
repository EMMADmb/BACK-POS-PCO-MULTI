import os
import re

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

# ADD IMPORT
if 'PosInventario' not in ts:
    ts = ts.replace("import { PosProducto } from './entities/pos-producto.entity';", "import { PosProducto } from './entities/pos-producto.entity';\nimport { PosInventario } from './entities/pos-inventario.entity';")

# Replace getProductos using regex
pattern = r"async getProductos\(idSucursal\?: number, idEmpresa\?: number, page: number = 1, limit: number = 20, search\?: string\) \{.*?return \{ data, total, page, limit, totalPages: Math\.ceil\(total / limit\) \};\n  \}"

new_get_prod = """async getProductos(idSucursal?: number, idEmpresa?: number, page: number = 1, limit: number = 20, search?: string) {
    let empresaId = idEmpresa;
    if (!empresaId && idSucursal) {
      const suc = await this.sucursalRepo.findOne({ where: { idSucursal }, relations: { empresa: true } });
      if (suc?.empresa) empresaId = suc.empresa.idEmpresa;
    }

    const qb = this.productoRepo.createQueryBuilder('p')
      .leftJoinAndSelect('p.categoria', 'categoria')
      .leftJoinAndSelect('p.empresa', 'empresa')
      .leftJoinAndSelect('p.codigosAdicionales', 'codigosAdicionales');
      
    if (idSucursal) {
      qb.leftJoinAndSelect('p.inventarios', 'inventarios', 'inventarios.id_sucursal = :idSuc', { idSuc: idSucursal });
    } else {
      qb.leftJoinAndSelect('p.inventarios', 'inventarios');
    }

    if (empresaId) {
      qb.andWhere('p.id_empresa = :empresaId', { empresaId });
    }

    if (search) {
      qb.andWhere(new Brackets(qb => {
        qb.where('p.nombre LIKE :search', { search: `%${search}%` })
          .orWhere('p.codigo_barras LIKE :search', { search: `%${search}%` })
          .orWhere('p.clave_prod_serv LIKE :search', { search: `%${search}%` })
          .orWhere('p.aliasBusqueda LIKE :search', { search: `%${search}%` });
        
        if (!isNaN(Number(search))) {
          qb.orWhere('p.id_producto = :idNum', { idNum: Number(search) });
        }
      }));
    }

    qb.orderBy('p.nombre', 'ASC')
      .skip((page - 1) * limit)
      .take(limit);

    const [data, total] = await qb.getManyAndCount();

    const mappedData = data.map(prod => {
      let stockActual = 0;
      let stockMinimo = 0;
      
      if (prod.inventarios && prod.inventarios.length > 0) {
        stockActual = Number(prod.inventarios[0].stockActual || 0);
        stockMinimo = Number(prod.inventarios[0].stockMinimo || 0);
      }

      const mapped = {
        ...prod,
        stockActual,
        stockMinimo,
      };
      return mapped;
    });

    return { data: mappedData, total, page, limit, totalPages: Math.ceil(total / limit) };
  }"""

ts = re.sub(pattern, new_get_prod, ts, flags=re.DOTALL)

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
