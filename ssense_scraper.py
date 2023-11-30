import requests
import argparse
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0",
]


def get_url(base_url, gender="men", num_pages=1):
    # Construct URL
    url = f"{base_url}{gender}?page={num_pages}"
    return url


def get_response(url, headers):
    # Get response
    response = requests.get(url, headers=headers)
    return response


def parse(response):
    # Parse data
    items_list = []
    soup = BeautifulSoup(response.content, "html.parser")
    product_tiles = soup.find_all("div", class_="plp-products__product-tile")
    for product in product_tiles:
        item_attributes = product.find_all("span", class_="s-text")
        brand = (
            item_attributes[0].text.strip()
            if item_attributes and len(item_attributes) > 0
            else "Brand not available"
        )
        description = (
            item_attributes[1].text.strip()
            if item_attributes and len(item_attributes) > 1
            else "Description not available"
        )
        price_usd = (
            item_attributes[2].text.strip().split("$")[1]
            if item_attributes and len(item_attributes) > 2
            else "Price not available"
        )
        items_d = {"brand": brand, "description": description, "price_usd": price_usd}
        items_list.append(items_d)
    return items_list


def get_all_pages(base_url, headers, num_pages=10, gender="men"):
    # Get all pages
    all_items = []
    for page_number in tqdm(range(1, num_pages + 1), desc="Scraping pages"):
        current_url = get_url(base_url, gender, page_number)

        response = get_response(current_url, headers)

        if response.ok:
            page_items = parse(response)
            all_items.extend(page_items)
        else:
            print(f"Failed to get data from page {page_number}")
        time.sleep(random.randint(1, 3))
    return all_items


def main():
    parser = argparse.ArgumentParser(description="Scrape SSENSE website.")
    parser.add_argument(
        "--gender",
        type=str,
        default="men",
        choices=["men", "women"],
        help="Gender category to scrape. Options: 'men', 'women'. Default is 'men'.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=10,
        help="Number of pages to scrape. Default is 10.",
    )
    args = parser.parse_args()
    user_agent = random.choice(user_agents)
    headers = {"User-Agent": user_agent}
    base_url = "https://www.ssense.com/en-us/"

    all_products = get_all_pages(
        base_url, headers, num_pages=args.pages, gender=args.gender
    )

    all_products_df = pd.DataFrame(all_products)

    all_products_df.to_csv(f"ssense_{args.gender}.csv", index=False)


if __name__ == "__main__":
    main()
