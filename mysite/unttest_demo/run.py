import unittest
# from test_sample import MyTestAdd
# from test_sample2 import MyTestSub
#
#
# suit = unittest.TestSuite()
# suit.addTest(MyTestAdd("test_add_1"))
# suit.addTest(MyTestAdd("test_add_2"))
# suit.addTest(MyTestSub("test_sub_1"))
# suit.addTest(MyTestSub("test_sub_2"))

suit = unittest.defaultTestLoader.discover("./test_dir", "test_*.py")


# 测试运行器
runner = unittest.TextTestRunner()
runner.run(suit)
