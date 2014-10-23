from django.core.urlresolvers import reverse, resolve
from django.test import SimpleTestCase, TransactionTestCase
from ografy.apps.core.forms import SignUpForm
from urllib.parse import urlparse
from ast import literal_eval

import json

# python ../manage.py dumpdata -e contenttypes -e auth.Permission --natural > ../ografy/apps/xauth/fixtures/xauth_test_db.json --indent 2
# http://stackoverflow.com/questions/853796/problems-with-contenttypes-when-loading-a-fixture-in-django
# manage.py dumpdata --natural will use a more durable representation of foreign keys. They are called "natural keys". For example:
# Permission.codename is used in favour of Permission.id
# User.username is used in favour of User.id
#
# Read more: natural keys section in "serializing django objects"
#
# Some other useful arguments for dumpdata:
# --indent=4 make it human readable.
# -e sessions exclude session data
# -e admin exclude history of admin actions on admin site
# -e contenttypes -e auth.Permission exclude objects which are recreated automatically from schema every time during syncdb. Only use it together with --natural or else you might end up with badly aligned id numbers.

class TestXAuthViews(TransactionTestCase):
    fixtures = ['xauth_test_db.json']

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

        #Test that a non-signed-in proxy call just redirects to the main page
        response = self.client.get(reverse('xauth_proxy'), {'api_call_urls': 'https://www.google.com'}, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)

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

    def test_Associate(self):
        login_form_info = {
            'identifier': 'kbaran',
            'password': 'Foxtrot0196',
            'remember_me': True
        }

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        backend_type = {
            'backend': 'facebook'
        }
        backend_associate_info = {
            'access_token': 'PSHPVDWN0NCQCUUIPUC3CQBZCDMOY4B3AYOAHGAAW1Y0V0DT',
        }

        response = self.client.get(reverse('xauth_associate', kwargs=backend_type), backend_associate_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)

    # def test_Call(self):
    #     login_form_info = {
    #         'identifier': 'kbaran',
    #         'password': 'Foxtrot0196',
    #         'remember_me': True
    #     }
    #
    #     response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
    #     self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
    #     self.assertEqual(response.status_code, 302)
    #
    #     backend_call_info = {
    #         'backend': 'facebook',
    #     }
    #     response = self.client.get(reverse('xauth_call', kwargs=backend_call_info), HTTP_USER_AGENT='Mozilla/5.0')
    #     self.assertEqual(response.status_code, 200)

    #Test backend signal call when logged in
    def test_Signals(self):

        login_form_info = {
            'identifier': 'kbaran',
            'password': 'Foxtrot0196',
            'remember_me': True
        }

        #Test that a non-signed-in signals call redirects to the main page
        response = self.client.get(reverse('xauth_signals'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('xauth_signals'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)
        auths = literal_eval(response.content.decode('utf-8'))
        self.assertNotEqual(len(auths), 0)
        for item in auths:
            self.assertGreater(item.get('id'), 0)
