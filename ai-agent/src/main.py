import uvicorn
from fastapi import FastAPI

from config import get_config

def main():
    config = get_config()
    app = FastAPI()
    uvicorn.run(app, host=config.server.host, port=config.server.port)

if __name__ == "__main__":
    main()
