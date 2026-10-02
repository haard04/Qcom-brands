# Quick Commerce Data Scraper

A FastAPI-based application for scraping and managing brand data from various quick commerce platforms including Zepto, Blinkit, BigBasket, and Swiggy.

## Features

- Scrapes brand data from multiple quick commerce platforms
- Stores data in MongoDB with duplicate prevention
- Provides RESTful APIs for data access and management
- Background task processing for data scraping
- Admin data tracking for last scrape times
- Health check endpoint for system monitoring

## Prerequisites

- Python 3.12+
- MongoDB
- Chrome/Chromium browser (for web scraping)
- ChromeDriver (automatically installed via webdriver-manager)
- uv (Python package installer and resolver)

## Project Setup

1. Clone the repository:
```bash
git clone https://github.com/haard04/Qcom-brands.git
cd Qcom-brands
```

2. Install uv if not already installed:
```bash
pip install uv
```

3. Create and activate a virtual environment using uv:
```bash
uv venv
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

4. Install dependencies using uv:
```bash
uv pip install -e .
```

5. Create a `.env` file in the root directory with the following variables:
```env
MONGODB_URL=mongodb://localhost:27017
```

6. Initialize the database:
```bash
python -m app.database.create_db
```

## Running the Application

The project provides two ways to run the server:

### Development Server
```bash
# Using the provided script
python -m scripts.dev_server

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
# Using the provided script
python -m scripts.prod_server

# Or directly with gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at `http://localhost:8000`

## Project Structure

```
quick-com-scrapper/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── browser.py           # Browser automation and scraping
│   ├── models.py            # Database models and connection
│   ├── database/           # Database related scripts
│   ├── data/              # Data storage directory
│   ├── bigbasket/         # BigBasket specific scraping
│   ├── zepto/            # Zepto specific scraping
│   └── swiggy/           # Swiggy specific scraping
├── scripts/
│   ├── dev_server.py     # Development server script
│   └── prod_server.py    # Production server script
├── .env                   # Environment variables
├── pyproject.toml        # Project configuration and dependencies
└── README.md             # Project documentation
```


## API Documentation

### Data Processing Endpoints

#### Process Zepto Brands
```http
GET /processZepto
```
Starts background processing of Zepto brands.

#### Process Blinkit Brands
```http
GET /processBlinkit
```
Starts background processing of Blinkit brands.

#### Process BigBasket Brands
```http
GET /processBigbasket
```
Starts background processing of BigBasket brands.

#### Process Swiggy Brands
```http
GET /processSwiggy
```
Starts background processing of Swiggy brands.

### Data Retrieval Endpoints

#### Get Zepto Brands
```http
GET /getZeptoBrands
```
Returns all Zepto brands from the database.

#### Get Blinkit Brands
```http
GET /getBlinkitBrands
```
Returns all Blinkit brands from the database.

#### Get BigBasket Brands
```http
GET /getBigbasketBrands
```
Returns all BigBasket brands from the database.

#### Get Swiggy Brands
```http
GET /getSwiggyBrands
```
Returns all Swiggy brands from the database.

### Admin Endpoints

#### Get Admin Data
```http
GET /getAdminData
```
Returns the last scrape times for all platforms.

#### Health Check
```http
GET /health
```
Returns the health status of the application and database connection.

## Scraping Process Details

### BigBasket Scraping Process
1. Initializes a headless Chrome browser using Selenium
2. Navigates to BigBasket's sitemap XML URL (`https://www.bigbasket.com/sitemap/brands.xml`)
3. Waits for the page to load and retrieves the page source
4. Parses the XML content using BeautifulSoup with 'lxml' parser
5. Extracts brand names and URLs from the XML structure
   - Brand names are extracted from the URL path after '/pb/'
   - Both brand names and their corresponding URLs are stored
6. Stores the data in MongoDB with duplicate prevention
7. Updates the last scrape timestamp in admin data

### Blinkit Scraping Process
1. Initializes a headless Chrome browser using Selenium
2. Navigates to Blinkit's brands XML URL (`https://blinkit.com/brands.xml`)
3. Downloads the XML file to the local filesystem
4. Reads and parses the downloaded XML file using ElementTree
5. Extracts brand information:
   - Processes each URL in the XML
   - Extracts brand names from the URL path
   - Maps brand names to their corresponding URLs
6. Cleans up by removing the downloaded XML file
7. Stores the data in MongoDB with duplicate prevention
8. Updates the last scrape timestamp in admin data

### Zepto Scraping Process
1. Initializes a headless Chrome browser using Selenium
2. Navigates to Zepto's sitemap XML URL (`https://www.zeptonow.com/sitemap/brands.xml`)
3. Retrieves the page source after loading
4. Parses the XML content using BeautifulSoup with 'lxml' parser
5. Extracts brand information:
   - Processes each URL in the XML
   - Extracts brand names from the URL path after '/brand/'
   - Cleans brand names by replacing underscores with spaces
6. Stores the data in MongoDB with duplicate prevention
7. Updates the last scrape timestamp in admin data

### Swiggy Scraping Process
Swiggy data is scraped using two different approaches:

#### 1. API-Based Approach
1. Uses a predefined list of categories and store IDs for different cities
2. For each category and store combination:
   - Constructs API URLs with proper parameters
   - Makes requests to Swiggy's Instamart API endpoints
   - Processes paginated responses (handles offset)
   - Extracts brand information from the JSON response
3. Stores unique brands in MongoDB

#### 2. Sitemap-Based Approach
1. Initializes a headless Chrome browser using Selenium
2. Downloads and processes the main sitemap index from `https://www.swiggy.com/instamart/sitemap/brand-sitemap.xml.gz`
3. For each sitemap URL found in the index:
   - Downloads the gzipped XML file
   - Extracts and parses the XML content
   - Filters URLs containing "/b/" (brand URLs) but not "/cb/"
   - Extracts brand names from the URL paths
4. Cleans up by removing downloaded files
5. Stores unique brands in MongoDB
6. Updates the last scrape timestamp in admin data

Both approaches ensure comprehensive brand data collection, with the API approach providing category-specific data and the sitemap approach ensuring complete brand coverage.

Each platform's data is stored in its respective MongoDB collection with the following structure:
```json
{
    "brand_name": "string",
    "brand_url": "string",
    "brand_created_at": "datetime"
}
```

The scraping process includes error handling, duplicate prevention, and logging for monitoring and debugging purposes.

## Response Formats

### Brand List Response
```json
{
    "total_brands": 100,
    "brands": [
        {
            "id": "string",
            "brand_name": "string",
            "brand_url": "string or null",
            "brand_created_at": "ISO format datetime string or null"
        }
    ]
}
```

### Process Response
```json
{
    "message": "process started"
}
```

### Admin Data Response
```json
{
    "user": "admin",
    "last_zepto_scrape": "ISO format datetime string",
    "last_blinkit_scrape": "ISO format datetime string",
    "last_bigbasket_scrape": "ISO format datetime string",
    "last_swiggy_scrape": "ISO format datetime string"
}
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 500: Internal Server Error

All errors include a detail message explaining the error.