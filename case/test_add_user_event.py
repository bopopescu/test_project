import os
import sys
import unittest
import requests
from data import test_data

cur_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, cur_path)


class TestAddUser(unittest.TestCase):
    """添加用户"""

    def setUp(self):
        self.base_url = " https://easy-mock.com/mock/5d4bf9dbfdf8955fdbbfefca/example/posttest"

    def tearDown(self) -> None: print("")

    def test_add_event_all_null(self):
        """所有参数为空"""
        userload = {"username": "", "password": "", "telephone": "", "address": "",
                    "reg_time": ""}
        request = requests.post(self.base_url, data=userload)
        self.result = request.json()
        self.assertEqual(self.result["status"], 10001)
        self.assertEqual(self.result["message"], "Parameter error")

    def test_add_event_data_type_error(self):
        """日期格式错误"""
        postData = {"id": 5, "username": "小佳", "password": "789456", "telephone": "13298745632", "address": "广州天河新区",
                    "reg_time": "2018"}
        request = requests.post(self.base_url, data=postData)
        self.result = request.json()
        self.assertEqual(self.result["status"], 10002)
        self.assertEqual(self.result["message"], "Data Type Error")

    def test_add_event_success(self):
        """添加成功"""
        # postData = {"id": 6, "username": "小宋", "password": "888888", "telephone": "13298745632", "address": "广州天河新区",
        #             "reg_time": "2018-09-26 08:00:00"}
        postData = {}
        request = requests.post(self.base_url, data=postData)
        self.result = request.json()
        self.assertEqual(self.result["status"], 200)


if __name__ == "__main__":
    test_data.init_data()
    unittest.main()
