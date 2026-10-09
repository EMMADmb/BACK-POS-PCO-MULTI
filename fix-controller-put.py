import os

with open('src/pos/pos.controller.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

old_actualizar = """  @Put('empresas/:id')
  actualizarEmpresa(@Param("id") id: string, @Body() payload: EmpresaDto) {
    return this.posService.actualizarEmpresa(Number(id), payload);
  }"""

new_actualizar = """  @Put('empresas/:id')
  async actualizarEmpresa(@Param("id") id: string, @Body() payload: EmpresaDto) {
    try {
        return await this.posService.actualizarEmpresa(Number(id), payload);
    } catch(e: any) {
        require('fs').writeFileSync('empresa-error.log', e.stack || e.message);
        throw e;
    }
  }"""

ts = ts.replace(old_actualizar, new_actualizar)

with open('src/pos/pos.controller.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print('Added error logging to actualizarEmpresa')
