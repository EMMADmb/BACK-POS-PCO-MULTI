import re

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'async getProductos\(idSucursal\?: number, page: number = 1, limit: number = 20, search\?: string\) \{\s*let where: any = idSucursal \? \{ sucursal: \{ idSucursal \} \} : \{\};',
    'async getProductos(idSucursal?: number, idEmpresa?: number, page: number = 1, limit: number = 20, search?: string) {\n    let where: any = {};\n    if (idSucursal) where = { sucursal: { idSucursal } };\n    else if (idEmpresa) where = { sucursal: { empresa: { idEmpresa } } };',
    content
)

content = re.sub(
    r'async getClientes\(idSucursal\?: number, page: number = 1, limit: number = 20, search\?: string\) \{\s*let where: any = idSucursal \? \{ sucursal: \{ idSucursal \} \} : \{\};',
    'async getClientes(idSucursal?: number, idEmpresa?: number, page: number = 1, limit: number = 20, search?: string) {\n    let where: any = {};\n    if (idSucursal) where = { sucursal: { idSucursal } };\n    else if (idEmpresa) where = { sucursal: { empresa: { idEmpresa } } };',
    content
)

content = re.sub(
    r'async getVentas\(idSucursal\?: number, folio\?: string, limit: number = 100, offset: number = 0\) \{\s*const where: any = idSucursal \? \{ usuario: \{ sucursal: \{ idSucursal \} \} \} : \{\};',
    'async getVentas(idSucursal?: number, idEmpresa?: number, folio?: string, limit: number = 100, offset: number = 0) {\n    const where: any = {};\n    if (idSucursal) where = { usuario: { sucursal: { idSucursal } } };\n    else if (idEmpresa) where = { usuario: { sucursal: { empresa: { idEmpresa } } } };',
    content
)

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(content)
    print("Updated pos.service.ts")
