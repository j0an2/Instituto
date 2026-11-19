"""Genera N variantes (semillas distintas) de cada postura de la mascota Xola.

Uso (desde 1ESO/Matematicas/codigo, con ComfyUI abierto en http://127.0.0.1:8000):
    ~\\venvs\\manim\\Scripts\\python.exe -I img/generar_variantes_xola.py [N]

Salida: assets/mascota/variantes/<postura>_s<semilla>.png (+ _raw.png). Las semillas de cada postura
son <base> .. <base>+N-1, para poder repetir cualquier imagen con generar_imagen.py.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../codigo
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10

XOLA = ("A cute pink axolotl girl with fluffy coral feathery gills on her head, cream belly, rosy cheeks, "
        "big shiny black eyes, a pink tail, wearing a small mint green backpack and blue and white sneakers")
MASCOTA = ("Mascot character design for a school math video series for 12-year-olds, full body, front view, "
           "kawaii style but not babyish, simple geometric shapes, soft pastel colors, thick clean outlines, "
           "flat vector illustration, isolated on a plain white background, no text, no letters, no numbers.")

POSTURAS = {  # nombre: (semilla base, postura)
    "saluda": (100, "smiling and waving hello with one hand raised, friendly welcoming pose"),
    "sorpresa": (200, "shocked and surprised, eyes wide open, mouth open in a round O shape, eyebrows raised, "
                      "both hands on her cheeks, no smile, a small exclamation sweat drop"),
    "pensando": (300, "thinking with one hand on her chin, eyes looking up, curious expression, "
                      "a small question mark bubble above her head"),
    "burbuja": (400, "happily blowing a big shiny soap bubble from her mouth, small bubbles floating around her"),
    "idea": (500, "having a bright idea, her feathery gills glowing with warm yellow light, one finger pointing up, "
                  "excited smile"),
    "celebra": (600, "celebrating with both arms raised in the air and jumping with joy, eyes closed happily, "
                     "big smile, small sparkles around her"),
}

os.makedirs(os.path.join(AQUI, "..", "..", "..", "assets", "mascota", "variantes"), exist_ok=True)
for nombre, (base, postura) in POSTURAS.items():
    prompt = f"{XOLA}, {postura}. {MASCOTA}"
    for s in range(base, base + N):
        salida = f"../../../assets/mascota/variantes/{nombre}_s{s}.png"
        if os.path.exists(os.path.join(AQUI, salida)):
            continue
        r = subprocess.run([sys.executable, "-I", "generar_imagen.py", prompt, salida, str(s), "1024", "1024"],
                           cwd=AQUI, capture_output=True, text=True)
        print(nombre, s, (r.stdout or r.stderr).strip()[-80:], flush=True)
