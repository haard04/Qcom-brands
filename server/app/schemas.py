from pymongo import MongoClient
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGODB_URL)
db = client['quick_com_scrapper']  # Database name

# Collections
zepto_brands = db['zepto_brands']
blinkit_brands = db['blinkit_brands']
bigbasket_brands = db['bigbasket_brands']
swiggy_brands = db['swiggy_brands']
instamart_products = db['instamart_products']  # Timeseries collection for Instamart products

admin_data = db['admin_data']

# Brand collections indexes
zepto_brands.create_index('brand_name', unique=True)
blinkit_brands.create_index('brand_name', unique=True)
bigbasket_brands.create_index('brand_name', unique=True)
swiggy_brands.create_index('brand_name', unique=True)

# Admin data indexes
admin_data.create_index('last_zepto_scrape', unique=True)
admin_data.create_index('last_blinkit_scrape', unique=True)
admin_data.create_index('last_bigbasket_scrape', unique=True)
admin_data.create_index('last_swiggy_scrape', unique=True)

# Instamart products timeseries collection indexes
# Time field index for timeseries functionality
instamart_products.create_index([('created_at', 1)], expireAfterSeconds=0)

# Indexes for efficient grouping and querying
instamart_products.create_index('brand_name')
instamart_products.create_index('swiggy_product_id')
instamart_products.create_index('product_name')
instamart_products.create_index('variant_id')
instamart_products.create_index('variant_name')
instamart_products.create_index('city')

# Compound indexes for common query patterns
instamart_products.create_index([('brand_name', 1), ('created_at', -1)])
instamart_products.create_index([('product_name', 1), ('created_at', -1)])
instamart_products.create_index([('city', 1), ('created_at', -1)])
instamart_products.create_index([('brand_name', 1), ('city', 1), ('created_at', -1)])

# Helper functions for database operations
def get_db():
    return db

def init_db():
    # Create indexes if they don't exist
    zepto_brands.create_index('brand_name', unique=True)
    blinkit_brands.create_index('brand_name', unique=True)
    bigbasket_brands.create_index('brand_name', unique=True)
    swiggy_brands.create_index('brand_name', unique=True)
    
    # Instamart products indexes
    instamart_products.create_index([('created_at', 1)], expireAfterSeconds=0)
    instamart_products.create_index('brand_name')
    instamart_products.create_index('swiggy_product_id')
    instamart_products.create_index('product_name')
    instamart_products.create_index('variant_id')
    instamart_products.create_index('variant_name')
    instamart_products.create_index('city')
    instamart_products.create_index([('brand_name', 1), ('created_at', -1)])
    instamart_products.create_index([('product_name', 1), ('created_at', -1)])
    instamart_products.create_index([('city', 1), ('created_at', -1)])
    instamart_products.create_index([('brand_name', 1), ('city', 1), ('created_at', -1)])

def insert_instamart_product(product_data):
    """
    Insert a new instamart product record
    
    Args:
        product_data (dict): Product data with the following structure:
        {
            'brand_name': str,
            'swiggy_product_id': str,
            'product_name': str,
            'variant_id': str,
            'variant_name': str,
            'mrp': float,
            'discounted_price': float,
            'discount_name': str,
            'city': str,
            'is_available': bool,
            'created_at': datetime (optional, will use current time if not provided)
        }
    """
    if 'created_at' not in product_data:
        product_data['created_at'] = datetime.utcnow()
    
    return instamart_products.insert_one(product_data)

def get_instamart_products(group_by=None, filters=None, limit=None, sort_by='created_at', sort_order=-1):
    """
    Get instamart products with optional grouping and filtering
    
    Args:
        group_by (str or list): Field(s) to group by ('brand_name', 'product_name', 'swiggy_product_id', 'variant_name', 'variant_id', 'city')
        filters (dict): Filter criteria
        limit (int): Limit number of results
        sort_by (str): Field to sort by
        sort_order (int): 1 for ascending, -1 for descending
    
    Returns:
        list: Aggregated results or filtered documents
    """
    if group_by:
        # Aggregation pipeline for grouping
        pipeline = []
        
        # Add match stage if filters provided
        if filters:
            pipeline.append({'$match': filters})
        
        # Group stage
        group_stage = {
            '_id': {field: f'${field}' for field in (group_by if isinstance(group_by, list) else [group_by])},
            'count': {'$sum': 1},
            'latest_record': {'$last': '$$ROOT'},
            'avg_mrp': {'$avg': '$mrp'},
            'avg_discounted_price': {'$avg': '$discounted_price'},
            'min_discounted_price': {'$min': '$discounted_price'},
            'max_discounted_price': {'$max': '$discounted_price'},
            'latest_created_at': {'$max': '$created_at'}
        }
        pipeline.append({'$group': group_stage})
        
        # Sort stage
        pipeline.append({'$sort': {sort_by: sort_order}})
        
        # Limit stage
        if limit:
            pipeline.append({'$limit': limit})
        
        return list(instamart_products.aggregate(pipeline))
    else:
        # Simple find query
        query = filters or {}
        cursor = instamart_products.find(query).sort(sort_by, sort_order)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)

# Example document structure for reference:
"""
Brand collections:
{
    'brand_name': str,
    'brand_url': str,
    'brand_created_at': datetime
}

Instamart products timeseries collection:
{
    '_id': ObjectId,  # Auto-generated by MongoDB
    'brand_name': str,
    'swiggy_product_id': str,
    'product_name': str,
    'variant_id': str,
    'variant_name': str,
    'mrp': float,
    'discounted_price': float,
    'is_available': bool,
    'discount_name': str,
    'city': str,
    'created_at': datetime
}
""" 