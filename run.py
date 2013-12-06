import os
from prescription.service import RecommendationService
from prescription.service.models import MysqlConnectionManager
from prescription.web import DoctorPrescribesApp, load


def build_recommendations_using_user_preferences_from_db(table_name, user_field, item_field, config):
    load(config)
    MysqlConnectionManager.create_and_initialise()
    MysqlConnectionManager.connect()
    RecommendationService().build_using_user_config_table(table_name=table_name, user_field=user_field,
                                                          item_field=item_field)

if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(__file__), "prescription/web/config.yml")
    application = DoctorPrescribesApp(config_file)
    application.start()
