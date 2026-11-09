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
Otros cursos tienen su propio publicar.py (2ESO/Matematicas/codigo) que llama a este con --codigo.

Cada tN_*.py debe definir (a nivel de módulo):
    TEMA = "Tema N · Título"
    TITULOS = {"NombreEscena": "Título del vídeo", ...}
y puede definir vídeos extra, que llevan su etiqueta y no cuentan en la numeración:
    EXTRAS = {"NombreEscena": "E1", ...}      ->  videos/<tema>/E1.NombreEscena.mp4
y páginas interactivas (HTML) que se intercalan en la lista detrás de una escena:
    INTERACTIVOS = [("E1", "Título", "interactivos/pagina.html", "EscenaAnterior"), ...]
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

CALIDAD = ("-qh", "1080p60")
ABREV = {"Matematicas": "mat", "Fisica y Quimica": "fq", "Biologia y Geologia": "bg", "Geografia e Historia": "gh"}


def configurar(codigo):
    """Rutas a partir de la carpeta de código (<curso>/<asignatura>/codigo)."""
    global AQUI, ASIGNATURA, RAIZ, VIDEOS, HTML, CLAVE_WEB
    AQUI = os.path.abspath(codigo)
    ASIGNATURA = os.path.dirname(AQUI)                      # Manim/1ESO/Matematicas
    RAIZ = os.path.dirname(os.path.dirname(ASIGNATURA))     # Manim
    VIDEOS = os.path.join(ASIGNATURA, "videos")
    HTML = os.path.join(RAIZ, "index.html")
    curso = os.path.basename(os.path.dirname(ASIGNATURA))
    CLAVE_WEB = f"{curso.lower()}/{ABREV[os.path.basename(ASIGNATURA)]}"   # p. ej. "2eso/mat"


configurar(os.path.dirname(os.path.abspath(__file__)))
MIKTEX = os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64")


def leer_tema(fichero):
    """Devuelve (TEMA, [(escena, titulo, etiqueta), ...]) leyendo el fichero sin ejecutarlo.
    etiqueta: "1", "2"... para los vídeos normales y la de EXTRAS (p. ej. "E1") para los extra."""
    arbol = ast.parse(open(fichero, encoding="utf-8").read())
    tema, titulos, extras, escenas = None, {}, {}, []
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 and isinstance(nodo.targets[0], ast.Name):
            nombre = nodo.targets[0].id
            if nombre == "TEMA":
                tema = ast.literal_eval(nodo.value)
            elif nombre == "TITULOS":
                titulos = ast.literal_eval(nodo.value)
            elif nombre == "EXTRAS":
                extras = ast.literal_eval(nodo.value)
        elif isinstance(nodo, ast.ClassDef):
            bases = {getattr(b, "id", getattr(b, "attr", "")) for b in nodo.bases}
            if bases & {"Scene", "MovingCameraScene", "ThreeDScene", "ZoomedScene"}:
                escenas.append(nodo.name)
    if tema is None:
        sys.exit(f"{os.path.basename(fichero)}: falta TEMA = \"...\"")
    salida, n = [], 0
    for e in escenas:
        if e in extras:
            etiqueta = extras[e]
        else:
            n += 1
            etiqueta = str(n)
        salida.append((e, titulos.get(e, e), etiqueta))
    return tema, salida


def leer_interactivos(fichero):
    """INTERACTIVOS del tema: [(etiqueta, titulo, ruta desde la asignatura, escena anterior), ...]."""
    for nodo in ast.parse(open(fichero, encoding="utf-8").read()).body:
        if isinstance(nodo, ast.Assign) and getattr(nodo.targets[0], "id", None) == "INTERACTIVOS":
            return ast.literal_eval(nodo.value)
    return []


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
    for escena, _, etiqueta in escenas:
        nuevo = os.path.join(origen, f"{escena}.mp4")
        destino = os.path.join(carpeta, f"{etiqueta}.{escena}.mp4")
        # borra numeraciones viejas de esta escena (si cambió el orden)
        for viejo in glob.glob(os.path.join(carpeta, f"*.{escena}.mp4")):
            if os.path.abspath(viejo) != os.path.abspath(destino) and re.match(r"[A-Z]?\d+\.", os.path.basename(viejo)):
                os.remove(viejo)
        if os.path.exists(nuevo):
            if os.path.exists(destino):
                os.remove(destino)
            shutil.move(nuevo, destino)
            print(f"   {etiqueta}.{escena}.mp4")


def generar_web():
    temas = []
    for fichero in sorted(glob.glob(os.path.join(AQUI, "t[0-9]*_*.py"))):
        tema, escenas = leer_tema(fichero)
        carpeta = carpeta_videos(fichero)
        rel = os.path.relpath(carpeta, RAIZ).replace(os.sep, "/")
        interactivos = leer_interactivos(fichero)
        videos = []
        for escena, titulo, etiqueta in escenas:
            nombre = f"{etiqueta}.{escena}.mp4"
            if os.path.exists(os.path.join(carpeta, nombre)):
                videos.append((titulo, f"{rel}/{nombre}", None if etiqueta.isdigit() else etiqueta, None))
            else:
                print(f"   (aviso) falta {rel}/{nombre}: no se incluye en la web")
            for et, tit, ruta, detras in interactivos:
                if detras == escena:
                    if os.path.exists(os.path.join(ASIGNATURA, ruta.split("?")[0])):
                        src = os.path.relpath(os.path.join(ASIGNATURA, ruta), RAIZ).replace(os.sep, "/")
                        videos.append((tit, src, et, "web"))
                    else:
                        print(f"   (aviso) falta {ruta}: no se incluye en la web")
        if videos:
            temas.append((tema, videos))

    js = lambda s: json.dumps(s, ensure_ascii=False)
    lineas = [f"  {js(CLAVE_WEB)}: ["]
    for tema, videos in temas:
        lineas.append(f"    {{ tema: {js(tema)}, videos: [")
        for titulo, src, extra, tipo in videos:
            et = (f", extra: {js(extra)}" if extra else "") + (f", tipo: {js(tipo)}" if tipo else "")
            lineas.append(f"      {{ titulo: {js(titulo)}, src: {js(src)}{et} }},")
        lineas.append("    ]},")
    lineas.append("  ],")

    html = open(HTML, encoding="utf-8").read()
    patron = re.compile(r"(// <<AUTO " + re.escape(CLAVE_WEB) + r" [^\n]*\n).*?[ \t]*// AUTO>>", re.S)
    if not patron.search(html):
        # primer bloque de este curso/asignatura: se añade al final de const VIDEOS = { ... };
        inicio = html.index("const VIDEOS = {")
        fin = html.index("\n};", inicio)
        nuevo = f"\n  // <<AUTO {CLAVE_WEB} · generado por publicar.py, no editar a mano\n  // AUTO>>"
        html = html[:fin] + nuevo + html[fin:]
    html = patron.sub(lambda m: m.group(1) + "\n".join(lineas) + "\n  // AUTO>>", html, count=1)
    open(HTML, "w", encoding="utf-8", newline="\n").write(html)
    total = sum(len(v) for _, v in temas)
    print(f"\n>> index.html actualizado ({CLAVE_WEB}): {len(temas)} temas, {total} vídeos")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ficheros", nargs="*", help="temas a renderizar (tN_*.py)")
    ap.add_argument("--todos", action="store_true", help="renderiza todos los t*.py")
    ap.add_argument("--solo-web", action="store_true", help="no renderiza, solo actualiza index.html")
    ap.add_argument("--codigo", help="carpeta de código de otro curso (la usa 2ESO/.../codigo/publicar.py)")
    a = ap.parse_args()
    if a.codigo:
        configurar(a.codigo)

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
