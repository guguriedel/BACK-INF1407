from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404



from .models import Filme
from .serializers import FilmeSerializer

class FilmeListaView(APIView):
    """
    Endpoint para listar (GET) e criar (POST) filmes.
    Cada User só enxerga os proprios filmes
    """
    # Exige que o usuário esteja autenticado para acessar
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retorna a lista de filmes APENAS do usuário logado.
        Isso atende ao requisito de "visões diferentes por usuário"[cite: 1913, 1919].
        """
        filmes = Filme.objects.filter(usuario=request.user).order_by("-data_visto", "-id")
        serializer = FilmeSerializer(filmes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=FilmeSerializer)
    def post(self, request):
        """
        Cria um novo filme para o usuário logado.
        """
        data = request.data.copy()
        data["usuario"] = request.user.id

        serializer = FilmeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class FilmeDetalheView(APIView):
    """
    Endpoint para ver (GET), atualizar (PUT) e deletar (DELETE) um filme específico.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=FilmeSerializer)
    def get_object(self, usuario, pk):
        """
        Helper para buscar um filme (pk) que pertença ao usuário (usuario).
        """
        return get_object_or_404(Filme, pk=pk, usuario=usuario)

    def get(self, request, pk):
        """
        Retorna os detalhes de um filme, se ele pertencer ao usuário.
        """
        filme = self.get_object(request.user, pk)

        if filme is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FilmeSerializer(filme)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=FilmeSerializer)
    def put(self, request, pk):
        """
        Atualiza um filme, se ele pertencer ao usuário.
        """
        filme = self.get_object(request.user, pk)
        data = request.data.copy()
        data['usuario'] = request.user.id
        if filme is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FilmeSerializer(filme, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def delete(self, request, pk):
        """
        Deleta um filme, se ele pertencer ao usuário.
        """
        filme = self.get_object(request.user, pk)
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
        return Response({'token': token.key}, status=status.HTTP_200_OK)    