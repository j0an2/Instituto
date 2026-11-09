"""Publica los temas de 2.º ESO Matemáticas: usa el mismo publicar.py de 1.º ESO con esta carpeta.

Uso (desde esta carpeta, con el Python del entorno de Manim):
    python publicar.py t01_enteros.py
    python publicar.py --solo-web
"""
import os
import runpy
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
COMUN = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "1ESO", "Matematicas", "codigo", "publicar.py"))
sys.argv[1:1] = ["--codigo", AQUI]
runpy.run_path(COMUN, run_name="__main__")
