from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import os
from dotenv import load_dotenv

# ✅ Carga las variables de entorno desde el archivo openAI.env
# Ojo: el archivo debe estar un nivel arriba de moviereviewsproject
load_dotenv('../openAI.env')

# ✅ Inicializa el cliente de OpenAI con la API Key
client = OpenAI(api_key=os.environ.get('openai_apikey'))

# ✅ Función auxiliar para obtener respuesta de la API
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0  # Controla la creatividad (0 = más preciso)
    )
    return response.choices[0].message.content.strip()


class Command(BaseCommand):
    help = "Update movie descriptions using OpenAI API"

    def handle(self, *args, **kwargs):
        instruction = "Mejora y enriquece la siguiente descripción de película:"
        movies = Movie.objects.all()

        for movie in movies:
            prompt = f"{instruction} Actualiza la descripción '{movie.description}' de la película '{movie.title}'"
            response = get_completion(prompt)
            movie.description = response
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))
            break  # 🚫 No quitar el break (solo actualiza la primera película)
