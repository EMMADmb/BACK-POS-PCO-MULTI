import glob, re

for f in glob.glob('src/**/*.ts', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = re.sub(r"type:\s*'tinyint'", "type: 'smallint'", content)
    new_content = re.sub(r"type:\s*'longtext'", "type: 'text'", new_content)
    new_content = re.sub(r"type:\s*'datetime'", "type: 'timestamp'", new_content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Fixed {f}')

print('Done!')
