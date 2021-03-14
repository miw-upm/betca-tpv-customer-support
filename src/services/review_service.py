from fastapi import HTTPException, status

from src.models.article import Article
from src.models.review import DBReview, Review, EmptyReview, OutReview
from src.rest_client.core_api import assert_article_existing_and_return, get_all_bought_articles

mock_articles = [
    Article(barcode="8400000000017", description="Mock most rated article", retailPrice=30),
    Article(barcode="8400000000024", description="Mock second most rated article", retailPrice=5, stock=15),
    Article(barcode="8400000000031", description="Mock third most rated article", retailPrice=305),
    Article(barcode="8400000000048", description="Nothing", retailPrice=305),
    Article(barcode="8400000000055", description="Another article", retailPrice=305),
    Article(barcode="8400000000079", description="Another of another article", retailPrice=305),
    Article(barcode="8400000000086", description="Look at this article", retailPrice=305)
]

mock_reviews = [
    Review(id="1", barcode=mock_articles[0].barcode, score=2.5, opinion="Is ok but not that much"),
    Review(id="2", barcode=mock_articles[1].barcode, score=5, opinion="Best product"),
    Review(id="3", barcode=mock_articles[2].barcode, score=0.5, opinion="Really bad"),
    Review(id="4", barcode=mock_articles[0].barcode, score=4, opinion="Is ok but not that much"),
    Review(id="5", barcode=mock_articles[0].barcode, score=3.5, opinion="Is ok but not that much"),
    Review(id="6", barcode=mock_articles[1].barcode, score=4.5, opinion="Is ok but not that much")
]

mock_out_reviews = [
    OutReview(id="1", article=mock_articles[0], score=2.5, opinion="Is ok but not that much"),
    OutReview(id="2", article=mock_articles[1], score=5, opinion="Best product"),
    OutReview(id="3", article=mock_articles[2], score=0.5, opinion="Really bad"),
    OutReview(id="4", article=mock_articles[0], score=4, opinion="Is ok but not that much"),
    OutReview(id="5", article=mock_articles[0], score=3.5, opinion="Is ok but not that much"),
    OutReview(id="6", article=mock_articles[1], score=4.5, opinion="Is ok but not that much"),
    EmptyReview(article=mock_articles[3]),
    EmptyReview(article=mock_articles[4]),
    EmptyReview(article=mock_articles[5]),
    EmptyReview(article=mock_articles[6])
]


def create(customer, review_creation: Review):
    article = assert_article_existing_and_return(customer['token'], review_creation.barcode)
    return OutReview(**review_creation.dict(), article=article)
    # return review_data.create(review_creation)


def read(mobile, identifier):
    # review = review_data.read(identifier)
    # Mock, see if operating with correct dto
    review = None
    for mock_review in mock_reviews:
        if mock_review.id == identifier:
            review = DBReview(**mock_review.dict(), mobile=mobile)

    if mobile != review.mobile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for other customer")
    return review


def update(customer, ide, review_updating: Review):
    db_review = read(customer['mobile'], ide)
    article = assert_article_existing_and_return(customer['token'], review_updating.barcode)
    db_review.opinion = review_updating.opinion
    db_review.score = review_updating.score
    return OutReview(**db_review.dict(), article=article)
    # return review_data.update(db_review)


def find(customer):
    # reviews = review_data.find_by_mobile(mobile)
    reviews = []
    for review in mock_reviews:
        article = assert_article_existing_and_return(customer['token'], review.barcode)
        reviews.append(OutReview(**review.dict(), article=article))

    articles = get_all_bought_articles(customer['token'], customer['mobile'])

    for review in reviews:
        for article in articles:
            if review.article.barcode == article.barcode:
                articles.remove(article)

    for article in articles:
        reviews.append(EmptyReview(article=article))

    return reviews


def top_articles(token):
    # First, recover each article with their reviews (ids)
    # all_reviews = review_data.find_all()
    all_reviews = []
    for review in mock_reviews:
        all_reviews.append(DBReview(**review.dict(), mobile="66"))

    # Second, operate and store barcode - scores
    articles_score = []
    for review in all_reviews:
        has_review = False
        for article_score in articles_score:
            if review.barcode in article_score.values():
                article_score['scores'].append(review.score)
                has_review = True
        if not has_review:
            articles_score.append({'article': review.barcode, 'scores': [review.score]})

    # Third, sort list & sort by an average of votes-score
    max_votes = len(max(articles_score, key=lambda article_score_inside: len(article_score_inside['scores']))['scores'])
    articles_score.sort(reverse=True,
                        key=lambda article_score_inside: weighted_sum_score_votes(article_score_inside, max_votes))

    # Return around 3 or 5 articles
    articles_to_return = []
    if len(articles_score) >= 3:
        for i in range(3):
            articles_to_return.append(assert_article_existing_and_return(token=token,
                                                                         barcode=articles_score[i]['article']))
    else:
        for article_score in articles_score:
            articles_to_return.append(
                assert_article_existing_and_return(token=token, barcode=article_score['article']))

    return articles_to_return


def weighted_sum_score_votes(article_score, max_votes):
    sum_scores = 0
    for score in article_score['scores']:
        sum_scores += score
    num_votes = len(article_score['scores'])
    medium_score = sum_scores / num_votes
    medium_votes = (num_votes / max_votes) * 10 / 2
    return medium_score * 0.7 + medium_votes * 0.3
