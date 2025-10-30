from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

# Carga variables desde openAI.env (un nivel arriba de moviereviewsproject)
load_dotenv('../openAI.env')

# Inicializa cliente OpenAI usando la variable tal como está en la guía
client = OpenAI(api_key=os.environ.get('openai_apikey'))


class Command(BaseCommand):
    help = "Genera una imagen para la primera película usando OpenAI y la guarda en media/"

    def generate_and_download_image(self, client, movie_title, save_folder):
        prompt = f"Movie poster of {movie_title}"
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            n=1,
        )
        image_url = response.data[0].url

        # Nombre/ubicación del archivo (tal como pide el taller)
        image_filename = f"m_{movie_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        # Descarga la imagen desde la URL devuelta por la API
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        with open(image_path_full, 'wb') as f:
            f.write(image_response.content)

        # Ruta relativa que se guardará en el campo image de Movie
        return os.path.join('movie/images', image_filename)

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)
                movie.image = image_relative_path
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))
            except Exception as e:
                self.stderr.write(f"Failed to generate image for {movie.title}: {str(e)}")
            break  # 🚫 NO QUITAR: solo procesar la primera película
