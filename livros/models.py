from django.db import models

# Create your models here.
class Livro(models.Model):
  titulo = models.CharField(max_length= 70, blank=False, default='')
  descricao = models.CharField(max_length=200, blank=False, default='')
  disponivel = models.BooleanField(default=False)