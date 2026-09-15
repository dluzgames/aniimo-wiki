import asyncio
from playwright.async_api import async_playwright

async def run():
    print("============================================================")
    print("🌐 VALIDATING PRODUCTION DEPLOYMENT AT aniimo.dluz.com.br")
    print("============================================================")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel="msedge")
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # 1. Test Home Page
        print("\n[1] Testing Home Page: https://aniimo.dluz.com.br/ ...")
        resp = await page.goto("https://aniimo.dluz.com.br/", wait_until="networkidle", timeout=30000)
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        
        # Check PT default
        placeholder = await page.get_attribute("#search-input", "placeholder")
        lang_btn_text = await page.inner_text("#btn-lang-toggle")
        grid_count = await page.locator(".creature-card").count()
        print(f" -> Status: {resp.status}")
        print(f" -> Search placeholder: '{placeholder}' (Expected Portuguese)")
        print(f" -> Active Language Button: '{lang_btn_text}'")
        print(f" -> Creature Cards Rendered: {grid_count} (Expected 94)")
        assert "Buscar por nome" in placeholder, f"Unexpected placeholder: {placeholder}"
        assert grid_count == 94, f"Expected 94 cards, found {grid_count}"
        await page.screenshot(path="production_home_pt.png")
        print(" -> Screenshot saved to production_home_pt.png")

        # 2. Test Direct Creature URL: https://aniimo.dluz.com.br/inferlupa
        print("\n[2] Testing Direct Slug URL: https://aniimo.dluz.com.br/inferlupa ...")
        resp2 = await page.goto("https://aniimo.dluz.com.br/inferlupa", wait_until="networkidle", timeout=30000)
        assert resp2.status == 200, f"Expected 200, got {resp2.status}"
        await page.wait_for_selector(".creature-detail-view", state="visible", timeout=10000)
        
        detail_name = await page.inner_text(".creature-detail-name")
        detail_desc = await page.inner_text(".creature-detail-desc")
        detail_role = await page.inner_text(".detail-stat-val")
        print(f" -> Status: {resp2.status}")
        print(f" -> Detail Creature Name: '{detail_name}' (Expected 'Inferlupa')")
        print(f" -> Detail Description (PT): '{detail_desc[:80]}...'")
        print(f" -> Current URL in Browser: '{page.url}'")
        assert "Inferlupa" in detail_name, f"Expected Inferlupa, got {detail_name}"
        assert page.url.endswith("/inferlupa"), f"URL did not match: {page.url}"
        await page.screenshot(path="production_inferlupa.png")
        print(" -> Screenshot saved to production_inferlupa.png")

        # 3. Test Navigation: Back to Catalog
        print("\n[3] Testing Navigation: Back to Catalog from Inferlupa...")
        back_btn = page.locator(".back-btn")
        await back_btn.click()
        await page.wait_for_selector(".creatures-grid", state="visible")
        print(f" -> URL after back click: '{page.url}'")
        assert not page.url.endswith("/inferlupa"), "URL still contains slug after back"

        # 4. Test Direct Slug URL: https://aniimo.dluz.com.br/emberpup
        print("\n[4] Testing Direct Slug URL: https://aniimo.dluz.com.br/emberpup ...")
        resp3 = await page.goto("https://aniimo.dluz.com.br/emberpup", wait_until="networkidle", timeout=30000)
        assert resp3.status == 200, f"Expected 200, got {resp3.status}"
        await page.wait_for_selector(".creature-detail-view", state="visible", timeout=10000)
        ember_name = await page.inner_text(".creature-detail-name")
        print(f" -> Detail Creature Name: '{ember_name}' (Expected 'Emberpup')")
        print(f" -> Current URL: '{page.url}'")
        assert "Emberpup" in ember_name, f"Expected Emberpup, got {ember_name}"
        await page.screenshot(path="production_emberpup.png")
        print(" -> Screenshot saved to production_emberpup.png")

        await browser.close()
        print("\n🎉 ALL PRODUCTION TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    asyncio.run(run())
