import requests
from bs4 import BeautifulSoup
import csv, time, os

BASE_URL = 'https://books.toscrape.com/catalogue/'
START_URL = 'https://books.toscrape.com/catalogue/page-1.html'
OUTPUT_CSV = 'scraped_books.csv'
MAX_PAGES = 5

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 Chrome/120.0 Safari/537.36'
    )
}

RATING_MAP = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}

# ---- Scrape a single page ---------------------------------
def scrape_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'[ERROR] {url}: {e}')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    data = []
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').get_text(strip=True)
        rating = RATING_MAP.get(
            book.find('p', class_='star-rating')['class'][1], 0)
        avail = book.find('p', class_='instock').get_text(strip=True)

        data.append({
            'title': title,
            'price': price,
            'rating': rating,
            'availability': avail
        })

    return data

# ---- Get next page URL ------------------------------------
def get_next_page(soup):
    nxt = soup.find('li', class_='next')
    return BASE_URL + nxt.a['href'] if nxt else None

# ---- Main scraper loop ------------------------------------
def run_scraper():
    all_books = []
    url = START_URL
    page = 1

    print(f'Scraping up to {MAX_PAGES} pages...')

    while url and page <= MAX_PAGES:
        print(f'Page {page}: {url}')

        books = scrape_page(url)
        all_books.extend(books)

        print(f'+{len(books)} books | Total: {len(all_books)}')

        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')

        url = get_next_page(soup)
        page += 1

        time.sleep(1)

    return all_books

# ---- Save to CSV ------------------------------------------
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f, fieldnames=['title','price','rating','availability'])
        writer.writeheader()
        writer.writerows(data)

    print(f'Saved {len(data)} books to {filename}')
    print(f'Path: {os.path.abspath(filename)}')

# ---- Run --------------------------------------------------
if __name__ == '__main__':
    books = run_scraper()
    save_to_csv(books, OUTPUT_CSV)
    print(f'\nDone! Total: {len(books)} books scraped.')