import os
import unicodedata
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update images for movies from local folder"

    def handle(self, *args, **kwargs):
        images_folder = "media/movie/images/images/"
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        updated_count = 0

        for movie in movies:
            image_filename_base = self.normalize_filename(movie.title)
            image_path = self.find_image_file(images_folder, "m_" + image_filename_base)

            if image_path:
                # Guardar ruta relativa (desde "media")
                movie.image = os.path.relpath(image_path, "media")
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Updated image for: {movie.title}"))
            else:
                self.stderr.write(
                    f"❌ Image not found for: {movie.title} "
                    f"(expected m_{image_filename_base}.png/.jpg/.jpeg)"
                )

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies."))

    def normalize_filename(self, name):
        """
        Normaliza el nombre de la película para usarlo en el archivo:
        - Quita acentos
        - Reemplaza espacios y símbolos por "_"
        - Elimina caracteres no alfanuméricos
        """
        nfkd = unicodedata.normalize("NFKD", name)
        only_ascii = nfkd.encode("ASCII", "ignore").decode("utf-8")
        clean = "".join(c if c.isalnum() else "_" for c in only_ascii)
        return "_".join(filter(None, clean.split("_")))

    def find_image_file(self, images_folder, base_name):
        """
        Busca la imagen con varias extensiones válidas (.png, .jpg, .jpeg).
        """
        for ext in [".png", ".jpg", ".jpeg"]:
            candidate = os.path.join(images_folder, base_name + ext)
            if os.path.exists(candidate):
                return candidate
        return None
