import uvicorn
from fastapi import FastAPI
from fastapi_injector import attach_injector
from injector import Injector

from config import get_config
from container import AppModule
from domain.errors import DomainError
from infrastructure.controllers.http.health import health_controller
from infrastructure.controllers.http.messages import message_controller
from infrastructure.errors.http.errors import domain_error_handler, unhandled_error_handler

def main():
    config = get_config()
    app = FastAPI()
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
    app.include_router(health_controller.router)
    app.include_router(message_controller.router)
    attach_injector(app, Injector([AppModule()]))
    uvicorn.run(app, host=config.server.host, port=config.server.port)

if __name__ == "__main__":
    main()
