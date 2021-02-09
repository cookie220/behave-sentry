"""
 Created by cookie.luo at 2020-08-28
"""
from os import listdir
from os.path import isfile, join
import os
from datetime import datetime, timedelta
import random
import xml.etree.ElementTree as et
import requests
from sentry.utilities.log import sentry_logger


class TestResultELK:

    @staticmethod
    def import_test_result(service_prefix, logstash_report_url, report_dir, need_import=True, report_type='behave_xml'):
        # prepare the output field
        if not need_import:
            return

        if report_type == 'behave_xml':
            now_time = datetime.now()
            local_time = now_time + timedelta(hours=8)
            local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
            test_execution_name = service_prefix + '-' + local_time
            component = service_prefix

            report_files = [f for f in listdir(report_dir) if isfile(join(report_dir, f))]

            for file in report_files:
                file_path = os.path.join(report_dir, file)
                tree = et.parse(file_path)
                root = tree.getroot()
                passes = str(int(root.attrib['tests']) - int(root.attrib['failures']) - int(root.attrib['skipped']))
                root.set('testExecutionName', test_execution_name)
                root.set('component', component)
                root.set('pass', passes)
                for testcase in root.iter('testcase'):
                    testcase.set('id', str(random.randint(888888888, 999999999)))
                tree.write(file_path)

                tree = et.parse(file_path)
                root = tree.getroot()
                xml_str = et.tostring(root, encoding='utf-8', method='xml')

                # send the xml str to logstash
                req = requests.session()
                req.keep_alive = False
                req.adapters.DEFAULT_RETRIES = 5
                request = req.post(logstash_report_url, data=xml_str)

                if request.status_code is 200:
                    sentry_logger.logger.info(f'import test result({file}) successfully!')
                else:
                    sentry_logger.logger.error(f'import test result({file}) failed!')
        else:
            sentry_logger.logger.error(f'failed to import test result, not found matched report type with({report_type}).')

