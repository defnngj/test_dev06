from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone


class QuestionTestCase(TestCase):

    def setUp(self):
        Question.objects.create(id=1, question_text="what's new?", pub_date=timezone.now())

    def test_question_query(self):
        """测试查询问题"""
        question = Question.objects.get(id=1)
        self.assertEqual(question.question_text, "what's new?")

    def test_question_create(self):
        """测试创建问题"""
        Question.objects.create(id=2, question_text="今天吃什么?", pub_date=timezone.now())
        question = Question.objects.get(id=2)
        self.assertEqual(question.question_text, "今天吃什么?")

    def test_question_update(self):
        """测试问题更新"""
        question = Question.objects.get(id=1)
        question.question_text = "周末是否加班？"
        question.save()
        question = Question.objects.get(id=1)
        self.assertEqual(question.question_text, "周末是否加班？")

    def test_question_delete(self):
        """测试删除问题"""
        question = Question.objects.get(id=1)
        question.delete()
        questions = Question.objects.all()
        self.assertEqual(len(questions), 0)


class ChoiceTestCase(TestCase):

    def setUp(self):
        Question.objects.create(id=1, question_text="what's new?", pub_date=timezone.now())
        Choice.objects.create(id=1, choice_text='Not much', votes=0, question_id=1)
        Choice.objects.create(id=2, choice_text='The sky', votes=0, question_id=1)

    def test_choice_query(self):
        """测试问题选项查询"""
        choice = Choice.objects.get(id=1)
        self.assertEqual(choice.choice_text, "The sky")

    # ... 作业






















