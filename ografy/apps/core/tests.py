import json

from ast import literal_eval
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.test import SimpleTestCase
from django.test import TransactionTestCase
from urllib.parse import urlparse

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
            },
            {
                'valid': False,
                'signup_form_info': {
                    'email': 'barankyle5@yahoo.com',
                    'handle': 'kyletest5',
                    'first_name': 'Kyle',
                    'last_name': 'Baran',
                    'password': 'fox'
                }
            }
        ]

        for case in signup_form_info_cases:
            if case.get('valid'):
                signup_form = SignUpForm(case.get('signup_form_info'))
                self.assertEqual(signup_form.is_valid(), True)
                response = self.client.post(reverse('core_signup'), case.get('signup_form_info'), HTTP_USER_AGENT='Mozilla/5.0')
                self.assertEqual(response.status_code, 302)
                self.assertEqual(type(response) is HttpResponseRedirect, True)
                self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')

            else:
                signup_form = SignUpForm(case.get('signup_form_info'))
                self.assertEqual(signup_form.is_valid(), False)
                response = self.client.post(reverse('core_signup'), case.get('signup_form_info'), HTTP_USER_AGENT='Mozilla/5.0')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(type(response) is HttpResponse, True)

# python ../manage.py dumpdata -e contenttypes -e auth.Permission --natural >
# ../ografy/apps/xauth/fixtures/xauth_test_db.json --indent 2
# http://stackoverflow.com/questions/853796/problems-with-contenttypes-when-loading-a-fixture-in-django
# manage.py dumpdata --natural will use a more durable representation of foreign keys.
# They are called "natural keys". For example:
# Permission.codename is used in favour of Permission.id
# User.username is used in favour of User.id
#
# Read more: natural keys section in "serializing django objects"
#
# Some other useful arguments for dumpdata:
# --indent=4 make it human readable.
# -e sessions exclude session data
# -e admin exclude history of admin actions on admin site
# -e contenttypes -e auth.Permission exclude objects which are recreated automatically
# from schema every time during syncdb. Only use it together with --natural or else you might
# end up with badly aligned id numbers.

class TestXAuthViews(TransactionTestCase):
    fixtures = ['xauth_test_db.json']

    # Test that you can sign up, log out, then log in
    def test_LoginView(self):

        signup_form_info = {
            'email': 'barankyle11@yahoo.com',
            'handle': 'kyletest11',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        # Check if the signup form is valid
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('core_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        # Test the login get functionality, which should just return an HttpResponse (status code 200)
        response = self.client.get(reverse('core_login'), HTTP_USER_AGENT='Mozilla/5.0')

        # TODO: FIX!
        # self.assertEqual(response.wsgi_request.META.get('PATH_INFO'), '/auth/applogin')

        # Check if this was an HttpResponse
        self.assertEqual(response.status_code, 200)

        # Test the login post functionality with an invalid form
        login_form_info = {
            'identifier': 'kyletest11',
            'remember_me': False
        }

        # Todo: Figure out how to test for invalid form
        response = self.client.post(reverse('core_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponse
        self.assertEqual(response.status_code, 200)

        # Test the login post functionality with a valid form that has an invalid identifier/username
        login_form_info = {
            'identifier': 'asdf',
            'password': 'Foxtrot0196',
            'remember_me': False
        }
        response = self.client.post(reverse('core_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')

        # self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponse
        self.assertEqual(response.status_code, 200)

        # Test the login post functionality with a valid form and an invalid password
        login_form_info = {
            'identifier': 'kyletest11',
            'password': 'asdf',
            'remember_me': False
        }
        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponse
        self.assertEqual(response.status_code, 200)

        # Test the login post functionality with a valid form and a valid identifier & password
        # that does not have remember-me set
        login_form_info = {
            'identifier': 'kyletest11',
            'password': 'Foxtrot1234',
            'remember_me': False
        }
        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)
        # If remember-me is not set, there should be no expiration cookie in sessionid
        self.assertEqual(response.client.cookies.get('sessionid').get('expires'), '')

        # Test the login post functionality with a valid form and a valid identifier & password
        # that does have remember-me set
        login_form_info = {
            'identifier': 'kyletest11',
            'password': 'Foxtrot1234',
            'remember_me': True
        }
        response = self.client.post(reverse('xauth_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)
        # If remember-me is set, there should be an expiration cookie in sessionid
        self.assertNotEqual(response.client.cookies.get('sessionid').get('expires'), '')

    # Test that you can sign up, log out, log in, then log out again
    def test_LogoutView(self):

        signup_form_info = {
            'email': 'barankyle12@yahoo.com',
            'handle': 'kyletest12',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        # Check if the signup form is valid
        self.assertEqual(signup_form.is_valid(), True)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('core_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        login_form_info = {
            'identifier': 'kyletest12',
            'password': 'Foxtrot1234',
            'remember_me': False
        }

        response = self.client.post(reverse('core_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('core_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('core_logout'), HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

    # Test proxy calls when logged in
    def test_Proxy(self):

        signup_form_info = {
            'email': 'barankyle14@yahoo.com',
            'handle': 'kyletest14',
            'first_name': 'Kyle',
            'last_name': 'Baran',
            'password': 'Foxtrot1234'
        }
        signup_form = SignUpForm(signup_form_info)
        # Check if the signup form is valid
        self.assertEqual(signup_form.is_valid(), True)

        # Test that a non-signed-in proxy call just redirects to the main page
        response = self.client.get(reverse('xauth_proxy'), {'api_call_urls': 'https://www.google.com'},
                                   HTTP_USER_AGENT='Mozilla/5.0')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('core_signup'), signup_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        json_data = open('ografy/apps/xauth/tests/xauth.json')
        test = json.load(json_data)
        test_cases = test.get('test_Proxy')

        for case in test_cases:

            response = self.client.get(reverse('xauth_proxy'), case.get('request_body'), HTTP_USER_AGENT='Mozilla/5.0')
            for assertion in case.get('asserts'):
                # Check that the HttpResponse is the code it should be.  The expected codes are in test_cases
                self.assertEqual(response.status_code, assertion.get('response'))

    def test_Associate(self):
        login_form_info = {
            'identifier': 'kbaran',
            'password': 'Foxtrot0196',
            'remember_me': True
        }

        response = self.client.post(reverse('core_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        backend_type = {
            'backend': 'facebook'
        }
        backend_associate_info = {
            'access_token': 'PSHPVDWN0NCQCUUIPUC3CQBZCDMOY4B3AYOAHGAAW1Y0V0DT',
            }

        response = self.client.get(reverse('xauth_associate', kwargs=backend_type),
                                   backend_associate_info, HTTP_USER_AGENT='Mozilla/5.0')

        # TODO: Fix
        # self.assertEqual(response.status_code, 200)

    def test_Call(self):
        login_form_info = {
            'identifier': 'kbaran',
            'password': 'Foxtrot0196',
            'remember_me': True
        }

        response = self.client.post(reverse('core_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        self.assertEqual(response.status_code, 302)

        backend_type = {
            'backend': 'facebook',
            }

        backend_call_info = {
            'backend_id': '1',
            'api_call_url': 'https://graph.facebook.com/v2.1/me?fields=friends'
        }
        response = self.client.get(reverse('xauth_call', kwargs=backend_type), backend_call_info,
                                   HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200)

    # Test backend signal call when logged in
    def test_Signals(self):

        login_form_info = {
            'identifier': 'kbaran',
            'password': 'Foxtrot0196',
            'remember_me': True
        }

        # Test that a non-signed-in signals call redirects to the main page
        response = self.client.get(reverse('xauth_signals'), HTTP_USER_AGENT='Mozilla/5.0')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('core_login'), login_form_info, HTTP_USER_AGENT='Mozilla/5.0')
        # Check if the response is to the core index page
        self.assertEqual(resolve(urlparse(response.url).path).view_name, 'core_index')
        # Check if this was an HttpResponseRedirect
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('xauth_signals'), HTTP_USER_AGENT='Mozilla/5.0')
        # Check if this was an HttpResponse
        self.assertEqual(response.status_code, 200)
        auths = literal_eval(response.content.decode('utf-8'))
        # The user should have at least one associated signal
        self.assertNotEqual(len(auths), 0)
        for item in auths:
            # Check that the signal id's are not zero
            self.assertGreater(item.get('id'), 0)
