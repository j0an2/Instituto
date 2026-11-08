"""Genera las fórmulas decorativas del fondo de la web (assets/formulas/formulas.js).

Cada fórmula se compila con LaTeX y se pasa a SVG vectorial con dvisvgm (misma tipografía que
Manim). El SVG usa fill="currentColor", así la web le da el color del tema claro u oscuro.
Se guardan en un .js (no en .svg sueltos) para que funcionen también abriendo index.html desde disco.

Uso: python generar_formulas_web.py
"""
import json
import os
import re
import subprocess
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SALIDA = os.path.join(RAIZ, "assets", "formulas", "formulas.js")

FORMULAS = [
    r"\frac{a}{b}+\frac{c}{d}=\frac{a\cdot d+b\cdot c}{b\cdot d}",
    r"\frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}",
    r"-(-a)=a",
    r"|-5|=5",
    r"12=2^2\cdot 3",
    r"\mathrm{m.c.m.}(4,6)=12",
    r"\frac{2}{3}=\frac{4}{6}=\frac{6}{9}",
    r"(-)\cdot(-)=+",
]

PLANTILLA = r"""\documentclass[preview,border=1pt]{standalone}
\usepackage{amsmath}
\begin{document}
$\displaystyle %s$
\end{document}
"""


def a_svg(tex, carpeta, n):
    base = os.path.join(carpeta, f"f{n}")
    with open(base + ".tex", "w", encoding="utf-8") as f:
        f.write(PLANTILLA % tex)
    subprocess.run(["latex", "-interaction=nonstopmode", "-output-directory", carpeta, base + ".tex"],
                   check=True, capture_output=True)
    subprocess.run(["dvisvgm", "--no-fonts", "--exact-bbox", "-o", base + ".svg", base + ".dvi"],
                   check=True, capture_output=True)
    svg = open(base + ".svg", encoding="utf-8").read()
    svg = svg[svg.index("<svg"):]                              # fuera cabecera XML y comentarios
    svg = re.sub(r"\s(width|height)=['\"][^'\"]*['\"]", "", svg, count=2)  # el tamaño lo pone el CSS
    svg = svg.replace("<svg ", '<svg fill="currentColor" aria-hidden="true" ', 1)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r">\s+<", "><", svg).strip()
    # ids únicos por fórmula: dvisvgm repite g0-1, g0-2... en cada SVG
    return re.sub(r"(id=['\"]|href=['\"]#)(g[\d-]+)", rf"\1f{n}\2", svg)


with tempfile.TemporaryDirectory() as tmp:
    svgs = [a_svg(tex, tmp, i) for i, tex in enumerate(FORMULAS)]

os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
    f.write("// Generado por 1ESO/Matematicas/codigo/generar_formulas_web.py, no editar a mano\n")
    f.write("window.FORMULAS = " + json.dumps(svgs, ensure_ascii=False, indent=0) + ";\n")
print(f"{SALIDA}: {len(svgs)} fórmulas, {os.path.getsize(SALIDA) // 1024} KB")
