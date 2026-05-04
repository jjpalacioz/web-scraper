# 📚 Books Web Scraper

A clean, beginner-friendly Python web scraper that extracts structured book data from [books.toscrape.com](https://books.toscrape.com) — a publicly available sandbox site built for scraping practice.

---

## 📌 Project Description

This scraper navigates all 50 catalogue pages of `books.toscrape.com`, collecting the following fields for every book:

| Field          | Description                          | Example             |
|----------------|--------------------------------------|---------------------|
| `title`        | Full book title                      | A Light in the Attic |
| `price`        | Listed price (GBP)                   | £51.77              |
| `rating`       | Star rating (1–5)                    | 3                   |
| `availability` | Stock status                         | In stock            |

Results are saved to a clean CSV file ready for analysis.

---

## 💡 Use Case

- Learning web scraping in Python
- Building a junior developer portfolio project
- Practicing data extraction and CSV export workflows
- Analysing book pricing or rating distributions

---

## 🛠️ Technologies

| Library          | Purpose                              |
|------------------|--------------------------------------|
| `requests`       | Send HTTP requests to fetch pages    |
| `BeautifulSoup4` | Parse HTML and navigate the DOM      |
| `csv` (stdlib)   | Write structured results to CSV      |
| `time` (stdlib)  | Polite delays between requests       |

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/jjpalacioz/web-scraper.git
cd web-scraper
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python scraper.py
```

The scraper will print progress to the terminal and save all results to **`output.csv`**.

---

## 📂 Project Structure

```
web-scraper/
├── scraper.py        # Main scraper script
├── output.csv        # Example output (20 sample records)
├── requirements.txt  # Pinned Python dependencies
└── README.md         # This file
```

---

## 📊 Example Output

```
============================================================
  Books to Scrape — Web Scraper
  Target: https://books.toscrape.com
============================================================
Scraping page 1: https://books.toscrape.com/catalogue/page-1.html
  → found 20 books (total so far: 20)
Scraping page 2: https://books.toscrape.com/catalogue/page-2.html
  → found 20 books (total so far: 40)
...
✓ Saved 1000 books to 'output.csv'

Sample output (first 3 records):
  {'title': 'A Light in the Attic', 'price': '£51.77', 'rating': 3, 'availability': 'In stock'}
  {'title': 'Tipping the Velvet',   'price': '£53.74', 'rating': 1, 'availability': 'In stock'}
  {'title': 'Soumission',           'price': '£50.10', 'rating': 1, 'availability': 'In stock'}
```

The first few rows of `output.csv`:

```
title,price,rating,availability
A Light in the Attic,£51.77,3,In stock
Tipping the Velvet,£53.74,1,In stock
Soumission,£50.10,1,In stock
Sharp Objects,£47.82,4,In stock
Sapiens: A Brief History of Humankind,£54.23,5,In stock
```

---

## 🛡️ Error Handling

The scraper gracefully handles:

- **Connection errors** — prints a descriptive message and stops cleanly
- **Timeouts** — 10-second request timeout with a clear error message
- **HTTP errors** (4xx/5xx) — logged and execution stops
- **Missing HTML elements** — defaults to `"N/A"` instead of crashing

---

## 🔧 Customisation

| Option            | Location in `scraper.py`      | Default |
|-------------------|-------------------------------|---------|
| Output filename   | `OUTPUT_FILE`                 | `output.csv` |
| Request timeout   | `get_page()` — `timeout=`     | 10 s    |
| Delay between pages | `REQUEST_DELAY`             | 0.5 s   |
| Max pages to scrape | `scrape_all_books(max_pages=)` | All (50) |

---

## 📜 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
