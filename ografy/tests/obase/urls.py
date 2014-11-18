from django.conf.urls import patterns, url, include

import ografy.tests.obase.views as views


urlpatterns = patterns('',
    url(r'^form$', views.form, name='test_obase_form'),
    url(r'^list$', views.obase_list, name='test_obase_list')
)
