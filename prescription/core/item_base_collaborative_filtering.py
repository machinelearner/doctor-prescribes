from collections import defaultdict
from prescription.core import JaccardCoefficient


class ItemBasedColaborativeFiltering():
    COLLAB_FILTERING_THRESHOLD = 0.5

    def __init__(self, user_items_preference_map, boolean=True):
        self.boolean_preference = boolean
        self.user_items_preferences_map = user_items_preference_map

    #Parallelise
    def build_recommendations(self):
        if not self.boolean_preference:
            raise Exception("Sorry, No implementation to account to Weighted Preferences")
        item_users_map = defaultdict(list)
        for user, items_map in self.user_items_preferences_map.iteritems():
            for item, weight in items_map.iteritems():
                item_users_map[item].append(user)
        recommendations = defaultdict(lambda: defaultdict(float))
        for item, users in item_users_map.iteritems():
            for other_item, other_users in item_users_map.iteritems():
                if item == other_item:
                    continue
                similarity = JaccardCoefficient().compute(users, other_users)
                if similarity > self.COLLAB_FILTERING_THRESHOLD:
                    recommendations[item][other_item] = similarity

        return recommendations
