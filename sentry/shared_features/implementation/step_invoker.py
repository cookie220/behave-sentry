from sentry.utilities.middleware.sentry_kafka import KafkaClient

from sentry.utilities.database.sentry_cassandra import Cassandra
from sentry.utilities.database.sentry_postgresql import PostgreSQL
from sentry.utilities.log import sentry_logger
from retrying import retry


def send_get(context):
    """
    """
    params = _get_params(context)
    context.response = context.session.get(
        context.request_url,
        params=params,
        headers=context.request_json_headers
    )
    sentry_logger.logger.info(context.response.text)


def send_post(context):
    """
    """
    context.response = context.session.post(
        context.request_url,
        data=context.request_json_data,
        json=context.request_json_payload,
        headers=context.request_json_headers
    )
    sentry_logger.logger.info(context.response.text)


def send_put(context):
    """
    """
    context.response = context.session.put(
        context.request_url,
        json=context.request_json_payload,
        headers=context.request_json_headers
    )
    sentry_logger.logger.info(context.response.text)


def send_patch(context):
    """
    """
    context.response = context.session.patch(
        context.request_url,
        json=context.request_json_payload,
        headers=context.request_json_headers
    )
    sentry_logger.logger.info(context.response.text)


def send_delete(context):
    """
    """
    context.response = context.session.delete(
        context.request_url,
        headers=context.request_json_headers
    )
    sentry_logger.logger.info(context.response.text)


def produce_event(context):
    """
    """
    context.kafka_client = KafkaClient(context.kafka_server, context.kafka_topic)
    context.kafka_client.produce_message(context.kafka_event)


def consume_event(context):
    """
    """
    context.kafka_client = KafkaClient(context.kafka_server, context.kafka_topic)
    all_events = context.kafka_client.get_consumer_messages()
    latest_event = all_events[max(all_events)]
    context.kafka_consumed_event = latest_event


@retry(wait_fixed=2000, stop_max_attempt_number=30)
def execute_cassandra_sql(context):
    """
    """
    server = context.cassandra_server_name
    keyspace = context.cassandra_keyspace
    username = context.cassandra_username
    password = context.cassandra_password
    cassandra_client = Cassandra(server, keyspace, username, password)
    sql = context.sql_script
    if sql:
        context.query_result = cassandra_client.execute_sql(sql)
        sentry_logger.logger.info(f'SQL query result count is - {len(context.query_result)}')


@retry(wait_fixed=2000, stop_max_attempt_number=30)
def execute_postgresql_query_sql(context):
    """
    """
    server = context.postgresql_server_name
    keyspace = context.postgresql_keyspace
    username = context.postgresql_username
    password = context.postgresql_password
    postgresql_client = PostgreSQL(server, keyspace, username, password)
    sql = context.sql_script
    if sql:
        context.query_result = postgresql_client.exec_query(sql)
        sentry_logger.logger.info(f'SQL query result count is - {len(context.query_result)}')


@retry(wait_fixed=2000, stop_max_attempt_number=30)
def execute_postgresql_non_query_sql(context):
    """
    """
    server = context.postgresql_server_name
    keyspace = context.postgresql_keyspace
    username = context.postgresql_username
    password = context.postgresql_password
    postgresql_client = PostgreSQL(server, keyspace, username, password)
    sql = context.sql_script
    if sql:
        context.query_result = postgresql_client.exec_non_query(sql)
        sentry_logger.logger.info(f'SQL non query result is - {context.query_result}')


def _get_params(context):
    return context.request_params if hasattr(context, 'request_params') else None
