import glob
import os
import shutil
import re

REPO_DIR = "/home/hermes/hermes-intel-briefs"
ARCHIVE_DIR = os.path.join(REPO_DIR, "archive")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 1. Move any stray reports into the archive
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

# 3. Clean up the old injected menus from the archived files
for filepath in archived_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the old dynamic navs and the first attempt's flexbox nav
    cleaned = re.sub(r'<div id="dynamic-nav">.*?</div>\s*(<header class="hero">)', r'\1', content, flags=re.DOTALL)
    cleaned = re.sub(r'<div style="margin-bottom: 20px; display: flex; justify-content: flex-end;">\s*<select.*?</select>\s*</div>\s*(<header class="hero">)', r'\1', cleaned, flags=re.DOTALL)
    
    if cleaned != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)

latest_file_rel = f"archive/{os.path.basename(archived_files[0])}"

# 4. Generate the options for the dropdown
options_html = ""
for f in archived_files:
    filename = os.path.basename(f)
    date_str = filename.replace("intel_briefing_", "").replace(".html", "")
    options_html += f'      <option value="archive/{filename}">{date_str}</option>\n'

# 5. Build the standalone wrapper index.html with an iframe
index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GitHub Intelligence Briefings</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root {{
    --bg: #0f172a; --card: #1e293b; --line: #334155; --link: #38bdf8; --neon: #00f2fe;
  }}
  body, html {{
    margin: 0; padding: 0; height: 100vh; overflow: hidden; 
    background: var(--bg); font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }}
  .top-bar {{
    height: 60px; background: var(--card); border-bottom: 1px solid var(--line); 
    display: flex; justify-content: space-between; align-items: center; padding: 0 20px;
  }}
  .btn {{
    background: var(--bg); color: var(--neon); border: 1px solid var(--line); 
    padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 13px;
  }}
  .btn:hover {{ border-color: var(--neon); }}
  select {{
    background: var(--bg); color: var(--link); border: 1px solid var(--line); 
    padding: 8px 16px; border-radius: 8px; cursor: pointer; outline: none; font-size: 13px;
  }}
  iframe {{
    width: 100%; height: calc(100vh - 60px); border: none; display: block;
  }}
</style>
</head>
<body>
  <!-- Minimal Top Navigation -->
  <div class="top-bar">
    <button class="btn" onclick="loadLatest()">🏠 Home (Latest)</button>
    <select id="historySelect" onchange="loadReport(this.value)">
      <option value="">📂 View History...</option>
{options_html}
    </select>
  </div>
  
  <!-- Content Window (Defaults to the newest report) -->
  <iframe id="reportFrame" src="{latest_file_rel}"></iframe>

  <script>
    const latestReport = "{latest_file_rel}";
    
    function loadReport(url) {{
      if(url) {{
        document.getElementById('reportFrame').src = url;
      }}
    }}
    
    function loadLatest() {{
      document.getElementById('reportFrame').src = latestReport;
      document.getElementById('historySelect').value = "";
    }}
  </script>
</body>
</html>'''

with open(os.path.join(REPO_DIR, "index.html"), 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"Built wrapper index.html. Total archived reports: {len(archived_files)}.")
