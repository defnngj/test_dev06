import os
import unittest
import requests
from XTestRunner import XMLTestRunner
from ddt import ddt, data, file_data, idata, unpack

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA = os.path.join(BASE_DIR, "test_data.json")
TEST_REPORT = os.path.join(BASE_DIR, "xml_result.xml")


@ddt
class MyTest(unittest.TestCase):

    @file_data(TEST_DATA)
    def test_api(self, url, method, header, params_type, params_body, assert_type, assert_text):
        resp = ""
        if method == "get":
            resp = requests.get(url, headers=header, params=params_body).text

        elif method == "post":
            if params_type == "form":
                resp = requests.post(url, headers=header, data=params_body).text
            elif params_type == "json":
                resp = requests.post(url, headers=header, json=params_body).text

        elif method == "put":
            if params_type == "form":
                resp = requests.put(url, headers=header, data=params_body).text
            elif params_type == "json":
                resp = requests.put(url, headers=header, json=params_body).text

        elif method == "delete":
            if params_type == "form":
                resp = requests.delete(url, headers=header, data=params_body).text
            elif params_type == "json":
                resp = requests.delete(url, headers=header, json=params_body).text

        if assert_type == "include":
            self.assertIn(assert_text, resp)

        elif assert_type == "equal":
            self.assertEqual(assert_text, resp)


if __name__ == '__main__':
    with(open(TEST_REPORT, 'wb')) as fp:
        unittest.main(testRunner=XMLTestRunner(output=fp))






















