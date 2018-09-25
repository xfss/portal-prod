from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from crm import views

router = DefaultRouter()

router.register('invoice', views.InvoiceViewSet)
router.register('contract/adfusion', views.AdfusionContractViewSet)
router.register('contract/newsfusion', views.NewsfusionContractViewSet)

urlpatterns = [
    url('', include(router.urls)),
    path('publisher/<int:publisher_id>/invoice/', views.generate_invoice_for_publisher),
    path('generate_invoices/', views.generate_invoices),
    path('generate_invoices/<str:product>/', views.generate_invoices),
    path('contract/<int:contract_id>/invoice/', views.generate_invoice_for_contract),
]
