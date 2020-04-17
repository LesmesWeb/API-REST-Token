from django.urls import path
from.views import PersonaList,VehiculoViewSet,PersonaViewSet

urlpatterns = [
    path('persona_create/',PersonaList.as_view(),name='persona_list_create'),
    #path('vehiculo/',VehiculoViewSet.as_view(),name='vehiculo_list'),
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet, basename='api_vehiculo')
router.register(r'personas', PersonaViewSet, basename='api_personas')
urlpatterns += router.urls
