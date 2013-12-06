import sys

import os

sys.path.append(os.path.abspath('.'))
from run import build_recommendations_using_user_preferences_from_db
from paver.easy import task
from paver.tasks import cmdopts


@task
@cmdopts([
    ('table=', 't', 'Table name with user preferences'),
    ('user_field=', 'u', 'User Field name '),
    ('item_field=', 'i', 'Item Field name '),
    ('config=', 'c', 'Config File')
])
def build_from_db(options):
    """Deploy the HTML to the server."""
    build_recommendations_using_user_preferences_from_db(options.table, options.user_field, options.item_field,
                                                         options.config)