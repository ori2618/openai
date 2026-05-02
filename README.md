# schooler.biz scraper

Python script that logs into a schooler.biz page, downloads the rendered
content, and saves it to disk.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
python scrape_schooler.py
```

The script writes two files in the current directory:

- `page_content.html` — the full rendered HTML of the target page.
- `page_content.txt` — the visible text only (`document.body.innerText`).

## Notes

- Credentials are hard-coded at the top of `scrape_schooler.py`. Move them
  to environment variables before committing to a shared repo.
- The login form selectors are a best-effort guess; if schooler.biz changes
  its markup, update the `email_selectors` / `password_selectors` lists.
- Set `headless=False` in `scrape_schooler.py` to watch the browser run,
  which is helpful for debugging the login flow.
