import shutil
from pathlib import Path

source_dir = Path(r"H:\ollama\aniimo-wiki-copy")
target_site = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site")
target_root = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki")

# 1. Clean old site directory and copy fresh from H:\ollama\aniimo-wiki-copy
print("Syncing files from H:\\ollama\\aniimo-wiki-copy to scratch...")
if target_site.exists():
    # keep robots and sitemaps if needed
    robots_text = (target_site / "robots.txt").read_text(encoding="utf-8") if (target_site / "robots.txt").exists() else None
    sitemap_text = (target_site / "sitemap.xml").read_text(encoding="utf-8") if (target_site / "sitemap.xml").exists() else None
    sitemap_idx = (target_site / "sitemap_index.xml").read_text(encoding="utf-8") if (target_site / "sitemap_index.xml").exists() else None
    
    shutil.rmtree(target_site)

target_site.mkdir(parents=True, exist_ok=True)

# Copy core files
shutil.copy2(source_dir / "index.html", target_site / "index.html")
shutil.copy2(source_dir / "app.js", target_site / "app.js")
shutil.copy2(source_dir / "styles.css", target_site / "styles.css")
shutil.copy2(source_dir / "README.md", target_site / "README.md")
shutil.copytree(source_dir / "assets", target_site / "assets", dirs_exist_ok=True)

# Restore sitemap & robots.txt
if robots_text:
    (target_site / "robots.txt").write_text(robots_text, encoding="utf-8")
if sitemap_text:
    (target_site / "sitemap.xml").write_text(sitemap_text, encoding="utf-8")
if sitemap_idx:
    (target_site / "sitemap_index.xml").write_text(sitemap_idx, encoding="utf-8")

# Also copy 404 handler (index.html as 404 for SPA routing)
shutil.copy2(target_site / "index.html", target_site / "404.html")

print(f"Copied {len(list(target_site.rglob('*')))} files to {target_site}")

# 2. Update nginx.conf in target_root for SPA routing
nginx_conf = """server {
    listen 80;
    server_name localhost aniimo.dluz.com.br;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        application/json
        application/javascript
        image/svg+xml
        font/ttf
        font/woff2;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # SPA Clean URL Fallback (Requirement 15: direct refresh on detail route)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static Assets Long-Term Caching
    location ~* \\.(?:css|js|woff2|woff|ttf|svg|ico)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
        access_log off;
    }

    # High-Res Media & Images Caching
    location ~* \\.(?:png|jpg|jpeg|webp|gif)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        access_log off;
    }

    error_page 404 /index.html;
}
"""
(target_root / "nginx.conf").write_text(nginx_conf, encoding="utf-8")
print("Updated nginx.conf with SPA fallback routing")
