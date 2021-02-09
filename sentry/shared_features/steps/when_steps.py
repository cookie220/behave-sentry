"""
"""
from behave import *
import sentry.shared_features.implementation.step_invoker as _invoker


@step('the request verb is {method}')
def step_impl(context, method):
    invoker_function_name = 'send_' + method.lower()
    request_method = getattr(_invoker, invoker_function_name)
    request_method(context)


@step('the event is produced')
def step_impl(context):
    _invoker.produce_event(context)


@step('consumer start to consume')
def step_impl(context):
    _invoker.consume_event(context)


@step('the cassandra script is executed')
def step_impl(context):
    _invoker.execute_cassandra_sql(context)


@step('the postgresql query script is executed')
def step_impl(context):
    _invoker.execute_postgresql_query_sql(context)


@step('the postgresql non query script is executed')
def step_impl(context):
    _invoker.execute_postgresql_non_query_sql(context)