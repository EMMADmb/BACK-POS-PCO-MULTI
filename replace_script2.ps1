$content = Get-Content -Raw 'src/pos/pos.service.ts'

# Fix let where: any = idSucursal ? { sucursal: { idSucursal } } : {};
$content = $content -replace 'let where: any = idSucursal \? \{ sucursal: \{ idSucursal \} \} : \{\};', 'let where: any = {}; if (idSucursal) { where.sucursal = { idSucursal }; } else if (typeof idEmpresa !== "undefined") { where.sucursal = { empresa: { idEmpresa } }; }'

Set-Content 'src/pos/pos.service.ts' -Value $content
