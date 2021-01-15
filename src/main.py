import logging

from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .data.database import start_database
from .rest.resources import complaints


def create_app() -> FastAPI:
    logging.getLogger("uvicorn.error").propagate = False
    logging.getLogger().setLevel(logging.INFO)
    _app = FastAPI(title='TPV', debug=True)
    _app.include_router(complaints)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.info("Creating App...")
    start_database()
    return _app


app = create_app()


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)}
    )
