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
    url(r'^signals/?$', user_views.signals, name='core_signals'),

    url(r'^contact/?$', views.contact, name='core_contact'),
    url(r'^login/?$', views.LoginView.as_view(), name='core_login'),
    url(r'^logout/?$', views.logout, name='core_logout'),
    url(r'^signup/?$', views.SignupView.as_view(), name='core_signup'),
    url(r'^start/?$', views.start, name='core_start'),
)
