from django.test import TestCase
from challenges.models import Challenge
from users.models import Clinician, User


class ChallengeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Clinician.objects.create(user= User.objects.create_user(username="TestUser"))
        test_clinician = Clinician.objects.get(id=1)
        Challenge.objects.create(title="Test Challenge", brief="Test Challenge Brief", clinician=test_clinician)

    def test_string_representation(self):
        challenge = Challenge.objects.get(id=1)
        self.assertEquals(str(challenge), "Challenge: Test Challenge")

    def test_get_absolute_url(self):
        challenge = Challenge.objects.get(id=1)
        self.assertEquals(challenge.get_absolute_url(), '/challenges/1/')

    def test_date_created_label(self):
        challenge = Challenge.objects.get(id=1)
        field_label = challenge._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_title_max_length(self):
        challenge = Challenge.objects.get(id=1)
        max_length = challenge._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

