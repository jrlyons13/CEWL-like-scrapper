import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import sys
import os
from datetime import datetime

visited_urls = set()
collected_words = set()

def is_same_domain(base_url, new_url):
    return urlparse(base_url).netloc == urlparse(new_url).netloc
  
def scrape_words_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        words = re.findall(r'\b[A-Za-z]{5,}\b', text)
        for word in words:
            collected_words.add(word.lower())
        return soup
    except Exception as e:
        print(f"[!] Error scraping {url}: {e}")
        return None
      
def crawl(url, depth, base_url):
    if depth == 0 or url in visited_urls:
        return
    visited_urls.add(url)
    print(f"[+] Visiting: {url}")
    soup = scrape_words_from_url(url)
    if not soup:
        return
    for link in soup.find_all('a', href=True):
        full_url = urljoin(url, link['href'])
        if is_same_domain(base_url, full_url) and full_url not in visited_urls:
            crawl(full_url, depth - 1, base_url)
          
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cewl_like_scraper.py <URL>")
        sys.exit(1)
      
    start_url = sys.argv[1]
    crawl(start_url, depth=2, base_url=start_url)
  
    # Create timestamped directory in home folder
    home_dir = os.path.expanduser("~")
    output_dir = os.path.join(home_dir, "cewl_wordlists", datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(output_dir, exist_ok=True)
  
    output_path = os.path.join(output_dir, "wordlist.txt")
    with open(output_path, "w") as f:
        for word in sorted(collected_words):
            f.write(word + "\n")
          
    print(f"\n[:heavy_check_mark:] Wordlist saved to {output_path} — {len(collected_words)} unique words collected.")
