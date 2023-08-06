from django.urls import path

from . import views

urlpatterns = [
    path('swagger_ui.html', views.swagger_ui, name="swagger_ui"),
    path('openapi_spec.yaml', views.openapi_spec_yaml, name='openapi_spec_yaml'),
]