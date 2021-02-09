"""
"""
import json
from sentry.utilities.common.file import File


def set_json_data(context, data):
    """
    """
    resolved_data = context.vars.resolve(data)
    context.request_json_data = json.loads(resolved_data)


def set_json_headers(context, data):
    """
    """
    resolved_data = context.vars.resolve(data)
    context.request_json_headers = json.loads(resolved_data)


def set_url(context, url):
    """
    """
    set_default_request(context)
    resolved_url = context.vars.resolve(url)
    context.request_url = resolved_url


def set_json_payload(context, payload):
    """
    """
    resolved_payload = context.vars.resolve(payload)
    context.request_json_payload = json.loads(resolved_payload)


def set_request_params(context, params):
    """
    """
    resolve = context.vars.resolve
    resolved_params = {resolve(param['param']): resolve(param['value']) for param in params}
    context.request_params = resolved_params

'''
kakfa 
'''


def set_kafka_event(context, event):
    """
    """
    resolved_event = context.vars.resolve(event)
    context.kafka_event = json.loads(resolved_event)


def set_kafka_server(context, server):
    """
    """
    set_default_kafka(context)
    resolved_server = context.vars.resolve(server)
    context.kafka_server = resolved_server


def set_kafka_topic(context, topic):
    """
    """
    resolved_topic = context.vars.resolve(topic)
    context.kafka_topic = resolved_topic


'''
database 
'''


def set_cassandra_server_name(context, server):
    """
    """
    set_default_cassandra_database(context)
    resolved_server = context.vars.resolve(server)
    context.cassandra_server_name = resolved_server


def set_cassandra_keyspace(context, keyspace):
    """
    """
    resolved_keyspace = context.vars.resolve(keyspace)
    context.cassandra_keyspace = resolved_keyspace


def set_cassandra_username(context, username):
    """
    """
    resolved_username = context.vars.resolve(username)
    context.cassandra_username = resolved_username


def set_cassandra_password(context, password):
    """
    """
    resolved_password = context.vars.resolve(password)
    context.cassandra_password= resolved_password


def set_postgresql_server_name(context, server):
    """
    """
    set_default_postgresql_database(context)
    resolved_server = context.vars.resolve(server)
    context.postgresql_server_name = resolved_server


def set_postgresql_keyspace(context, keyspace):
    """
    """
    resolved_keyspace = context.vars.resolve(keyspace)
    context.postgresql_keyspace = resolved_keyspace


def set_postgresql_username(context, username):
    """
    """
    resolved_username = context.vars.resolve(username)
    context.postgresql_username = resolved_username


def set_postgresql_password(context, password):
    """
    """
    resolved_password = context.vars.resolve(password)
    context.postgresql_password = resolved_password


def set_sql(context, sql):
    """
    """
    resolved_sql = context.vars.resolve(sql)
    context.sql_script = resolved_sql


def set_sql_via_file(context, filename):
    """
    """
    if filename.find('/') < 0:
        filename = context.vars.get('DEFAULT_SQL_PATH') + filename

    resolved_filename = context.vars.resolve(filename)
    sql = File.read(resolved_filename)
    context.sql_script = sql


def set_default_request(context):
    context.request_json_headers = None
    context.request_json_data = None
    context.request_json_payload = None
    context.request_url = None
    context.request_params = None


def set_default_kafka(context):
    context.kafka_event = None
    context.kafka_server = None
    context.kafka_topic = None
    context.kafka_consumed_events = None


def set_default_cassandra_database(context):
    context.cassandra_server_name = None
    context.cassandra_keyspace = None
    context.cassandra_username = None
    context.cassandra_password = None
    context.sql_script = None
    context.query_result = None


def set_default_postgresql_database(context):
    context.postgresql_server_name = None
    context.postgresql_keyspace = None
    context.postgresql_username = None
    context.postgresql_password = None
    context.sql_script = None
    context.query_result = None
