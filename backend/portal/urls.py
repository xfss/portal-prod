"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from portal import views

router = DefaultRouter()

router.register('publisher', views.PublisherViewSet)
router.register('publication', views.PublicationViewSet)
router.register('publication_config_rule', views.PublicationConfigRuleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_auth.urls')),
    path('api/docs/', include_docs_urls(title='API Docs')),
    path('api/status/', include('status.urls')),
    path('api/crm/', include('crm.urls')),
    path('api/webhook/', include('webhook.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(packages=('recurrence',))),
    path('api/language/', views.CurrentLanguageView.as_view()),
    path('api/languages/', views.languages),
    path('api/timezones/', views.timezones),
    url('api/', include(router.urls))
]
