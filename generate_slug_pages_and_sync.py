import json
import shutil
import re
from pathlib import Path

source_dir = Path(r"H:\ollama\aniimo-wiki-copy")
target_site = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site")
creatures = json.loads((source_dir / "creatures_pt.json").read_text(encoding="utf-8"))

print("=" * 60)
print("🚀 GENERATING STATIC SLUG PAGES AND SYNCING FOR PRODUCTION")
print("=" * 60)

# 1. Clean and sync base assets
if target_site.exists():
    shutil.rmtree(target_site)
target_site.mkdir(parents=True, exist_ok=True)

shutil.copy2(source_dir / "index.html", target_site / "index.html")
shutil.copy2(source_dir / "app.js", target_site / "app.js")
shutil.copy2(source_dir / "styles.css", target_site / "styles.css")
shutil.copy2(source_dir / "README.md", target_site / "README.md")
shutil.copytree(source_dir / "assets", target_site / "assets", dirs_exist_ok=True)

# 2. Read base index.html template
base_html = (source_dir / "index.html").read_text(encoding="utf-8")

# 3. Generate static slug pages for each creature for maximum Google SEO
BASE_DOMAIN = "https://aniimo.dluz.com.br"
sitemap_urls = [f"{BASE_DOMAIN}/"]

for c in creatures:
    slug = c["slug"]
    slug_dir = target_site / slug
    slug_dir.mkdir(parents=True, exist_ok=True)

    # Creature SEO metadata
    c_title = f"{c['name']} (NO.{c['number']}) — Aniimo Wiki Brasil | DLuz Games"
    c_desc = c.get("desc_pt", c.get("desc", ""))
    c_img = f"{BASE_DOMAIN}/assets/creatures/Wiki_Aniimo_{c['image']}.png"
    c_url = f"{BASE_DOMAIN}/{slug}"
    sitemap_urls.append(c_url)

    c_schema = {
        "@context": "https://schema.org",
        "@type": "ItemPage",
        "url": c_url,
        "name": c_title,
        "description": c_desc,
        "inLanguage": "pt-BR",
        "mainEntity": {
            "@type": "Thing",
            "name": c["name"],
            "description": c_desc,
            "image": c_img,
            "identifier": f"NO.{c['number']}",
            "category": "Criatura Aniimo",
            "isPartOf": {
                "@type": "VideoGame",
                "name": "Aniimo"
            }
        }
    }

    # Inject metadata into HTML
    slug_html = base_html
    slug_html = re.sub(r'<title>.*?</title>', f'<title>{c_title}</title>', slug_html)
    slug_html = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{c_desc}" />', slug_html)
    slug_html = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{c_url}" />', slug_html)
    slug_html = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{c_title}" />', slug_html)
    slug_html = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{c_desc}" />', slug_html)
    slug_html = re.sub(r'<meta property="og:url" content=".*?" />', f'<meta property="og:url" content="{c_url}" />', slug_html)
    slug_html = re.sub(r'<meta property="og:image" content=".*?" />', f'<meta property="og:image" content="{c_img}" />', slug_html)
    slug_html = re.sub(r'<meta name="twitter:image" content=".*?" />', f'<meta name="twitter:image" content="{c_img}" />', slug_html)
    
    # Adjust assets path for subdirectory
    slug_html = slug_html.replace('href="assets/', 'href="/assets/')
    slug_html = slug_html.replace('src="assets/', 'src="/assets/')
    slug_html = slug_html.replace('href="styles.css"', 'href="/styles.css"')
    slug_html = slug_html.replace('src="app.js"', 'src="/app.js"')

    # Replace schema
    schema_tag = f'<script type="application/ld+json">\n{json.dumps(c_schema, ensure_ascii=False, indent=2)}\n</script>'
    slug_html = re.sub(r'<script type="application/ld\+json">.*?</script>', schema_tag, slug_html, flags=re.DOTALL)

    (slug_dir / "index.html").write_text(slug_html, encoding="utf-8")

print(f"Generated {len(creatures)} static slug folders (e.g. site/inferlupa/index.html)!")

# 4. Generate Google XML Sitemap with all clean URLs
sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sitemap_urls:
    prio = "1.0" if u == f"{BASE_DOMAIN}/" else "0.8"
    freq = "daily" if u == f"{BASE_DOMAIN}/" else "weekly"
    sitemap_xml.append(f"  <url>\n    <loc>{u}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
sitemap_xml.append("</urlset>")
(target_site / "sitemap.xml").write_text("\n".join(sitemap_xml), encoding="utf-8")

sitemap_index_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>{BASE_DOMAIN}/sitemap.xml</loc>
    </sitemap>
</sitemapindex>
"""
(target_site / "sitemap_index.xml").write_text(sitemap_index_xml, encoding="utf-8")

robots_txt = f"""User-agent: *
Allow: /
Sitemap: {BASE_DOMAIN}/sitemap_index.xml
Sitemap: {BASE_DOMAIN}/sitemap.xml
"""
(target_site / "robots.txt").write_text(robots_txt, encoding="utf-8")

# 404 page
shutil.copy2(target_site / "index.html", target_site / "404.html")

print("Generated sitemap.xml with 95 clean URLs and robots.txt!")
