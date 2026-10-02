import uvicorn
import logging
import dotenv
import os

dotenv.load_dotenv()

def main():
    host = os.getenv("HOST","127.0.0.1")
    port = int(os.getenv("PORT",8002))
    reload = os.getenv("RELOAD",True)
    logLevel = os.getenv("LOG_LEVEL",logging.INFO)
    # Configure logging before starting uvicorn
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    uvicorn.run(
        "app.main:app", 
        host=host, 
        port=port, 
        reload=reload, 
        log_level=logLevel,
        access_log=True  # This helps with seeing all logs
    )

if __name__ == "__main__":
    main()
