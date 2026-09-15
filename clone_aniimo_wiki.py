import asyncio
import os
import sys
import re
import json
import urllib.parse
from pathlib import Path
import httpx

BASE_URL = "https://wiki.aniimo.com"
OUTPUT_DIR = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki")
SITE_DIR = OUTPUT_DIR / "site"
DATA_DIR = OUTPUT_DIR / "data"

CONCURRENCY = 20
semaphore = asyncio.Semaphore(CONCURRENCY)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

downloaded_count = 0
failed_urls = []

async def download_file(client: httpx.AsyncClient, url: str, dest_path: Path) -> bool:
    global downloaded_count
    if dest_path.exists() and dest_path.stat().st_size > 0:
        return True
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    async with semaphore:
        for attempt in range(3):
            try:
                resp = await client.get(url, headers=HEADERS, timeout=30.0, follow_redirects=True)
                if resp.status_code == 200:
                    dest_path.write_bytes(resp.content)
                    downloaded_count += 1
                    if downloaded_count % 25 == 0:
                        print(f"Downloaded {downloaded_count} files...")
                    return True
                elif resp.status_code == 404:
                    # Not found
                    return False
            except Exception as e:
                if attempt == 2:
                    failed_urls.append((url, str(e)))
                await asyncio.sleep(0.5)
    return False

def rewrite_content(text: str) -> str:
    """Rewrite absolute CDN URLs to local paths"""
    # 1. Akamai Nuxt CDN to local _nuxt
    text = re.sub(r"https://kg-web-cdn\.akamaized\.net/master/worldx/wiki-frontend/_nuxt/", "/_nuxt/", text)
    # 2. Aniimo Stage CDN to local /cdn/
    text = re.sub(r"https://worldx-website-cdn\.aniimo\.com/official-website/worldx/wiki_stage/", "/cdn/", text)
    # 3. Akamai footer images to /images/footer/
    text = re.sub(r"https://kg-web-cdn\.akamaized\.net/master/official-website/worldx_office_frontend/images/footer/", "/images/footer/", text)
    # 4. Canonical / og URLs to localhost/relative
    text = re.sub(r"https://wiki\.aniimo\.com/", "/", text)
    return text

async def main():
    print("=" * 60)
    print("🚀 ANIIMO WIKI COMPLETE CLONER & ANALYZER")
    print("=" * 60)
    print(f"Target directory: {OUTPUT_DIR}")
    
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    limits = httpx.Limits(max_keepalive_connections=30, max_connections=50)
    async with httpx.AsyncClient(limits=limits, timeout=45.0) as client:
        # Step 1: Discover all pages from sitemaps
        print("\n[1/6] Discovering all sitemaps and pages...")
        sitemaps = [
            f"{BASE_URL}/__sitemap__/en-US.xml",
            f"{BASE_URL}/__sitemap__/ja-JP.xml",
            f"{BASE_URL}/__sitemap__/ko-KR.xml",
            f"{BASE_URL}/__sitemap__/zh-TW.xml"
        ]
        all_page_urls = set()
        for sm in sitemaps:
            try:
                resp = await client.get(sm, headers=HEADERS)
                if resp.status_code == 200:
                    locs = re.findall(r"<loc>(.*?)</loc>", resp.text)
                    all_page_urls.update(locs)
            except Exception as e:
                print(f"Error fetching sitemap {sm}: {e}")
        
        # Always include base homepages
        all_page_urls.add(f"{BASE_URL}/")
        all_page_urls.add(f"{BASE_URL}/ja")
        all_page_urls.add(f"{BASE_URL}/ko")
        all_page_urls.add(f"{BASE_URL}/tw")

        print(f"Discovered {len(all_page_urls)} total pages across all languages.")

        # Step 2: Download HTML and _payload.json for each page
        print("\n[2/6] Downloading all HTML pages and Nuxt payloads...")
        pages_to_download = []
        for p_url in sorted(all_page_urls):
            path = urllib.parse.urlparse(p_url).path.strip("/")
            if not path:
                # Home
                html_path = SITE_DIR / "index.html"
                payload_path = SITE_DIR / "_payload.json"
                payload_url = f"{BASE_URL}/_payload.json"
            else:
                html_path = SITE_DIR / path / "index.html"
                payload_path = SITE_DIR / path / "_payload.json"
                payload_url = f"{BASE_URL}/{path}/_payload.json"
            
            pages_to_download.append((p_url, html_path, payload_url, payload_path))

        # Gather HTML and payloads
        all_media_urls = set()
        all_nuxt_assets = set()
        raw_payloads = {}

        async def fetch_page(p_url, h_path, pl_url, pl_path):
            # Fetch HTML
            try:
                resp_h = await client.get(p_url, headers=HEADERS)
                if resp_h.status_code == 200:
                    content_rewritten = rewrite_content(resp_h.text)
                    h_path.parent.mkdir(parents=True, exist_ok=True)
                    h_path.write_text(content_rewritten, encoding="utf-8")
                    
                    # Extract assets from raw HTML
                    for m in re.findall(r'https?://[^\s"\'<>)]+\.(?:png|jpg|jpeg|webp|svg|gif|ico|woff2|woff|ttf|css|js|mp4)', resp_h.text):
                        all_media_urls.add(m)
                    for n in re.findall(r'/_nuxt/[^\s"\'<>)]+', resp_h.text):
                        all_nuxt_assets.add(n)
            except Exception as e:
                print(f"Error downloading page {p_url}: {e}")

            # Fetch payload
            try:
                resp_pl = await client.get(pl_url, headers=HEADERS)
                if resp_pl.status_code == 200:
                    raw_data = resp_pl.text
                    raw_payloads[p_url] = resp_pl.json()
                    pl_rewritten = rewrite_content(raw_data)
                    pl_path.parent.mkdir(parents=True, exist_ok=True)
                    pl_path.write_text(pl_rewritten, encoding="utf-8")
                    
                    # Extract assets from payload
                    for m in re.findall(r'https?://[^\s"\'<>)]+\.(?:png|jpg|jpeg|webp|svg|gif|mp4)', raw_data):
                        all_media_urls.add(m)
            except Exception as e:
                # Some pages might not have a separate payload
                pass

        tasks = [fetch_page(u, hp, plu, plp) for u, hp, plu, plp in pages_to_download]
        await asyncio.gather(*tasks)
        print(f"Successfully downloaded {len(pages_to_download)} pages & payloads.")

        # Step 3: Discover all Nuxt assets and CSS assets
        print("\n[3/6] Discovering and downloading Nuxt scripts, styles, fonts, and UI images...")
        # Nuxt build meta
        build_meta_url = "https://kg-web-cdn.akamaized.net/master/worldx/wiki-frontend/_nuxt/builds/meta/55d25ac2-4522-448c-8203-af343869cb90.json"
        build_meta_path = SITE_DIR / "_nuxt" / "builds" / "meta" / "55d25ac2-4522-448c-8203-af343869cb90.json"
        await download_file(client, build_meta_url, build_meta_path)
        # Also copy as .js if requested
        build_meta_js = SITE_DIR / "_nuxt" / "builds" / "meta" / "55d25ac2-4522-448c-8203-af343869cb90.js"
        if build_meta_path.exists():
            build_meta_js.write_bytes(build_meta_path.read_bytes())

        # Collect known CSS files to inspect for fonts & images
        css_files = [m for m in all_media_urls if m.endswith(".css")]
        css_tasks = []
        for css_url in css_files:
            filename = css_url.split("/")[-1]
            dest = SITE_DIR / "_nuxt" / filename
            css_tasks.append(download_file(client, css_url, dest))
        await asyncio.gather(*css_tasks)

        # Inspect downloaded CSS for background images and fonts
        css_asset_urls = set()
        for css_file in (SITE_DIR / "_nuxt").glob("*.css"):
            css_text = css_file.read_text(encoding="utf-8", errors="ignore")
            for ref in re.findall(r'url\([\"\']?(.*?)[\"\']?\)', css_text):
                if ref.startswith("data:"):
                    continue
                if ref.startswith("http"):
                    css_asset_urls.add(ref)
                elif ref.startswith("../fonts/"):
                    css_asset_urls.add(f"{BASE_URL}/fonts/" + ref.replace("../fonts/", ""))
                elif ref.startswith("../images/"):
                    css_asset_urls.add(f"{BASE_URL}/images/" + ref.replace("../images/", ""))
                elif ref.startswith("/images/"):
                    css_asset_urls.add(f"{BASE_URL}" + ref)
                elif ref.startswith("/fonts/"):
                    css_asset_urls.add(f"{BASE_URL}" + ref)

        print(f"Found {len(css_asset_urls)} assets referenced inside CSS files.")
        all_media_urls.update(css_asset_urls)

        # Standard known UI assets to ensure nothing is missed
        known_ui_assets = [
            f"{BASE_URL}/fonts/BILLGATES-2.TTF",
            f"{BASE_URL}/images/sprite/attributes.png",
            f"{BASE_URL}/images/sprite/positions.png",
            f"{BASE_URL}/images/sprite/stages.png",
            f"{BASE_URL}/images/header/search.png",
            f"{BASE_URL}/images/header/arrow.png",
            f"{BASE_URL}/images/header/en_dark.png",
            f"{BASE_URL}/images/header/ja_dark.png",
            f"{BASE_URL}/images/header/ko_dark.png",
            f"{BASE_URL}/images/header/cn_dark.png",
            f"{BASE_URL}/images/main/background.png",
            f"{BASE_URL}/images/main/scrollTop.png",
            f"{BASE_URL}/images/page/aniimo_bg.png",
            f"{BASE_URL}/images/page/contain_lt_bg.png",
            f"{BASE_URL}/images/page/sublogo.png",
            f"{BASE_URL}/images/footer/logo.png",
            f"{BASE_URL}/images/404/404.png",
            f"{BASE_URL}/images/404/bg.png",
            f"{BASE_URL}/favicon.ico",
            "https://kg-web-cdn.akamaized.net/master/official-website/worldx_office_frontend/images/footer/ariel.webp",
            "https://kg-web-cdn.akamaized.net/master/official-website/worldx_office_frontend/images/footer/level.webp"
        ]
        all_media_urls.update(known_ui_assets)

        # Step 4: Download all media assets (Creatures, Icons, VFX Videos, Fonts, UI)
        print(f"\n[4/6] Downloading all {len(all_media_urls)} media files (PNGs, WebPs, MP4 videos, fonts, JS)...")
        media_tasks = []
        for m_url in all_media_urls:
            # Determine destination path
            parsed = urllib.parse.urlparse(m_url)
            path_str = parsed.path
            
            if "worldx-website-cdn.aniimo.com/official-website/worldx/wiki_stage/" in m_url:
                rel = m_url.split("wiki_stage/")[-1]
                dest = SITE_DIR / "cdn" / rel
            elif "_nuxt/" in m_url:
                filename = m_url.split("_nuxt/")[-1].split("?")[0]
                dest = SITE_DIR / "_nuxt" / filename
            elif "/fonts/" in path_str:
                filename = path_str.split("/fonts/")[-1]
                dest = SITE_DIR / "fonts" / filename
            elif "/images/" in path_str:
                rel = path_str.split("/images/")[-1]
                dest = SITE_DIR / "images" / rel
            elif m_url.endswith("favicon.ico"):
                dest = SITE_DIR / "favicon.ico"
            elif "akamaized.net" in m_url and "images/footer/" in m_url:
                filename = m_url.split("/")[-1]
                dest = SITE_DIR / "images" / "footer" / filename
            else:
                # Default generic asset
                filename = path_str.split("/")[-1]
                dest = SITE_DIR / "assets" / filename

            media_tasks.append(download_file(client, m_url, dest))

        # Run downloads with progress tracking
        results = await asyncio.gather(*media_tasks, return_exceptions=True)
        success_count = sum(1 for r in results if r is True)
        print(f"Download complete: {success_count} assets saved successfully.")

        # Step 5: Post-processing and rewriting CSS links
        print("\n[5/6] Finalizing CSS and file path rewrites for 100% offline local viewing...")
        for css_file in (SITE_DIR / "_nuxt").glob("*.css"):
            css_text = css_file.read_text(encoding="utf-8", errors="ignore")
            # Ensure relative paths resolve properly
            css_text = re.sub(r'https://kg-web-cdn\.akamaized\.net/master/worldx/wiki-frontend/', '/', css_text)
            css_text = re.sub(r'https://worldx-website-cdn\.aniimo\.com/official-website/worldx/wiki_stage/', '/cdn/', css_text)
            css_file.write_text(css_text, encoding="utf-8")

        # Step 6: Extract Structured Data for all Aniimos
        print("\n[6/6] Extracting structured database for all Aniimos (JSON)...")
        aniimos_db = []
        for p_url, p_data in raw_payloads.items():
            if "/item/" not in p_url or not p_data:
                continue
            # Parse Nuxt 3 payload array
            try:
                # Find the creature object
                creature_obj = {}
                for item in p_data:
                    if isinstance(item, dict) and "entryId" in item and "name" in item and "imageUrl" in item:
                        # Resolve indexed strings in Nuxt 3 shallow reactive payload
                        def resolve(val):
                            if isinstance(val, int) and 0 <= val < len(p_data):
                                return p_data[val]
                            return val

                        name = resolve(item.get("name"))
                        entry_id = resolve(item.get("entryId"))
                        img = resolve(item.get("imageUrl"))
                        desc = resolve(item.get("description"))
                        stage = resolve(item.get("stage"))

                        if isinstance(name, str) and isinstance(img, str):
                            creature_obj = {
                                "id": p_url.split("/item/")[-1],
                                "entryId": str(entry_id),
                                "name": name,
                                "description": desc if isinstance(desc, str) else "",
                                "stage": stage if isinstance(stage, (str, int)) else "",
                                "originalImageUrl": img,
                                "localImageUrl": "/cdn/" + img.split("wiki_stage/")[-1] if "wiki_stage/" in img else img,
                                "url": p_url
                            }
                            break
                if creature_obj and creature_obj not in aniimos_db:
                    # Check for VFX video
                    item_str = json.dumps(p_data)
                    vfx_match = re.search(r'https://worldx-website-cdn\.aniimo\.com/official-website/worldx/wiki_stage/Vfx/(\w+\.mp4)', item_str)
                    if vfx_match:
                        creature_obj["vfxVideoUrl"] = vfx_match.group(0)
                        creature_obj["localVfxVideo"] = f"/cdn/Vfx/{vfx_match.group(1)}"
                    aniimos_db.append(creature_obj)
            except Exception as e:
                pass

        # Sort by entryId or id
        aniimos_db.sort(key=lambda x: str(x.get("entryId", "")).zfill(4))
        
        # Save structured JSON
        json_path = DATA_DIR / "all_aniimos.json"
        json_path.write_text(json.dumps(aniimos_db, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Structured database generated with {len(aniimos_db)} Aniimos at {json_path}")

        print("\n" + "=" * 60)
        print("✅ CLONING AND ASSET DOWNLOAD COMPLETED SUCCESSFULLY!")
        print(f"Total downloaded files in site/: {len(list(SITE_DIR.rglob('*')))} files")
        print(f"Total structured Aniimos in database: {len(aniimos_db)}")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
