"""
"""
from behave import *
import sentry.shared_features.implementation.step_builder as _builder


@step('a request form urlencoded json')
def step_impl(context):
    _builder.set_json_data(context, context.text)


@step('a request headers json')
def step_impl(context):
    _builder.set_json_headers(context, context.text)


@step('a new request url {url}')
def step_impl(context, url):
    _builder.set_url(context, url)


@step('a kafka event json')
def step_impl(context):
    _builder.set_kafka_event(context, context.text)


@step('a kafka server {server}')
def step_impl(context, server):
    _builder.set_kafka_server(context, server)


@step('a kafka topic {topic}')
def step_impl(context, topic):
    _builder.set_kafka_topic(context, topic)


@step('a cassandra server {server}')
def step_impl(context, server):
    _builder.set_cassandra_server_name(context, server)


@step('a cassandra keyspace {keyspace}')
def step_impl(context, keyspace):
    _builder.set_cassandra_keyspace(context, keyspace)


@step('a cassandra username {username}')
def step_impl(context, username):
    _builder.set_cassandra_username(context, username)


@given('a cassandra password {password}')
def step_impl(context, password):
    _builder.set_cassandra_password(context, password)


@step('a sql script')
def step_impl(context):
    _builder.set_sql(context, context.text)


@step('a sql script file {file}')
def step_impl(context, file):
    _builder.set_sql_via_file(context, file)


@step('a postgresql server {server}')
def step_impl(context, server):
    _builder.set_postgresql_server_name(context, server)


@step('a postgresql keyspace {keyspace}')
def step_impl(context, keyspace):
    _builder.set_postgresql_keyspace(context, keyspace)


@step('a postgresql username {username}')
def step_impl(context, username):
    _builder.set_postgresql_username(context, username)


@given('a postgresql password {password}')
def step_impl(context, password):
    _builder.set_postgresql_password(context, password)
