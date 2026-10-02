import logging
import time
import aiohttp
from app.browser import initialize_browser
from app.swiggy.categories import swiggy_api,categories,store_ids
from datetime import datetime
from app.database.create_db import create_instamart_products
from app.schemas import get_db
db = get_db()

async def process_swiggy_instamart_products():
    driver = initialize_browser()
    logging.info("Initializing browser")
    driver.get("https://www.swiggy.com/instamart")
    logging.info("Navigated to swiggy instamart")
    time.sleep(10)
    selenium_cookies = driver.get_cookies()
    logging.info("Got selenium cookies")
    cookie_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in selenium_cookies])
    headers = {
        "cookie":cookie_string,
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding":"gzip, deflate, br, zstd",
        "accept-language":"en-US,en;q=0.9,hi;q=0.8,gu;q=0.7",
        "Content-Type":"application/json",
        "if-none-match":"W/\"201e4-BA5Ztb/Q345x4qT1Wtlydm/bt3c\"",
        "matcher":"9fcbf8ebga7d9a8c8d99ddf",
        "referer": "https://www.swiggy.com/instamart/category-listing?categoryName=Atta,%20Rice%20and%20Dal&storeId=1402796&offset=0&filterName=&taxonomyType=Speciality%20taxonomy%201&showAgeConsent=false",
        "sec-ch-ua":"\"Google Chrome\";v=\"120\", \"Not_A Brand\";v=\"99\", \"Chromium\";v=\"120\"",
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"\"Windows\"",
        "sec-fetch-dest":"document",
        "sec-fetch-mode":"navigate",
        "sec-fetch-site":"same-origin",
        "sec-fetch-user":"?1",
    }
    products = []
    total_urls = 0
    for category in categories:
        logging.info(f"Processing category: {category}")
        for store in store_ids:
            city = store["location"]
            has_more = True
            offset = 0
            prev_url = ""
            while has_more:
                try:
                    time.sleep(1)
                    total_urls += 1
                    url = swiggy_api(category["name"],store["id"],offset)  # Change to your API URL
                    if url == prev_url:
                        has_more = False
                        break
                    prev_url = url
                    logging.info(f"Requesting URL: {url}")
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=headers) as response:
                            if 'application/json' in response.headers.get('Content-Type', ''):
                                response_json = await response.json()
                                widgets = response_json.get("data", {}).get("widgets", [])
                                if widgets:
                                    for widget in widgets:
                                        widget_data = widget.get("data", [])
                                        if widget_data:
                                            for item in widget_data:
                                               
                                                product_name = item.get("display_name", "")
                                                brand = item.get("brand", "")
                                                swiggy_product_id = item.get("product_id", "")
                                                
                                                variant_items = item.get("variations", [])
                                                for variant_item in variant_items:
                                                    variantId = variant_item.get("id", "")
                                                    variantName = variant_item.get("sku_quantity_with_combo", "")
                                                    variantData = {}
                                                    variantData["mrp"] = variant_item.get("price", {}).get("mrp", "")
                                                    variantData["discounted_price"] = variant_item.get("price", {}).get("offer_price", "")
                                                    variantData["discount_name"] = variant_item.get("offer_applied", {}).get("listing_description", "")
                                                    variantData["city"] = city
                                                    variantData["is_available"] = variant_item.get("inventory", {}).get("in_stock", False)
                                                    variantData["variant_id"] = variantId
                                                    variantData["variant_name"] = variantName
                                                    variantData["brand_name"] = brand
                                                    variantData["product_name"] = product_name
                                                    variantData["swiggy_product_id"] = swiggy_product_id
                                                    products.append(variantData)
                                has_more = response_json.get("data", {}).get("hasMore", False)
                                new_offset = response_json.get("data", {}).get("offset", 0)
                                if new_offset == offset:
                                    has_more = False
                                offset = new_offset
                                logging.info("Request sent")
                            else:
                                logging.warning(f"Non-JSON response for URL: {url}, Content-Type: {response.headers.get('Content-Type')}")
                                continue
                except Exception as e:
                    logging.error(f"Error processing category {category['name']} for store {store['id']}: {str(e)}")
                    continue
    driver.quit()
    successful, failed =  create_instamart_products(products)
    print(f"Total products: {len(products)}")
    print(f"Successful inserts: {successful}")
    print(f"Failed inserts: {failed}")

    
    return {"products":products, "total_products":len(products)}

def serialize_sku(sku):
    return {
        "id": str(sku["_id"]),
        "product_name": sku.get("product_name"),
        "brand_name": sku.get("brand_name"),
        "swiggy_product_id": sku.get("swiggy_product_id"),
        "variant_id": sku.get("variant_id"),
        "variant_name": sku.get("variant_name"),
        "mrp": sku.get("mrp"),
        "discounted_price": sku.get("discounted_price"),
        "discount_name": sku.get("discount_name"),
        "city": sku.get("city"),
        "is_available": sku.get("is_available"),
        "created_at": sku["created_at"].isoformat() if sku.get("created_at") else None,
    }

def serialize_brand(brand):
    return {
        "id": str(brand["_id"]),
        "brand_name": brand["brand_name"],
        "brand_url": brand.get("brand_url", ""),
        "brand_created_at": brand["brand_created_at"].isoformat() if brand["brand_created_at"] else None,
        "skus": [serialize_sku(s) for s in brand.get("skus", [])],
    }
async def get_swiggy_instamart_skus(brandName:str):
    aggregation_query = [
    {
        '$match': {
            'brand_name': brandName
        }
    },
    {
        '$lookup': {
            'from': 'instamart_products', 
            'let': {
                'localBrand': {
                    '$replaceAll': {
                        'input': {
                            '$replaceAll': {
                                'input': {
                                    '$toLower': '$brand_name'
                                }, 
                                'find': ' ', 
                                'replacement': '_'
                            }
                        }, 
                        'find': '-', 
                        'replacement': '_'
                    }
                }
            }, 
            'pipeline': [
                {
                    '$match': {
                        '$expr': {
                            '$eq': [
                                {
                                    '$replaceAll': {
                                        'input': {
                                            '$replaceAll': {
                                                'input': {
                                                    '$toLower': '$brand_name'
                                                }, 
                                                'find': ' ', 
                                                'replacement': '_'
                                            }
                                        }, 
                                        'find': '-', 
                                        'replacement': '_'
                                    }
                                }, '$$localBrand'
                            ]
                        }
                    }
                }
            ], 
            'as': 'skus'
        }
    }, {
        '$set': {
            'skus': {
                '$reduce': {
                    'input': '$skus', 
                    'initialValue': {
                        'variant_names': [], 
                        'results': []
                    }, 
                    'in': {
                        'variant_names': {
                            '$cond': {
                                'if': {
                                    '$in': [
                                        '$$this.variant_name', '$$value.variant_names'
                                    ]
                                }, 
                                'then': '$$value.variant_names', 
                                'else': {
                                    '$concatArrays': [
                                        '$$value.variant_names', [
                                            '$$this.variant_name'
                                        ]
                                    ]
                                }
                            }
                        }, 
                        'results': {
                            '$cond': {
                                'if': {
                                    '$in': [
                                        '$$this.variant_name', '$$value.variant_names'
                                    ]
                                }, 
                                'then': '$$value.results', 
                                'else': {
                                    '$concatArrays': [
                                        '$$value.results', [
                                            '$$this'
                                        ]
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }, {
        '$set': {
            'skus': '$skus.results'
        }
    }
]
    cursor = db.swiggy_brands.aggregate(aggregation_query)
    result = []
    
    for doc in cursor:
        doc = serialize_brand(doc)
        result.append(doc)
    print(result)
    
    return {"brands": result}