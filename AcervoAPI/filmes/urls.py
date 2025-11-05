from django.urls import path
from . import views

app_name = 'filmes' # Define um namespace para as URLs

urlpatterns = [
    # Rota para /filmes/ (Listar e Criar)
    path('', views.FilmeListaView.as_view(), name='filme-lista'),

    # Rota para /filmes/<id>/ (Ver, Atualizar, Deletar)
    path('<int:pk>/', views.FilmeDetalheView.as_view(), name='filme-detalhe'),
]