import logging
from http.client import responses

from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from src.api.complaint_resource import complaints
from src.config import config
from src.data.database import start_database


def create_app() -> FastAPI:
    logging.getLogger("uvicorn.error").propagate = False
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Configuration environment: " + config.ENVIRONMENT)
    logging.info("Creating App...")
    _app = FastAPI(title='TPV', debug=True)
    _app.include_router(complaints)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    start_database()
    return _app


app = create_app()


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": responses[exc.status_code], "message": exc.detail, "code": exc.status_code}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": responses[status.HTTP_422_UNPROCESSABLE_ENTITY], "message": str(exc.errors()),
                 "code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    )
