import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://aniimo.dluz.com.br/",
    "https://aniimo.dluz.com.br/robots.txt",
    "https://aniimo.dluz.com.br/sitemap.xml",
    "https://aniimo.dluz.com.br/item/10002688/",
    "https://aniimo.dluz.com.br/cdn/init/Wiki_Aniimo_10443.png",
    "https://aniimo.dluz.com.br/cdn/Vfx/1044300.mp4"
]

all_ok = True
for u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = resp.read()
            ct = resp.headers.get("Content-Type")
            print(f"✅ {u:55} -> Status: {resp.status} (Type: {ct}, Size: {len(data):,} bytes)")
    except Exception as e:
        print(f"❌ {u:55} -> Error: {e}")
        all_ok = False

if all_ok:
    print("\n🎉 PRODUCTION DEPLOYMENT AT HTTPS://ANIIMO.DLUZ.COM.BR IS 100% ONLINE AND WORKING!")
