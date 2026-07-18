from .views import (
                    InvoiceViewSet,
                    CustomerViewSet,
                    dashboard_cards,
                    latest_invoices,
                    revenues_list,
                    )
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()
router.register("invoices", InvoiceViewSet)
router.register("customers", CustomerViewSet)
urlpatterns = [
    path("",include(router.urls)),
    path("dashboard/cards/", dashboard_cards),
    path("dashboard/latest-invoices/", latest_invoices),
    path("dashboard/revenue/", revenues_list),
            ]

