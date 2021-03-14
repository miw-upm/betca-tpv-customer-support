from fastapi import HTTPException, status

from src.data import review_data
from src.models.review import DBReview, Review, EmptyReview, OutReview, __to_out_review
from src.rest_client.core_api import assert_article_existing_and_return, get_all_bought_articles


def create(customer, review_creation: Review):
    article = assert_article_existing_and_return(customer['token'], review_creation.barcode)
    out_review = review_data.create(DBReview(**review_creation.dict(), mobile=customer['mobile']))
    return OutReview(**out_review.dict(), article=article)


def read(mobile, identifier):
    db_review = review_data.read(identifier)

    if mobile != db_review.mobile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for other customer")
    return db_review


def update(customer, ide, review_updating: Review):
    db_review = read(customer['mobile'], ide)
    article = assert_article_existing_and_return(customer['token'], review_updating.barcode)
    db_review.opinion = review_updating.opinion
    db_review.score = review_updating.score
    updated_review = review_data.update(db_review)
    return OutReview(**updated_review.dict(), article=article)


def find(customer):
    reviews = review_data.find_by_mobile(customer['mobile'])
    reviews = list(map(lambda mod_review: __to_out_review(mod_review, customer['mobile']), reviews))

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
    all_reviews = review_data.find_all()

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
