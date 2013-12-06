from collections import defaultdict
import json
from prescription.service import Recommender
from prescription.service.models import MysqlConnectionManager
from tornado.web import RequestHandler


class RecommendationService():

    def build_using_user_config_table(self, table_name, user_field, item_field):
        database = MysqlConnectionManager.get_database()
        select_user_preferences_query = "select %s, %s from %s;"
        print "Fetching User Preferences"
        user_preference_results = database.execute_sql(select_user_preferences_query % (user_field, item_field,
                                                                                        table_name)).fetchall()
        print "Fetch User Preferences Complete"
        user_preferences = defaultdict(lambda: defaultdict(float))
        for preference in user_preference_results:
            user_preferences[preference[0]].update({
                preference[1]: 1.0
            })
        Recommender().build_and_save_recommendations(user_items_preference_map=user_preferences)


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
