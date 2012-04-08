from django.conf.urls.defaults import patterns, include, url

from tastypie.api import Api
from geddit.api.resources import UserResource, ItemResource, ClaimResource, CategoryResource, FilterResource
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

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


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^jstest/', 'jstest.views.index'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', 'data.views.buy_page'),

    url(r'^buy$', 'data.views.buy_page'),    
    url(r'^sell$', 'data.views.sell_page'),
    url(r'^cart$', 'data.views.cart_page'),

    url(r'^create_listing$', 'data.views.create_listing'),
    url(r'^claim$', 'data.views.claim_listing'),
    url(r'^unclaim$', 'data.views.unclaim_listing'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    #url(r'login', 'auth.view.scripts_login'),
)
