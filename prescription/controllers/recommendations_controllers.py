from prescription.service import Recommender
from tornado.web import RequestHandler


class ItemRecommendationController(RequestHandler):
    def get(self, item_id):
        serialised_recommendations = Recommender().recommend_item(item_id)
        self.set_header("Content-Type", "application/json")
        self.write(serialised_recommendations)


class UserRecommendationController(RequestHandler):
    def get(self, user_id):
        serialised_recommendations = Recommender().recommend_item_for(user_id)
        self.set_header("Content-Type", "application/json")
        self.write(serialised_recommendations)
