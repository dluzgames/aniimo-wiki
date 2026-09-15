import re
from pathlib import Path

site_dir = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site")

files_fixed = 0
for f in site_dir.rglob("*"):
    if f.is_file() and f.suffix in [".html", ".json", ".js"]:
        try:
            content = f.read_text(encoding="utf-8")
            orig = content
            # Replace Nuxt cdnUrl with local root '/'
            content = content.replace("https://kg-web-cdn.akamaized.net/master/worldx/wiki-frontend/", "/")
            content = content.replace("https://worldx-website-cdn.aniimo.com/official-website/worldx/wiki_stage/", "/cdn/")
            content = content.replace("https://kg-web-cdn.akamaized.net/master/official-website/worldx_office_frontend/images/footer/", "/images/footer/")
            
            # Remove cookiebot banner script so it doesn't hang offline
            content = re.sub(r'<script[^>]*consent\.cookiebot\.com[^>]*></script>', '', content)
            
            if content != orig:
                f.write_text(content, encoding="utf-8")
                files_fixed += 1
        except Exception as e:
            pass

print(f"Updated {files_fixed} files for seamless offline hydration.")
