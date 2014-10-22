from django.core.urlresolvers import reverse, resolve
from django.test import SimpleTestCase
from ografy.apps.core.forms import SignUpForm
from urllib.parse import urlparse

import json

class TestXAuthViews(SimpleTestCase):

    fixtures = ['xauth_test_db']

    #Test that you can sign up, then logout
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

    #Test that you can sign up, log out, then log in
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

    #Test that you can sign up, log out, log in, then log out again
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

    #Test proxy calls when logged in
    def test_Proxy(self):

        signup_form_info = {
            'email': 'barankyle14@yahoo.com',
            'handle': 'kyletest14',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)


        json_data=open('ografy/apps/xauth/tests/xauth.json')
        test = json.load(json_data)
        test_cases = test.get('test_Proxy')

        for case in test_cases:

            response = self.client.get(reverse('xauth_proxy'), case.get('request_body'), HTTP_USER_AGENT='Mozilla/5.0')
            for assertion in case.get('asserts'):
                self.assertEqual(response.status_code, assertion.get('response'))

    # def test_Associate(self):
    #
    #     signup_form_info = {
    #         'email': 'barankyle15@yahoo.com',
    #         'handle': 'kyletest15',
    #         'first_name': 'Kyle',
    #         'last_name': 'Baran',
    #         'password': 'Foxtrot1234'
    #     }
    #     signup_form = SignUpForm(signup_form_info)
    #     self.assertEqual(signup_form.is_valid(), True)
    #
    #     response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
    #     self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
    #     self.assertEqual(response.status_code, 302)
    #
    #     backend_associate_info = {
    #         'backend': 'facebook',
    #
    #     }
    #     response = self.client.get(reverse('xauth_associate', {'backend': 'facebook'}), backend_associate_info, HTTP_USER_AGENT='Mozilla/5.0')
    #     self.assertEqual(response.status_code, 200)


    #Test backend signal call when logged in
    def test_Signals(self):

        login_form_info = {
            'identifier': 'barankyle30@gmail.com',
            'password': 'Foxtrot0196',
            'remember_me': True
        }

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('xauth_signals'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)

    #Test that you can't do proxy or backend signal calls when not logged in/signed up
    def test_NoProxy_NoSignals_WithoutLogin(self):

        signup_form_info = {
            'email': 'barankyle17@yahoo.com',
            'handle': 'kyletest17',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.get(reverse('xauth_proxy'), {'api_call_urls': 'https://www.google.com'}, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('xauth_signals'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)

