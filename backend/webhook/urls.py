from django.conf.urls import url, include
from webhook import views


urlpatterns = [
    url('fileEvent', views.WebhookFileEventView.as_view())
]