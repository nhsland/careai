from django.test import TestCase
from solutions.models import Solution
from challenges.models import Challenge
from users.models import Developer, Clinician, User


class SolutionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up developer required to associate solution with
        Developer.objects.create(user= User.objects.create_user(username="TestDeveloper"))
        test_developer = Developer.objects.get(id=1)

        # set up challenge required to associate solution with
        Clinician.objects.create(user=User.objects.create_user(username="TestClinician"))
        test_clinician = Clinician.objects.get(id=1)
        Challenge.objects.create(title="Test Challenge", brief="Test Challenge Brief", clinician=test_clinician)
        test_challenge = Challenge.objects.get(id=1)

        Solution.objects.create(title="Test Solution", developer=test_developer, challenge=test_challenge)

    def test_string_representation(self):
        solution = Solution.objects.get(id=1)
        self.assertEquals(str(solution), "Solution: Test Solution")

    def test_get_absolute_url(self):
        solution = Solution.objects.get(id=1)
        self.assertEquals(solution.get_absolute_url(), '/solutions/1/')

    def test_date_created_label(self):
        solution = Solution.objects.get(id=1)
        field_label = solution._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_title_max_length(self):
        solution = Solution.objects.get(id=1)
        max_length = solution._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_default_accuracy_level_is_zero(self):
        solution = Solution.objects.get(id=1)
        self.assertEquals(solution.accuracy, 0.0)

