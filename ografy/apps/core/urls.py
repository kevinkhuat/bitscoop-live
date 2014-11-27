from django.conf.urls import patterns, url

import ografy.apps.core.views as views
import ografy.apps.core.views.account as account_views
import ografy.apps.core.views.user as user_views


urlpatterns = patterns('',
    url(r'^$', views.index, name='core_index'),

    url(r'^account/?$', account_views.index, name='core_account_index'),
    url(r'^account/details/?$', account_views.DetailsView.as_view(), name='core_account_details'),
    url(r'^account/password/?$', account_views.PasswordView.as_view(), name='core_account_password'),

    url(r'^user/?$', user_views.my_profile, name='core_user_my_profile'),
    url(r'^user/(?P<handle>\w+)/?$', user_views.profile, name='core_user_profile'),

    url(r'^login/?$', account_views.LoginView.as_view(), name='core_account_login'),
    url(r'^logout/?$', account_views.logout, name='core_account_logout'),
    url(r'^signup/?$', account_views.SignupView.as_view(), name='core_account_signup'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^start/?$', views.start, name='core_start'),
)
