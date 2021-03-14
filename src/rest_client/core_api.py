from http import HTTPStatus

from fastapi import HTTPException, status
from requests import get

from src.config import config
from src.models.article import Article


def assert_article_existing_and_return(token, barcode):
    bearer = "Bearer " + token
    try:
        response = get(config.TPV_CORE + "/articles/" + barcode, headers={"Authorization": bearer})
    except Exception:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Failed to establish a new connection: TPV-core")
    if HTTPStatus.NOT_FOUND == response.status_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The barcode do not exist: " + barcode)
    elif HTTPStatus.OK != response.status_code:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="TPV-core does not work: " + barcode
                                                                            + '::' + str(response.status_code))
    return Article(**response.json())


def get_all_bought_articles(token):
    bearer = "Bearer " + token
    try:
        response = get(config.TPV_CORE + "/tickets/search/boughtArticles", headers={"Authorization": bearer})
    except Exception:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Failed to establish a new connection: TPV-core")
    if HTTPStatus.OK != response.status_code:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="TPV-core does not work: " + str(bearer)
                                                                            + '::' + str(response.status_code))
    json_response = response.json()
    articles = []
    for json_article in json_response:
        articles.append(Article(**json_article))
    return articles
