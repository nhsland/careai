from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from challenges.models import Challenge
from solutions.models import Solution
from users.models import User, Developer, Clinician


class SolutionViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/solutions/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('solutions_main'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('solutions_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solutions/solution_list.html')


class SolutionUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_developer1 = User.objects.create_user(username='developer1', password='hello123!', is_developer=True)
        Developer.objects.create(user=test_developer1)
        test_developer2 = User.objects.create_user(username='developer2', password='hello123!', is_developer=True)
        Developer.objects.create(user=test_developer2)
        test_clinician1 = User.objects.create_user(username='clinician1', password='hello123!', is_clinician=True)
        Clinician.objects.create(user=test_clinician1)

        # create challenge object using test_clinician1
        test_clinician = Clinician.objects.get(id=1)
        test_challenge = Challenge.objects.create(title="Test Challenge", brief="Test Challenge Brief", clinician=test_clinician)

        # set up file data and developer to create test solution
        test_developer = Developer.objects.get(id=1)
        solution_data = SimpleUploadedFile("data.txt", b"file_content")
        solution_notebook = ContentFile(b'{"cells":[]}')
        solution_notebook.name = "solution.ipynb"
        Solution.objects.create(title="Test Solution", description="Test Description",
                                developer=test_developer, challenge=test_challenge,
                                solution_notebook=solution_notebook,solution_data=solution_data)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.get('/solutions/1/update')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.get(reverse('solutions_update', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.get(reverse('solutions_update', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solutions/solution_form.html')

    def test_view_is_403_forbidden_for_other_users(self):
        # log in using developer2 who is not the creator of the challenge
        self.client.login(username="developer2", password="hello123!")
        response = self.client.get(reverse('solutions_update', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_redirects_for_users_not_logged_in(self):
        response = self.client.get(reverse('solutions_update', kwargs={"pk": 1}))
        self.assertRedirects(response, '/login/?next=/solutions/1/update')

    def test_view_updates_challenge_when_posted_to(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.post(reverse("solutions_update", kwargs={"pk": 1}), {
            "title": "Revised Solution",
            "description": "Revised Description",
        })
        self.assertEqual(response.status_code, 302)

        # fetch and test updated challenge's field
        solution = Solution.objects.get(id=1)
        self.assertEqual(solution.title, "Revised Solution")


class SolutionDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_developer1 = User.objects.create_user(username='developer1', password='hello123!', is_developer=True)
        Developer.objects.create(user=test_developer1)
        test_developer2 = User.objects.create_user(username='developer2', password='hello123!', is_developer=True)
        Developer.objects.create(user=test_developer2)
        test_clinician1 = User.objects.create_user(username='clinician1', password='hello123!', is_clinician=True)
        Clinician.objects.create(user=test_clinician1)

        # create challenge object using test_clinician1
        test_clinician = Clinician.objects.get(id=1)
        test_challenge = Challenge.objects.create(title="Test Challenge", brief="Test Challenge Brief",
                                                  clinician=test_clinician)

        # create solution object using test_developer1 and test_challenge
        test_developer = Developer.objects.get(id=1)
        Solution.objects.create(title="Test Solution", description="Test Description", developer=test_developer,
                                challenge=test_challenge)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.get('/solutions/1/delete')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.get(reverse('solutions_delete', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.get(reverse('solutions_delete', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solutions/solution_confirm_delete.html')

    def test_view_is_403_forbidden_for_other_users(self):
        # log in using developer2 who is not the creator of the challenge
        self.client.login(username="developer2", password="hello123!")
        response = self.client.get(reverse('solutions_delete', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_redirects_for_users_not_logged_in(self):
        response = self.client.get(reverse('solutions_delete', kwargs={"pk": 1}))
        self.assertRedirects(response, '/login/?next=/solutions/1/delete')

    def test_view_deletes_challenge_when_posted_to(self):
        self.client.login(username="developer1", password="hello123!")
        response = self.client.post(reverse("solutions_delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRaises(Solution.DoesNotExist, Solution.objects.get, id="1")
