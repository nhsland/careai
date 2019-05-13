from django.test import TestCase
from django.urls import reverse
from users.models import Developer, User, Clinician


class DeveloperCreationViewTest(TestCase):
    # def setUp(self):
    #     test_user1 = User.objects.create_user(username='testuser1', password='hello123!')
    #     test_user2 = User.objects.create_user(username='testuser2', password='hello123!')
    #
    #     test_user1.save()
    #     test_user2.save()

    def test_developer_form_without_email_input(self):
        response = self.client.post(reverse('developer_register'), {
            "username": "TestDeveloper",
            "password1": "hello123!",
            "password2": "hello123!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test_developer_form_with_mismatched_password(self):
        response = self.client.post(reverse('developer_register'), {
            "username": "TestDeveloper",
            "email": "test@gmail.com",
            "password1": "hello123!",
            "password2": "hello12!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn\'t match.')

    def test_valid_developer_form_data_returns_302_response(self):
        response = self.client.post(reverse('developer_register'), {
            "username": "TestDeveloper",
            "email": "test@gmail.com",
            "password1": "hello123!",
            "password2": "hello123!"
        })
        self.assertEqual(response.status_code, 302)

    # necessary since developer object is coded to be created when user is saved
    def test_valid_developer_form_data_creates_developer_object(self):
        response = self.client.post(reverse('developer_register'), {
            "username": "TestDeveloper",
            "email": "test@gmail.com",
            "password1": "hello123!",
            "password2": "hello123!"
        })
        self.assertEqual(str(Developer.objects.get(id=1)), "TestDeveloper")
        self.assertTrue(User.objects.get(id=1).is_developer)


class ClinicianCreationViewTest(TestCase):
    def test_clinician_form_without_email_input(self):
        response = self.client.post(reverse('clinician_register'), {
            "username": "TestClinician",
            "password1": "hello123!",
            "password2": "hello123!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test_clinician_form_with_mismatched_password(self):
        response = self.client.post(reverse('clinician_register'), {
            "username": "TestClinician",
            "email": "test@gmail.com",
            "password1": "hello123!",
            "password2": "hello12!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn\'t match.')

    def test_valid_clinician_form_data_returns_302_response(self):
        response = self.client.post(reverse('clinician_register'), {
            "username": "TestClinician",
            "email": "test@gmail.com",
            "password1": "hello123!",
            "password2": "hello123!"
        })
        self.assertEqual(response.status_code, 302)

    def test_valid_clinician_form_data_creates_clinician_object(self):
        response = self.client.post(reverse('clinician_register'), {
            "username": "TestClinician",
            "email": "test@gmail.com",
            "password1": "hello123!",
            "password2": "hello123!"
        })
        self.assertEqual(str(Clinician.objects.get(id=1)), "TestClinician")
        self.assertTrue(User.objects.get(id=1).is_clinician)
