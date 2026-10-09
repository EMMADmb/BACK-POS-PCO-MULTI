$content = Get-Content -Raw 'src/pos/pos.controller.ts'

# getProductos
$content = $content -replace 'getProductos\((\r?\n)\s*@Headers\("x-sucursal-id"\) idSucursal: string,', 'getProductos(      @Headers("x-sucursal-id") idSucursal: string,      @Headers("x-empresa-id") idEmpresa: string,'
$content = $content -replace 'return this\.posService\.getProductos\((\r?\n)\s*Number\(idSucursal\),', 'return this.posService.getProductos(        idSucursal ? Number(idSucursal) : undefined,        idEmpresa ? Number(idEmpresa) : undefined,'

# getClientes
$content = $content -replace 'getClientes\((\r?\n)\s*@Headers\("x-sucursal-id"\) idSucursal: string,', 'getClientes(      @Headers("x-sucursal-id") idSucursal: string,      @Headers("x-empresa-id") idEmpresa: string,'
$content = $content -replace 'return this\.posService\.getClientes\((\r?\n)\s*Number\(idSucursal\),', 'return this.posService.getClientes(        idSucursal ? Number(idSucursal) : undefined,        idEmpresa ? Number(idEmpresa) : undefined,'

# getVentas
$content = $content -replace 'getVentas\((\r?\n)\s*@Headers\("x-sucursal-id"\) idSucursal: string,', 'getVentas(      @Headers("x-sucursal-id") idSucursal: string,      @Headers("x-empresa-id") idEmpresa: string,'
$content = $content -replace 'return this\.posService\.getVentas\(Number\(idSucursal\), folio, Number\(limit\) \|\| 100, Number\(offset\) \|\| 0\);', 'return this.posService.getVentas(idSucursal ? Number(idSucursal) : undefined, idEmpresa ? Number(idEmpresa) : undefined, folio, Number(limit) || 100, Number(offset) || 0);'

Set-Content 'src/pos/pos.controller.ts' -Value $content
