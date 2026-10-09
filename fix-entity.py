import os

with open('src/pos/entities/pos-empresa.entity.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

ts = ts.replace("@Column({ length: 500, nullable: true })\n  logoUrl: string;", "@Column({ type: 'text', nullable: true })\n  logoUrl: string;")

with open('src/pos/entities/pos-empresa.entity.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print('Changed logoUrl to text')
