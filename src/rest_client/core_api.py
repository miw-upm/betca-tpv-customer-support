from http import HTTPStatus

import requests
from fastapi import HTTPException, status

from src.config import Config
from src.security import SecurityContext


def article_existing(barcode):
    bearer = "Bearer " + SecurityContext.customer["token"]
    try:
        response = requests.get(Config.tpv_core + "/articles/" + barcode, headers={"Authorization": bearer})
    except:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Failed to establish a new connection: TPV-core")
    if HTTPStatus.NOT_FOUND == response.status_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The barcode do not exist: " + barcode)
    elif HTTPStatus.OK != response.status_code:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="TPV-core does not work: " + barcode
                                                                            + '::' + str(response.status_code))
