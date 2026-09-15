import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://aniimo.dluz.com.br"

async def test_prod():
    print("=" * 60)
    print(f"🧪 TESTING LIVE REPLICA AT {BASE_URL}")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )

        # 1. Desktop 1440px
        print("\n[TEST 1] Desktop 1440px Viewport...")
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

        await page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
        cards = await page.locator(".creature-card").count()
        print(f"  -> Total cards: {cards}")
        assert cards == 94, f"Expected 94, got {cards}"

        grid_cols = await page.eval_on_selector(".grid", "el => window.getComputedStyle(el).gridTemplateColumns.split(' ').length")
        print(f"  -> Grid columns: {grid_cols}")
        assert grid_cols == 7

        # 2. Search Emberpup
        print("\n[TEST 2] Search Emberpup...")
        await page.locator("#search").fill("Emberpup")
        await page.wait_for_timeout(300)
        sc = await page.locator(".creature-card").count()
        print(f"  -> Search count: {sc}")
        assert sc == 1
        await page.locator("#search").fill("")
        await page.wait_for_timeout(300)

        # 3. Filter Fire + DPS
        print("\n[TEST 3] Filter Fire + DPS...")
        await page.locator('.filter-chip[data-filter-group="element"][data-filter-value="fire"]').click()
        await page.locator('.filter-chip[data-filter-group="role"][data-filter-value="dps"]').click()
        await page.wait_for_timeout(300)
        fd_count = await page.locator(".creature-card").count()
        print(f"  -> Fire + DPS count: {fd_count}")
        assert fd_count == 4

        # Reset filters
        await page.locator('.filter-chip[data-filter-group="element"][data-filter-value="all"]').click()
        await page.locator('.filter-chip[data-filter-group="role"][data-filter-value="all"]').click()
        await page.wait_for_timeout(300)

        # 4. Detail View: Emberpup
        print("\n[TEST 4] Open Emberpup detail...")
        await page.locator('.creature-card[href="#item=10002767"]').click()
        await page.wait_for_timeout(400)
        title = await page.locator(".hero-title").text_content()
        overview = await page.locator(".hero-desc").text_content()
        evo_count = await page.locator(".evo-node").count()
        skill_count = await page.locator(".skill").count()
        print(f"  -> Title: {title.strip()[:30]}")
        print(f"  -> Overview: {overview.strip()[:40]}...")
        print(f"  -> Evolution Nodes: {evo_count}, Skills: {skill_count}")
        assert "Emberpup" in title
        assert evo_count == 4
        assert skill_count >= 2

        # 5. Direct Reload of Detail URL
        print("\n[TEST 5] Direct reload of detail page...")
        await page.goto(f"{BASE_URL}/#item=10002688", wait_until="domcontentloaded")
        await page.wait_for_timeout(400)
        eklue = await page.locator(".hero-title").text_content()
        print(f"  -> Loaded: {eklue.strip()[:30]}")
        assert "Eklue" in eklue

        # 6. Back to Catalog
        print("\n[TEST 6] Back to catalog...")
        await page.locator(".nav-back").click()
        await page.wait_for_timeout(400)
        back_cards = await page.locator(".creature-card").count()
        print(f"  -> Total cards after back: {back_cards}")
        assert back_cards == 94

        # 7. Mobile View 390px
        print("\n[TEST 7] Mobile 390px Viewport...")
        page_mobile = await browser.new_page(viewport={"width": 390, "height": 844})
        await page_mobile.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
        m_cols = await page_mobile.eval_on_selector(".grid", "el => window.getComputedStyle(el).gridTemplateColumns.split(' ').length")
        print(f"  -> Mobile grid columns: {m_cols}")
        assert m_cols == 3
        scroll_w = await page_mobile.evaluate("() => document.documentElement.scrollWidth")
        inner_w = await page_mobile.evaluate("() => window.innerWidth")
        print(f"  -> Scroll width: {scroll_w}, Inner: {inner_w}")
        assert scroll_w <= inner_w + 1
        await page_mobile.close()

        # 8. Console Errors
        print("\n[TEST 8] Console errors...")
        print(f"  -> Errors count: {len(console_errors)}")
        assert len(console_errors) == 0

        print("\n" + "=" * 60)
        print("🎉 LIVE PRODUCTION VALIDATION PASSED WITH 100% SUCCESS!")
        print("=" * 60)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_prod())
