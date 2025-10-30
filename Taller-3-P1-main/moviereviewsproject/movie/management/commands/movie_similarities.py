import os
import numpy as np
from django.core.management.base import BaseCommand
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie

class Command(BaseCommand):
    help = "Calcular similitud de coseno entre películas y/o un prompt usando embeddings de OpenAI"

    def handle(self, *args, **kwargs):
        # 🔹 Cargar API key
        load_dotenv("openAI.env")
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # 🔹 Seleccionar películas (puedes cambiarlas después)
        movie1 = Movie.objects.get(title="Pauvre Pierrot")
        movie2 = Movie.objects.get(title="Carmencita")

        # 🔹 Funciones internas
        def get_embedding(text):
            if not text:
                raise ValueError("The input text is empty or None")
            response = client.embeddings.create(
                 model="text-embedding-3-small",
                 input=text
    )
            return np.array(response.data[0].embedding, dtype=np.float32)


        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # 🔹 Embeddings de películas
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"🎬 {movie1.title} vs {movie2.title}: {similarity:.4f}")

        # 🔹 Comparación con un prompt
        prompt = "película sobre la Segunda Guerra Mundial"  # cámbialo a gusto
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
