"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/(?P<version>v1)/', include('drf_auth.api_urls')),
    url(r'^auth/', include('drf_auth.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
