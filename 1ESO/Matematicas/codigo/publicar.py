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

Ficheros-biblioteca sin tema propio (p. ej. potencias_raices.py, jerarquia.py): no definen TEMA, sino dónde va
cada escena en la web, dentro de otro tema:
    UBICACION = {"Escena": ("t03_enteros", "EscenaAnterior", None), ...}   # None = vídeo normal (cuenta en la numeración)
    UBICACION = {"Escena": ("t01_naturales", "EscenaAnterior", "E1"), ...} # "E1" = vídeo extra
EscenaAnterior puede ser de ese tema o una escena ya ubicada antes; None = al final del tema.
Sus vídeos se guardan en videos/<biblioteca>/ y se renderizan igual: python publicar.py potencias_raices.py
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
    tema, titulos, extras, escenas, ubic = None, {}, {}, [], None
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 and isinstance(nodo.targets[0], ast.Name):
            nombre = nodo.targets[0].id
            if nombre == "TEMA":
                tema = ast.literal_eval(nodo.value)
            elif nombre == "TITULOS":
                titulos = ast.literal_eval(nodo.value)
            elif nombre == "EXTRAS":
                extras = ast.literal_eval(nodo.value)
            elif nombre == "UBICACION":
                ubic = ast.literal_eval(nodo.value)
        elif isinstance(nodo, ast.ClassDef):
            bases = {getattr(b, "id", getattr(b, "attr", "")) for b in nodo.bases}
            if bases & {"Scene", "MovingCameraScene", "ThreeDScene", "ZoomedScene"}:
                escenas.append(nodo.name)
    if ubic is not None:
        # biblioteca: solo cuentan las escenas que tienen sitio en la web (el resto no se publica)
        extras = {e: u[2] for e, u in ubic.items() if u[2]}
        escenas = [e for e in escenas if e in ubic]
    if tema is None and ubic is None:
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


def leer_ubicacion(fichero):
    """UBICACION de un fichero-biblioteca ({} si no tiene)."""
    texto = open(fichero, encoding="utf-8").read()
    if "UBICACION" not in texto:
        return {}
    for nodo in ast.parse(texto).body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 and getattr(nodo.targets[0], "id", "") == "UBICACION":
            return ast.literal_eval(nodo.value)
    return {}


def bibliotecas():
    """Ficheros sin tema propio cuyas escenas van dentro de otros temas."""
    return [f for f in sorted(glob.glob(os.path.join(AQUI, "*.py")))
            if not re.match(r"t\d", os.path.basename(f)) and leer_ubicacion(f)]


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
    por_id = {}
    for fichero in sorted(glob.glob(os.path.join(AQUI, "t[0-9]*_*.py"))):
        tema, escenas = leer_tema(fichero)
        carpeta = carpeta_videos(fichero)
        rel = os.path.relpath(carpeta, RAIZ).replace(os.sep, "/")
        interactivos = leer_interactivos(fichero)
        videos = []
        for escena, titulo, etiqueta in escenas:
            nombre = f"{etiqueta}.{escena}.mp4"
            if os.path.exists(os.path.join(carpeta, nombre)):
                videos.append((titulo, f"{rel}/{nombre}", None if etiqueta.isdigit() else etiqueta, None, escena))
            else:
                print(f"   (aviso) falta {rel}/{nombre}: no se incluye en la web")
            for et, tit, ruta, detras in interactivos:
                if detras == escena:
                    if os.path.exists(os.path.join(ASIGNATURA, ruta.split("?")[0])):
                        src = os.path.relpath(os.path.join(ASIGNATURA, ruta), RAIZ).replace(os.sep, "/")
                        videos.append((tit, src, et, "web", escena + "#web"))
                    else:
                        print(f"   (aviso) falta {ruta}: no se incluye en la web")
        temas.append((tema, videos))
        por_id[tema_id(fichero)] = videos

    # Escenas de las bibliotecas, dentro de su tema. Se colocan por pasadas: una escena que va detrás
    # de otra escena ubicada (de otra biblioteca) espera a que esa ya esté puesta.
    pendientes = []
    for fichero in bibliotecas():
        ubic = leer_ubicacion(fichero)
        _, escenas = leer_tema(fichero)
        carpeta = carpeta_videos(fichero)
        rel = os.path.relpath(carpeta, RAIZ).replace(os.sep, "/")
        for escena, titulo, etiqueta in escenas:
            if escena not in ubic:
                continue
            destino, detras, extra = ubic[escena]
            nombre = f"{etiqueta}.{escena}.mp4"
            if destino not in por_id:
                print(f"   (aviso) {escena}: no existe el tema {destino}")
            elif not os.path.exists(os.path.join(carpeta, nombre)):
                print(f"   (aviso) falta {rel}/{nombre}: no se incluye en la web")
            else:
                pendientes.append((escena, titulo, f"{rel}/{nombre}", destino, detras, extra))

    def colocar(item, al_final=False):
        escena, titulo, src, destino, detras, extra = item
        lista = por_id[destino]
        idx = [i for i, v in enumerate(lista) if detras and v[4] in (detras, detras + "#web")]
        if detras and not idx and not al_final:
            return False
        lista.insert(idx[-1] + 1 if idx else len(lista), (titulo, src, extra, None, escena))
        return True

    while pendientes:
        resto = [it for it in pendientes if not colocar(it)]
        if len(resto) == len(pendientes):  # no se encuentra la escena anterior: al final del tema
            for it in resto:
                print(f"   (aviso) {it[0]}: no se encuentra {it[4]} en {it[3]}; va al final")
                colocar(it, al_final=True)
            resto = []
        pendientes = resto
    temas = [(t, v) for t, v in temas if v]

    js = lambda s: json.dumps(s, ensure_ascii=False)
    lineas = [f"  {js(CLAVE_WEB)}: ["]
    for tema, videos in temas:
        lineas.append(f"    {{ tema: {js(tema)}, videos: [")
        for titulo, src, extra, tipo, _ in videos:
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

    ficheros = sorted(glob.glob(os.path.join(AQUI, "t[0-9]*_*.py"))) + bibliotecas() if a.todos else \
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
