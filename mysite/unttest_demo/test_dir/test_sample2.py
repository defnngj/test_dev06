import unittest


# 功能
def sub(a, b):
    return a - b


def setUpModule():
    print("===模块的开始")


def tearDownModule():
    print("===模块的结束")


# 1. 测试类必须继承 unittest.TestCase
class MyTestSub(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("测试类开始")

    @classmethod
    def tearDownClass(cls) -> None:
        print("测试类结束")

    def setUp(self):
        print("用例开始：创建测试数据")

    def tearDown(self):
        print("用例结束：删除测试数据")

    # 2. 测试用例必须要”test“开头
    def test_sub_1(self):
        print("this is test case1")
        result = sub(1, 2)
        self.assertNotEqual(result, -1)

    def test_sub_2(self):
        print("this is test case2")
        result = sub(1.2, 2.1)
        self.assertEqual(result, -0.9000000000000001)


if __name__ == '__main__':
    unittest.main()


