from django.contrib import admin
from django.urls import path
from predicciones import views
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API de Predicción de Imágenes (Dígitos)",
        default_version='2.0',
        description="Esta API proporciona un único punto de acceso para hacer predicciones basadas en una imagen de entrada y un modelo de aprendizaje automático especificado. La API acepta una solicitud POST con un formulario que contiene un archivo de imagen y el nombre del modelo, y devuelve el resultado de la predicción.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('predict/', views.predict, name='predict'),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
