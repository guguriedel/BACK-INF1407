from django.urls import path
from .views import FilmeListaView, FilmeDetalheView, LoginView

app_name = 'filmes' # Define um namespace para as URLs

urlpatterns = [
    # Rota para /filmes/ (Listar e Criar)
    path('', FilmeListaView.as_view(), name='filme-lista'),

    # Rota para /filmes/<id>/ (Ver, Atualizar, Deletar)
    path('<int:pk>/', FilmeDetalheView.as_view(), name='filme-detalhe'),
    path('login/', LoginView.as_view(), name='login'),
]