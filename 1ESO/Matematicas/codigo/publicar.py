"""Renderiza los temas en 1080p, deja los vídeos numerados en videos/<tema>/ y actualiza la web.

Estructura (como la web: curso → asignatura → vídeos):
    Manim/index.html                         ← la web
    Manim/1ESO/Matematicas/videos/<tema>/    ← vídeos finales (1.Escena.mp4, 2.Escena.mp4...)
    Manim/1ESO/Matematicas/codigo/           ← este script, los temas y la caché de Manim (media/)

Uso (desde 1ESO/Matematicas/codigo, con el Python del entorno de Manim):
    python publicar.py t03_enteros.py         # renderiza ese tema y actualiza la web
    python publicar.py t01_*.py t02_*.py      # varios temas
    python publicar.py --todos                # todos los t*.py
    python publicar.py --solo-web             # no renderiza, solo regenera index.html

Cada tN_*.py debe definir (a nivel de módulo):
    TEMA = "Tema N · Título"
    TITULOS = {"NombreEscena": "Título del vídeo", ...}
El orden de los vídeos es el orden de las clases Scene en el fichero.
"""
import argparse
import ast
import glob
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CALIDAD = ("-qh", "1080p60")
CLAVE_WEB = "1eso/mat"
ASIGNATURA = os.path.dirname(AQUI)                      # Manim/1ESO/Matematicas
RAIZ = os.path.dirname(os.path.dirname(ASIGNATURA))     # Manim
VIDEOS = os.path.join(ASIGNATURA, "videos")
HTML = os.path.join(RAIZ, "index.html")
MIKTEX = os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64")


def leer_tema(fichero):
    """Devuelve (TEMA, [(escena, titulo), ...]) leyendo el fichero sin ejecutarlo."""
    arbol = ast.parse(open(fichero, encoding="utf-8").read())
    tema, titulos, escenas = None, {}, []
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 and isinstance(nodo.targets[0], ast.Name):
            nombre = nodo.targets[0].id
            if nombre == "TEMA":
                tema = ast.literal_eval(nodo.value)
            elif nombre == "TITULOS":
                titulos = ast.literal_eval(nodo.value)
        elif isinstance(nodo, ast.ClassDef):
            bases = {getattr(b, "id", getattr(b, "attr", "")) for b in nodo.bases}
            if bases & {"Scene", "MovingCameraScene", "ThreeDScene", "ZoomedScene"}:
                escenas.append(nodo.name)
    if tema is None:
        sys.exit(f"{os.path.basename(fichero)}: falta TEMA = \"...\"")
    return tema, [(e, titulos.get(e, e)) for e in escenas]


def tema_id(fichero):
    return os.path.splitext(os.path.basename(fichero))[0]


def carpeta_render(fichero):
    """Donde deja Manim los vídeos recién renderizados."""
    return os.path.join(AQUI, "media", "videos", tema_id(fichero), CALIDAD[1])


def carpeta_videos(fichero):
    """Carpeta final del tema (la que usa la web)."""
    return os.path.join(VIDEOS, tema_id(fichero))


def renderizar(fichero):
    env = os.environ.copy()
    if os.path.isdir(MIKTEX):
        env["PATH"] = MIKTEX + os.pathsep + env["PATH"]
    print(f"\n>> Renderizando {os.path.basename(fichero)} en {CALIDAD[1]}...")
    r = subprocess.run([sys.executable, "-m", "manim", CALIDAD[0], os.path.basename(fichero), "-a"],
                       cwd=AQUI, env=env)
    if r.returncode:
        sys.exit(f"Error renderizando {fichero} (código {r.returncode})")


def numerar(fichero):
    """media/.../Escena.mp4 -> videos/<tema>/N.Escena.mp4 (sustituye la versión anterior)."""
    _, escenas = leer_tema(fichero)
    origen = carpeta_render(fichero)
    carpeta = carpeta_videos(fichero)
    os.makedirs(carpeta, exist_ok=True)
    for i, (escena, _) in enumerate(escenas, 1):
        nuevo = os.path.join(origen, f"{escena}.mp4")
        destino = os.path.join(carpeta, f"{i}.{escena}.mp4")
        # borra numeraciones viejas de esta escena (si cambió el orden)
        for viejo in glob.glob(os.path.join(carpeta, f"*.{escena}.mp4")):
            if os.path.abspath(viejo) != os.path.abspath(destino) and re.match(r"\d+\.", os.path.basename(viejo)):
                os.remove(viejo)
        if os.path.exists(nuevo):
            if os.path.exists(destino):
                os.remove(destino)
            shutil.move(nuevo, destino)
            print(f"   {i}.{escena}.mp4")


def generar_web():
    temas = []
    for fichero in sorted(glob.glob(os.path.join(AQUI, "t[0-9]*_*.py"))):
        tema, escenas = leer_tema(fichero)
        carpeta = carpeta_videos(fichero)
        rel = os.path.relpath(carpeta, RAIZ).replace(os.sep, "/")
        videos = []
        for i, (escena, titulo) in enumerate(escenas, 1):
            nombre = f"{i}.{escena}.mp4"
            if os.path.exists(os.path.join(carpeta, nombre)):
                videos.append((titulo, f"{rel}/{nombre}"))
            else:
                print(f"   (aviso) falta {rel}/{nombre}: no se incluye en la web")
        if videos:
            temas.append((tema, videos))

    js = lambda s: json.dumps(s, ensure_ascii=False)
    lineas = [f"  {js(CLAVE_WEB)}: ["]
    for tema, videos in temas:
        lineas.append(f"    {{ tema: {js(tema)}, videos: [")
        for titulo, src in videos:
            lineas.append(f"      {{ titulo: {js(titulo)}, src: {js(src)} }},")
        lineas.append("    ]},")
    lineas.append("  ],")

    html = open(HTML, encoding="utf-8").read()
    patron = re.compile(r"(// <<AUTO[^\n]*\n).*?[ \t]*// AUTO>>", re.S)
    if not patron.search(html):
        sys.exit("index.html: no encuentro los marcadores // <<AUTO ... // AUTO>>")
    html = patron.sub(lambda m: m.group(1) + "\n".join(lineas) + "\n  // AUTO>>", html, count=1)
    open(HTML, "w", encoding="utf-8", newline="\n").write(html)
    total = sum(len(v) for _, v in temas)
    print(f"\n>> index.html actualizado: {len(temas)} temas, {total} vídeos")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ficheros", nargs="*", help="temas a renderizar (tN_*.py)")
    ap.add_argument("--todos", action="store_true", help="renderiza todos los t*.py")
    ap.add_argument("--solo-web", action="store_true", help="no renderiza, solo actualiza index.html")
    a = ap.parse_args()

    ficheros = sorted(glob.glob(os.path.join(AQUI, "t[0-9]*_*.py"))) if a.todos else \
        [os.path.join(AQUI, f) for f in a.ficheros]
    if not a.solo_web:
        if not ficheros:
            ap.error("indica algún tema, --todos o --solo-web")
        for f in ficheros:
            renderizar(f)
            numerar(f)
    generar_web()


if __name__ == "__main__":
    main()
