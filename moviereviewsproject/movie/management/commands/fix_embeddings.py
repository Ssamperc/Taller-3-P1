from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Regenera embeddings corruptos para todas las películas"

    def handle(self, *args, **kwargs):
        load_dotenv("openAI.env")
        client = OpenAI(api_key=os.environ.get("openai_apikey"))

        movies = Movie.objects.all()
        self.stdout.write(f"Checking {movies.count()} movies...")

        for movie in movies:
            try:
                # verificar si el emb es válido
                if not movie.emb or len(movie.emb) % 4 != 0:
                    raise ValueError("Invalid embedding")

                arr = np.frombuffer(movie.emb, dtype=np.float32)
                if arr.shape[0] != 1536:
                    raise ValueError("Wrong embedding size")

            except Exception:
                # regenerar el embedding
                self.stdout.write(f"🔄 Fixing embedding for: {movie.title}")
                if movie.description:
                    response = client.embeddings.create(
                        input=[movie.description],
                        model="text-embedding-3-small"
                    )
                    emb = np.array(response.data[0].embedding, dtype=np.float32).tobytes()
                    movie.emb = emb
                    movie.save()
                else:
                    self.stdout.write(f"⚠️ Skipping {movie.title} (no description)")

        self.stdout.write("✅ All embeddings fixed")
