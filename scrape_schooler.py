"""Login to schooler.biz and save the page content to a file.

Usage:
    pip install playwright
    playwright install chromium
    python scrape_schooler.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://my.schooler.biz/s/74985/easytheory/aoa_EJQ"
EMAIL = "orikaynan@gmail.com"
PASSWORD = "Rd!^4HZj"
OUTPUT_FILE = Path("page_content.html")
TEXT_FILE = Path("page_content.txt")


def run() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(URL, wait_until="networkidle")

        # The portal usually redirects to a login form. Fill it in.
        # Try a few common selectors so the script keeps working if the
        # markup changes slightly.
        email_selectors = [
            'input[type="email"]',
            'input[name="email"]',
            'input[name="username"]',
            'input[id*="email" i]',
        ]
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[id*="password" i]',
        ]
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Sign in")',
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'button:has-text("התחבר")',
            'button:has-text("כניסה")',
        ]

        def first_visible(selectors):
            for sel in selectors:
                loc = page.locator(sel).first
                try:
                    if loc.count() and loc.is_visible():
                        return loc
                except Exception:
                    continue
            return None

        email_box = first_visible(email_selectors)
        password_box = first_visible(password_selectors)

        if email_box and password_box:
            email_box.fill(EMAIL)
            password_box.fill(PASSWORD)

            submit = first_visible(submit_selectors)
            if submit:
                submit.click()
            else:
                password_box.press("Enter")

            page.wait_for_load_state("networkidle")

            # If the login redirected away from the target page, navigate back.
            if URL not in page.url:
                page.goto(URL, wait_until="networkidle")
        else:
            print("Login form not detected — saving the page as-is.")

        html = page.content()
        text = page.evaluate("() => document.body.innerText")

        OUTPUT_FILE.write_text(html, encoding="utf-8")
        TEXT_FILE.write_text(text, encoding="utf-8")

        print(f"Saved HTML to {OUTPUT_FILE.resolve()}")
        print(f"Saved text to {TEXT_FILE.resolve()}")
        print(f"Final URL: {page.url}")

        browser.close()


if __name__ == "__main__":
    run()
