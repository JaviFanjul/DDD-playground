import uvicorn
from fastapi import FastAPI

from config import get_config
from domain.errors import DomainError
from infrastructure.controllers.http import health_check_controller
from infrastructure.errors.http.errors import domain_error_handler, unhandled_error_handler

def main():
    config = get_config()
    app = FastAPI()
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
    app.include_router(health_check_controller.router)
    uvicorn.run(app, host=config.server.host, port=config.server.port)

if __name__ == "__main__":
    main()
