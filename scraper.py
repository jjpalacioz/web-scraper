"""
scraper.py
----------
Web scraper that extracts book data (title, price, rating, availability)
from https://books.toscrape.com — a sandbox site built for scraping practice.

Libraries used:
  - requests     : sends HTTP GET requests to fetch page HTML
  - BeautifulSoup: parses the HTML and lets us navigate the DOM
  - csv          : writes the structured results to a CSV file
"""

import csv
import time

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT_FILE = "output.csv"

# Map the word-based star ratings the site uses to numeric values
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

# CSV column headers
CSV_HEADERS = ["title", "price", "rating", "availability"]

# Polite delay (seconds) between page requests so we don't hammer the server
REQUEST_DELAY = 0.5


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_page(url: str) -> BeautifulSoup | None:
    """Fetch a URL and return a BeautifulSoup object, or None on failure."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises HTTPError for 4xx / 5xx responses
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Could not connect to {url}. Check your internet connection.")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request to {url} timed out.")
    except requests.exceptions.HTTPError as exc:
        print(f"[ERROR] HTTP error for {url}: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Unexpected request error for {url}: {exc}")
    return None


def parse_books(soup: BeautifulSoup) -> list[dict]:
    """
    Extract book data from a single catalogue page.

    Each <article class="product_pod"> element represents one book.
    Returns a list of dicts with keys: title, price, rating, availability.
    """
    books = []

    for article in soup.select("article.product_pod"):
        # --- Title ---
        # The full title is stored in the 'title' attribute of the <a> tag
        # inside the <h3> element (the visible text is often truncated).
        title_tag = article.select_one("h3 > a")
        title = title_tag["title"].strip() if title_tag and title_tag.get("title") else "N/A"

        # --- Price ---
        price_tag = article.select_one("p.price_color")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        # --- Star rating ---
        # The rating is encoded as a CSS class, e.g. <p class="star-rating Three">
        rating_tag = article.select_one("p.star-rating")
        if rating_tag:
            # The second class is the word rating (e.g. "Three")
            rating_word = rating_tag["class"][1] if len(rating_tag["class"]) > 1 else "N/A"
            rating = RATING_MAP.get(rating_word, "N/A")
        else:
            rating = "N/A"

        # --- Availability ---
        availability_tag = article.select_one("p.availability")
        availability = availability_tag.get_text(strip=True) if availability_tag else "N/A"

        books.append(
            {
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
            }
        )

    return books


def get_next_page_url(soup: BeautifulSoup) -> str | None:
    """
    Look for the 'next' button on the page and return its absolute URL,
    or None if we are on the last page.
    """
    next_btn = soup.select_one("li.next > a")
    if next_btn:
        return BASE_URL + next_btn["href"]
    return None


def scrape_all_books(max_pages: int | None = None) -> list[dict]:
    """
    Iterate through every catalogue page and collect all book records.

    Parameters
    ----------
    max_pages : int or None
        Stop after this many pages (useful for testing). Pass None to scrape
        all pages.

    Returns
    -------
    list[dict]
        Every book found, each represented as a dict.
    """
    all_books: list[dict] = []
    current_url: str | None = START_URL
    page_number = 0

    while current_url:
        page_number += 1
        print(f"Scraping page {page_number}: {current_url}")

        soup = get_page(current_url)
        if soup is None:
            # get_page already printed an error; stop scraping gracefully
            break

        books_on_page = parse_books(soup)
        all_books.extend(books_on_page)
        print(f"  → found {len(books_on_page)} books (total so far: {len(all_books)})")

        # Respect max_pages limit when set
        if max_pages and page_number >= max_pages:
            break

        current_url = get_next_page_url(soup)

        # Be polite: wait a little before the next request
        if current_url:
            time.sleep(REQUEST_DELAY)

    return all_books


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------


def save_to_csv(books: list[dict], filepath: str) -> None:
    """Write a list of book dicts to a CSV file."""
    if not books:
        print("[WARNING] No data to save.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(books)

    print(f"\n✓ Saved {len(books)} books to '{filepath}'")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 60)
    print("  Books to Scrape — Web Scraper")
    print("  Target: https://books.toscrape.com")
    print("=" * 60)

    # Scrape all pages (set max_pages=N to limit during development/testing)
    books = scrape_all_books()

    if books:
        save_to_csv(books, OUTPUT_FILE)
        print(f"\nSample output (first 3 records):")
        for book in books[:3]:
            print(f"  {book}")
    else:
        print("[ERROR] No books were scraped. Please check the output above.")


if __name__ == "__main__":
    main()
