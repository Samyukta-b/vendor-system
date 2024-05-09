from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from django.views.generic import RedirectView
from .views import VendorViewCreateAPI, VendorDetailsAPI, POViewCreateAPI
from .views import PODetailsAPI, PerformanceMetricsView, VendorAcknowledge, QualityRating

app_name = 'api'

urlpatterns = [
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('', RedirectView.as_view(url='/api/vendors/', permanent=True)),
    path('api/vendors/', VendorViewCreateAPI.as_view(), name='api-vendors-list'),
    path('api/vendors/<str:vendor_id>/', VendorDetailsAPI.as_view(), name='api-vendor-details'),
    path('api/purchase_orders/', POViewCreateAPI.as_view(), name='api-purchase-orders-list'),
    path('api/purchase_orders/<str:po_id>/', PODetailsAPI.as_view(), name='api-po-details'),
    path('api/vendors/<str:vendor_id>/performance/', PerformanceMetricsView.as_view()), 
    path('api/purchase_orders/<str:po_id>/acknowledge/', VendorAcknowledge.as_view()),
    path('api/purchase_orders/<str:po_id>/quality_rate/', QualityRating.as_view())
]
