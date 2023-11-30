# SSENSE Scraper

SSENSE Scraper is a  simple Python-based web scraping tool, utilizing BeautifulSoup and Requests, designed to extract product listing data from [SSENSE](https://www.ssense.com/). It allows users to specify categories like 'men' or 'women' and choose the number of pages to scrape, exporting the data in CSV format.

## Features
- Scrape product listings from SSENSE based on specified categories (men/women).
- Control the number of pages to scrape.
- Export data to CSV format.
- Extracted data fields include:
  - Brand
  - Description
  - Price in USD
  - Type (Men/Women)

## Installation
1. Clone the repository:
```
git clone https://github.com/justinpakzad/SSENSE-Scraper
```
2. Install required dependencies:
```cd ssense_scraper
pip install -r requirements.txt
```
## Command Line Options
- `--gender`: Specify the gender category to scrape ('men' or 'women', default: 'men').
- `--pages`: Limit the number of pages to scrape (default: 10).
- `-o`, `--output`: Specify the output file name (default output format is CSV).

## Example usage:
```
python ssense_scraper.py --gender women --pages 5
```
