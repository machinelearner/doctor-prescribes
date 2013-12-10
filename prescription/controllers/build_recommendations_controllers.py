import json
from prescription.service import Recommender, RecommendationService
from tornado.web import RequestHandler


class RecommendationsBuildController(RequestHandler):
    def post(self):
        user_preferences = json.loads(self.request.body, encoding="ascii")
        print self.__class__, " Post Received request"
        Recommender().build_and_save_recommendations(user_items_preference_map=user_preferences)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({
            "status": "success"
        }))

    def put(self):
        table_configuration = json.loads(self.request.body)
        table_name = table_configuration["table_name"]
        user_field = table_configuration["user_field"]
        item_field = table_configuration["item_field"]
        RecommendationService().build_using_user_config_table(table_name, user_field, item_field)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({
            "status": "success"
        }))
