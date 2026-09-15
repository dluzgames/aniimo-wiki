import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        page = await browser.new_page()

        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(f"FAILED: {req.url} -> {req.failure}"))

        print("Navigating to http://localhost:8080/ ...")
        await page.goto("http://localhost:8080/", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        print("\n=== CONSOLE LOGS ===")
        for log in console_logs:
            print(" ", log)

        print("\n=== FAILED REQUESTS ===")
        for req in failed_requests:
            print(" ", req)

        # Check rendered images
        imgs = await page.eval_on_selector_all('img', 'els => els.map(e => ({ src: e.src, visible: e.offsetParent !== null }))')
        print(f"\nTotal <img> tags in DOM: {len(imgs)}")
        for img in imgs[:15]:
            print("  IMG:", img)

        # Check .aniimo-item-container
        cards = await page.eval_on_selector_all('.aniimo-item-container', 'els => els.length')
        print(f"\nTotal .aniimo-item-container: {cards}")
        
        # Check first card HTML
        first_card = await page.eval_on_selector('.aniimo-item-container', 'el => el.innerHTML')
        print("\nFirst card innerHTML:")
        print(first_card)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
