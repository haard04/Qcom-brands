from app.schemas import zepto_brands, blinkit_brands, bigbasket_brands, swiggy_brands, instamart_products
from datetime import datetime
from typing import List, Dict
from pymongo.errors import BulkWriteError

def create_zepto_brands(brands: List[Dict[str, str]]):
    """
    Create multiple Zepto brands in bulk
    Args:
        brands: List of dictionaries containing brand_name and brand_url
    Returns:
        tuple: (successful_inserts, failed_inserts)
    """
    documents = [
        {
            'brand_name': brand['brand_name'],
            'brand_url': brand.get('brand_url'),
            'brand_created_at': datetime.now()
        }
        for brand in brands
    ]
    try:
        result = zepto_brands.insert_many(documents, ordered=False)
        return len(result.inserted_ids), 0
    except BulkWriteError as bwe:
        # Get the number of successful inserts
        successful = len(bwe.details.get('nInserted', 0))
        # Calculate failed inserts
        failed = len(documents) - successful
        return successful, failed

def create_blinkit_brands(brands: List[Dict[str, str]]):
    """
    Create multiple Blinkit brands in bulk
    Args:
        brands: List of dictionaries containing brand_name and brand_url
    Returns:
        tuple: (successful_inserts, failed_inserts)
    """
    documents = [
        {
            'brand_name': brand['brand_name'],
            'brand_url': brand.get('brand_url'),
            'brand_created_at': datetime.now()
        }
        for brand in brands
    ]
    try:
        result = blinkit_brands.insert_many(documents, ordered=False)
        return len(result.inserted_ids), 0
    except BulkWriteError as bwe:
        successful = len(bwe.details.get('nInserted', 0))
        failed = len(documents) - successful
        return successful, failed

def create_bigbasket_brands(brands: List[Dict[str, str]]):
    """
    Create multiple BigBasket brands in bulk
    Args:
        brands: List of dictionaries containing brand_name and brand_url
    Returns:
        tuple: (successful_inserts, failed_inserts)
    """
    documents = [
        {
            'brand_name': brand['brand_name'],
            'brand_url': brand.get('brand_url'),
            'brand_created_at': datetime.now()
        }
        for brand in brands
    ]
    try:
        result = bigbasket_brands.insert_many(documents, ordered=False)
        return len(result.inserted_ids), 0
    except BulkWriteError as bwe:
        successful = len(bwe.details.get('nInserted', 0))
        failed = len(documents) - successful
        return successful, failed

def create_swiggy_brands(brands: List[Dict[str, str]]):
    """
    Create multiple Swiggy brands in bulk
    Args:
        brands: List of dictionaries containing brand_name and brand_url
    Returns:
        tuple: (successful_inserts, failed_inserts)
    """
    documents = [
        {
            'brand_name': brand['brand_name'],
            'brand_url': brand.get('brand_url'),
            'brand_created_at': datetime.now()
        }
        for brand in brands
    ]
    try:
        result = swiggy_brands.insert_many(documents, ordered=False)
        return len(result.inserted_ids), 0
    except BulkWriteError as bwe:
        successful = len(bwe.details.get('nInserted', 0))
        failed = len(documents) - successful
        return successful, failed
    
def create_instamart_products(products: List[Dict[str, str]]):
    """
    Create multiple Instamart products in bulk
    Args:
        products: List of dictionaries containing product_name, brand_name, swiggy_product_id, variant_id, variant_name, mrp, discounted_price, discount_name, city, is_available
    Returns:
        tuple: (successful_inserts, failed_inserts)
    """
    documents = [
        {
            'product_name': product['product_name'],
            'brand_name': product['brand_name'],
            'swiggy_product_id': product['swiggy_product_id'],
            'variant_id': product['variant_id'],
            'variant_name': product['variant_name'],
            'mrp': product['mrp'],
            'discounted_price': product['discounted_price'],
            'discount_name': product['discount_name'],
            'city': product['city'],    
            'is_available': product['is_available'],
            'created_at': datetime.now()
        }
        for product in products
    ]
    try:
        result = instamart_products.insert_many(documents, ordered=False)
        return len(result.inserted_ids), 0
    except BulkWriteError as bwe:
        successful = len(bwe.details.get('nInserted', 0))
        failed = len(documents) - successful
        return successful, failed
    