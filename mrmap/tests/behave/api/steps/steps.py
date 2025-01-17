import json
from unittest.mock import Mock, patch

from behave import given, step, then
from django.db import reset_queries
from django.http import SimpleCookie
from rest_framework.authtoken.models import Token


@step('I am logged in as {username} with password {password}')
def step_impl(context, username, password):
    success = context.client.login(username=username, password=password)
    if not success:
        raise Exception(
            f"can't log in user {username} with password {password}")


@step('I logout the current user')
def step_impl(context,):
    context.client.logout()


@step('I use token authentication as {username}')
def step_impl(context, username):
    token = Token.objects.get_or_create(user__username=username)
    context.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


@step('I enforce csrf checks')
def step_impl(context):
    context.client.enforce_csrf_checks = True


@step('I use the endpoint {url}')
def step_impl(context, url):
    context.endpoint = url


@given('I set the request payload to')
def step_impl(context):
    context.payload = context.text


@given('I set a queryparam "{param}" with value "{value}"')
def step_impl(context, param, value):
    context.query_params.update({param: value})


@step('I set the content type of the request to {content_type}')
def step_impl(context, content_type):
    context.content_type = content_type


@step('I send the request with GET method')
def step_impl(context):
    reset_queries()
    context.response = context.client.get(
        path=context.endpoint,
        data=context.query_params or None)


@step('I send the request with PATCH method')
def step_impl(context):
    reset_queries()
    context.response = context.client.patch(
        path=context.endpoint,
        data=context.payload,
        content_type=context.content_type if hasattr(context, 'content_type') else 'application/json',)


@step('I send the request with POST method')
def step_impl(context):
    reset_queries()
    context.response = context.client.post(
        path=context.endpoint,
        data=context.payload,
        content_type=context.content_type if hasattr(context, 'content_type') else 'application/json')


@step('I send the request with DELETE method')
def step_impl(context):
    reset_queries()
    context.response = context.client.delete(
        path=context.endpoint)


@then('I expect the response status is {expected_status}')
def step_impl(context, expected_status: int):
    context.test.assertEqual(
        context.response.status_code, int(expected_status))


def _traverse_json(context, attribute):
    keys = attribute.split('.')
    json = context.response.json()
    value = None
    for key in keys:
        if '[' and ']' in key:
            key = int(key.split('[')[-1].split(']')[0])
        value = json[key] if not value else value[key]
    return value


@then('I expect that response json has an attribute "{attribute}"')
@then('I expect that response json has an attribute "{attribute}" with value "{expected_value}"')
def step_impl(context, attribute, expected_value=None):
    value = _traverse_json(context=context, attribute=attribute)
    if expected_value:
        if expected_value == 'false' or expected_value == 'true':
            context.test.assertEqual(bool(value), bool(expected_value))
        else:
            context.test.assertEqual(str(value), expected_value)


@then('I expect that "{expected_value}" queries where made')
def step_impl(context, expected_value):
    context.test.assertNumQueries(expected_value)


@given('I mock the function "{func_name}" of the module "{module_name}" with return value as object')
def step_impl(context, func_name, module_name):
    mock = Mock()
    setattr(mock, func_name, Mock(return_value=json.loads(context.text)))
    patcher = patch(module_name, mock)
    patcher.start()
    context.patchers.append(patcher)

# @then('I expect that the function "{func_name}" of the module "{module_name}" was called with')
# def step_impl(context, func_name, module_name, args, kwargs):
#     callvalues = dict(context.text)


@given('I set the cookie "{cookie_name}" with value "{cookie_value}"')
def step_impl(context, cookie_name, cookie_value):
    if not context.client.cookies:
        context.client.cookies = SimpleCookie()
    context.client.cookies[cookie_name] = cookie_value
