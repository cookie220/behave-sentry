"""
"""
from jsonpath import jsonpath
import jsonschema
from assertpy import assert_that, fail


def save_value_from_response_json_at_path(context, json_path, key):
    """
    """
    context.vars.add(key, _get_values(context.response.json(), json_path)[0])


def save_value_from_kafka_json_at_path(context, json_path, key):
    """
    """
    context.vars.add(key, _get_values(context.kafka_consumed_event, json_path)[0])


def response_json_at_path_is_equal_to(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_equal_to(eval(value)) for actual_value in values]


def _get_values(json_body, json_path):
    results = jsonpath(json_body, json_path)
    if not results: fail('Match not found at <{path}> for <{body}>'.format(path=json_path, body=json_body))
    return results


def _validate_with_schema(json_body, schema):
    jsonschema.validate(json_body, schema)


def kafka_json_at_path_is_equal_to(event, json_path, value):
    """
    """
    values = _get_values(event, json_path)
    [assert_that(actual_value).is_equal_to(eval(value)) for actual_value in values]


def kafka_json_at_path_is_not_null(event, json_path):
    """
    """
    values = _get_values(event, json_path)
    [assert_that(actual_value).is_not_none() for actual_value in values]


def data_table_at_column_name_is_not_null(query_result, column_name):
    """
    """
    values = _get_query_values(query_result, column_name)
    [assert_that(actual_value).is_not_none() for actual_value in values]


def data_table_at_column_name_contains(query_result, column_name, value):
    """
    """
    values = _get_query_values(query_result, column_name)
    assert values.count(value) > 0


def _get_query_values(result, column_name):
    values = []
    if len(result) >= 1:
        for r in result:
            values.append(str(r[column_name]))
    return values

