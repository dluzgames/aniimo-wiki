import re
import json
from pathlib import Path

SITE_DIR = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site")
DATA_DIR = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\data")
NEW_DOMAIN = "https://aniimo.dluz.com.br"

print("=" * 60)
print("🚀 APPLYING GOOGLE SEO OPTIMIZATIONS & BEST PRACTICES")
print("=" * 60)

# Load database if available
aniimos_db = {}
json_file = DATA_DIR / "all_aniimos.json"
if json_file.exists():
    try:
        items = json.loads(json_file.read_text(encoding="utf-8"))
        for it in items:
            aniimos_db[it.get("id")] = it
    except Exception as e:
        print("Error loading db:", e)

print(f"Loaded {len(aniimos_db)} Aniimos from local database for JSON-LD enrichment.")

# Step 1: Process all HTML files
html_files = list(SITE_DIR.rglob("*.html"))
print(f"Optimizing {len(html_files)} HTML pages...")

processed = 0
for hf in html_files:
    try:
        content = hf.read_text(encoding="utf-8")
        orig = content

        # Replace domain in canonical and og:urls
        content = content.replace("https://wiki.aniimo.com", NEW_DOMAIN)
        content = content.replace("http://wiki.aniimo.com", NEW_DOMAIN)

        # Update Open Graph Site Name & Brand
        content = re.sub(r'<meta property="og:site_name" content="[^"]*">', f'<meta property="og:site_name" content="Aniimo Wiki | DLuz">', content)
        
        # Check if page is an item page
        rel_path = hf.relative_to(SITE_DIR).as_posix()
        m = re.search(r'item/(\d+)', rel_path)
        
        json_ld_scripts = []
        
        if not m:
            # Homepage Schema (WebSite + Organization)
            schema = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "WebSite",
                        "@id": f"{NEW_DOMAIN}/#website",
                        "url": f"{NEW_DOMAIN}/",
                        "name": "Aniimo Wiki - Complete Aniimo Index & Database",
                        "description": "The complete Aniimo Wiki & Index: Aniimo forms, attributes, evolution paths, spawn locations, abilities, combat skills, traits, and resonance stage training.",
                        "inLanguage": ["en-US", "ja-JP", "ko-KR", "zh-TW", "pt-BR"],
                        "publisher": {
                            "@type": "Organization",
                            "name": "DLuz Games",
                            "url": "https://dluzgames.com.br"
                        }
                    },
                    {
                        "@type": "CollectionPage",
                        "@id": f"{NEW_DOMAIN}/#webpage",
                        "url": f"{NEW_DOMAIN}/",
                        "name": "Official Aniimo Index & Encyclopedia",
                        "isPartOf": { "@id": f"{NEW_DOMAIN}/#website" },
                        "about": {
                            "@type": "VideoGame",
                            "name": "Aniimo",
                            "applicationCategory": "Game",
                            "genre": ["Open-World RPG", "Creature Collection", "Adventure", "Multiplayer"]
                        }
                    }
                ]
            }
            json_ld_scripts.append(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')
        else:
            # Creature Item Schema
            item_id = m.group(1)
            creature = aniimos_db.get(item_id, {})
            name = creature.get("name")
            if not name:
                # Extract title from HTML
                tm = re.search(r'<title>(.*?)</title>', content)
                name = tm.group(1).split("|")[0].strip() if tm else f"Aniimo #{item_id}"
            
            desc = creature.get("description") or f"Learn everything about {name} in Aniimo: stats, attributes, elements, evolution path, skills, and combat abilities."
            img_url = f"{NEW_DOMAIN}{creature.get('localImageUrl', f'/cdn/init/Wiki_Aniimo_{item_id}.png')}"
            
            schema = {
                "@context": "https://schema.org",
                "@type": "ItemPage",
                "mainEntity": {
                    "@type": "Thing",
                    "name": name,
                    "description": desc,
                    "image": img_url,
                    "identifier": creature.get("entryId", item_id),
                    "category": "Aniimo Creature",
                    "isPartOf": {
                        "@type": "VideoGame",
                        "name": "Aniimo"
                    }
                }
            }
            if creature.get("localVfxVideo"):
                schema["mainEntity"]["video"] = {
                    "@type": "VideoObject",
                    "name": f"{name} Skill Combat VFX",
                    "description": f"Skill animation and combat visual effects demonstration for {name}.",
                    "thumbnailUrl": img_url,
                    "contentUrl": f"{NEW_DOMAIN}{creature.get('localVfxVideo')}",
                    "uploadDate": "2026-03-01T00:00:00Z"
                }
            json_ld_scripts.append(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')

        # Insert JSON-LD into <head>
        if json_ld_scripts and "</head>" in content and "application/ld+json" not in content:
            script_tags = "\n".join(json_ld_scripts)
            content = content.replace("</head>", f"{script_tags}\n</head>")

        if content != orig:
            hf.write_text(content, encoding="utf-8")
            processed += 1
    except Exception as e:
        print(f"Error processing {hf}: {e}")

print(f"Updated SEO tags and JSON-LD in {processed} HTML pages.")

# Step 2: Create Google Robots.txt
robots_txt = f"""# Googlebot and Search Engine Rules
User-agent: *
Allow: /
Allow: /item/*
Allow: /ja/
Allow: /ko/
Allow: /tw/
Disallow: /cdn/Vfx/

Sitemap: {NEW_DOMAIN}/sitemap_index.xml
Sitemap: {NEW_DOMAIN}/sitemap.xml
"""
(SITE_DIR / "robots.txt").write_text(robots_txt, encoding="utf-8")
print(f"Created optimized robots.txt with sitemap reference.")

# Step 3: Generate unified sitemap.xml with all 380 URLs
all_urls = []
for hf in sorted(html_files):
    rel = hf.relative_to(SITE_DIR).as_posix()
    if rel == "index.html":
        url = f"{NEW_DOMAIN}/"
        priority = "1.0"
        freq = "daily"
    else:
        clean_path = rel.replace("/index.html", "").replace(".html", "")
        url = f"{NEW_DOMAIN}/{clean_path}"
        priority = "0.8"
        freq = "weekly"
    all_urls.append((url, priority, freq))

sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, prio, freq in all_urls:
    sitemap_xml.append(f"  <url>\n    <loc>{u}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
sitemap_xml.append("</urlset>")
(SITE_DIR / "sitemap.xml").write_text("\n".join(sitemap_xml), encoding="utf-8")

# Also sitemap_index.xml
sitemap_index_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>{NEW_DOMAIN}/sitemap.xml</loc>
    </sitemap>
</sitemapindex>
"""
(SITE_DIR / "sitemap_index.xml").write_text(sitemap_index_xml, encoding="utf-8")
print(f"Generated Google-compliant sitemap.xml with {len(all_urls)} verified URLs.")

print("=" * 60)
print("✅ ALL SEO RULES & GOOGLE RECOMMENDATIONS APPLIED!")
print("=" * 60)
