from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from livros.models import Livro
from livros.serializers import LivroSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def livros_listar(request):
  if request.method == 'GET':
    titulo = request.GET.get('titulo', None)
    livros = Livro.objects.filter(titulo__icontains=titulo) if titulo else Livro.objects.all()
    
    livros_serializer = LivroSerializer(livros, many=True)
    return JsonResponse(livros_serializer.data, safe=False)
  
  elif request.method == 'POST':
    livro_data = JSONParser().parse(request)
    livros_serializer = LivroSerializer(data=livro_data)
    if livros_serializer.is_valid():
      livros_serializer.save()
      return JsonResponse(livros_serializer.data, status= status.HTTP_201_CREATED)
    
    return JsonResponse(livros_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    count = Livro.objects.all().delete()
    return JsonResponse({'message': '{} livros foram apagados com sucesso!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def livro_detalhe(request, pk):
  try:
    livro = Livro.objects.get(pk=pk)
    
  except Livro.DoesNotExist:
    return JsonResponse({'message': 'Esse livro não existe'}, status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    livro_serializer = LivroSerializer(livro)
    return JsonResponse(livro_serializer.data)
  
  elif request.method == 'PUT':
    livro_data = JSONParser().parse(request)
    livro_serializer = LivroSerializer(livro, data=livro_data)
    if livro_serializer.is_valid():
      livro_serializer.save()
      return JsonResponse(livro_serializer.data)
    return JsonResponse(livro_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    livro.delete()
    return JsonResponse({'message': 'O livro foi apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def livro_lista_disponiveis(request):
  livros = Livro.objects.filter(disponivel=True)
  
  if request.method == 'GET':
    livros_serializer = LivroSerializer(livros, many=True)
    return JsonResponse(livros_serializer.data,safe=False)