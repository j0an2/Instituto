r"""Tema 8 · Lenguaje algebraico (1º ESO) — unidad 7 del libro

Guion del libro: expresiones algebraicas y traducción · monomios · polinomios · ecuaciones · resolución de primer grado.
Los vídeos de teoría son los de 2.º ESO (temas 3 y 4), que encajan tal cual en 1.º; se vuelven a renderizar aquí.
No entran (son de 2.º): multiplicar polinomios, identidades notables, denominadores y segundo grado.

Escenas:
    ExpresionesAlgebraicas  – traducir, el perímetro de un rectángulo, valor numérico            (2.º t03)
    Monomios                – partes, grado, semejantes con fichas, producto y cociente          (2.º t03)
    Polinomios              – términos, grado, ordenar y completar, valor numérico               (2.º t03)
    SumaRestaPolinomios     – en columnas y en línea                                             (2.º t03)
    QueEsEcuacion           – igualdad, identidad y ecuación; partes; la solución                (2.º t04)
    EcuacionesEquivalentes  – la balanza y la transposición                                      (2.º t04)
    PrimerGrado             – la receta, con paréntesis, con la balanza, casos especiales        (2.º t04)
    EjerciciosEjemplo / EjerciciosResueltos1 / EjerciciosResueltos2  – 10 ejercicios de nivel de 1.º

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\venvs\manim\Scripts\python.exe -m manim -pql t08_lenguaje_algebraico.py Monomios
    ~\venvs\manim\Scripts\python.exe publicar.py t08_lenguaje_algebraico.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COD_2ESO = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "2ESO", "Matematicas", "codigo"))
sys.path.append(COD_2ESO)          # al final: los nombres de 1.º tienen prioridad
from estilo import *  # noqa: E402,F403
from potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
import t03_lenguaje_algebraico as L  # noqa: E402
import t04_ecuaciones as E  # noqa: E402
from t03_lenguaje_algebraico import lista, pagina_enunciados  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 8 · Lenguaje algebraico"
TITULOS = {
    "ExpresionesAlgebraicas": "Expresiones algebraicas: traducir y valor numérico",
    "Monomios": "Monomios",
    "Polinomios": "Polinomios",
    "SumaRestaPolinomios": "Suma y resta de polinomios",
    "QueEsEcuacion": "¿Qué es una ecuación?",
    "EcuacionesEquivalentes": "Ecuaciones equivalentes: la balanza",
    "PrimerGrado": "Resolver ecuaciones de primer grado",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 5)",
    "EjerciciosResueltos2": "Ejercicios resueltos (6 a 10)",
}


# --- Teoría: las escenas de 2.º tal cual (Scene en las bases para que publicar.py las vea)
class ExpresionesAlgebraicas(L.ExpresionesAlgebraicas, Scene):
    pass


class Monomios(L.Monomios, Scene):
    def antes_de_multiplicar(self, cab, notas):
        """En 1.º aún no han visto las propiedades de las potencias: se justifican contando factores."""
        A, B = L.COEF, L.LETRA
        # --- Producto: x² · x³
        subtitulo(self, cab, "¿Por qué se suman los exponentes?")
        notas("Recuerda: x² es x·x y x³ es x·x·x")
        l1 = MathTex("x^{2}", "\\cdot", "x^{3}", font_size=60).move_to([-3.2, 1.9, 0])
        l1[0].set_color(A)
        l1[2].set_color(B)
        self.play(Write(l1))
        l2 = MathTex("=", "(x\\cdot x)", "\\cdot", "(x\\cdot x\\cdot x)", font_size=60)
        l2.next_to(l1, RIGHT, buff=0.25)
        l2[1].set_color(A)
        l2[3].set_color(B)
        self.play(TransformFromCopy(l1[0], l2[1]), TransformFromCopy(l1[2], l2[3]), FadeIn(l2[0], l2[2]))
        b2 = Brace(l2[1], DOWN, buff=0.1, color=A)
        b3 = Brace(l2[3], DOWN, buff=0.1, color=B)
        t2 = texto("2 factores", 24, A).next_to(b2, DOWN, buff=0.1)
        t3 = texto("3 factores", 24, B).next_to(b3, DOWN, buff=0.1)
        self.play(GrowFromCenter(b2), GrowFromCenter(b3), FadeIn(t2), FadeIn(t3))
        self.wait(1)
        l3 = MathTex("=", "x\\cdot x\\cdot x\\cdot x\\cdot x", "=", "x^{5}", font_size=60)
        l3.next_to(l2, DOWN, buff=1.3).align_to(l2, LEFT)
        l3[3].set_color(ACENTO)
        notas("En total multiplicamos la x cinco veces: 2 + 3 = 5")
        self.play(Write(l3[:2]))
        b5 = Brace(l3[1], DOWN, buff=0.1, color=ACENTO)
        t5 = texto("2 + 3 = 5 factores", 24, ACENTO).next_to(b5, DOWN, buff=0.1)
        self.play(GrowFromCenter(b5), FadeIn(t5))
        self.play(Write(l3[2:]))
        self.wait(1)
        regla = L.tarjeta(VGroup(
            MathTex("x^{2}\\cdot x^{3} = x^{2+3} = x^{5}", font_size=52),
            texto("Al multiplicar, los exponentes se suman", 30, ACENTO)).arrange(DOWN, buff=0.25))
        regla.move_to([0, -2.0, 0])
        self.play(FadeIn(regla))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Cociente: x⁵ : x²
        subtitulo(self, cab, "¿Y por qué se restan al dividir?")
        notas("Escribimos la división como una fracción")
        d1 = MathTex("x^{5} : x^{2}", "=", font_size=60)
        num = MathTex(*sum([["x", "\\cdot"] for _ in range(5)], [])[:-1], font_size=60)
        den = MathTex("x", "\\cdot", "x", font_size=60)
        raya = Line(LEFT, RIGHT).set_width(num.width + 0.2)
        frac = VGroup(num, raya, den).arrange(DOWN, buff=0.18)
        VGroup(d1, frac).arrange(RIGHT, buff=0.3).move_to([-1.6, 1.2, 0])
        self.play(Write(d1))
        self.play(Write(num), Create(raya), Write(den))
        self.wait(1)
        notas("Una x de arriba con una de abajo: x : x = 1, se van")
        for i in (0, 2):
            cr = VGroup(Line(num[i].get_corner(DL), num[i].get_corner(UR), color=MAL, stroke_width=6),
                        Line(den[i].get_corner(DL), den[i].get_corner(UR), color=MAL, stroke_width=6))
            self.play(Create(cr), run_time=0.8)
            self.wait(0.4)
        res = MathTex("=", "x\\cdot x\\cdot x", "=", "x^{3}", font_size=60).next_to(frac, RIGHT, buff=0.3)
        res[3].set_color(ACENTO)
        notas("Quedan tres x arriba: 5 − 2 = 3")
        self.play(Write(res))
        self.wait(1)
        regla = L.tarjeta(VGroup(
            MathTex("x^{5} : x^{2} = x^{5-2} = x^{3}", font_size=52),
            texto("Al dividir, los exponentes se restan", 30, ACENTO)).arrange(DOWN, buff=0.25))
        regla.move_to([0, -2.2, 0])
        self.play(FadeIn(regla))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)


class Polinomios(L.Polinomios, Scene):
    pass


class SumaRestaPolinomios(L.SumaRestaPolinomios, Scene):
    pass


class QueEsEcuacion(E.QueEsEcuacion, Scene):
    pass


class EcuacionesEquivalentes(E.EcuacionesEquivalentes, Scene):
    pass


class PrimerGrado(E.PrimerGrado, Scene):
    pass


# ---------------------------------------------------------------------------
# Ejercicios: 1–5 de lenguaje algebraico (los de 2.º) y 6–10 de ecuaciones de primer grado
def enunciados_1():
    return [
        ("1. Escribe en lenguaje algebraico (llama x al número):",
         "a) El doble de un número más 5      b) El cuadrado de un número menos su triple\n"
         "c) La edad de Ana dentro de 7 años (hoy tiene x)      d) Tres números consecutivos"),
        ("2. Calcula el valor numérico de P(x) = 2x² − 3x + 1 para:", lista(["x = 2", "x = −1", "x = 0", "x = 3"])),
        ("3. Di el coeficiente, la parte literal y el grado:", lista(["−5x³", "7x²y", "−x", "6"])),
        ("4. Reduce:", lista(["3x + 5x − 2x", "4x² − x + 2x² + 3x", "5x · (−2x²)", "12x⁵ : 4x²"])),
    ]


def enunciados_2():
    return [
        ("5. Con P(x) = 3x³ − 2x + 5  y  Q(x) = x³ + 4x² − 6, calcula:",
         lista(["P(x) + Q(x)", "P(x) − Q(x)", "Q(x) − P(x)"], 3)),
        ("6. Comprueba si x = 3 es solución:", lista(["2x + 1 = 7", "5x − 4 = 3x + 1", "x² − x = 6"], 3)),
        ("7. Resuelve:", lista(["3x + 5 = 20", "7x − 4 = 5x + 8", "2 − 3x = x + 14", "4x + 3 = 4x − 1"])),
    ]


def enunciados_3():
    return [
        ("8. Resuelve (con paréntesis):", lista(["2(x + 3) = 14", "4(x − 1) − 3 = 2x + 3", "3 − (x − 5) = 2(x + 1)"], 3)),
        ("9. Si al doble de un número le restas 7, obtienes 25. ¿Qué número es?", ""),
        ("10. 3 cuadernos iguales y un boli de 2 € cuestan 11 €. ¿Cuánto vale un cuaderno?", ""),
    ]


def problema_10(scene, notas):
    """Una sola incógnita y con contexto (el de Ana y Luis de 2.º es más bien de sistemas)."""
    enun = texto("Compro 3 cuadernos iguales y un bolígrafo de 2 €.\nEn total pago 11 €. ¿Cuánto cuesta cada cuaderno?", 28)
    scene.play(FadeIn(enun.move_to([0, 2.3, 0])))
    notas("x = el precio de un cuaderno.  3 cuadernos: 3x.  Más el bolígrafo: 3x + 2")
    pas = [("3x=11-2", None), ("3x=9", None), ("x=9:3=3", None)]
    E.cuenta(scene, "3x+2=11", pas, -3.0, 1.1, notas, None, False, 54, dy=1.0)
    notas("Cada cuaderno cuesta 3 €. Comprobamos: 3 · 3 + 2 = 9 + 2 = 11 ✓", color=OK)
    scene.wait(3)
    notas.fin()


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Lenguaje algebraico")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        L.ej_traduce(self, 0, 0.8, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        self.play(Write(L.p_valor()))
        L.ej_valor(self, 0, -3.0, 1.0, notas, ejemplo=True, size=54)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        L.tabla_monomios(self, notas, [0], ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 a)")
        L.ej_reduce(self, 0, -3.0, 1.2, notas, ejemplo=True, size=56)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 a)")
        L.ej5_suma(self, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        E.ej_comprueba(self, 0, -3.0, 1.2, notas, ejemplo=True, size=54)
        notas.fin()
        limpiar(self, cab)
        for n, datos, y in ((7, E.RESUELVE, 1.5), (8, E.PARENTESIS, 1.5)):
            subtitulo(self, cab, f"Ejercicio {n} a)")
            E.ej_lista(self, datos, 0, -3.4, y, notas, ejemplo=True, size=52, dy=1.05)
            self.wait(1)
            notas.fin()
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9")
        E.problema_8(self, notas)
        limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 5")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1: b), c) y d)")
        for i, y in zip((1, 2, 3), (1.4, 0.0, -1.4)):
            L.ej_traduce(self, i, y, notas)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2 b)")
        self.play(Write(L.p_valor()))
        L.ej_valor(self, 1, -3.0, 1.0, notas, size=54)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2: c) y d)")
        self.play(Write(L.p_valor()))
        L.ej_valor(self, 2, -5.8, 1.0, notas, size=48)
        L.ej_valor(self, 3, 1.0, 1.0, notas, size=48)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        L.tabla_monomios(self, notas, [1, 2, 3])
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 4 b)")
        L.ej_reduce(self, 1, -4.4, 1.2, notas, size=54)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4: c) y d)")
        L.ej_reduce(self, 2, -5.8, 1.2, notas, size=46)
        L.ej_reduce(self, 3, 1.2, 1.2, notas, size=46)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 b)")
        L.ej5_resta(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 c)")
        L.ej5_inversa(self, notas)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo: ejercicios 6 a 10.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 6 a 10")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 6: b) y c)")
        E.ej_comprueba(self, 1, -5.8, 1.6, notas)
        E.ej_comprueba(self, 2, 1.2, 1.6, notas)
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 7: b) y c)")
        E.ej_lista(self, E.RESUELVE, 1, -5.8, 1.5, notas, size=46)
        E.ej_lista(self, E.RESUELVE, 2, 0.8, 1.5, notas, size=46)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 d)")
        E.ej_lista(self, E.RESUELVE, 3, -3.0, 1.5, notas, size=52, sin_sol="Sin solución")
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 8: b) y c)")
        E.ej_lista(self, E.PARENTESIS, 1, -6.0, 1.6, notas, size=44, dy=0.85)
        E.ej_lista(self, E.PARENTESIS, 2, 0.8, 1.6, notas, size=44, dy=0.85)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 10")
        problema_10(self, notas)
        limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
