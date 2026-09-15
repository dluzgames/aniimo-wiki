import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

SERVER_DIR = r"H:\ollama\aniimo-wiki-copy"
PORT = 4173
BASE_URL = f"http://localhost:{PORT}"

async def run_tests():
    # Start server
    proc = subprocess.Popen(["python", "-m", "http.server", str(PORT), "--directory", SERVER_DIR], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    print("=" * 60)
    print("🧪 RUNNING EXTENSIVE VALIDATION SUITE ON H:\\ollama\\aniimo-wiki-copy")
    print("=" * 60)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                headless=True
            )
            
            # --- 1. Desktop Test (1440x900) ---
            print("\n[TEST 1] Desktop 1440px viewport & catalog loading...")
            page = await browser.new_page(viewport={"width": 1440, "height": 900})
            
            console_errors = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            
            await page.goto(f"{BASE_URL}/", wait_until="networkidle")
            
            # Check 94 cards
            cards = await page.locator(".creature-card").count()
            print(f"  -> Cards found: {cards} (Expected 94)")
            assert cards == 94, f"Expected 94 cards, found {cards}"
            
            # Check desktop columns
            grid_cols = await page.eval_on_selector(".grid", "el => window.getComputedStyle(el).gridTemplateColumns.split(' ').length")
            print(f"  -> Grid columns: {grid_cols} (Expected 7)")
            assert grid_cols == 7, f"Expected 7 columns, got {grid_cols}"

            # --- 2. Search Emberpup ---
            print("\n[TEST 2] Search for 'Emberpup'...")
            search_input = page.locator("#search")
            await search_input.fill("Emberpup")
            await page.wait_for_timeout(300)
            cards_search = await page.locator(".creature-card").count()
            name = await page.locator(".creature-name").first.text_content()
            print(f"  -> Search results: {cards_search}, Name: {name}")
            assert cards_search == 1 and "Emberpup" in name
            await search_input.fill("")
            await page.wait_for_timeout(300)

            # --- 3. Filter Element 'fire' ---
            print("\n[TEST 3] Filter by Element 'fire'...")
            fire_chip = page.locator('.filter-chip[data-filter-group="element"][data-filter-value="fire"]')
            await fire_chip.click()
            await page.wait_for_timeout(300)
            fire_count = await page.locator(".creature-card").count()
            print(f"  -> Fire creatures: {fire_count}")
            assert fire_count > 0

            # --- 4. Filter Role 'DPS' combined with 'fire' ---
            print("\n[TEST 4] Combine Element 'fire' + Role 'dps'...")
            dps_chip = page.locator('.filter-chip[data-filter-group="role"][data-filter-value="dps"]')
            await dps_chip.click()
            await page.wait_for_timeout(300)
            fire_dps_count = await page.locator(".creature-card").count()
            print(f"  -> Fire + DPS creatures: {fire_dps_count}")
            assert fire_dps_count > 0

            # --- 5. Filter by Each Stage ---
            print("\n[TEST 5] Filter by Stages (Resetting other filters)...")
            await page.locator('.filter-chip[data-filter-group="element"][data-filter-value="all"]').click()
            await page.locator('.filter-chip[data-filter-group="role"][data-filter-value="all"]').click()
            for stage in ["Lumin Stage", "Gamma Stage", "Nova Stage"]:
                chip = page.locator(f'.filter-chip[data-filter-group="stage"][data-filter-value="{stage}"]')
                await chip.click()
                await page.wait_for_timeout(300)
                st_count = await page.locator(".creature-card").count()
                print(f"  -> {stage} creatures: {st_count}")
                assert st_count > 0

            # Reset stage
            await page.locator('.filter-chip[data-filter-group="stage"][data-filter-value="all"]').click()

            # --- 6. Sort by Name ---
            print("\n[TEST 6] Sort by Name...")
            sort_select = page.locator("#sort")
            await sort_select.select_option("name_asc")
            await page.wait_for_timeout(300)
            first_name = await page.locator(".creature-name").first.text_content()
            print(f"  -> First creature sorted A-Z: {first_name} (starts with A/B)")
            assert first_name.startswith(("A", "B"))

            # --- 7. Detail View: Emberpup ---
            print("\n[TEST 7] Open Emberpup detail page...")
            await sort_select.select_option("number_asc")
            await page.wait_for_timeout(300)
            emberpup_card = page.locator('.creature-card[href="#item=10002767"]')
            await emberpup_card.click()
            await page.wait_for_timeout(500)
            
            # Verify detail contents
            title = await page.locator(".hero-title").text_content()
            overview = await page.locator(".hero-desc").text_content()
            evo_nodes = await page.locator(".evo-node").count()
            habitats = await page.locator(".habitats-list li").count()
            skills = await page.locator(".skill").count()
            print(f"  -> Detail Title: {title.strip()[:30]}")
            print(f"  -> Overview: {overview.strip()[:50]}...")
            print(f"  -> Evolution Nodes: {evo_nodes}, Habitats: {habitats}, Skills: {skills}")
            assert "Emberpup" in title
            assert evo_nodes >= 2
            assert habitats >= 1
            assert skills >= 2

            # --- 8. Next and Previous Navigation ---
            print("\n[TEST 8] Test Next and Previous navigation...")
            next_btn = page.locator(".next-btn")
            await next_btn.click()
            await page.wait_for_timeout(400)
            next_title = await page.locator(".hero-title").text_content()
            print(f"  -> After Next clicked: {next_title.strip()[:30]}")
            assert "Flameruff" in next_title

            prev_btn = page.locator(".prev-btn")
            await prev_btn.click()
            await page.wait_for_timeout(400)
            prev_title = await page.locator(".hero-title").text_content()
            print(f"  -> After Prev clicked: {prev_title.strip()[:30]}")
            assert "Emberpup" in prev_title

            # --- 9. Navigation Back to Catalog ---
            print("\n[TEST 9] Back to catalog navigation...")
            back_btn = page.locator(".nav-back")
            await back_btn.click()
            await page.wait_for_timeout(400)
            catalog_cards = await page.locator(".creature-card").count()
            print(f"  -> Back to catalog, total cards: {catalog_cards}")
            assert catalog_cards == 94

            # --- 10. Direct URL refresh for a detail page ---
            print("\n[TEST 10] Direct reload of detail URL...")
            await page.goto(f"{BASE_URL}/#item=10002688", wait_until="networkidle")
            await page.wait_for_timeout(400)
            eklue_title = await page.locator(".hero-title").text_content()
            print(f"  -> Direct URL loaded creature: {eklue_title.strip()[:30]}")
            assert "Eklue" in eklue_title

            # --- 11. Responsive Tablet View (768px) ---
            print("\n[TEST 11] Tablet 768px viewport...")
            page_tablet = await browser.new_page(viewport={"width": 768, "height": 1024})
            await page_tablet.goto(f"{BASE_URL}/", wait_until="networkidle")
            tablet_cols = await page_tablet.eval_on_selector(".grid", "el => window.getComputedStyle(el).gridTemplateColumns.split(' ').length")
            print(f"  -> Tablet grid columns: {tablet_cols} (Expected 4 to 6)")
            assert 4 <= tablet_cols <= 6
            await page_tablet.close()

            # --- 12. Responsive Mobile View (390px) ---
            print("\n[TEST 12] Mobile 390px viewport...")
            page_mobile = await browser.new_page(viewport={"width": 390, "height": 844})
            await page_mobile.goto(f"{BASE_URL}/", wait_until="networkidle")
            mobile_cols = await page_mobile.eval_on_selector(".grid", "el => window.getComputedStyle(el).gridTemplateColumns.split(' ').length")
            print(f"  -> Mobile grid columns: {mobile_cols} (Expected 3)")
            assert mobile_cols == 3
            
            # Check horizontal overflow
            scroll_width = await page_mobile.evaluate("() => document.documentElement.scrollWidth")
            inner_width = await page_mobile.evaluate("() => window.innerWidth")
            print(f"  -> Scroll width: {scroll_width}, Inner width: {inner_width}")
            assert scroll_width <= inner_width + 1, "No horizontal scroll allowed on mobile!"
            await page_mobile.close()

            # --- 13. Back to Top Button ---
            print("\n[TEST 13] Back to top button...")
            await page.goto(f"{BASE_URL}/", wait_until="networkidle")
            await page.evaluate("() => window.scrollTo(0, 1000)")
            await page.wait_for_timeout(400)
            to_top_visible = await page.locator("#to-top.visible").count()
            print(f"  -> Back to top button visible on scroll: {to_top_visible == 1}")
            assert to_top_visible == 1
            await page.locator("#to-top").click()
            await page.wait_for_timeout(600)
            scroll_y = await page.evaluate("() => window.scrollY")
            print(f"  -> Scroll position after click: {scroll_y}")
            assert scroll_y < 50

            # --- 14. Check Console Errors ---
            print("\n[TEST 14] Console errors check...")
            print(f"  -> Total console errors: {len(console_errors)}")
            assert len(console_errors) == 0, f"Found console errors: {console_errors}"

            print("\n" + "=" * 60)
            print("🎉 ALL 14 AUTOMATED VALIDATION CHECKS PASSED WITH 100% SUCCESS!")
            print("=" * 60)

            await browser.close()
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_tests())
