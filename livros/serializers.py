from rest_framework import serializers
from livros.models import Livro

class LivroSerializer(serializers.ModelSerializer):
  class Meta:
    model = Livro
    fields = ('id', 'titulo', 'descricao', 'disponivel')