from prescription.controllers import ItemRecommendationController, UserRecommendationController, RecommendationsBuildController
from prescription.service.models import MysqlConnectionManager
from config import load, config
from tornado.ioloop import IOLoop
from tornado.web import Application


class DoctorPrescribesApp(Application):
    def __init__(self, config_file):
        load(config_file)
        MysqlConnectionManager.create_and_initialise()
        MysqlConnectionManager.connect()

        handlers = [
            (r'/recommendation/item/([\w\d\-]+)', ItemRecommendationController),
            (r'/recommendation/user/([\w\d\-]+)', UserRecommendationController),
            ('/recommendations/_build', RecommendationsBuildController),
        ]
        Application.__init__(self, handlers)

    def start(self):
        self.listen(config("app.port"))
        print "Starting IOLoop in port ", config("app.port")
        IOLoop.instance().start()
        print "Listening in port ", config("app.port")





