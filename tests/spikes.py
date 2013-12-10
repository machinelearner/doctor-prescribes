from scikits.crab.metrics import loglikehood_coefficient, pearson_correlation
from scikits.crab.models import MatrixBooleanPrefDataModel
from scikits.learn.covariance import log_likelihood


def main():
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    from scikits.crab import datasets
    movies = datasets.load_sample_songs()

    print "Movies Data:", pp.pformat(movies)
    print "Movies Data Matrix :", pp.pformat(movies.data)
    from scikits.crab.models import MatrixPreferenceDataModel
    #Build the model
    #new_movies = {u'1': [1, 2, 3, 4, 5], u'3': [2, 3, 4, 5, 6], u'2': [1, 2, 3, 4, 5, 6], u'5': [2, 3, 4], u'4': [1, 2, 3, 4, 5, 6], u'7': [1, 2, 4, 5], u'6': [1, 2, 3, 4, 5, 6]}
    #print "New moview hash", pp.pformat(new_movies)
    #model = MatrixBooleanPrefDataModel(new_movies)
    model = MatrixPreferenceDataModel(movies.data)
    import json
    from scikits.crab.metrics import spearman_coefficient
    from scikits.crab.similarities import UserSimilarity, ItemSimilarity
    #Build the similarity
    user_similarity = UserSimilarity(model, pearson_correlation)
    item_similarity = ItemSimilarity(model, pearson_correlation)

    from scikits.crab.recommenders.knn import UserBasedRecommender, ItemBasedRecommender
    #Build the User based recommender
    user_recommender = UserBasedRecommender(model, user_similarity, with_preference=True)
    item_recommender = ItemBasedRecommender(model, item_similarity, with_preference=True)
    print "recommendations for user 5", user_recommender.recommend("5")
    print "recommendations for item 3", item_recommender.recommend("3")

if __name__ == "__main__":
    main()