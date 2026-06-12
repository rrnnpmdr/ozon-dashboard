import json

# ── Load analysis data ──
with open('analysis.json') as f:
    D = json.load(f)

# ── Read template ──
with open('report.html', 'r') as f:
    content = f.read()

# Inject the analysis data as a JS variable
placeholder = '// ANALYIS_DATA_PLACEHOLDER'
json_str = json.dumps(D, ensure_ascii=False)
script_tag = f'const ANALYIS_DATA = {json_str};'

if placeholder in content:
    new_content = content.replace(placeholder, script_tag)
    with open('report.html', 'w') as f:
        f.write(new_content)
    print("Data injected successfully!")
else:
    print(f"Placeholder not found. Content length: {len(content)}")
    # Show first 200 chars to check
    print("First 200 chars:", content[:200])
