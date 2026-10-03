import glob

files = glob.glob("/home/hermes/hermes-intel-briefs/archive/*.html")
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="wrap">' in content and '<header class="hero">' in content:
        # Split the file exactly at the wrap and the hero header
        before_wrap = content.split('<div class="wrap">')[0]
        after_header = content.split('<header class="hero">', 1)[1]
        
        # Reconstruct the file with absolutely nothing in between
        clean_content = before_wrap + '<div class="wrap">\n\n<header class="hero">' + after_header
        
        if clean_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(clean_content)

print(f"Surgically cleaned all injected HTML in {len(files)} files.")
