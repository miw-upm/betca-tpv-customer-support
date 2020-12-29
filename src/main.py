from fastapi import FastAPI, Depends, status, Request
from starlette.responses import JSONResponse

from .rest.resources import router
from .rest.security import JWTBearer


def create_app() -> FastAPI:
    _app = FastAPI(title='TPV', dependencies=[Depends(JWTBearer(["ADMIN", "MANAGER", "OPERATOR"]))])
    _app.include_router(router)
    return _app


app = FastAPI(title='TPV', dependencies=[Depends(JWTBearer(["ADMIN", "MANAGER", "OPERATOR"]))])
app.include_router(router)


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)}
    )
