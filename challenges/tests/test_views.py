from django.test import TestCase
from django.urls import reverse

from challenges.models import Challenge
from users.models import User, Clinician


class ChallengeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 challenges for pagination tests
        number_of_challenges = 13

        for challenge_id in range(number_of_challenges):
            name = 'testuser' + str(challenge_id)
            test_user = User.objects.create_user(username=name, password='hello123!', is_clinician=True)
            test_clinician = Clinician.objects.create(user=test_user)
            title = "Test Challenge " + str(challenge_id)
            Challenge.objects.create(title=title, brief="Test Challenge Brief", clinician=test_clinician)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/challenges/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('challenges_main'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('challenges_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenges/challenge_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('challenges_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['challenges']), 5)

    def test_lists_all_challenges(self):
        # Get third page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('challenges_main') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['challenges']), 3)


class ChallengeUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='hello123!', is_clinician=True)
        Clinician.objects.create(user=test_user1)
        test_user2 = User.objects.create_user(username='testuser2', password='hello123!')
        Clinician.objects.create(user=test_user2)

        # create challenge object using test_user1
        test_clinician = Clinician.objects.get(id=1)
        Challenge.objects.create(title="Test Challenge", brief="Test Challenge Brief", clinician=test_clinician)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.get('/challenges/1/update')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.get(reverse('challenges_update', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.get(reverse('challenges_update', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenges/challenge_form.html')

    def test_view_is_403_forbidden_for_other_users(self):
        # log in using testuser2 who is not the creator of the challenge
        self.client.login(username="testuser2", password="hello123!")
        response = self.client.get(reverse('challenges_update', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_redirects_for_users_not_logged_in(self):
        response = self.client.get(reverse('challenges_update', kwargs={"pk": 1}))
        self.assertRedirects(response, '/login/?next=/challenges/1/update')

    def test_view_updates_challenge_when_posted_to(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.post(reverse("challenges_update", kwargs={"pk": 1}), {
            "title": "Revised Challenge",  # necessary to populate the whole form for a successful post
            "brief": "Revised Brief",
            "award": 70,
            "description": "test",
            "evaluation": "test",
            "timeline": "test",
            "rule": "test"
        })
        self.assertEqual(response.status_code, 302)

        # fetch and test updated challenge's field
        challenge = Challenge.objects.get(id=1)
        self.assertEqual(challenge.title, "Revised Challenge")


class ChallengeDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='hello123!', is_clinician=True)
        Clinician.objects.create(user=test_user1)
        test_user2 = User.objects.create_user(username='testuser2', password='hello123!')
        Clinician.objects.create(user=test_user2)

        # create challenge object using test_user1
        test_clinician = Clinician.objects.get(id=1)
        Challenge.objects.create(title="Test Challenge", brief="Test Challenge Brief", clinician=test_clinician)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.get('/challenges/1/delete')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.get(reverse('challenges_delete', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.get(reverse('challenges_delete', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'challenges/challenge_confirm_delete.html')

    def test_view_is_403_forbidden_for_other_users(self):
        # log in using testuser2 who is not the creator of the challenge
        self.client.login(username="testuser2", password="hello123!")
        response = self.client.get(reverse('challenges_delete', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_redirects_for_users_not_logged_in(self):
        response = self.client.get(reverse('challenges_delete', kwargs={"pk": 1}))
        self.assertRedirects(response, '/login/?next=/challenges/1/delete')

    def test_view_deletes_challenge_when_posted_to(self):
        self.client.login(username="testuser1", password="hello123!")
        response = self.client.post(reverse("challenges_delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRaises(Challenge.DoesNotExist, Challenge.objects.get, id="1")
