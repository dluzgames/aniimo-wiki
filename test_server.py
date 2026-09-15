import urllib.request

test_paths = [
    "/",
    "/_payload.json",
    "/_nuxt/DYDCMPRo.js",
    "/item/10002688/",
    "/item/10002688/_payload.json",
    "/cdn/init/Wiki_Aniimo_10443.png",
    "/cdn/Vfx/1044300.mp4",
    "/fonts/BILLGATES-2.TTF",
    "/images/sprite/attributes.png"
]

all_passed = True
for p in test_paths:
    url = f"http://localhost:8080{p}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            ct = resp.headers.get("Content-Type")
            print(f"✅ {p:32} -> {resp.status} (Type: {ct}, Size: {len(data):,} bytes)")
    except Exception as e:
        print(f"❌ {p:32} -> Error: {e}")
        all_passed = False

if all_passed:
    print("\n🎉 ALL LOCAL ENDPOINTS TESTED AND WORKING PERFECTLY!")
