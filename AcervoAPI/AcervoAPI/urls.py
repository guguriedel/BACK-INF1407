from django.contrib import admin
from django.urls import path, include

# Importações para o Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Schema do Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Acervo de Filmes",
      default_version='v1',
      description="API para gerenciar um acervo pessoal de filmes.",
      contact=openapi.Contact(email="rodrikauer@yahoo.com.br"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filmes/', include('filmes.urls')),

    # Rotas do Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]