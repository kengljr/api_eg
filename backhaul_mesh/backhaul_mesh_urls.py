from django.urls import include, path
from rest_framework import urls
from . import backhaul_mesh_views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('',backhaul_mesh_views.snippet_detail),
    path('GETMediaTypebackhaulmesh',backhaul_mesh_views.get_mediatype_backhaul_mesh),
    path('GETSignalStrengthbackhaulmesh',backhaul_mesh_views.get_signal_strength_backhaul_mesh),
    path('GETPHYRatebackhaulmesh',backhaul_mesh_views.get_phy_rate_backhaul_mesh),
    path('GETSerialNumberbackhaulmesh',backhaul_mesh_views.get_serial_number_backhaul_mesh),
    path(f"GETLog/<int:time>",backhaul_mesh_views.get_log),


]

