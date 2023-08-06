# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import spirit.urls

# Override admin login for security purposes
from django.contrib.auth.decorators import login_required
admin.site.login = login_required(admin.site.login)
import debug_toolbar

urlpatterns = [
    re_path(r'^', include(spirit.urls)),
    re_path('__debug__/', include(debug_toolbar.urls)),

    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
