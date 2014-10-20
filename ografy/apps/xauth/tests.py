from urllib.parse import urlparse
from django.test import SimpleTestCase
from django.core.urlresolvers import reverse, resolve


class LoginTest(SimpleTestCase):

    def test_LoginView(self):

        signup_form_info = {
            'email': 'barankyl2e@yahoo.com',
            'handle': 'kyletest2',
            'first_name': 'Kyle2',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')

        login_form_info = {
            'identifier': 'kyletest2',
            'password': 'Foxtrot1234',
            'remember_me': False
        }

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')


class SingleLogoutTest(SimpleTestCase):

    def test_logout(self):
        signup_form_info = {
            'email': 'barankyl3e@yahoo.com',
            'handle': 'kyletest3',
            'first_name': 'Kyle3',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')

        
class DoubleLogoutTest(SimpleTestCase):

    def test_logout(self):
        signup_form_info = {
            'email': 'barankyle4@yahoo.com',
            'handle': 'kyletest4',
            'first_name': 'Kyle4',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')
