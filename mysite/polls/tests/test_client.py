from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone
from polls.tests.common import init_data


class IndexTestCase(TestCase):

    def setUp(self):
        init_data()

    def test_index_page(self):
        """问题列表页面"""
        response = self.client.get("/polls/")
        # print(response.content)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"what is new?", response.content)
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_detail_page(self):
        """问题详情页"""
        response = self.client.get("/polls/1/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"what is new?", response.content)
        self.assertIn(b"Not much", response.content)
        self.assertIn(b"The sky", response.content)
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_result_page(self):
        """投票结果页"""
        response = self.client.get("/polls/1/results/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"what is new?", response.content)
        self.assertIn(b"Not much", response.content)
        self.assertIn(b"The sky", response.content)
        self.assertIn(b"777", response.content)  # 验证投票数
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_vote_action(self):
        """投票行为"""
        response = self.client.post("/polls/1/vote/", data={"choice": 2})
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/polls/1/results/")
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"what is new?", response.content)
        # self.assertIn(b"Not much", response.content)
        # self.assertIn(b"The sky", response.content)
        self.assertIn(b"778", response.content)  # 验证投票数
        self.assertTemplateUsed(response, 'polls/results.html')


