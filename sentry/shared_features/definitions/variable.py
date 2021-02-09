import uuid
import rootpath

vars = {
    'RANDOM_ID': str(uuid.uuid4()),
    'DEFAULT_SQL_PATH': rootpath.detect() + '/sentry/shared_features/sql_scripts/',
}


def initialize_definition(context):
    context.vars.add_vars(vars)
    context.session.adapters.DEFAULT_RETRIES = 5
