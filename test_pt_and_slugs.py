import asyncio
import subprocess
import time
from playwright.async_api import async_playwright

SERVER_DIR = r"H:\ollama\aniimo-wiki-copy"
PORT = 4173
BASE_URL = f"http://localhost:{PORT}"

async def run_tests():
    proc = subprocess.Popen(["python", "-m", "http.server", str(PORT), "--directory", SERVER_DIR], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    print("=" * 60)
    print("🧪 TESTING PT-BR DEFAULT & CLEAN SLUG URLS (/inferlupa)")
    print("=" * 60)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                headless=True
            )
            page = await browser.new_page(viewport={"width": 1440, "height": 900})
            
            # 1. Load Homepage
            print("\n[TEST 1] Load Home (verify PT default)...")
            await page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
            
            # Verify PT text
            search_placeholder = await page.get_attribute("#search", "placeholder")
            print(f"  -> Search Placeholder: {search_placeholder}")
            assert "Buscar" in search_placeholder

            elem_label = await page.locator(".filter-label").first.text_content()
            print(f"  -> First filter label: {elem_label}")
            assert "Elementos" in elem_label

            fire_chip = await page.locator('.filter-chip[data-filter-value="fire"]').text_content()
            print(f"  -> Fire chip text: {fire_chip.strip()}")
            assert "Fogo" in fire_chip

            # 2. Click on Inferlupa card & verify URL changes to /inferlupa
            print("\n[TEST 2] Click Inferlupa card & check clean slug URL...")
            inferlupa_card = page.locator('a.creature-card[data-slug="inferlupa"]')
            await inferlupa_card.click()
            await page.wait_for_timeout(400)
            
            current_url = page.url
            print(f"  -> Current URL after click: {current_url}")
            assert current_url.endswith("/inferlupa"), f"Expected URL to end with /inferlupa, got {current_url}"

            title = await page.locator(".hero-title").text_content()
            print(f"  -> Page title: {title.strip()[:30]}")
            assert "Inferlupa" in title

            overview_label = await page.locator(".section-title").first.text_content()
            print(f"  -> Overview label: {overview_label}")
            assert "Visão Geral" in overview_label

            desc_pt = await page.locator(".hero-desc").text_content()
            print(f"  -> Lore description: {desc_pt.strip()[:60]}...")
            assert "Flameruff" in desc_pt or "veterano" in desc_pt

            # 3. Test Back button returns to /
            print("\n[TEST 3] Click Back to Wiki button...")
            back_btn = page.locator('a.nav-back[data-nav="home"]')
            await back_btn.click()
            await page.wait_for_timeout(400)
            home_url = page.url
            print(f"  -> URL after back: {home_url}")
            assert home_url.rstrip("/").endswith(str(PORT))
            
            total_cards = await page.locator(".creature-card").count()
            print(f"  -> Total cards on catalog: {total_cards}")
            assert total_cards == 94

            # 4. Direct Navigation via URL (hash fallback or slug)
            print("\n[TEST 4] Test direct navigation via #inferlupa...")
            await page.goto(f"{BASE_URL}/#inferlupa", wait_until="domcontentloaded")
            await page.wait_for_timeout(400)
            direct_title = await page.locator(".hero-title").text_content()
            print(f"  -> Loaded directly: {direct_title.strip()[:30]}")
            assert "Inferlupa" in direct_title

            # 5. Language Toggle Test (PT -> EN -> PT)
            print("\n[TEST 5] Test Language Toggle Button...")
            lang_btn = page.locator(".language-button")
            btn_text = await lang_btn.text_content()
            print(f"  -> Initial button text: {btn_text.strip()}")
            assert "PT" in btn_text

            await lang_btn.click()
            await page.wait_for_timeout(300)
            btn_text_en = await lang_btn.text_content()
            overview_en = await page.locator(".section-title").first.text_content()
            print(f"  -> After click (EN): button={btn_text_en.strip()}, overview={overview_en.strip()}")
            assert "EN" in btn_text_en
            assert "Overview" in overview_en

            # Switch back to PT
            await lang_btn.click()
            await page.wait_for_timeout(300)
            overview_pt = await page.locator(".section-title").first.text_content()
            print(f"  -> Switched back to PT: {overview_pt.strip()}")
            assert "Visão Geral" in overview_pt

            print("\n" + "=" * 60)
            print("🎉 ALL PT-BR AND CLEAN SLUG TESTS PASSED PERFECTLY!")
            print("=" * 60)

            await browser.close()
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_tests())
