# Ekantipur Scraper

A Playwright-based web scraper that extracts entertainment news and cartoon of the day from [ekantipur.com](https://ekantipur.com).

## What it does

- Scrapes top 5 articles from the entertainment section with title, image, category and author
- Scrapes the Cartoon of the Day with title, image and cartoonist name
- Saves everything to `output.json`

## Project Structure
```
ekantipur-scraper/
├── scraper.py        # main script
├── output.json       # scraped output
├── pyproject.toml    # project dependencies
└── prompts.txt       # prompts used with Cursor
```

## Setup

Install uv if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies and browser:
```bash
uv add playwright
uv run playwright install chromium
```

## Run
```bash
uv run python scraper.py
```

Output will be saved to `output.json`.

## Output Format
```json
{
  "entertainment_news": [
    {
      "title": "...",
      "image_url": "https://...",
      "category": "मनोरञ्जन",
      "author": "..."
    }
  ],
  "cartoon_of_the_day": {
    "title": "...",
    "image_url": "https://...",
    "author": "..."
  }
}
```

## Notes

- Scrolls to bottom of page before scraping to trigger lazy-loaded images
- Author field is `null` if not available on the article
- JSON is saved with `ensure_ascii=False` to preserve Nepali unicode text
