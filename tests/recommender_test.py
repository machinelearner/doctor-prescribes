from unittest import TestCase
from peewee import MySQLDatabase
from prescription.service import RecommendationService
from prescription.service.models import MysqlConnectionManager


class RecommenderTest(TestCase):
    def test_shouldRecommendItems(self):
        table_configuration = {
            "table_name": "USER_DEAL_FAVOURITES",
            "user_field": "FK_USER_ID",
            "item_field": "FK_DEALS_ID"
        }
        table_name = table_configuration["table_name"]
        user_field = table_configuration["user_field"]
        item_field = table_configuration["item_field"]
        database = MySQLDatabase(host="192.168.10.10",
                                 database="co_op_prod",
                                 user="recommendation")
        MysqlConnectionManager.database = database
        MysqlConnectionManager.proxy_database.initialize(database)
        RecommendationService().build_using_user_config_table_for_items(table_name, user_field, item_field)
