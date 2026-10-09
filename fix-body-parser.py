import os

with open('src/main.ts', 'r', encoding='utf-8') as f:
    ts = f.read()

old_create = "const app = await NestFactory.create<NestExpressApplication>(AppModule);"
new_create = "const app = await NestFactory.create<NestExpressApplication>(AppModule, { bodyParser: false });"

ts = ts.replace(old_create, new_create)

with open('src/main.ts', 'w', encoding='utf-8') as f:
    f.write(ts)
print("Fixed body parser collision in NestJS")
