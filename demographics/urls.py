from django.urls import path, include

urlpatterns = [
    path('', include('demographics_monitor.urls')),
]
