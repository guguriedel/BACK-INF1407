from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated # Para proteger o endpoint
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Filme
from .serializers import FilmeSerializer

class FilmeListaView(APIView):
    """
    Endpoint para listar (GET) e criar (POST) filmes.
    """
    # Exige que o usuário esteja autenticado para acessar 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retorna a lista de filmes APENAS do usuário logado.
        Isso atende ao requisito de "visões diferentes por usuário"[cite: 1913, 1919].
        """
        filmes = Filme.objects.filter(usuario=request.user)
        serializer = FilmeSerializer(filmes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Cria um novo filme para o usuário logado.
        """
        serializer = FilmeSerializer(data=request.data)
        if serializer.is_valid():
            # Salva o filme associando ao usuário logado (request.user)
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilmeDetalheView(APIView):
    """
    Endpoint para ver (GET), atualizar (PUT) e deletar (DELETE) um filme específico.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, usuario):
        """
        Helper para buscar um filme (pk) que pertença ao usuário (usuario).
        """
        try:
            return Filme.objects.get(pk=pk, usuario=usuario)
        except Filme.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retorna os detalhes de um filme, se ele pertencer ao usuário.
        """
        filme = self.get_object(pk, request.user)
        if filme is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FilmeSerializer(filme)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Atualiza um filme, se ele pertencer ao usuário.
        """
        filme = self.get_object(pk, request.user)
        if filme is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FilmeSerializer(filme, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deleta um filme, se ele pertencer ao usuário.
        """
        filme = self.get_object(pk, request.user)
        if filme is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        filme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LoginView(ObtainAuthToken):
    """
    Endpoint de Login.
    Envia 'username' e 'password' via POST.
    Retorna um 'token' se for bem-sucedido.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})    