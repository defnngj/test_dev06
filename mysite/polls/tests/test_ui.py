from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from polls.models import Question, Choice
from django.utils import timezone
from time import sleep


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        Question.objects.create(id=1, question_text="what is new?", pub_date=timezone.now())
        Choice.objects.create(id=1, choice_text='Not much', votes=0, question_id=1)
        Choice.objects.create(id=2, choice_text='The sky', votes=0, question_id=1)

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/polls/'))
        sleep(2)
        self.selenium.find_element(By.ID, "1").click()
        sleep(2)
        self.selenium.find_element(By.XPATH, "//input[@type='radio' and @value='1']").click()  # not much
        sleep(2)
        self.selenium.find_element(By.ID, "voteButton").click()
        sleep(2)
        vote_number = self.selenium.find_elements(By.XPATH, "//div[@class='progress']/p")[0].text
        print(vote_number)
        self.assertEqual(vote_number, "1")




























