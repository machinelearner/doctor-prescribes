import multiprocessing
from prescription.service import ItemRecommendations


class ItemRecommenderWorker(multiprocessing.Process):
    def __init__(self, work_queue, item_recommender):
        multiprocessing.Process.__init__(self)
        self.work_queue = work_queue
        self.kill_received = False
        self.item_recommender = item_recommender

    def run(self):
        while not self.kill_received:
            try:
                item_id = self.work_queue.get_nowait()
            except multiprocessing.Queue.Empty:
                break

            recommendations = self.item_recommender.recommend(item_id, how_many=10)
            ItemRecommendations.save_recommendations_for_item(item_id, recommendations)
