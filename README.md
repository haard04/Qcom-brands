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
