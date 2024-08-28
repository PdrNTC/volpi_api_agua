from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    peso = models.FloatField(help_text="Informe seu peso em KG")

