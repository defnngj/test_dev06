from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone


def init_data():
    Question.objects.create(id=1, question_text="what is new?", pub_date=timezone.now())
    Choice.objects.create(id=1, choice_text='Not much', votes=0, question_id=1)
    Choice.objects.create(id=2, choice_text='The sky', votes=777, question_id=1)