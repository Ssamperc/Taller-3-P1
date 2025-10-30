import os

# Ruta correcta de las imágenes
carpeta = r"C:\Users\samko\Downloads\P1-Taller1-main\moviereviewsproject\media\movie\images\images"

for archivo in os.listdir(carpeta):
    ruta_vieja = os.path.join(carpeta, archivo)

    if os.path.isfile(ruta_vieja):
        nombre, ext = os.path.splitext(archivo)

        # Solo procesar imágenes
        if ext.lower() in [".jpg", ".jpeg", ".png"]:
            # Reemplazar espacios por "_"
            nombre_nuevo = nombre.replace(" ", "_")
            ruta_nueva = os.path.join(carpeta, nombre_nuevo + ext)

            if ruta_vieja != ruta_nueva:
                os.rename(ruta_vieja, ruta_nueva)
                print(f"✅ Renombrado: {archivo} → {nombre_nuevo+ext}")
