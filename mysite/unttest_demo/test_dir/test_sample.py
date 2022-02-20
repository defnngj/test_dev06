import unittest


# 功能
def add(a, b):
    return a + b


def setUpModule():
    print("===模块的开始")


def tearDownModule():
    print("===模块的结束")


# 1. 测试类必须继承 unittest.TestCase
class MyTestAdd(unittest.TestCase):

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
    def test_add_1(self):
        print("this is test case1")
        result = add(1, 2)
        self.assertNotEqual(result, 4)

    def test_add_2(self):
        print("this is test case2")
        result = add(1.2, 2.1)
        self.assertEqual(result, 3.3)

    def test_in(self):
        self.assertIn("hi", "hello world")


if __name__ == '__main__':
    unittest.main()
    # 测试套件
    # suit = unittest.TestSuite()
    # suit.addTest(MyTest("test_add_1"))
    # suit.addTest(MyTest("test_add_2"))
    # # 测试运行器
    # runner = unittest.TextTestRunner()
    # runner.run(suit)








