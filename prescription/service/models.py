import json
from playhouse.proxy import Proxy
from prescription.web import config
from peewee import MySQLDatabase, Model, CharField, FloatField


class MysqlConnectionManager():
    database = None
    proxy_database = Proxy()

    @classmethod
    def proxy(cls):
        return cls.proxy_database

    @classmethod
    def create_and_initialise(cls):
        if cls.database is None:
            cls.database = MySQLDatabase(host=config("database.host", "localhost"),
                                         database=config("database.name", "mysql"),
                                         user=config("database.user", "root"))
        cls.proxy_database.initialize(cls.database)

    @classmethod
    def connect(cls):
        cls.database.connect()
        if not UserRecommendations.table_exists():
            UserRecommendations.create_table()
        if not ItemRecommendations.table_exists():
            ItemRecommendations.create_table()


    @classmethod
    def get_database(cls):
        return cls.database


class MySQLModel(Model):
    class Meta:
        database = MysqlConnectionManager.proxy()


class UserRecommendations(MySQLModel):
    user_id = CharField()
    recommended_item_id = CharField()
    weightage = FloatField()

    class Meta:
        db_table = "USER_RECOMMENDATIONS"

    @classmethod
    def save_recommendations_for_user(cls, user='', recommendations=[]):
        for (recommendation, weightage) in recommendations:
            print "Saving User", user, " ", recommendation, " ", weightage
            UserRecommendations(user_id=user, recommended_item_id=recommendation, weightage=weightage).save()

    def to_map(self):
        return {
            "recommended_item_id": self.recommended_item_id,
            "weightage": self.weightage
        }

    @classmethod
    def serialize(cls, recommendations):
        return json.dumps([recommendation.to_map() for recommendation in recommendations])


class ItemRecommendations(MySQLModel):
    item_id = CharField()
    recommended_item_id = CharField()
    weightage = FloatField()

    class Meta:
        db_table = "ITEM_RECOMMENDATIONS"

    def to_map(self):
        return {
            "item_id": self.item_id,
            "recommended_item_id": self.recommended_item_id,
            "weightage": self.weightage
        }

    @classmethod
    def save_recommendations_for_item(cls, item='', recommendations=[]):
        for (recommendation, weightage) in recommendations:
            print "Saving Item", item, " ", recommendation, " ", weightage
            ItemRecommendations(item_id=item, recommended_item_id=recommendation, weightage=weightage).save()

    @classmethod
    def serialize(cls, recommendations):
        return json.dumps([recommendation.to_map() for recommendation in recommendations])
