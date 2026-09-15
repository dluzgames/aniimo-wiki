import urllib.request
import re
from bs4 import BeautifulSoup

url_orig = "https://wiki.aniimo.com/"
req = urllib.request.Request(url_orig, headers={"User-Agent": "Mozilla/5.0"})
html_orig = urllib.request.urlopen(req).read().decode("utf-8")

# Let's find Emberpup or NO.001 in original html
soup = BeautifulSoup(html_orig, "html.parser")
card = soup.find(href="/item/10002767")
if card:
    print("=== ORIGINAL CARD HTML ===")
    print(card.prettify()[:1000])
else:
    print("Card not found by href")

# Let's check our local site/index.html
local_html = open(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\index.html", "r", encoding="utf-8").read()
soup_local = BeautifulSoup(local_html, "html.parser")
local_card = soup_local.find(href="/item/10002767")
if local_card:
    print("\n=== LOCAL CARD HTML ===")
    print(local_card.prettify()[:1000])
