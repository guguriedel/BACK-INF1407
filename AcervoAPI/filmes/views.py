from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User 
from django.core.mail import send_mail
from django.conf import settings
import secrets

# Importa os models e serializers
from .models import Filme
# Agora o UserSerializer existe e pode ser importado
from .serializers import FilmeSerializer, UserSerializer, PasswordResetSerializer 

# -----------------------------------------------------------------
# VIEW DE REGISTRO DE NOVO USUÁRIO (ESTAVA EM FALTA)
# -----------------------------------------------------------------
class RegisterView(APIView):
    """
    Endpoint para registrar um novo usuário.
    """
    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        operation_summary='Registra um novo usuário',
        request_body=UserSerializer,
        responses={
            201: openapi.Response('Usuário criado com sucesso.', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )),
            400: 'Erro de validação.'
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data, 
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------
# VIEW DE LOGIN
# -----------------------------------------------------------------
class LoginView(ObtainAuthToken):
    """
    Endpoint de Login.
    """
    @swagger_auto_schema(
        operation_summary='Realiza login (obtém token)',
        request_body=openapi.Schema(
             type=openapi.TYPE_OBJECT,
             properties={
                 'username': openapi.Schema(type=openapi.TYPE_STRING),
                 'password': openapi.Schema(type=openapi.TYPE_STRING),
             },
             required=['username', 'password']
         ),
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'token': openapi.Schema(type=openapi.TYPE_STRING)})}
    )
    def post(self, request, *args, **kwargs):
        """
        Envia 'username' e 'password' via POST.
        Retorna um 'token' se for bem-sucedido.
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

# -----------------------------------------------------------------
# VIEW DE TROCA DE SENHA (ESTAVA EM FALTA)
# -----------------------------------------------------------------
class ChangePasswordView(APIView):
    """
    Endpoint para o usuário logado trocar sua própria senha.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Troca a senha do usuário (logado)',
        security=[{'Token': []}], 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha antiga'),
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING, description='Nova senha'),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmação da nova senha'),
            },
            required=['old_password', 'new_password1', 'new_password2']
        ),
        responses={
            200: openapi.Response('Senha alterada com sucesso.', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'token': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            400: 'Senhas não conferem ou senha antiga incorreta.',
            401: 'Usuário não autenticado.',
        }
    )
    def post(self, request): 
        user = request.user
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        if not all([old_password, new_password1, new_password2]):
            return Response({'error': 'Todos os campos são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(old_password):
            return Response({'error': 'A senha antiga está incorreta.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password1 != new_password2:
            return Response({'error': 'As novas senhas não conferem.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password1)
        user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        token.delete() 
        token = Token.objects.create(user=user)
        
        return Response({'token': token.key, 'message': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)

# -----------------------------------------------------------------
# VIEW DE RECUPERAÇÃO DE SENHA
# -----------------------------------------------------------------
class PasswordResetView(APIView):
    """
    Endpoint para recuperação de senha.
    O usuário envia seu email e recebe uma senha temporária.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Solicita reset de senha',
        request_body=PasswordResetSerializer,
        responses={
            200: openapi.Response('Email com senha temporária enviado.', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            400: 'Email não encontrado ou erro na validação.',
        }
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Gera uma senha temporária
            temp_password = secrets.token_urlsafe(12)
            user.set_password(temp_password)
            user.save()
            
            # Envia email com a senha temporária
            subject = 'Sua Senha Temporária - Acervo de Filmes'
            message = f"""
Olá {user.first_name or user.username},

Você solicitou uma recuperação de senha para sua conta.

Sua senha temporária é: {temp_password}

Por favor, faça login com essa senha e altere para uma senha de sua preferência.

Obrigado!
            """
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response(
                    {'message': 'Email com a senha temporária foi enviado com sucesso.'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': f'Erro ao enviar email: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------
# VIEWS DE FILMES (Corrigido para o Swagger)
# -----------------------------------------------------------------
class FilmeListaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Lista todos os filmes do usuário logado',
        security=[{'Token': []}],
        responses={200: FilmeSerializer(many=True)} 
    )
    def get(self, request):
        filmes = Filme.objects.filter(usuario=request.user).order_by("-data_visto", "-id")
        serializer = FilmeSerializer(filmes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Cria um novo filme para o usuário logado',
        security=[{'Token': []}],
        request_body=FilmeSerializer
    )
    def post(self, request):
        data = request.data.copy()
        data["usuario"] = request.user.id 
        serializer = FilmeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(usuario=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FilmeDetalheView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, usuario, pk):
        return get_object_or_404(Filme, pk=pk, usuario=usuario)

    @swagger_auto_schema(
        operation_summary='Vê os detalhes de um filme específico',
        security=[{'Token': []}],
        responses={200: FilmeSerializer}
    )
    def get(self, request, pk):
        filme = self.get_object(request.user, pk)
        serializer = FilmeSerializer(filme)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Atualiza um filme específico',
        security=[{'Token': []}],
        request_body=FilmeSerializer
    )
    def put(self, request, pk):
        filme = self.get_object(request.user, pk)
        data = request.data.copy()
        data['usuario'] = request.user.id 
        serializer = FilmeSerializer(filme, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary='Deleta um filme específico',
        security=[{'Token': []}]
    )
    def delete(self, request, pk):
        filme = self.get_object(request.user, pk)
        filme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)