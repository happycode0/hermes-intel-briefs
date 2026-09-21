import glob
import os
import shutil
import re

REPO_DIR = "/home/hermes/hermes-intel-briefs"
ARCHIVE_DIR = os.path.join(REPO_DIR, "archive")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 1. Move new reports to archive
home_reports = glob.glob("/home/hermes/intel_briefing_*.html")
repo_reports = glob.glob(os.path.join(REPO_DIR, "intel_briefing_*.html"))

for filepath in home_reports + repo_reports:
    filename = os.path.basename(filepath)
    target_path = os.path.join(ARCHIVE_DIR, filename)
    shutil.move(filepath, target_path)

# 2. Get sorted archive files
archived_files = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "intel_briefing_*.html")), reverse=True)

if not archived_files:
    print("No briefing files found.")
    exit(1)

latest_file = archived_files[0]

# 3. Dynamic Navigation Generator
def generate_nav(is_index=True):
    # Adjust paths based on folder depth
    home_url = "index.html" if is_index else "../index.html"
    archive_prefix = "archive/" if is_index else ""
    
    nav = f'''
    <div id="dynamic-nav" style="margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
      <a href="{home_url}" style="background: var(--card); color: var(--neon); text-decoration: none; border: 1px solid var(--line); padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: bold; box-shadow: 0 0 10px rgba(0,242,254,0.1); transition: transform 0.15s ease;">
        🏠 Home (Latest)
      </a>
      <select onchange="if(this.value) window.location.href=this.value" 
              style="background: var(--card); color: var(--link); border: 1px solid var(--line); padding: 8px 16px; border-radius: 8px; font-family: inherit; font-size: 13px; cursor: pointer; outline: none;">
        <option value="">📂 View History...</option>
    '''
    
    # Include all files in the dropdown so you can jump between any dates
    for f in archived_files:
        filename = os.path.basename(f)
        date_str = filename.replace("intel_briefing_", "").replace(".html", "")
        path = archive_prefix + filename if is_index else filename
        nav += f'        <option value="{path}">{date_str}</option>\n'
        
    nav += '      </select>\n    </div>\n'
    return nav

def inject_nav(filepath, nav_html, output_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Safely remove any previously injected nav to avoid duplicates
    content = re.sub(r'<div id="dynamic-nav">.*?</div>\s*(<header class="hero">)', r'\1', content, flags=re.DOTALL)
    
    # Inject the new nav directly above the hero header
    if '<header class="hero">' in content:
        content = content.replace('<header class="hero">', nav_html + '<header class="hero">')
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 4. Inject navigation into EVERY file in the archive
print("Updating archive files...")
nav_for_archive = generate_nav(is_index=False)
for f in archived_files:
    inject_nav(f, nav_for_archive, f)

# 5. Inject navigation into the root index.html
print("Updating index.html...")
nav_for_index = generate_nav(is_index=True)
inject_nav(latest_file, nav_for_index, os.path.join(REPO_DIR, "index.html"))

print(f"Success! Processed {len(archived_files)} reports. Index and archive navigation updated.")
