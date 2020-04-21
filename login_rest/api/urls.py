from django.urls import path
from .views import PersonaList,VehiculoViewSet,PersonaViewSet,UserGroupViewSet
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

"""
DRF agrega sufijos en los conjuntos de vistas para diferentes URL con
apoyo de basename: ejemplo:
	success_url = reverse_lazy('api:api_vehiculo-list')
	success_url = reverse_lazy('api:api_vehiculo-detail')
"""

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet, basename='api_vehiculo')
router.register(r'personas', PersonaViewSet, basename='api_personas')
router.register(r'grupos_usuarios', UserGroupViewSet, basename='api_grupos_usuarios')

urlpatterns = [
	path('persona_create/',PersonaList.as_view(),name='persona_list_create'),
	path('', include(router.urls)), #Using Routers https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers
]
