"""Hoja de contactos de un vídeo: extrae N fotogramas repartidos y los pega en una cuadrícula PNG.

Sirve para que una IA (que no puede ver vídeos, pero sí imágenes) revise una animación.

Uso (desde Mates/1ESO):
    python revisar.py media/videos/t03_enteros/480p15/RectaEnteros.mp4 revision.png 12
"""
import sys

import av
from PIL import Image

if len(sys.argv) < 3:
    sys.exit(__doc__)
video, salida = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 12

contenedor = av.open(video)
fotos = [f.to_image() for f in contenedor.decode(contenedor.streams.video[0])]
indices = [int(i * (len(fotos) - 1) / (n - 1)) for i in range(n)]
ancho, alto = fotos[0].size
cols = 4
filas = -(-n // cols)
hoja = Image.new("RGB", (ancho * cols, alto * filas))
for k, i in enumerate(indices):
    hoja.paste(fotos[i], ((k % cols) * ancho, (k // cols) * alto))
hoja.save(salida)
print(f"{salida}: {n} fotogramas de {len(fotos)}")
