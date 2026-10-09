import os

with open('src/pos/pos.controller.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

old_crear = """  @Post('productos')
  crearProducto(@Headers("x-sucursal-id") idSucursal: string, @Body() body: any) {
    body.idSucursal = Number(idSucursal);
    return this.posService.crearProducto(body);
  }"""

new_crear = """  @Post('productos')
  crearProducto(@Headers("x-sucursal-id") idSucursal: string, @Headers("x-empresa-id") idEmpresa: string, @Body() body: any) {
    if (idSucursal) body.idSucursal = Number(idSucursal);
    if (idEmpresa) body.idEmpresa = Number(idEmpresa);
    return this.posService.crearProducto(body);
  }"""

ts = ts.replace(old_crear, new_crear)

with open('src/pos/pos.controller.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
