from django.conf.urls.defaults import patterns, include, url

from tastypie.api import Api
from Geddit.api.resources import UserResource, ItemResource, ClaimResource, CategoryResource, FilterResource
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ClaimResource())
v1_api.register(ItemResource())
v1_api.register(CategoryResource())
v1_api.register(FilterResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geddit.views.home', name='home'),
    # url(r'^geddit/', include('geddit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'data.views.index'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
    url(r'^jstest/', 'jstest.views.index'),
    url(r'^api/', include(v1_api.urls)),
    url(r'', 'data.views.index')
=======

    #url(r'login', 'auth.view.scripts_login'),
>>>>>>> 37111aa80d2b74813177659f17acd64aec8b4f60
)
