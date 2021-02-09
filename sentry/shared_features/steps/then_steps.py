"""
"""
from behave import *
import sentry.shared_features.implementation.step_validator as _validate
from sentry.utilities.log import sentry_logger


@sentry_logger.logging_decorator
@step('the response json at {json_path} with {key} is saved')
def step_impl(context, json_path, key):
    _validate.save_value_from_response_json_at_path(context, json_path, key)
    sentry_logger.logger.info(f" {json_path}: {context.vars.get(key)} ")


@sentry_logger.logging_decorator
@step('the kafka json at {json_path} with {key} is saved')
def step_impl(context, json_path, key):
    _validate.save_value_from_kafka_json_at_path(context, json_path, key)
    sentry_logger.logger.info(f" {json_path}: {context.vars.get(key)} ")


@step('the kafka json at {json_path} is equal to {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.kafka_json_at_path_is_equal_to, context, json_path, value_str)


@step('the kafka json at {json_path} is not null')
def step_impl(context, json_path):
    _check_value_with(_validate.kafka_json_at_path_is_not_null, context, json_path)


@step('the data table at column {column_name} is not null')
def step_impl(context, column_name):
    _check_query_with(_validate.data_table_at_column_name_is_not_null, context, column_name)


@then('the data table at column {column_name} contains {value_str}')
def step_impl(context, column_name, value_str):
    _invoke_query_match(_validate.data_table_at_column_name_contains, context, column_name, value_str)


def _invoke_match(func, context, json_path, value_str):
    json_path = context.vars.resolve(json_path)
    value_str = context.vars.resolve(value_str)
    func(context.kafka_consumed_event, json_path, value_str)


def _check_value_with(func, context, json_path):
    json_path = context.vars.resolve(json_path)
    func(context.kafka_consumed_event, json_path)


def _invoke_query_match(func, context, column_name, value_str):
    column_name = context.vars.resolve(column_name)
    value_str = context.vars.resolve(value_str)
    func(context.query_result, column_name, value_str)


def _check_query_with(func, context, column_name):
    column_name = context.vars.resolve(column_name)
    func(context.query_result, column_name)
