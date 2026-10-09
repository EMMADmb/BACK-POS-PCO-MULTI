import glob, re

for f in glob.glob('src/**/*.ts', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = re.sub(r",\s*charset:\s*'[^']+'", '', content)
    new_content = re.sub(r",\s*collation:\s*'[^']+'", '', new_content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Fixed {f}')
