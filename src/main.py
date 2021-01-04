from fastapi import FastAPI, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .rest.resources import router
from .rest.security import JWTBearer


origins = [
    "*"
]


def create_app() -> FastAPI:
    _app = FastAPI(title='TPV', dependencies=[Depends(JWTBearer(["CUSTOMER"]))])
    _app.include_router(router)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = create_app()


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)}
    )
