from bs4 import BeautifulSoup
import time
import logging

def scrape_xml_urls(soup):
    """Scrape brand URLs and names from XML sitemap"""
    logging.info("Scraping XML URLs")
        
        # Extract data
    data = []
    urls = {}
    for url_tag in soup.find_all('url'):
        loc = url_tag.find('loc')
        if loc:
            url = loc.text.strip()
            # Extract brand name from URL (assuming format: .../brand/BRAND_NAME/...)
            brand_name = url.split('/brand/')[-1].split('/')[0].replace('_', ' ')
            data.append(brand_name)
            urls[brand_name] = url

    
    return data, urls
