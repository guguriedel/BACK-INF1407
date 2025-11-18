from rest_framework import serializers
from .models import Filme
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import secrets

class FilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = ["id", "usuario", "nome", "data_visto", "nota", "duracao_min"]
        # Garante que o usuário não possa ser definido diretamente no POST/PUT
        extra_kwargs = {
            'usuario': {'read_only': True}
        }

# -----------------------------------------------------------------
# CLASSE NECESSÁRIA PARA O REGISTERVIEW (ESTAVA EM FALTA NO SEU FICHEIRO ORIGINAL)
# -----------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o registro de novos usuários.
    """
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'email': {'required': True},
        }

    def validate(self, data):
        """
        Valida se as duas senhas são iguais.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "As senhas não conferem."})
        return data

    def create(self, validated_data):
        """
        Cria o novo usuário no banco de dados.
        """
        validated_data.pop('password_confirm') 
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# -----------------------------------------------------------------
# SERIALIZER PARA RECUPERAÇÃO DE SENHA
# -----------------------------------------------------------------
class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer para solicitar reset de senha.
    O usuário envia apenas o email.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Valida se o email existe no banco de dados.
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Esse email não está cadastrado.")
        return value