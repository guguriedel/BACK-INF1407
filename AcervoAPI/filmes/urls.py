from django.urls import path
from .views import (
    FilmeListaView, 
    FilmeDetalheView, 
    LoginView, 
    RegisterView,  # <-- Importar
    ChangePasswordView # <-- Importar
)

app_name = 'filmes' 

urlpatterns = [
    # Rotas de Filmes (CRUD)
    path('', FilmeListaView.as_view(), name='filme-lista'),
    path('<int:pk>/', FilmeDetalheView.as_view(), name='filme-detalhe'),
    
    # Rotas de Autenticação
    path('register/', RegisterView.as_view(), name='register'), # <-- Adicionar
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), # <-- Adicionar
]