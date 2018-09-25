from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from status import views

router = DefaultRouter()

router.register('service', views.ServiceViewSet)
router.register('serviceEvent', views.ServiceEventViewSet)
router.register('file', views.FileViewSet)
router.register('fileEvent', views.FileEventViewSet)
urlpatterns = [
    url('', include(router.urls))
]
