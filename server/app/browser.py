from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import os
from app.swiggy.categories import store_ids,categories,swiggy_api,extract_slug_from_url
import dotenv
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from datetime import datetime
from app.zepto.scrape import scrape_xml_urls
import aiohttp
import bs4
import gzip
from app.bigbasket.scrap import scrape_xml_urls_bigbasket
from app.schemas import get_db
from pymongo.errors import BulkWriteError
from fastapi import HTTPException
from bson import ObjectId
dotenv.load_dotenv()
from collections import defaultdict

def initialize_browser(download_dir:str=None):
    """Initialize a headless Chrome browser instance."""
    try:
        if download_dir is None:
            download_dir = os.path.abspath("./app/data/blinkit")
       
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")  # Ensures browser runs in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
})
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to initialize browser: {str(e)}")
        raise

async def process_zepto():
    driver = initialize_browser()
    logging.info("Initializing browser")
    xml_url = "https://www.zeptonow.com/sitemap/brands.xml"
    driver.get(xml_url)
    time.sleep(10)
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    
    brands, urls = scrape_xml_urls(soup=soup)
    driver.quit()
    
    # Insert into MongoDB
    db = get_db()
    brands_to_insert = [
        {
            "brand_name": brand,
            "brand_url": urls[brand],
            "brand_created_at": datetime.now()
        }
        for brand in brands
    ]
    
    try:
        result = db.zepto_brands.insert_many(brands_to_insert, ordered=False)
        return {
            "message": "Zepto brands processed successfully",
            "total_brands": len(brands),
            "inserted_count": len(result.inserted_ids),
            "duplicate_count": 0
        }
    except BulkWriteError as bwe:
        return {
            "message": "Zepto brands processed with some duplicates",
            "total_brands": len(brands),
            "inserted_count": bwe.details.get('nInserted', 0),
            "duplicate_count": len(bwe.details.get('writeErrors', []))
        }
    except Exception as e:
        logging.error(f"Error processing zepto brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.admin_data.update_one(
            {"user": "admin"},
            {"$set": {"last_zepto_scrape": datetime.now()}}
        )

async def process_blinkit():
    driver = initialize_browser()
    logging.info("Initializing browser")
    driver.get("https://blinkit.com/brands.xml")
    time.sleep(10)
    
    # Load the XML content
    with open("app/data/blinkit/brands.xml", "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Parse XML
    root = ET.fromstring(xml_content)

    # Define the namespace
    ns = {
        "ns": "http://www.sitemaps.org/schemas/sitemap/0.9"
    }

    # Extract brand names from <loc> elements
    brands = set()
    urls = {}
    for loc in root.findall("ns:url/ns:loc", ns):
        url = loc.text.strip()
        path = urlparse(url).path
        slug = path.split("/")[-1]
        if slug:  # skip empty ones
            brands.add(slug)
            urls[slug] = url
    
    driver.quit()
    os.remove("app/data/blinkit/brands.xml")
    
    # Insert into MongoDB
    db = get_db()
    brands_to_insert = [
        {
            "brand_name": brand,
            "brand_url": urls[brand],
            "brand_created_at": datetime.now()
        }
        for brand in brands
    ]
    try:
        result = db.blinkit_brands.insert_many(brands_to_insert, ordered=False)
        return {
            "message": "Blinkit brands processed successfully",
            "total_brands": len(brands),
            "inserted_count": len(result.inserted_ids),
            "duplicate_count": 0
        }
    except BulkWriteError as bwe:
        return {
            "message": "Blinkit brands processed with some duplicates",
            "total_brands": len(brands),
            "inserted_count": bwe.details.get('nInserted', 0),
            "duplicate_count": len(bwe.details.get('writeErrors', []))
        }
    except Exception as e:
        logging.error(f"Error processing blinkit brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.admin_data.update_one(
            {"user": "admin"},
            {"$set": {"last_blinkit_scrape": datetime.now()}}
        )

async def process_bigbasket():
    driver = initialize_browser()
    logging.info("Initializing browser")
    driver.get("https://www.bigbasket.com/sitemap/brands.xml")
    time.sleep(10)
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    
    brands, urls = scrape_xml_urls_bigbasket(soup=soup)
    driver.quit()
    
    # Insert into MongoDB
    db = get_db()
    brands_to_insert = [
        {
            "brand_name": brand,
            "brand_url": urls[brand],
            "brand_created_at": datetime.now()
        }
        for brand in brands
    ]
    try:
        result = db.bigbasket_brands.insert_many(brands_to_insert, ordered=False)
        return {
            "message": "BigBasket brands processed successfully",
            "total_brands": len(brands),
            "inserted_count": len(result.inserted_ids),
            "duplicate_count": 0
        }
    except BulkWriteError as bwe:
        return {
            "message": "BigBasket brands processed with some duplicates",
            "total_brands": len(brands),
            "inserted_count": bwe.details.get('nInserted', 0),
            "duplicate_count": len(bwe.details.get('writeErrors', []))
        }
    except Exception as e:
        logging.error(f"Error processing bigbasket brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.admin_data.update_one(
            {"user": "admin"},
            {"$set": {"last_bigbasket_scrape": datetime.now()}}
        )
async def process_swiggy():
    download_dir = os.path.abspath("./app/data/swiggy")
    driver = initialize_browser(download_dir)
    logging.info("Initializing browser")
    driver.get("https://www.swiggy.com/instamart/sitemap/brand-sitemap.xml.gz")
    time.sleep(10)
    index_file = os.path.join("app/data/swiggy/brand-sitemap.xml.gz")
    with gzip.open(index_file, 'rt', encoding='utf-8') as f:
        root = ET.parse(f).getroot()

    # Get namespaces
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = [el.text for el in root.findall("ns:sitemap/ns:loc", ns)]

    brands = set()
    urls = {}
    
    for sitemap_url in sitemap_urls:
        driver.get(sitemap_url)
        time.sleep(5)
        file_name = sitemap_url.split("/")[-1]
        file_path = os.path.join("app/data/swiggy/"+file_name)
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            root = ET.parse(f).getroot()
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    
        for loc in root.findall("ns:url/ns:loc", ns):
            url = loc.text.strip()
            if "/b/" in url and not "/cb/" in url:
                slug = extract_slug_from_url(url)
                if slug:
                    brands.add(slug)
                    urls[slug] = url
        os.remove(file_path)

    os.remove("app/data/swiggy/brand-sitemap.xml.gz")
    driver.quit()
    
    # Insert into MongoDB
    db = get_db()
    brands_to_insert = [
        {
            "brand_name": brand,
            "brand_url": urls[brand],
            "brand_created_at": datetime.now()
        }
        for brand in brands
    ]
    try:
        result = db.swiggy_brands.insert_many(brands_to_insert, ordered=False)
        return {
            "message": "Swiggy brands processed successfully",
            "total_brands": len(brands),
            "inserted_count": len(result.inserted_ids),
            "duplicate_count": 0
        }
    except BulkWriteError as bwe:
        return {
            "message": "Swiggy brands processed with some duplicates",
            "total_brands": len(brands),
            "inserted_count": bwe.details.get('nInserted', 0),
            "duplicate_count": len(bwe.details.get('writeErrors', []))
        }
    except Exception as e:
        logging.error(f"Error processing swiggy brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.admin_data.update_one(
            {"user": "admin"},
            {"$set": {"last_swiggy_scrape": datetime.now()}}
        )

async def get_zepto_brands():
    db = get_db()
    brands = db.zepto_brands.find()
    return [{
        "id": str(brand["_id"]),
        "brand_name": brand["brand_name"],
        "brand_url": brand["brand_url"],
        "brand_created_at": brand["brand_created_at"].isoformat() if brand["brand_created_at"] else None
    } for brand in brands]

async def get_blinkit_brands():
    db = get_db()
    brands = db.blinkit_brands.find()
    return [{
        "id": str(brand["_id"]),
        "brand_name": brand["brand_name"],
        "brand_url": brand["brand_url"],
        "brand_created_at": brand["brand_created_at"].isoformat() if brand["brand_created_at"] else None
    } for brand in brands]

async def get_bigbasket_brands():
    db = get_db()
    brands = db.bigbasket_brands.find()
    return [{
        "id": str(brand["_id"]),
        "brand_name": brand["brand_name"],
        "brand_url": brand["brand_url"],
        "brand_created_at": brand["brand_created_at"].isoformat() if brand["brand_created_at"] else None
    } for brand in brands]

def serialize_brand(brand, total_products=0):
    return {
        "id": str(brand["_id"]),
        "brand_name": brand.get("brand_name"),
        "brand_url": brand.get("brand_url"),
        "brand_created_at": brand.get("brand_created_at").isoformat() if brand.get("brand_created_at") else None,
        "total_products": total_products
    }

def get_enriched_swiggy_brands():
    db = get_db()

    # Step 1: Fetch all brands and products
    brands = db.swiggy_brands.find().to_list(length=None)
    products = db.swiggy_products.find().to_list(length=None)

    # Step 2: Build product count per normalized brand name
    product_count_map = defaultdict(set)  # brand-slug -> set of variant_ids

    for product in products:
        brand_name = product.get("brand_name", "")
        variant_id = product.get("variant_id")

        if brand_name and variant_id:
            normalized = brand_name.strip().replace(" ", "-").lower()
            product_count_map[normalized].add(variant_id)

    # Step 3: Attach total count to each brand
    enriched_brands = []

    for brand in brands:
        brand_name = brand.get("brand_name", "")
        normalized = brand_name.strip().replace(" ", "-").lower()

        total_products = len(product_count_map.get(normalized, set()))
        enriched_brands.append(serialize_brand(brand, total_products))

    return enriched_brands



    # db = get_db()
    # # brands = db.swiggy_brands.find()
    # # return [{
    # #     "id": str(brand["_id"]),
    # #     "brand_name": brand["brand_name"],
    # #     "brand_url": brand["brand_url"],
    # #     "brand_created_at": brand["brand_created_at"].isoformat() if brand["brand_created_at"] else None
    # # } for brand in brands]
    # brands =  db.swiggy_brands.find().to_list(length=None)
    # products = db.swiggy_products.find().to_list(length=None)

    # # Step 2: Normalize brand names and group products by brand_name (using variant_id to dedupe)
    # product_map = defaultdict(dict)  # brand_name -> {variant_id: product}

    # for product in products:
    #     brand_name = product.get("brand_name", "").strip().replace(" ", "-").lower()
    #     variant_id = product.get("variant_id")
    #     if brand_name and variant_id:
    #         if variant_id not in product_map[brand_name]:
    #             product_map[brand_name][variant_id] = product

    # # Step 3: Attach products to corresponding brands
    # enriched_brands = []

    # for brand in brands:
    #     normalized_name = brand.get("brand_name", "").strip().replace(" ", "-").lower()
    #     brand_with_products = {
    #         "_id": brand["_id"],
    #         "brand_name": brand["brand_name"],
    #         "brand_url": brand.get("brand_url"),
    #         "brand_created_at": brand.get("brand_created_at"),
    #         "products": list(product_map.get(normalized_name, {}).values())
    #     }
    #     enriched_brands.append(brand_with_products)

    # return enriched_brands