$content = Get-Content -Raw 'src/pos/pos.service.ts'

$content = $content -replace '    } else if \(idEmpresa\) \{(\r?\n)\s*const sucursales = await this\.sucursalRepo\.find\(\{ where: \{ empresa: \{ idEmpresa \} \} \}\);(\r?\n)\s*sucursalesIds = sucursales\.map\(s => s\.idSucursal\);(\r?\n)\s*\}', '    } else if (idEmpresa) {      const sucursales = await this.sucursalRepo.find({ where: { empresa: { idEmpresa } } });      sucursalesIds = sucursales.map(s => s.idSucursal);    } else {      const sucursales = await this.sucursalRepo.find();      sucursalesIds = sucursales.map(s => s.idSucursal);    }'

Set-Content 'src/pos/pos.service.ts' -Value $content
