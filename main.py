import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urljoin

def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

def crawl_website(start_url, max_depth=3):
    visited_urls = set()
    queue = [(start_url, 0)]

    try:
        while queue:
            current_url, depth = queue.pop(0)

            if current_url not in visited_urls and depth <= max_depth:
                print(f"crawling: {current_url}")

                links = get_all_links(current_url)
                visited_urls.add(current_url)

                for link in links:
                    absolute_url = urljoin(current_url, link)
                    if urlparse(absolute_url).scheme in ('http', 'https'):
                        queue.append((absolute_url, depth + 1))

    except Exception as e:
        print(f"Error during crawling: {e}")

    return visited_urls

if __name__ == "__main__":
    start_url = "https://gglvxd.eu.org"
    max_depth = 3

    crawled_urls = crawl_website(start_url, max_depth)

    with open("urls.json", "w") as json_file:
            json.dump(list(crawled_urls), json_file, indent=2)
    print("Crawled URLs saved to urls.json")

    print(f"Error saving crawled URLs to urls.json")
