from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

from .models import Movie
from .forms import PromptForm

# ================== VISTAS BÁSICAS ==================
def mi_vista(request):
    return HttpResponse("Hola Samuel, tu vista funciona 🎉")

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html', {'name': 'Samuel Samper'})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

# ================== VISTA DE ESTADÍSTICAS ==================
def statistics_view(request):
    matplotlib.use('Agg')
    
    # ============ GRÁFICA POR AÑOS ============
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(12, 6))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer_years = io.BytesIO()
    plt.savefig(buffer_years, format='png')
    buffer_years.seek(0)
    plt.close()
    graphic_years = base64.b64encode(buffer_years.getvalue()).decode('utf-8')
    buffer_years.close()

    # ============ GRÁFICA POR GÉNEROS ============
    movies = Movie.objects.exclude(genre__isnull=True).exclude(genre='')
    movie_counts_by_genre = {}
    for movie in movies:
        first_genre = movie.genre.split(',')[0].strip()
        movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1
    
    sorted_genres = dict(sorted(movie_counts_by_genre.items(), key=lambda x: x[1], reverse=True))
    bar_positions_genre = range(len(sorted_genres))

    plt.figure(figsize=(12, 6))
    plt.bar(bar_positions_genre, sorted_genres.values(), width=0.6, align='center')
    plt.title('Movies per Genre (First Genre Only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, sorted_genres.keys(), rotation=45, ha='right')
    plt.tight_layout()

    buffer_genres = io.BytesIO()
    plt.savefig(buffer_genres, format='png')
    buffer_genres.seek(0)
    plt.close()
    graphic_genres = base64.b64encode(buffer_genres.getvalue()).decode('utf-8')
    buffer_genres.close()

    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })

# ================== SISTEMA DE RECOMENDACIÓN ==================
# Cargar API Key
load_dotenv("openAI.env")
client = OpenAI(api_key=os.environ.get("openai_apikey"))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend_movie(request):
    best_movie = None
    similarity_score = None

    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]

            # Generar embedding del prompt
            response = client.embeddings.create(
                input=[prompt],
                model="text-embedding-3-small"
            )
            prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

            # Comparar con cada película
            max_similarity = -1
            for movie in Movie.objects.all():
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                similarity = cosine_similarity(prompt_emb, movie_emb)

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_movie = movie
                    similarity_score = similarity
    else:
        form = PromptForm()

    return render(request, "movie/recommend.html", {
        "form": form,
        "best_movie": best_movie,
        "similarity": similarity_score
    })
