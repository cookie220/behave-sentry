"""
 Created by cookie.luo at 2020-08-13
"""
import requests
from sentry.utilities.common.config import Config
from sentry.utilities.log import sentry_logger
import json
import ast


class XrayClient:
    XRAY_SERVICE_NAME = 'https://xray.cloud.xpand-it.com/'
    XRAY_AUTH_URL_ENDPOINT = 'api/v1/authenticate'
    XRAY_GRAPHQL = 'api/v1/graphql'
    XRAY_TEST_PROJECT_KEY = 'key'
    XRAY_IMPORT_CUCUMBER_TESTS = 'api/v1/import/feature'

    @staticmethod
    def get_xray_token() -> str:
        # Instantiate the client and secret.
        client_id = Config.get_config().get('xray', 'client_id')
        client_secret = Config.get_config().get('xray', 'client_secret')

        # Instantiate the url and body
        url = XrayClient.XRAY_SERVICE_NAME + XrayClient.XRAY_AUTH_URL_ENDPOINT
        body = {'client_id': client_id, 'client_secret': client_secret}

        re = requests.post(url, data=body)
        sentry_logger.logger.info(' Xray token is %s', re.text)

        return eval(re.text)

    @staticmethod
    def create_xray_test_plan(plan_summary):
        # Instantiate the url and header.
        url = XrayClient.XRAY_SERVICE_NAME + XrayClient.XRAY_GRAPHQL
        headers = {'Authorization': 'Bearer ' + XrayClient.get_xray_token()}

        mutation = '''mutation{{
                     createTestPlan(
                             jira:{{
                                fields:{{
                                        summary: "{summary}",
                                        project: {{key: "{cht_key}"}}
                                     }}
                         }}
                    )
                    {{
                         testPlan {{
                             issueId
                             jira(fields: ["key"])
                    }}
                         warnings
                    }}
                 }}
             '''.format(summary=plan_summary, cht_key=XrayClient.XRAY_TEST_PROJECT_KEY)

        request = requests.post(url, json={'query': mutation}, headers=headers)

        if request.status_code == 200:
            created_test_plan = request.json()['data']['createTestPlan']['testPlan']['issueId'], \
                                request.json()['data']['createTestPlan']['testPlan']['jira']['key']
            sentry_logger.logger.info(' Created test plan : %s', created_test_plan)
            return created_test_plan

        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, mutation))

    @staticmethod
    def is_xray_test_plan_created(issue_id) -> bool:
        # Instantiate the url and header.
        url = XrayClient.XRAY_SERVICE_NAME + XrayClient.XRAY_GRAPHQL
        headers = {'Authorization': 'Bearer ' + XrayClient.get_xray_token()}

        query = '''query{{
                        getTestPlan(issueId: "{issueId}"){{                      
                        issueId
                        }}
                    }}
                     '''.format(issueId=issue_id)

        request = requests.post(url, json={'query': query}, headers=headers)

        if request.status_code == 200:
            if 'errors' not in request.json():
                return request.json()['data']['getTestPlan']['issueId'] == issue_id
            else:
                return False
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    @staticmethod
    def import_xray_feature(filename) -> list:
        url = XrayClient.XRAY_SERVICE_NAME + XrayClient.XRAY_IMPORT_CUCUMBER_TESTS \
              + f'?projectKey={XrayClient.XRAY_TEST_PROJECT_KEY}'
        headers = {'Authorization': 'Bearer ' + XrayClient.get_xray_token()}

        if filename.endswith('feature'):
            openfile = open(filename, 'rb')
            multipart_form_data = {'file': openfile}
            request = requests.post(url, headers=headers, files=multipart_form_data)

            if request.status_code == 200:
                imported_tests = json.dumps([r['id'] for r in request.json()['updatedOrCreatedTests']])
                imported_precondition = json.dumps([r['id'] for r in request.json()['updatedOrCreatedPreconditions']])
                sentry_logger.logger.info(' Imported tests : %s', imported_tests)
                return imported_tests, imported_precondition
            else:
                raise Exception("import failed to run by returning code of {}. {}".format(request.json(), request.text))

    @staticmethod
    def add_tests_to_test_plan(testPlan_issue_id, test_issue_ids) -> list:
        # Instantiate the url and header.
        url = XrayClient.XRAY_SERVICE_NAME + XrayClient.XRAY_GRAPHQL
        headers = {'Authorization': 'Bearer ' + XrayClient.get_xray_token()}

        mutation = '''
                     mutation {{
                            addTestsToTestPlan(
                                    issueId: "{testPlan_issue_id}",
                                    testIssueIds: {test_issue_ids}
                                ) 
                                {{
                                    addedTests
                                    warning
                                }}
                            }}
                            '''.format(testPlan_issue_id=testPlan_issue_id, test_issue_ids=test_issue_ids)

        request = requests.post(url, json={'query': mutation}, headers=headers)

        if request.status_code == 200:
            added_tests = request.json()['data']['addTestsToTestPlan']['addedTests']
            sentry_logger.logger.info(' Added tests to plan : %s', added_tests)
            return added_tests
        else:
            raise Exception("query failed to run by returning code of {}. {}".format(request.status_code, mutation))

    @staticmethod
    def add_precondition_to_test(precondition_issue_ids, test_issue_id) -> list:
        # Instantiate the url and header.
        url = XrayClient.XRAY_SERVICE_NAME + XrayClient.XRAY_GRAPHQL
        headers = {'Authorization': 'Bearer ' + XrayClient.get_xray_token()}

        mutation = '''
                         mutation {{
                                addPreconditionsToTest(
                                        issueId: "{test_issue_id}",
                                        preconditionIssueIds: {precondition_issue_ids}
                                    ) 
                                    {{
                                        addedPreconditions
                                        warning
                                    }}
                                }}
                                '''.format(precondition_issue_ids=precondition_issue_ids, test_issue_id=test_issue_id)

        request = requests.post(url, json={'query': mutation}, headers=headers)

        if request.status_code == 200:
            added_Preconditions = request.json()['data']['addPreconditionsToTest']['addedPreconditions']
            sentry_logger.logger.info(' Added preconditions to plan : %s', added_Preconditions)
            return added_Preconditions
        else:
            raise Exception("query failed to run by returning code of {}. {}".format(request.status_code, mutation))

    @staticmethod
    def perform_xray_flow(feature_files, test_plan_summary, force_import=False):
        if Config.get_config_value('xray', 'test_plan_issue_id') is None:
            test_plan = XrayClient.create_xray_test_plan(test_plan_summary)
            Config.write_config('xray', 'test_plan_issue_id', test_plan[0])
            Config.write_config('xray', 'test_plan_project_id', test_plan[1])
            force_import = True

        if force_import:
            for feature in feature_files:
                imported_response = XrayClient.import_xray_feature(feature)
                imported_tests, imported_precondition = imported_response[0], imported_response[1]
                XrayClient.add_tests_to_test_plan(Config.get_config_value('xray', 'test_plan_issue_id'), imported_tests)
                for test in ast.literal_eval(imported_tests):
                    XrayClient.add_precondition_to_test(imported_precondition, test)

