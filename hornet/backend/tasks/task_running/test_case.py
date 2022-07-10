import os
import sys
import json
import jmespath
import unittest
import requests
from XTestRunner import XMLTestRunner
from ddt import ddt, data, file_data, idata, unpack

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from cases.apis.common import get_replace_string, update_extract_vlue, query_extract_vlue


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA = os.path.join(BASE_DIR, "test_data.json")
TEST_REPORT = os.path.join(BASE_DIR, "xml_result.xml")


@ddt
class MyTest(unittest.TestCase):

    @file_data(TEST_DATA)
    def test_api(self, case_id, url, method, header, params_type, params_body, assert_type, assert_text):

        # 使用提取器
        url = get_replace_string(url)

        header_new = {}
        for key, value in header.items():
            header_new[key] = get_replace_string(value)

        params_body_new = {}
        for key, value in params_body.items():
            params_body_new[key] = get_replace_string(value)

        # 执行用例
        resp = ""
        if method == "get":
            resp = requests.get(url, headers=header_new, params=params_body_new)

        elif method == "post":
            if params_type == "form":
                resp = requests.post(url, headers=header_new, data=params_body_new)
            elif params_type == "json":
                resp = requests.post(url, headers=header_new, json=params_body_new)

        elif method == "put":
            if params_type == "form":
                resp = requests.put(url, headers=header_new, data=params_body_new)
            elif params_type == "json":
                resp = requests.put(url, headers=header_new, json=params_body_new)

        elif method == "delete":
            if params_type == "form":
                resp = requests.delete(url, headers=header_new, data=params_body_new)
            elif params_type == "json":
                resp = requests.delete(url, headers=header_new, json=params_body_new)

        if assert_type == "include":
            self.assertIn(assert_text, resp.text)

        elif assert_type == "equal":
            self.assertEqual(assert_text, resp.text)

        # 提取变量
        # extracts = TestExtract.objects.filter(case_id=case_id)
        extracts = query_extract_vlue(case_id)

        if len(extracts) > 0:

            response = resp.json()
            for extract_obj in extracts:
                result = jmespath.search(extract_obj[2], response)
                if result is None:
                    raise ValueError(f"提取器错误: {extract_obj[2]}")
                else:
                    update_extract_vlue(case_id, extract_obj[1], result)


if __name__ == '__main__':
    with(open(TEST_REPORT, 'wb')) as fp:
        unittest.main(testRunner=XMLTestRunner(output=fp))






















