import uvicorn
from fastapi import FastAPI

from config import get_config
from infrastructure.controllers.http import health_check_controller

def main():
    config = get_config()
    app = FastAPI()
    app.include_router(health_check_controller.router)
    uvicorn.run(app, host=config.server.host, port=config.server.port)

if __name__ == "__main__":
    main()
