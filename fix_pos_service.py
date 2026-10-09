import re

with open('src/pos/pos.service.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace colorPrincipal with colorPrimario
content = content.replace('colorPrincipal', 'colorPrimario')

# Fix PosConfiguracion create/update
# Find config = this.configRepo.create({ ... })
content = re.sub(r'nombreEmpresa:[^\n]+,\n', '', content)
content = re.sub(r'rfcEmpresa:[^\n]+,\n', '', content)
content = re.sub(r'iva:\s*0,\n', '', content)
content = re.sub(r'imprimirLogo:\s*false,\n', '', content)

content = re.sub(r'if \(payload\.nombreEmpresa !== undefined\) config\.nombreEmpresa = payload\.nombreEmpresa;\n', '', content)
content = re.sub(r'if \(payload\.rfcEmpresa !== undefined\) config\.rfcEmpresa = payload\.rfcEmpresa;\n', '', content)
content = re.sub(r'if \(payload\.iva !== undefined\) config\.iva = payload\.iva;\n', '', content)
content = re.sub(r'if \(payload\.imprimirLogo !== undefined\) config\.imprimirLogo = payload\.imprimirLogo;\n', '', content)

with open('src/pos/pos.service.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print('pos.service.ts arreglado!')
