import multiprocessing
from prescription.service import UserRecommendations


class UserRecommenderWorker(multiprocessing.Process):
    def __init__(self, work_queue, user_recommender):
        multiprocessing.Process.__init__(self)
        self.work_queue = work_queue
        self.kill_received = False
        self.user_recommender = user_recommender

    def run(self):
        while not self.kill_received:
            try:
                user_id = self.work_queue.get_nowait()
            except multiprocessing.Queue.Empty:
                break

            recommendations = self.user_recommender.recommend(user_id, how_many=10)
            UserRecommendations.save_recommendations_for_user(user_id, recommendations)
