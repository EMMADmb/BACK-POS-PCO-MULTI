import os

with open('src/pos/pos.controller.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

old_stats = """  @Get('dashboard/stats')
  getDashboardStats(@Headers("x-sucursal-id") idSucursal: string, @Headers("x-empresa-id") idEmpresa: string) {
    return this.posService.getDashboardStats(idSucursal ? Number(idSucursal) : undefined, idEmpresa ? Number(idEmpresa) : undefined);
  }"""

new_stats = """  @Get('dashboard/stats')
  async getDashboardStats(@Headers("x-sucursal-id") idSucursal: string, @Headers("x-empresa-id") idEmpresa: string) {
    try {
      return await this.posService.getDashboardStats(idSucursal ? Number(idSucursal) : undefined, idEmpresa ? Number(idEmpresa) : undefined);
    } catch (e: any) {
      require('fs').writeFileSync('dashboard-error.log', e.stack || e.message);
      throw e;
    }
  }"""

ts = ts.replace(old_stats, new_stats)

with open('src/pos/pos.controller.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print('Updated getDashboardStats to log errors')
