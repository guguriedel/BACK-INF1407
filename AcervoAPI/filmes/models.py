from django.db import models
from django.contrib.auth.models import User

class Filme(models.Model):
    # Chave estrangeira para associar o filme ao usuário que o cadastrou
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # O nome do filme
    nome = models.CharField(max_length=200)

    # A data em que o filme foi visto
    data_visto = models.DateField()

    # A nota (ex: 8.5)
    nota = models.DecimalField(max_digits=3, decimal_places=1)

    # Duração em minutos
    duracao_min = models.IntegerField()

    def __str__(self):
        return self.nome