$content = Get-Content -Raw 'src/pos/pos.service.ts'

$content = $content -replace 'async getDashboardStats\(idSucursal: number\) \{(\r?\n)\s*if \(!idSucursal\) return null;', 'async getDashboardStats(idSucursal?: number, idEmpresa?: number) {    let sucursalesIds = [];    if (idSucursal) {        sucursalesIds.push(idSucursal);    } else if (idEmpresa) {        const sucursales = await this.sucursalRepo.find({ where: { empresa: { idEmpresa } }});        sucursalesIds = sucursales.map(s => s.idSucursal);    }    if (sucursalesIds.length === 0) return null;'

$content = $content -replace 'u\.id_sucursal = :idSucursal', 'u.id_sucursal IN (:...sucursalesIds)'
$content = $content -replace '\{ idSucursal \}', '{ sucursalesIds }'
$content = $content -replace 'sucursal: \{ idSucursal: idSucursal \}', 'sucursal: { idSucursal: In(sucursalesIds) }'

Set-Content 'src/pos/pos.service.ts' -Value $content
