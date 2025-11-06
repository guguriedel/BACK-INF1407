from rest_framework import serializers
from .models import Filme

class FilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme       # 1. Diz ao serializer qual modelo "traduzir".
        fields = ["id", "usuario", "nome", "data_visto", "nota", "duracao_min"]  # 2. Diz a ele para usar todos os campos do modelo.