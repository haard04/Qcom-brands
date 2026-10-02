import uvicorn
import multiprocessing


def main():
    # Set the start method to 'spawn' for Windows compatibility
    multiprocessing.set_start_method('spawn', force=True)
    
    uvicorn.run(
        "app.main:app",  # Use import string format
        host="0.0.0.0",
        port=8000,
        workers=1,  # Use single worker for Windows compatibility
        reload=False  # Disable reload in production
    )


if __name__ == "__main__":
    main()
