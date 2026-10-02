from fastapi import FastAPI, Query, Depends, HTTPException, Request
import app.browser as browser
import time
import logging
from app.schemas import init_db, get_db
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import app.swiggy.products as swiggy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize database
init_db()

# Response models
class Brand(BaseModel):
    id: str
    brand_name: str
    brand_url: Optional[str]
    brand_created_at: Optional[str]

class BrandList(BaseModel):
    brands: List[Brand]

app = FastAPI(
    title="Quick Commerce Scraper",
    description="API for scraping and managing quick commerce data",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Quick Commerce Scraper API"}

@app.get("/processZepto")
async def processZepto(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(browser.process_zepto)
        return {"message":"process started"}
    except Exception as e:
        logging.error(f"Error fetching zepto data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/processBlinkit")
async def processBlinkit(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(browser.process_blinkit)
        return {"message":"process started"}
    except Exception as e:
        logging.error(f"Error fetching blinkit data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/processBigbasket")
async def processBigbasket(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(browser.process_bigbasket)
        return {"message":"process started"}
    except Exception as e:
        logging.error(f"Error fetching bigbasket data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/processSwiggy")
async def processSwiggy(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(browser.process_swiggy)
        return {"message":"process started"}
    except Exception as e:
        logging.error(f"Error fetching swiggy data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getSwiggyBrands", response_model=BrandList)
async def getSwiggyBrands():
    try:
        brands = browser.get_enriched_swiggy_brands()
        return {"total_brands":len(brands),"brands": brands}
    except Exception as e:
        logging.error(f"Error fetching swiggy brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getZeptoBrands", response_model=BrandList)
async def getZeptoBrands():
    try:
        brands = await browser.get_zepto_brands()
        # return {"message":"process started"}
        return {"total_brands":len(brands),"brands": brands}
    except Exception as e:
        logging.error(f"Error fetching zepto brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getBlinkitBrands", response_model=BrandList)
async def getBlinkitBrands():
    try:
        brands = await browser.get_blinkit_brands()
        # return {"message":"process started"}
        return {"total_brands":len(brands),"brands": brands}
    except Exception as e:
        logging.error(f"Error fetching blinkit brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getBigbasketBrands", response_model=BrandList)
async def getBigbasketBrands():
    try:
        brands = await browser.get_bigbasket_brands()
        return {"total_brands":len(brands),"brands": brands}
    except Exception as e:
        logging.error(f"Error fetching bigbasket brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/processSwiggyInstamartProducts")
async def processSwiggyInstamartProducts(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(swiggy.process_swiggy_instamart_products)
        return {"message":"process started"}
    except Exception as e:
        logging.error(f"Error fetching swiggy instamart products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getSwiggySKUsByBrand/{brandName}")
async def getSwiggySKUsByBrand(brandName:str):
    try:
        brands = await swiggy.get_swiggy_instamart_skus(brandName)
        return brands
    except Exception as e:
        logging.error(f"Error fetching swiggy instamart brands: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Check MongoDB connection
        db = get_db()
        db.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": time.time()
        }
    
@app.get("/getAdminData")
async def getAdminData():
    try:
        admin_data = get_db().admin_data.find_one({"user": "admin"})
        totalZeptoBrands = get_db().zepto_brands.count_documents({})
        totalBlinkitBrands = get_db().blinkit_brands.count_documents({})
        totalBigbasketBrands = get_db().bigbasket_brands.count_documents({})
        totalSwiggyBrands = get_db().swiggy_brands.count_documents({})
        return {
            "user": admin_data["user"],
            "total_zepto_brands": totalZeptoBrands,
            "total_blinkit_brands": totalBlinkitBrands,
            "total_bigbasket_brands": totalBigbasketBrands,
            "total_swiggy_brands": totalSwiggyBrands,
            "last_zepto_scrape": admin_data["last_zepto_scrape"],
            "last_blinkit_scrape": admin_data["last_blinkit_scrape"],
            "last_bigbasket_scrape": admin_data["last_bigbasket_scrape"],
            "last_swiggy_scrape": admin_data["last_swiggy_scrape"]
        }
    except Exception as e:
        logging.error(f"Error fetching admin data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))