from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.test import SimpleTestCase
from ografy.apps.core.forms import SignUpForm
from urllib.parse import urlparse


class TestXAuthViews(SimpleTestCase):

    def test_SingleLogoutView(self):
        signup_form_info = {
            'email': 'barankyle10@yahoo.com',
            'handle': 'kyletest10',
            'first_name': 'Kyle10',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

    def test_LoginView(self):

        signup_form_info = {
            'email': 'barankyle11@yahoo.com',
            'handle': 'kyletest11',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        login_form_info = {
            'identifier': 'kyletest11',
            'password': 'Foxtrot1234',
            'remember_me': False
        }

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

    def test_DoubleLogoutView(self):
        signup_form_info = {
            'email': 'barankyle12@yahoo.com',
            'handle': 'kyletest12',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        login_form_info = {
            'identifier': 'kyletest12',
            'password': 'Foxtrot1234',
            'remember_me': False
        }

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

    def test_RememberMeView(self):
        signup_form_info = {
            'email': 'barankyle13@yahoo.com',
            'handle': 'kyletest13',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('xauth_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        login_form_info = {
            'identifier': 'kyletest13',
            'password': 'Foxtrot1234',
            'remember_me': True
        }

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        #Todo: Figure out where to navigate to to test remember_me functionality
        response = self.client.post(reverse('core_contact'), HTTP_USER_AGENT='Mozilla/5.0')
        # self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_contact')

        response = self.client.post(reverse('core_index'), HTTP_USER_AGENT='Mozilla/5.0')
        # self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # self.assert