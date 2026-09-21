import glob
import os
import shutil

REPO_DIR = "/home/hermes/hermes-intel-briefs"
ARCHIVE_DIR = os.path.join(REPO_DIR, "archive")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Collect reports from both the home directory and the repo root
home_reports = glob.glob("/home/hermes/intel_briefing_*.html")
repo_reports = glob.glob(os.path.join(REPO_DIR, "intel_briefing_*.html"))

# Move everything into the archive folder to keep directories clean
for filepath in home_reports + repo_reports:
    filename = os.path.basename(filepath)
    target_path = os.path.join(ARCHIVE_DIR, filename)
    shutil.move(filepath, target_path)

# Sort the archived files newest to oldest
archived_files = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "intel_briefing_*.html")), reverse=True)

if not archived_files:
    print("No briefing files found.")
    exit(1)

latest_file = archived_files[0]
older_files = archived_files[1:]

# Build the dropdown menu linking to the archived files
nav_html = '''
<div style="margin-bottom: 20px; display: flex; justify-content: flex-end;">
  <select onchange="if(this.value) window.location.href=this.value" 
          style="background: var(--card); color: var(--link); border: 1px solid var(--line); 
                 padding: 8px 16px; border-radius: 8px; font-family: inherit; font-size: 13px; cursor: pointer; outline: none;">
    <option value="">📂 View Previous Briefings...</option>
'''

for f in older_files:
    filename = os.path.basename(f)
    date_str = filename.replace("intel_briefing_", "").replace(".html", "")
    # The value points to the archive folder relative to index.html
    nav_html += f'    <option value="archive/{filename}">{date_str}</option>\n'

nav_html += '  </select>\n</div>\n'

# Inject the dropdown into the newest report and save it as index.html
with open(latest_file, 'r', encoding='utf-8') as f:
    content = f.read()

if '<header class="hero">' in content:
    content = content.replace('<header class="hero">', nav_html + '<header class="hero">')

index_path = os.path.join(REPO_DIR, "index.html")
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Archived {len(archived_files)} reports. Updated index.html with {os.path.basename(latest_file)}.")
