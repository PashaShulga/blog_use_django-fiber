"""untitled3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views.static import serve
from django.views.i18n import javascript_catalog
from django.conf.urls import include, url
from blog_rest.admin import admin
from blog_rest.views import ViewBlog, ViewBlogItem
from fiber.views import page
from django.conf.urls.static import static


urlpatterns = [
    url(r'^api/v2/', include('fiber.rest_api.urls')),
    url(r'^admin/fiber/', include('fiber.admin_urls')),
    url(r'^jsi18n/$', javascript_catalog, {'packages': ('fiber',),}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    url(r'^blog/$', ViewBlog.as_view(), name='blog'),
    url(r'^blog/(?P<page_slug>[\w-]+)', ViewBlogItem.as_view(), name='blog_detail'),
    url(r'^', page)
]