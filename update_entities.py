import re

# Modificar PosEmpresa
with open('src/pos/entities/pos-empresa.entity.ts', 'r', encoding='utf-8') as f:
    content = f.read()

if 'colorSecundario' not in content:
    content = content.replace('colorPrincipal: string;', 
        "colorPrimario: string;\n\n  @Column({ length: 20, default: '#333333' })\n  colorSecundario: string;\n\n  @Column({ length: 20, nullable: true })\n  rfc: string;\n\n  @Column({ length: 255, nullable: true })\n  razonSocial: string;"
    )
    content = content.replace('colorPrincipal', 'colorPrimario')
    with open('src/pos/entities/pos-empresa.entity.ts', 'w', encoding='utf-8') as f:
        f.write(content)

# Limpiar PosConfiguracion
with open('src/pos/entities/pos-configuracion.entity.ts', 'r', encoding='utf-8') as f:
    content2 = f.read()

content2 = re.sub(r"@Column\(\{[^\}]*name: 'nombre_empresa'[^\}]*\}\)\s+nombreEmpresa: string;", "", content2)
content2 = re.sub(r"@Column\(\{[^\}]*name: 'rfc_empresa'[^\}]*\}\)\s+rfcEmpresa: string;", "", content2)
content2 = re.sub(r"@Column\(\{[^\}]*name: 'imprimir_logo'[^\}]*\}\)\s+imprimirLogo: boolean;", "", content2)
content2 = re.sub(r"@Column\('decimal', \{[^\}]*\}\)\s+iva: number;", "", content2)

with open('src/pos/entities/pos-configuracion.entity.ts', 'w', encoding='utf-8') as f:
    f.write(content2)

print('Entidades actualizadas')
