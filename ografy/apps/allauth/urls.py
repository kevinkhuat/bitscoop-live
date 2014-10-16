from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='allauth_home'),
    url(r'^email-sent/', 'views.validation_sent', name='allauth_validation_sent'),
    url(r'^login/$', 'views.home', name='allauth_login'),
    url(r'^logout/$', 'views.logout', name='allauth_logout'),
    url(r'^done/$', 'views.done', name='allauth_done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'views.ajax_auth', name='allauth_ajax-auth'),
    url(r'^ajax-logged-in-backends/$', 'views.ajax_logged_in_backends',
       name='allauth_ajax-logged-in-backends'),
    url(r'^ajax-auth-call/(?P<backend>[^/]+)/$', 'views.ajax_auth_call', name='allauth_ajax-auth-call'),
    url(r'^email/$', 'views.require_email', name='allauth_require_email')
)
