from django.db import models
import pickle  # para convertir listas a binario

# 👇 Esta función devuelve una lista vacía serializada en binario
def get_default_array():
    default_arr = np.random.rand(1536).astype(np.float32)  # 👈 aquí la clave
    return default_arr.tobytes()


# Modelo Movie
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images/')
    url = models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)
    emb = models.BinaryField(default=get_default_array)  # ahora sí funciona
    
    def __str__(self):
        return self.title
