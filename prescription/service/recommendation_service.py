from collections import defaultdict
from prescription.service import Recommender
from prescription.service.models import MysqlConnectionManager


class RecommendationService():
    MIN_PREFERENCE_ELIGIBILITY_THRESHOLD = 10

    def build_using_user_config_table(self, table_name, user_field, item_field):
        database = MysqlConnectionManager.get_database()
        #select_user_preferences_query = "select %s, %s from %s;"
        select_user_preferences_query = "select %s, %s from %s as UDF, " \
                                        "(select %s as user, count(%s) as COUNT from %s group by %s) as SS" \
                                        " where UDF.%s=SS.user AND SS.COUNT > %d ;" % (
                                            user_field, item_field, table_name,
                                            user_field, user_field, table_name, user_field,
                                            user_field, self.MIN_PREFERENCE_ELIGIBILITY_THRESHOLD
                                        )
        print "Fetching User Preferences"
        #user_preference_results = database.execute_sql(select_user_preferences_query % (user_field, item_field,
        #                                                                                table_name)).fetchall()
        user_preference_results = database.execute_sql(select_user_preferences_query).fetchall()
        print "Fetch User Preferences Complete"
        user_preferences = defaultdict(lambda: defaultdict(float))
        for preference in user_preference_results:
            user_preferences[preference[0]].update({
                preference[1]: 1.0
            })
        Recommender().build_and_save_recommendations(user_items_preference_map=user_preferences)

    def build_using_user_config_table_for_items(self, table_name, user_field, item_field):
        database = MysqlConnectionManager.get_database()
        select_user_preferences_query = "select %s, %s from %s;" % (user_field, item_field, table_name)
        print "Fetching User Preferences"
        user_preference_results = database.execute_sql(select_user_preferences_query).fetchall()
        print "Fetch User Preferences Complete"
        user_preferences = defaultdict(lambda: defaultdict(float))
        for preference in user_preference_results:
            user_preferences[preference[0]].update({
                preference[1]: 1.0
            })
        Recommender().save_item_recommendations(user_items_preference_map=user_preferences)
