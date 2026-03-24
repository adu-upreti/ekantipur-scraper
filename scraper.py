import json

from playwright.sync_api import sync_playwright


def scrape_entertainment() -> dict[str, list[dict[str, str | None]]]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://ekantipur.com/entertainment")
        page.wait_for_selector("div.category-inner-wrapper")

        # grab category once from page header
        category_el = page.query_selector("div.category-name p a")
        category = category_el.text_content().strip() if category_el else None

        cards = page.query_selector_all("div.category-inner-wrapper")
        articles: list[dict[str, str | None]] = []

        for card in cards[:5]:
            title_el = card.query_selector("div.category-description h2 a")
            img_el = card.query_selector("div.category-image figure img")
            author_el = card.query_selector("div.author-name p a")

            articles.append(
                {
                    "title": title_el.text_content().strip() if title_el else None,
                    "image_url": img_el.get_attribute("src") if img_el else None,
                    "category": category,
                    "author": author_el.text_content().strip() if author_el else None,
                }
            )

        result = {"entertainment_news": articles}
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        browser.close()
        return result


def scrapr_cartoon() -> dict[str, str | None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://ekantipur.com/cartoon")
        page.wait_for_selector("div.cartoon-wrapper")

        card = page.query_selector("div.cartoon-wrapper")
        img_el = card.query_selector("div.cartoon-image figure img") if card else None
        desc_el = card.query_selector("div.cartoon-description p") if card else None

        text = desc_el.text_content().strip() if desc_el and desc_el.text_content() else ""
        parts = [part.strip() for part in text.split(" - ", 1)] if text else []
        title = parts[0] if len(parts) > 0 else None
        author = parts[1] if len(parts) > 1 else None

        result = {
            "title": title,
            "image_url": img_el.get_attribute("src") if img_el else None,
            "author": author,
        }
        browser.close()
        return result


if __name__ == "__main__":
    entertainment = scrape_entertainment()
    cartoon = scrapr_cartoon()

    entertainment["cartoon_of_the_day"] = cartoon
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(entertainment, f, ensure_ascii=False, indent=2)