from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Genera y guarda embeddings para todas las películas en la base de datos"

    def handle(self, *args, **kwargs):
        # 🔑 Cargar API key desde .env
        load_dotenv("openAI.env")
        client = OpenAI(api_key=os.environ.get("openai_apikey"))

        # 🔎 Obtener todas las películas
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            if not movie.description:
                self.stdout.write(f"⚠️ No description for: {movie.title}")
                continue

            # 🎯 Generar embedding de la descripción
            response = client.embeddings.create(
                input=[movie.description],
                model="text-embedding-3-small"
            )
            embedding = np.array(response.data[0].embedding, dtype=np.float32)

            # 💾 Guardar embedding como binario en el campo `emb`
            movie.emb = embedding.tobytes()
            movie.save()

            self.stdout.write(f"👌 Embedding stored for: {movie.title}")

        self.stdout.write("🌟 Finished generating embeddings for all movies")
