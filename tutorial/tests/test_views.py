from django.test import TestCase
from django.urls import reverse
from users.models import User


class TutorialListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tutorial/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('tutorial_main'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('tutorial_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutorial/tutorial_list.html')


class TutorialCreateViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='hello123!')
        test_user2 = User.objects.create_user(username='testuser2', password='hello123!')

        test_user1.save()
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('tutorial_create'))
        self.assertRedirects(response, '/login/?next=/tutorial/create/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='hello123!')
        response = self.client.get(reverse('tutorial_create'))

        # check that user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # check view is enabled for logged in user
        self.assertEqual(response.status_code, 200)

        # check correct template is used
        self.assertTemplateUsed(response, 'tutorial/tutorial_form.html')
