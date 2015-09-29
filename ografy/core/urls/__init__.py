from django.conf.urls import include, patterns, url

import ografy.core.views as views
import ografy.core.views.auth as auth_views


urlpatterns = patterns('ografy.core.views',
    url(r'^/?$', views.home, name='home'),
    url(r'^blog/?$', views.blog, name='blog'),
    url(r'^contact/?$', views.ContactView.as_view(), name='contact'),
    url(r'^faq/?$', views.faq, name='faq'),
    url(r'^help/(?P<slug>[a-z0-9-]+)/?$', views.help, name='help'),
    url(r'^pricing/?$', views.pricing, name='pricing'),
    url(r'^privacy/?$', views.privacy, name='privacy'),
    url(r'^providers/?$', views.providers, name='providers'),
    url(r'^security/?$', views.security, name='security'),
    url(r'^signup/?$', views.SignupView.as_view(), name='signup'),
    url(r'^team/?$', views.team, name='team'),
    url(r'^terms/?$', views.terms, name='terms'),
    url(r'^upcoming/?$', views.upcoming, name='upcoming'),

    url(r'^login/?$', auth_views.LoginView.as_view(), name='login'),
    url(r'^login/sudo/?$', auth_views.SudoView.as_view(), name='sudo'),
    url(r'^logout/?$', auth_views.logout, name='logout'),
    url(r'^tokens/mapbox/?$', auth_views.mapbox_token, name='mapbox_token'),

    url(r'^settings', include('ografy.core.urls.settings', namespace='settings')),
    url(r'^connections', include('ografy.core.urls.connections', namespace='connections')),

    # url(r'^[A-Za-z0-9]/?$', user_views.profile),
)
