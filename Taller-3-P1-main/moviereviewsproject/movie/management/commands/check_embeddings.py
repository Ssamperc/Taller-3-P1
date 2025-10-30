from django.core.management.base import BaseCommand
from movie.models import Movie
import numpy as np

class Command(BaseCommand):
    help = "Muestra embeddings guardados en la base de datos"

    def handle(self, *args, **kwargs):
        for movie in Movie.objects.all():
            try:
                emb_array = np.frombuffer(movie.emb, dtype=np.float32)
                self.stdout.write(f"{movie.title}: {emb_array[:5]} ...")
            except Exception as e:
                self.stdout.write(f"⚠️ Error en {movie.title}: {e}")
