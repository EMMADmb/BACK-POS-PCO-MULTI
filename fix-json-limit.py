import os

with open('src/main.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

ts = ts.replace("  import * as express from 'express';", "")
ts = "import * as express from 'express';\n" + ts

with open('src/main.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print('Fixed import')
