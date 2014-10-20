from urllib.parse import urlparse
from django.test import SimpleTestCase
from django.core.urlresolvers import reverse, resolve

from ografy.apps.core.forms import SignUpForm


class TestCoreViews(SimpleTestCase):
    def test_SignupView(self):

        response = self.client.get(reverse('core_signup'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)

        signup_form_info_cases = [
            {
                'valid': True,
                'signup_form_info': {
                    'email': 'barankyle@yahoo.com',
                    'handle': 'kyletest',
                    'first_name': 'Kyle',
                    'last_name': 'Baran',
                    'password': 'Foxtrot1234'
                }
            }
        ]

        for case in signup_form_info_cases:
            if case.get('valid'):
                signup_form = SignUpForm(case.get('signup_form_info'))
                self.assertEqual(signup_form.is_valid(), True)
                response = self.client.post(reverse('core_signup'), case.get('signup_form_info'), HTTP_USER_AGENT='Mozilla/5.0')
                self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')

            else:
                signup_form = SignUpForm(case.get('signup_form_info'))
                self.assertEqual(signup_form.is_valid(), False)
                response = self.client.post(reverse('core_signup'), case.get('signup_form_info'), HTTP_USER_AGENT='Mozilla/5.0')
                self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_signup')
