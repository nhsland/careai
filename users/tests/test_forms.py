from django.test import TestCase
from users.forms import DeveloperRegisterForm, ClinicianRegisterForm
from users.models import User


'''
the following tests test the validation of the form itself, the testing of post requests made to forms
will be under the testing code in the views folder of other applications
'''


class UserFormTest(TestCase):
    def test_clinician_form_success(self):
        form_data = {
            "username": "TestClinician",
            "email": "testclinician@gmail.com",
            "password1": "hello123!",
            "password2": "hello123!"
        }
        form = ClinicianRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_developer_form_success(self):
        form_data = {
            "username": "TestDeveloper",
            "email": "testdeveloper@gmail.com",
            "password1": "hello123!",
            "password2": "hello123!"
        }
        form = DeveloperRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
