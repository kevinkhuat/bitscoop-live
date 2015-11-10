from django.conf.urls import include, patterns, url

import server.core.views as views
import server.core.views.auth as auth_views


urlpatterns = patterns('server.core.views',
    url(r'^/?$', views.HomeView.as_view(), name='home'),
    url(r'^blog/?$', views.BlogView.as_view(), name='blog'),
    url(r'^contact/?$', views.ContactView.as_view(), name='contact'),
    url(r'^faq/?$', views.FaqView.as_view(), name='faq'),
    url(r'^help/(?P<slug>[a-z0-9-]+)/?$', views.HelpView.as_view(), name='help'),
    url(r'^pricing/?$', views.PricingView.as_view(), name='pricing'),
    url(r'^privacy/?$', views.PrivacyView.as_view(), name='privacy'),
    url(r'^providers/?$', views.ProvidersView.as_view(), name='providers'),
    url(r'^security/?$', views.SecurityView.as_view(), name='security'),
    url(r'^signup/?$', views.SignupView.as_view(), name='signup'),
    url(r'^team/?$', views.TeamView.as_view(), name='team'),
    url(r'^terms/?$', views.TermsView.as_view(), name='terms'),
    url(r'^upcoming/?$', views.UpcomingView.as_view(), name='upcoming'),

    url(r'^login/?$', auth_views.LoginView.as_view(), name='login'),
    url(r'^login/sudo/?$', auth_views.SudoView.as_view(), name='sudo'),
    url(r'^logout/?$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^tokens/mapbox/?$', auth_views.MapboxTokenView.as_view(), name='mapbox_token'),

    url(r'^settings', include('server.core.urls.settings', namespace='settings')),
    url(r'^connections', include('server.core.urls.connections', namespace='connections')),

    # url(r'^[A-Za-z0-9]/?$', user_views.profile),
)
