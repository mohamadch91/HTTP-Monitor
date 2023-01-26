from django.urls import path
from .views import *


urlpatterns = [
    path('create/', EndpointCreateView.as_view(), name='endpoint create'),
    path('user_endpoints/', UserEndpointView.as_view(), name='user endpoints'),
    path('endpoint_stats/<int:pk>/', EndpointStatsView.as_view(), name='endpoint stats'),
    path('warnings/<int:pk>/', EndpointWarningView.as_view(), name='warnings'),
    
    
    



]