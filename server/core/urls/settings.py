from django.conf.urls import patterns, url

import server.core.views.settings as views


urlpatterns = patterns('',
    url(r'^/?$', views.BaseView.as_view(), name='base'),
    url(r'^/account/?$', views.AccountView.as_view(), name='account'),
    url(r'^/account/handle/?$', views.AccountHandleView.as_view(), name='account-handle'),
    url(r'^/account/password/?$', views.AccountPasswordView.as_view(), name='account-password'),
    url(r'^/account/deactivate/?$', views.AccountDeactivateView.as_view(), name='account-deactivate'),
    url(r'^/billing/?$', views.BillingView.as_view(), name='billing'),
    url(r'^/emails/?$', views.EmailsView.as_view(), name='emails'),
    url(r'^/location/?$', views.LocationView.as_view(), name='location'),
    url(r'^/notifications/?$', views.NotificationsView.as_view(), name='notifications'),
    url(r'^/profile/?$', views.ProfileView.as_view(), name='profile'),
    url(r'^/security/?$', views.SecurityView.as_view(), name='security'),
    url(r'^/connections/?$', views.ConnectionsView.as_view(), name='connections'),
)
