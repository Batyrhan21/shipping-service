from django.urls import path
from service import views

urlpatterns = [
    path(
        "shipment/",
        views.ShipmentAPIView.as_view(),
        name="shipment-list",
    ),
    path(
        "shipment/<uuid:id>/",
        views.ShipmentRetrieveAPIView.as_view(),
        name="shipment-get",
    ),
]

