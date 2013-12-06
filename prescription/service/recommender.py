from prescription.service import UserRecommendations, ItemRecommendations
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import loglikehood_coefficient
from scikits.crab.similarities import UserSimilarity, ItemSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender, ItemBasedRecommender


class Recommender():
    def build_and_save_recommendations(self, user_items_preference_map):
        model = MatrixPreferenceDataModel(user_items_preference_map)

        user_similarity = UserSimilarity(model, loglikehood_coefficient)
        item_similarity = ItemSimilarity(model, loglikehood_coefficient)

        user_recommender = UserBasedRecommender(model, user_similarity, with_preference=True)
        item_recommender = ItemBasedRecommender(model, item_similarity, with_preference=True)

        for user_id in model.user_ids().tolist():
            recommendations = user_recommender.recommend(user_id, how_many=5)
            UserRecommendations.save_recommendations_for_user(user_id, recommendations)

        for item_id in model.item_ids().tolist():
            recommendations = item_recommender.recommend(item_id, how_many=5)
            ItemRecommendations.save_recommendations_for_item(item_id, recommendations)

    def recommend_item(self, item_id):
        recommendations = ItemRecommendations.select().where(ItemRecommendations.item_id == item_id)
        return ItemRecommendations.serialize(recommendations)

    def recommend_item_for(self, user_id):
        recommendations = UserRecommendations.select().where(UserRecommendations.user_id == user_id)
        return UserRecommendations.serialize(recommendations)
