import re

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Find getDashboardStats block
start = content.find('async getDashboardStats(idSucursal: number) {')
end = content.find('async getEmpresas', start)

if start != -1 and end != -1:
    method_content = content[start:end]
    
    # Replace signature
    method_content = method_content.replace(
        'async getDashboardStats(idSucursal: number) {',
        'async getDashboardStats(idSucursal?: number, idEmpresa?: number) {\n    let sucursalesIds: number[] = [];\n    if (idSucursal) {\n      sucursalesIds.push(idSucursal);\n    } else if (idEmpresa) {\n      const sucursales = await this.sucursalRepo.find({ where: { empresa: { idEmpresa } } });\n      sucursalesIds = sucursales.map(s => s.idSucursal);\n    }\n    if (sucursalesIds.length === 0) return null;'
    )
    
    # Replace early return
    method_content = method_content.replace('    if (!idSucursal) return null;\n', '')
    
    # Replace id_sucursal = :idSucursal inside QueryBuilders
    method_content = method_content.replace('u.id_sucursal = :idSucursal', 'u.id_sucursal IN (:...sucursalesIds)')
    method_content = method_content.replace('{ idSucursal }', '{ sucursalesIds }')
    method_content = method_content.replace('sucursal: { idSucursal: idSucursal }', 'sucursal: { idSucursal: In(sucursalesIds) }')
    method_content = method_content.replace('id_sucursal = :idSucursal', 'id_sucursal IN (:...sucursalesIds)')
    
    # Reassemble
    final_content = content[:start] + method_content + content[end:]
    
    # Add In to imports if needed
    if 'In' not in content[:1000]:
        final_content = final_content.replace('LessThanOrEqual, Between', 'LessThanOrEqual, Between, In')
        
    with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
        f.write(final_content)
        print("Updated pos.service.ts")
