import multiprocessing
from prescription.core import ItemBasedColaborativeFiltering
from prescription.service import UserRecommendations, ItemRecommendations
from prescription.service.workers import ParallelWork, UserRecommenderWorker
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import loglikehood_coefficient
from scikits.crab.similarities import UserSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender


class Recommender:
    def save_item_recommendations(self, user_items_preference_map):
        item_recommendations = ItemBasedColaborativeFiltering(user_items_preference_map).build_recommendations()
        for item, item_weight_map in item_recommendations.iteritems():
            ItemRecommendations.save_recommendations_for_item(item, item_weight_map.iteritems())

    def build_and_save_recommendations(self, user_items_preference_map):
        model = MatrixPreferenceDataModel(user_items_preference_map)

        #item_similarity = ItemSimilarity(model, loglikehood_coefficient)
        user_similarity = UserSimilarity(model, loglikehood_coefficient)

        item_recommendations = ItemBasedColaborativeFiltering(user_items_preference_map).build_recommendations()
        user_recommender = UserBasedRecommender(model, user_similarity, with_preference=True)

        for item, item_weight_map in item_recommendations.iteritems():
            ItemRecommendations.save_recommendations_for_item(item, item_weight_map.iteritems())

        user_work_queue = multiprocessing.Queue()
        for user_id in model.user_ids().tolist():
            user_work_queue.put(user_id)
        ParallelWork(UserRecommenderWorker, (user_work_queue, user_recommender)).begin()

    def recommend_item(self, item_id):
        recommendations = ItemRecommendations.select().where(ItemRecommendations.item_id == item_id)
        return ItemRecommendations.serialize(recommendations)

    def recommend_item_for(self, user_id):
        recommendations = UserRecommendations.select().where(UserRecommendations.user_id == user_id)
        return UserRecommendations.serialize(recommendations)
