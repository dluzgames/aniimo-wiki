import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load official site
        print("Loading official site: https://wiki.aniimo.com/ ...")
        await page.goto("https://wiki.aniimo.com/", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # Find first card
        card_html = await page.eval_on_selector('.aniimo-item-container', 'el => el.outerHTML')
        print("\n=== BROWSER RENDERED CARD (OFFICIAL) ===")
        print(card_html[:1500])
        
        # Check computed styles or background-image of .aniimo-item-top-image
        bg_style = await page.eval_on_selector('.aniimo-item-top-image', 'el => window.getComputedStyle(el).backgroundImage')
        print("\nComputed background-image on .aniimo-item-top-image:", bg_style)
        
        # Find all img tags inside card
        imgs = await page.eval_on_selector_all('.aniimo-item-container img', 'els => els.map(e => e.src)')
        print("IMG tags inside card:", imgs)

        # Now test our local site
        print("\nLoading local site: http://localhost:8080/ ...")
        local_errors = []
        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))
        
        await page.goto("http://localhost:8080/", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        local_card_html = await page.eval_on_selector('.aniimo-item-container', 'el => el.outerHTML')
        print("\n=== BROWSER RENDERED CARD (LOCAL) ===")
        print(local_card_html[:1500])
        
        local_bg_style = await page.eval_on_selector('.aniimo-item-top-image', 'el => window.getComputedStyle(el).backgroundImage')
        print("\nComputed background-image on local .aniimo-item-top-image:", local_bg_style)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
