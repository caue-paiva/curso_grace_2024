from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

class PaginaInicial(TemplateView):
   template_name = "index.html"
class BotaoView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse('use o livro 10')

import random

def recomendar_livro():
    livros = [
        {"titulo": "Telefone Preto", "descricao": "A luta de um garoto sequestrado contra um serial killer em um suspense de tirar o fôlego."},
        {"titulo": "O Castelo Animado", "descricao": "A mágica jornada de Sophie para quebrar uma maldição e descobrir o amor no castelo do mago Howl."},
        {"titulo": "Blue Period", "descricao": "Yatora descobre sua paixão pela arte e embarca em um intenso desafio rumo à faculdade de artes."},
        {"titulo": "A Mecânica do Amor", "descricao": "Uma mulher independente encontra um novo significado para o amor com um misterioso mecânico."},
        {"titulo": "Imperfeitos", "descricao": "Celestine desafia um sistema que exige perfeição, tornando-se símbolo de resistência."},
        {"titulo": "Melhor do que nos Filmes", "descricao": "Liz descobre que o amor verdadeiro pode ser inesperado, superando até mesmo os clichês dos livros."},
    ]

    livro_recomendado = random.choice(livros)
    return f"Recomendamos o livro: {livro_recomendado['titulo']} - {livro_recomendado['descricao']}"