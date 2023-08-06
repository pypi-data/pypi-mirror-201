from playwright.sync_api import sync_playwright

def start(url=None, selector=None, wrapper=(lambda x: x), headless=True, at=1, stop=None):
    def page_nums():
        current = at
        while True:
            yield current
            if current == stop:
                break
            current += 1

    def fetch_elements(browser_page):
        for page_num in page_nums():
            page_url = url % page_num
            resp = browser_page.goto(page_url)
            if resp.status == 404:
                break
            for selected in browser_page.query_selector_all(selector):
                yield selected

    with (
        sync_playwright() as play,
        play.chromium.launch(headless=headless) as browser,
        browser.new_context() as ctx
        ):
        page = ctx.new_page()
        for element in fetch_elements(page):
            yield wrapper(element)