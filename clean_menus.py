import glob
import re

files = glob.glob("/home/hermes/hermes-intel-briefs/archive/*.html")
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Forcefully strip anything injected between the main wrap and the hero header
    cleaned = re.sub(r'(<div class="wrap">\s*).*?(<header class="hero">)', r'\1\2', content, flags=re.DOTALL)
    
    if cleaned != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)

print(f"Cleaned menus from {len(files)} archive files.")
