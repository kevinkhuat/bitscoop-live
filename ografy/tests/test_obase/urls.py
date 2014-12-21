from django.conf.urls import patterns, url, include

import ografy.tests.test_obase.views as views
import ografy.apps.obase.views as ObaseViews


urlpatterns = patterns('',
    url(r'^form$', views.form, name='test_obase_form'),
    url(r'^list$', views.obase_list, name='test_obase_list')
)
