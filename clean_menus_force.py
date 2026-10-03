import glob
import re

files = glob.glob("/home/hermes/hermes-intel-briefs/archive/*.html")
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the ID-based nav
    cleaned = re.sub(r'<div id="dynamic-nav".*?</div>', '', content, flags=re.DOTALL)
    
    # Remove the style-based navs (both the flex-end and the space-between ones)
    cleaned = re.sub(r'<div style="margin-bottom: 20px;[^>]*>.*?</div>', '', cleaned, flags=re.DOTALL)
    
    if cleaned != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)

print(f"Force-cleaned menus from {len(files)} archive files.")
