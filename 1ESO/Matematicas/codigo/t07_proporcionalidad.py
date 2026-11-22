r"""Tema 7 · Proporcionalidad (1º ESO) — unidad 6 del libro

Escenas:
    Razon                   – chicas y chicos de una clase: 12/8 = 3/2; razón frente a fracción; km por hora
    Proporcion              – receta de crepes: 2/3 = 4/6, productos cruzados y el término que falta (sin ecuaciones)
    MagnitudesDirectas      – helados a 2 €: tabla con ×2 / ×3, cociente constante; edad y altura (no proporcional)
    MagnitudesInversas      – 12 caramelos entre amigos (bloques que se reordenan), producto constante; directa vs inversa
    ReglaDeTresDirecta      – cuadernos: reducción a la unidad y regla de tres con flechas
    ReglaDeTresInversa      – grifos: reducción a la unidad y regla de tres con la flecha dada la vuelta
    Porcentajes             – cuadrícula de 100; porcentajes fáciles; el 30 % de 80 de tres maneras
    AumentosDescuentos      – rebajas y subidas en dos pasos y en uno (0,80 · precio, 1,10 · precio)
    Escalas (extra E2)      – mapas y planos: 1 : 100 000, distancia real; escala gráfica
    EjerciciosEjemplo / EjerciciosResueltos1 / EjerciciosResueltos2

Reutiliza las herramientas del tema 6 de 2.º ESO (tablas, esquema de la regla de tres, barras, cuadrícula de 100).
Colores: 1.ª magnitud cian, 2.ª naranja, la x amarilla, los porcentajes verdes.

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\venvs\manim\Scripts\python.exe -m manim -pql t07_proporcionalidad.py Razon
    ~\venvs\manim\Scripts\python.exe publicar.py t07_proporcionalidad.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COD_2ESO = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "2ESO", "Matematicas", "codigo"))
sys.path.append(COD_2ESO)          # al final: los nombres de 1.º tienen prioridad
from estilo import *  # noqa: E402,F403
from potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t03_lenguaje_algebraico import X, cuenta, lista, tarjeta, ROSA, LETRA  # noqa: E402
from t06_proporcionalidad import (M1, M2, PCT, Sub, tabla_h, flecha_arco, esquema, rejilla_pos, llaves,  # noqa: E402
                                  barra, cuadricula100)

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 7 · Proporcionalidad"
TITULOS = {
    "Razon": "Razón: comparar dos cantidades",
    "Proporcion": "Proporción",
    "MagnitudesDirectas": "Magnitudes directamente proporcionales",
    "MagnitudesInversas": "Magnitudes inversamente proporcionales",
    "ReglaDeTresDirecta": "Regla de tres directa",
    "ReglaDeTresInversa": "Regla de tres inversa",
    "Porcentajes": "Porcentajes",
    "AumentosDescuentos": "Rebajas y subidas",
    "Escalas": "Escalas: mapas y planos",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 4)",
    "EjerciciosResueltos2": "Ejercicios resueltos (5 a 8)",
}
EXTRAS = {"Escalas": "E2"}
INTERACTIVOS = [("E1", "Pruébalo tú: ¿directa, inversa o ninguna?",
                 "../../2ESO/Matematicas/interactivos/directa_inversa.html", "MagnitudesInversas")]

CHICA, CHICO = ROSA, M1
HUEVO, LECHE = "#F7DC6F", "#D6EAF8"
CARAMELO = "#C39BD3"


def frac(n, d, c1=WHITE, c2=WHITE, size=56):
    """Fracción n/d con numerador y denominador de colores."""
    t = MathTex(f"\\dfrac{{{n}}}{{{d}}}", font_size=size)
    k = len(str(n).replace("{", "").replace("}", "").replace(",", ""))
    t[0][:k].set_color(c1)
    t[0][k + 1:].set_color(c2)
    return t


def eur(tex, size=46, color=WHITE):
    """Fórmula seguida de « €» (el símbolo € no se dibuja dentro de MathTex). [0] es el MathTex."""
    return VGroup(MathTex(tex, font_size=size, color=color),
                  texto("€", round(size * 0.62), color)).arrange(RIGHT, buff=0.14)


def enunciado(scene, cadena, y=2.35, size=30):
    t = texto(cadena, size)
    if t.width > config.frame_width - 1.0:
        t.scale_to_fit_width(config.frame_width - 1.0)
    t.move_to([0, y, 0])
    scene.play(FadeIn(t))
    return t


# ---------------------------------------------------------------------------
class Razon(Scene):
    def construct(self):
        cab = titulo(self, "Razón", "Comparar dos cantidades")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Chicas y chicos")
        ley = VGroup(Dot(radius=0.14, color=CHICA), texto("chica", 24, CHICA),
                     Dot(radius=0.14, color=CHICO), texto("chico", 24, CHICO)).arrange(RIGHT, buff=0.15)
        ley.to_corner(UR, buff=0.45)
        self.play(FadeIn(ley))
        chicas = VGroup(*[Dot(radius=0.17, color=CHICA) for _ in range(12)]).arrange(RIGHT, buff=0.28)
        chicos = VGroup(*[Dot(radius=0.17, color=CHICO) for _ in range(8)]).arrange(RIGHT, buff=0.28)
        chicas.move_to([0, 1.3, 0])
        chicos.move_to([0, 0.5, 0]).align_to(chicas, LEFT)
        notas("En una clase hay 12 chicas y 8 chicos")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in chicas], lag_ratio=0.05))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in chicos], lag_ratio=0.05))
        self.wait(1)
        notas("Hacemos grupos iguales con todos: ¿cuántos grupos salen?")
        cajas = VGroup()
        anims = []
        for g in range(4):
            cx = -4.5 + g * 3.0
            for k in range(3):
                anims.append(chicas[3 * g + k].animate.move_to([cx - 0.5 + k * 0.5, 1.0, 0]))
            for k in range(2):
                anims.append(chicos[2 * g + k].animate.move_to([cx - 0.25 + k * 0.5, 0.3, 0]))
            cajas.add(RoundedRectangle(width=2.1, height=1.45, corner_radius=0.15, color=GREY_B).move_to([cx, 0.65, 0]))
        self.play(*anims, run_time=1.6)
        self.play(LaggedStart(*[Create(c) for c in cajas], lag_ratio=0.2))
        notas("4 grupos iguales: en cada uno, 3 chicas y 2 chicos")
        self.wait(2)
        r = VGroup(frac(12, 8, CHICA, CHICO), MathTex("=", font_size=56), frac(3, 2, CHICA, CHICO))
        r.arrange(RIGHT, buff=0.25).move_to([-2.2, -1.25, 0])
        lee = texto("«por cada 3 chicas\n  hay 2 chicos»", 28).next_to(r, RIGHT, buff=0.7)
        self.play(Write(r[0]))
        notas("La RAZÓN compara dos cantidades dividiendo: 12 chicas entre 8 chicos")
        self.wait(1.5)
        self.play(Write(r[1:]))
        self.play(FadeIn(lee, shift=LEFT * 0.2))
        notas("Se simplifica como una fracción: 12/8 = 3/2", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Razón y fracción no son lo mismo")
        a = VGroup(texto("RAZÓN", 30, ACENTO), frac(12, 8, CHICA, CHICO, 60),
                   texto("chicas comparadas\ncon chicos", 26)).arrange(DOWN, buff=0.3)
        b = VGroup(texto("FRACCIÓN", 30, ACENTO), frac(12, 20, CHICA, WHITE, 60),
                   texto("chicas del total\nde la clase (20)", 26)).arrange(DOWN, buff=0.3)
        ta = tarjeta(a, buff=0.4).move_to([-3.2, 0.2, 0])
        tb = tarjeta(b, buff=0.4).move_to([3.2, 0.2, 0])
        tb[0].stretch_to_fit_height(ta[0].height).move_to([3.2, 0.2, 0])
        self.play(Create(ta[0]), FadeIn(a))
        notas("La razón compara una cantidad con OTRA")
        self.wait(2)
        self.play(Create(tb[0]), FadeIn(b))
        notas("La fracción compara una PARTE con el TOTAL: 12 de los 20 alumnos son chicas")
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Razones con unidades")
        enunciado(self, "Un tren recorre 150 km en 2 horas")
        r = VGroup(MathTex("\\dfrac{150\\ \\mathrm{km}}{2\\ \\mathrm{h}}", font_size=64, color=M1),
                   MathTex("=", font_size=64), MathTex("75\\ \\mathrm{km/h}", font_size=64, color=ACENTO))
        r.arrange(RIGHT, buff=0.3).move_to([0, 0.4, 0])
        self.play(Write(r[0]))
        notas("Comparamos los kilómetros con las horas...")
        self.wait(1)
        self.play(Write(r[1:]))
        notas("...75 km por cada hora: ¡la velocidad es una razón!", color=OK)
        otras = texto("También son razones: € por kilo, goles por partido, personas por km²...", 26, GREY_B)
        otras.move_to([0, -1.4, 0])
        self.play(FadeIn(otras))
        self.wait(3.5)
        notas.fin()


# ---------------------------------------------------------------------------
def huevos(n, cx, y, r=0.2):
    g = VGroup(*[Ellipse(width=r * 1.6, height=r * 2, color=HUEVO, fill_opacity=0.9) for _ in range(n)])
    return g.arrange(RIGHT, buff=0.12).move_to([cx, y, 0])


def vasos(n, cx, y, w=0.36, h=0.55):
    g = VGroup()
    for _ in range(n):
        v = VGroup(Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=2),
                   Rectangle(width=w - 0.06, height=h * 0.75, stroke_width=0, fill_color=LECHE, fill_opacity=0.9))
        v[1].align_to(v[0], DOWN).shift(UP * 0.03)
        g.add(v)
    return g.arrange(RIGHT, buff=0.12).move_to([cx, y, 0])


class Proporcion(Scene):
    def construct(self):
        cab = titulo(self, "Proporción")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("La receta de crepes")
        ley = VGroup(Ellipse(width=0.26, height=0.32, color=HUEVO, fill_opacity=0.9), texto("huevo", 24, HUEVO),
                     Rectangle(width=0.26, height=0.36, stroke_color=WHITE, fill_color=LECHE, fill_opacity=0.9),
                     texto("vaso de leche", 24, LECHE)).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.45)
        self.play(FadeIn(ley))
        t1 = texto("Para 6 crepes", 28).move_to([-3.4, 1.9, 0])
        t2 = texto("Para 12 crepes", 28).move_to([3.4, 1.9, 0])
        h1, v1 = huevos(2, -3.4, 1.0), vasos(3, -3.4, 0.05)
        h2, v2 = huevos(4, 3.4, 1.0), vasos(6, 3.4, 0.05)
        notas("La receta: 2 huevos por cada 3 vasos de leche")
        self.play(FadeIn(t1), LaggedStart(*[FadeIn(m, scale=0.5) for m in [*h1, *v1]], lag_ratio=0.15))
        r1 = frac(2, 3, HUEVO, LECHE, 60).move_to([-3.4, -1.3, 0])
        self.play(Write(r1))
        self.wait(1)
        notas("Para el doble de crepes, el doble de todo: 4 huevos y 6 vasos")
        self.play(FadeIn(t2), LaggedStart(*[FadeIn(m, scale=0.5) for m in [*h2, *v2]], lag_ratio=0.1))
        r2 = frac(4, 6, HUEVO, LECHE, 60).move_to([3.4, -1.3, 0])
        self.play(Write(r2))
        self.wait(1)
        igual = MathTex("=", font_size=80, color=OK).move_to([0, -1.3, 0])
        self.play(FadeIn(igual, scale=1.5))
        notas("Las dos razones son iguales (4/6 = 2/3): forman una PROPORCIÓN", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Productos cruzados")
        p = MathTex("\\dfrac{2}{3}", "=", "\\dfrac{4}{6}", font_size=100).move_to([0, 1.0, 0])
        self.play(Write(p))
        a_, b_, c_, d_ = p[0][0], p[0][2], p[2][0], p[2][2]
        l1 = Line(a_.get_center(), d_.get_center(), buff=0.4, color=M2, stroke_width=5)
        l2 = Line(b_.get_center(), c_.get_center(), buff=0.4, color=M1, stroke_width=5)
        notas("¿Cómo sabemos si dos razones forman proporción? Multiplicamos en cruz")
        self.play(Create(l1), a_.animate.set_color(M2), d_.animate.set_color(M2))
        pr1 = MathTex("2\\cdot 6=12", font_size=52, color=M2).move_to([-2.8, -1.1, 0])
        self.play(Write(pr1))
        self.play(Create(l2), b_.animate.set_color(M1), c_.animate.set_color(M1))
        pr2 = MathTex("3\\cdot 4=12", font_size=52, color=M1).move_to([2.8, -1.1, 0])
        self.play(Write(pr2))
        notas("Los dos productos son iguales: SÍ es una proporción", color=OK)
        self.wait(2.5)
        self.play(FadeOut(VGroup(p, l1, l2, pr1, pr2)))
        q = MathTex("\\dfrac{2}{3}", "\\ \\overset{?}{=}\\ ", "\\dfrac{3}{4}", font_size=90).move_to([0, 1.0, 0])
        self.play(Write(q))
        pr = MathTex("2\\cdot 4=8", "\\neq", "3\\cdot 3=9", font_size=52).move_to([0, -1.1, 0])
        pr[1].set_color(MAL)
        self.play(Write(pr))
        notas("8 no es 9: 2/3 y 3/4 NO forman proporción", color=MAL)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("El término que falta")
        enunciado(self, "Tengo 10 huevos. ¿Cuántos vasos de leche necesito para la receta?")
        p = VGroup(frac(2, 3, HUEVO, LECHE, 80), MathTex("=", font_size=80),
                   MathTex("\\dfrac{10}{x}", font_size=80)).arrange(RIGHT, buff=0.3).move_to([-3.2, 0.5, 0])
        p[2][0][:2].set_color(HUEVO)
        p[2][0][3:].set_color(LETRA)
        self.play(Write(p))
        notas("Llamamos x a los vasos que no sabemos")
        self.wait(1.5)
        pasos = VGroup(MathTex("x", "=", "\\dfrac{3\\cdot 10}{2}", font_size=60),
                       MathTex("x", "=", "\\dfrac{30}{2}", "=", "15", font_size=60))
        pasos[0][0].set_color(LETRA)
        pasos[1][0].set_color(LETRA)
        pasos[1][4].set_color(ACENTO)
        pasos.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.8, 0.5, 0])
        cruz = Line(p[0][0][2].get_center(), p[2][0][0].get_center(), buff=0.35, color=M2, stroke_width=5)
        notas("Multiplicamos en cruz los dos números que conocemos (3 · 10)...")
        self.play(Create(cruz))
        self.play(Write(pasos[0]))
        notas("...y dividimos entre el que queda (2)")
        self.wait(2)
        self.play(Write(pasos[1]))
        self.play(Circumscribe(pasos[1][4], color=ACENTO))
        notas("Necesito 15 vasos de leche. Comprobamos: 10/15 = 2/3 ✓", color=OK)
        self.wait(3.5)
        notas.fin()


# ---------------------------------------------------------------------------
class MagnitudesDirectas(Scene):
    def construct(self):
        cab = titulo(self, "Proporcionalidad directa")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Los helados")
        enunciado(self, "Cada helado cuesta 2 €")
        marco, labs, cel, (ytop, ybot) = tabla_h(["Helados", "Precio (€)"],
                                                 [["1", "2", "3", "4", "5"], ["2", "4", "6", "8", "10"]], 0, 1.0)
        self.play(Create(marco), FadeIn(labs))
        notas("Una MAGNITUD es algo que se puede medir o contar: los helados, el precio...")
        for k in range(5):
            self.play(FadeIn(cel[0][k]), FadeIn(cel[1][k]), run_time=0.45)
        self.wait(1)
        xs = [c.get_center()[0] for c in cel[0]]
        for i, j, f, txt in [(0, 1, "\\times 2", "El doble de helados..."), (0, 2, "\\times 3", "El triple de helados...")]:
            notas(txt)
            a1 = flecha_arco(xs[i], xs[j], ytop + 0.05, f, True)
            self.play(Create(a1[0]), FadeIn(a1[1]))
            a2 = flecha_arco(xs[i], xs[j], ybot - 0.05, f, False)
            notas(txt.replace("helados", "precio").replace("El doble de precio", "...el doble de precio")
                  .replace("El triple de precio", "...el triple de precio"))
            self.play(Create(a2[0]), FadeIn(a2[1]))
            self.wait(1.5)
            self.play(FadeOut(a1), FadeOut(a2))
        notas("Magnitudes DIRECTAMENTE proporcionales: si una se multiplica, la otra también", color=OK)
        self.wait(2.5)

        sub("Siempre el mismo cociente")
        q = MathTex("\\dfrac{2}{1}", "=", "\\dfrac{4}{2}", "=", "\\dfrac{6}{3}", "=", "\\dfrac{8}{4}", "=",
                    "\\dfrac{10}{5}", "=", "2", font_size=50).move_to([0, -1.2, 0])
        for i in range(0, 9, 2):
            k = 2 if i == 8 else 1
            q[i][0][:k].set_color(M2)
            q[i][0][k + 1:].set_color(M1)
        notas("Dividimos cada precio entre su número de helados...")
        self.play(Write(q[:9]), run_time=2)
        self.play(Write(q[9:]), q[10].animate.set_color(ACENTO))
        notas("...¡siempre sale 2! Es la constante de proporcionalidad: lo que cuesta 1 helado", color=ACENTO)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("¿Todo es proporcional?")
        enunciado(self, "La edad y la altura de una niña")
        marco, labs, cel, (ytop, ybot) = tabla_h(["Edad (años)", "Altura (cm)"],
                                                 [["1", "2", "4", "8"], ["75", "86", "102", "128"]], 0, 1.0, w=1.3)
        self.play(Create(marco), FadeIn(labs), *[FadeIn(c) for c in cel[0] + cel[1]])
        xs = [c.get_center()[0] for c in cel[0]]
        a1 = flecha_arco(xs[0], xs[1], ytop + 0.05, "\\times 2", True)
        notas("Con el doble de edad (2 años)... ¿mide el doble, 150 cm?")
        self.play(Create(a1[0]), FadeIn(a1[1]))
        self.wait(1.5)
        a2 = flecha_arco(xs[0], xs[1], ybot - 0.05, "\\times 2\\ ?", False, color=MAL)
        cruz = Cross(a2[1], stroke_color=MAL, stroke_width=5)
        self.play(Create(a2[0]), FadeIn(a2[1]))
        self.play(Create(cruz))
        notas("¡No! Mide 86 cm. Las dos crecen, pero NO son proporcionales", color=MAL)
        self.wait(3)
        regla = texto("Para que sean proporcionales no basta con que «las dos crezcan»:\n"
                      "al multiplicar una por un número, la otra se tiene que multiplicar por el MISMO número", 24)
        if regla.width > config.frame_width - 1.2:
            regla.scale_to_fit_width(config.frame_width - 1.2)
        regla.move_to([0, -1.5, 0])
        self.play(FadeIn(regla))
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
class MagnitudesInversas(Scene):
    def construct(self):
        cab = titulo(self, "Proporcionalidad inversa")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Repartir caramelos")
        enunciado(self, "Repartimos 12 caramelos a partes iguales entre unos amigos", y=2.4)
        centro, s = (2.8, -0.1, 0), 0.5
        pos = rejilla_pos(1, 12, centro, s)
        bloques = VGroup(*[Circle(radius=s * 0.38, stroke_color=WHITE, stroke_width=1.5, fill_color=CARAMELO,
                                  fill_opacity=0.85).move_to(p) for p in pos])
        ll = llaves(1, 12, centro, s, "1 amigo", "12 caramelos cada uno")
        notas("Si hay 1 amigo, se lo queda todo: 12 caramelos")
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in bloques], lag_ratio=0.05))
        self.play(FadeIn(ll))
        cab_t = VGroup(texto("amigos", 24, M1).move_to([-6.0, 1.45, 0]), texto("caramelos", 24, M2).move_to([-4.55, 1.45, 0]))
        raya = Line([-6.7, 1.17, 0], [-1.75, 1.17, 0], color=GREY_B, stroke_width=2)
        self.play(FadeIn(cab_t), Create(raya))
        filas = VGroup()

        def fila(a, c, k):
            y = 0.8 - k * 0.55
            f = VGroup(MathTex(str(a), font_size=36, color=M1).move_to([-6.0, y, 0]),
                       MathTex(str(c), font_size=36, color=M2).move_to([-4.55, y, 0]),
                       MathTex(f"{a}\\cdot {c}=12", font_size=32, color=GREY_B).move_to([-2.45, y, 0]))
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.6)
            filas.add(f)

        fila(1, 12, 0)
        for k, (a, c, txt) in enumerate([(2, 6, "2 amigos: 6 caramelos cada uno"),
                                         (3, 4, "3 amigos: 4 cada uno"),
                                         (4, 3, "4 amigos: 3 cada uno"),
                                         (6, 2, "6 amigos: solo 2 cada uno")], start=1):
            notas(txt)
            pos = rejilla_pos(a, c, centro, s)
            nl = llaves(a, c, centro, s, f"{a} amigos", f"{c} cada uno")
            self.play(*[q.animate.move_to(pp) for q, pp in zip(bloques, pos)], Transform(ll, nl), run_time=1.3)
            fila(a, c, k)
            self.wait(0.6)
        fx = [f[0].get_center() for f in filas]
        fc = [f[1].get_center() for f in filas]
        g1 = CurvedArrow(fx[1] + LEFT * 0.35, fx[3] + LEFT * 0.35, angle=PI / 2, color=ACENTO, stroke_width=3,
                         tip_length=0.14)
        t1 = MathTex("\\times 2", font_size=28, color=ACENTO).next_to(g1, LEFT, buff=0.05)
        g2 = CurvedArrow(fc[1] + RIGHT * 0.4, fc[3] + RIGHT * 0.4, angle=-PI / 2, color=ACENTO, stroke_width=3,
                         tip_length=0.14)
        t2 = MathTex(":2", font_size=28, color=ACENTO).next_to(g2, RIGHT, buff=0.05)
        notas("El doble de amigos (2 → 4)... la MITAD de caramelos para cada uno (6 → 3)")
        self.play(Create(g1), FadeIn(t1))
        self.play(Create(g2), FadeIn(t2))
        self.wait(2)
        notas("Magnitudes INVERSAMENTE proporcionales: el producto siempre es 12", color=OK)
        self.play(Indicate(VGroup(*[f[2] for f in filas]), color=ACENTO))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Directa o inversa")
        cd = VGroup(texto("DIRECTA", 30, OK), texto("una × 2  →  la otra × 2", 26), texto("una : 2  →  la otra : 2", 26),
                    texto("el COCIENTE no cambia", 26, ACENTO), texto("helados y precio", 24, GREY_B))
        ci = VGroup(texto("INVERSA", 30, ROSA), texto("una × 2  →  la otra : 2", 26), texto("una : 2  →  la otra × 2", 26),
                    texto("el PRODUCTO no cambia", 26, ACENTO), texto("amigos y caramelos", 24, GREY_B))
        cd.arrange(DOWN, buff=0.35)
        ci.arrange(DOWN, buff=0.35)
        t1 = tarjeta(cd, color=OK, buff=0.4).move_to([-3.3, 0.1, 0])
        t2 = tarjeta(ci, color=ROSA, buff=0.4).move_to([3.3, 0.1, 0])
        t2[0].stretch_to_fit_height(t1[0].height).move_to([3.3, 0.1, 0])
        self.play(Create(t1[0]), Create(t2[0]))
        for a, c in zip(cd, ci):
            self.play(FadeIn(a, shift=UP * 0.15), FadeIn(c, shift=UP * 0.15), run_time=0.7)
            self.wait(0.8)
        notas("Truco: más amigos → MENOS caramelos. Si una sube y la otra baja, piensa en la inversa")
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
def unidad(scene, lineas, x=1.2, y=0.9):
    """Reducción a la unidad: dos líneas de texto que aparecen una a una."""
    u = VGroup(*[texto(l, 32) for l in lineas]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
    u.move_to([x, y, 0], aligned_edge=LEFT)
    for m in u:
        scene.play(FadeIn(m, shift=RIGHT * 0.2))
        scene.wait(1.3)
    scene.play(Circumscribe(u[-1], color=ACENTO))
    return u


def x_igual(s_frac, resultado, size=56):
    """x = (a · b) : c = resultado, con la x amarilla."""
    m = MathTex("x", "=", s_frac, "=", resultado, font_size=size)
    m[0].set_color(LETRA)
    m[4].set_color(ACENTO)
    return m


class ReglaDeTresDirecta(Scene):
    def construct(self):
        cab = titulo(self, "Regla de tres directa")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Reducción a la unidad")
        enunciado(self, "3 cuadernos cuestan 6 €. ¿Cuánto cuestan 5 cuadernos?")
        notas("Primero: ¿cuánto cuesta UN cuaderno?")
        unidad(self, ["1 cuaderno  →  6 : 3 = 2 €", "5 cuadernos  →  5 · 2 = 10 €"], x=-3.8, y=0.6)
        notas("5 cuadernos cuestan 10 €", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("La regla de tres")
        enunciado(self, "3 cuadernos cuestan 6 €. ¿Cuánto cuestan 5 cuadernos?")
        cabs, filas, fl, tipo = esquema("cuadernos", "€", ("3", "6"), ("5", "x"), -4.0, 1.4)
        notas("Colocamos los datos: cada magnitud en su columna, la x donde está lo que buscamos")
        self.play(FadeIn(cabs), FadeIn(filas[0]))
        self.play(FadeIn(filas[1]))
        self.wait(1)
        notas("¿Más cuadernos → más euros? Sí: DIRECTA, las flechas van en el mismo sentido")
        self.play(GrowArrow(fl[0]), GrowArrow(fl[1]))
        self.play(FadeIn(tipo, scale=1.3))
        self.wait(1.5)
        cruz = Line(filas[0][1].get_center(), filas[1][0].get_center(), buff=0.3, color=M2, stroke_width=5)
        notas("En la directa se multiplica EN CRUZ (6 · 5) y se divide entre el que queda (3)")
        self.play(Create(cruz))
        m = x_igual("\\dfrac{6\\cdot 5}{3}", "10").move_to([2.4, 0.5, 0])
        self.play(Write(m[:3]))
        self.wait(1)
        self.play(Write(m[3:]))
        self.play(Circumscribe(m[4], color=ACENTO))
        notas("¡10 €, igual que antes! Usa el método que te resulte más cómodo", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Otro ejemplo")
        enunciado(self, "4 kg de naranjas cuestan 6 €. ¿Cuánto cuestan 10 kg?")
        cabs, filas, fl, tipo = esquema("kg", "€", ("4", "6"), ("10", "x"), -4.0, 1.4)
        self.play(FadeIn(cabs), FadeIn(filas), GrowArrow(fl[0]), GrowArrow(fl[1]), FadeIn(tipo))
        cruz = Line(filas[0][1].get_center(), filas[1][0].get_center(), buff=0.3, color=M2, stroke_width=5)
        self.play(Create(cruz))
        m = x_igual("\\dfrac{6\\cdot 10}{4}", "15").move_to([2.4, 1.0, 0])
        self.play(Write(m))
        u = texto("Por la unidad: 1 kg → 6 : 4 = 1,50 €;  10 kg → 15 €", 26, GREY_B).move_to([1.2, -1.15, 0])
        self.play(FadeIn(u))
        notas("10 kg cuestan 15 €. Aquí la unidad sale con decimales: la regla de tres va más directa", color=OK)
        self.wait(4)
        notas.fin()


class ReglaDeTresInversa(Scene):
    def construct(self):
        cab = titulo(self, "Regla de tres inversa")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Reducción a la unidad")
        enunciado(self, "4 grifos llenan una piscina en 6 horas. ¿Cuánto tardan 3 grifos?")
        notas("Primero: ¿cuánto tardaría UN grifo solo?")
        unidad(self, ["1 grifo  →  6 · 4 = 24 horas", "3 grifos  →  24 : 3 = 8 horas"], x=-3.8, y=0.6)
        notas("Un grifo solo tarda 4 veces más (24 h); con 3 grifos, la tercera parte: 8 horas", color=OK)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("La regla de tres")
        enunciado(self, "4 grifos llenan una piscina en 6 horas. ¿Cuánto tardan 3 grifos?")
        cabs, filas, fl, tipo = esquema("grifos", "horas", ("4", "6"), ("3", "x"), -4.0, 1.4, inversa=True)
        self.play(FadeIn(cabs), FadeIn(filas[0]))
        self.play(FadeIn(filas[1]))
        notas("Menos grifos → ¿menos horas? ¡No! MÁS horas: INVERSA, flechas en sentido contrario")
        self.play(GrowArrow(fl[0]))
        self.play(GrowArrow(fl[1]))
        self.play(FadeIn(tipo, scale=1.3))
        self.wait(2)
        linea = SurroundingRectangle(filas[0], color=M2, buff=0.15, corner_radius=0.12, stroke_width=4)
        notas("En la inversa se multiplica EN LÍNEA (4 · 6) y se divide entre el que queda (3)")
        self.play(Create(linea))
        m = x_igual("\\dfrac{4\\cdot 6}{3}", "8").move_to([2.4, 0.5, 0])
        self.play(Write(m[:3]))
        self.wait(1)
        self.play(Write(m[3:]))
        self.play(Circumscribe(m[4], color=ACENTO))
        notas("3 grifos tardan 8 horas. En la inversa, grifos · horas no cambia: 4 · 6 = 3 · 8 = 24", color=OK)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("¿Directa o inversa?")
        pasos_t = VGroup(texto("Antes de calcular, pregúntate:", 30),
                         texto("si una magnitud AUMENTA, ¿qué hace la otra?", 30),
                         texto("Aumenta también  →  DIRECTA:  en cruz", 28, OK),
                         texto("Disminuye  →  INVERSA:  en línea", 28, ROSA),
                         texto("¡Y comprueba que el resultado tiene sentido!", 28, ACENTO))
        pasos_t.arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        card = tarjeta(pasos_t, buff=0.4).move_to([0, 0.1, 0])
        self.play(Create(card[0]))
        for m in pasos_t:
            self.play(FadeIn(m, shift=RIGHT * 0.2))
            self.wait(1.2)
        notas("Con 3 grifos tardo más que con 4: 8 h > 6 h. ¡Tiene sentido!")
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
class Porcentajes(Scene):
    def construct(self):
        cab = titulo(self, "Porcentajes")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("¿Qué es un porcentaje?")
        cg = cuadricula100([-3.4, -0.2, 0])
        self.play(LaggedStart(*[FadeIn(q) for q in cg], lag_ratio=0.01))
        notas("100 cuadraditos. Pintamos 35...")
        self.play(LaggedStart(*[cg[k].animate.set_fill(PCT) for k in range(35)], lag_ratio=0.03))
        r = VGroup(MathTex("35\\,\\%", font_size=80, color=PCT), texto("35 de cada 100", 28),
                   MathTex("=\\dfrac{35}{100}", font_size=56), MathTex("=0{,}35", font_size=56))
        r.arrange(DOWN, buff=0.35).move_to([2.8, -0.1, 0])
        for m in r:
            self.play(FadeIn(m, shift=LEFT * 0.2))
            self.wait(0.6)
        notas("Un porcentaje es una fracción con denominador 100 (y también un decimal)")
        self.wait(3)
        self.play(FadeOut(r))
        casos = [(lambda k: k % 10 < 5, "50\\,\\%=\\dfrac{1}{2}", "la mitad"),
                 (lambda k: k % 10 < 5 and k // 10 < 5, "25\\,\\%=\\dfrac{1}{4}", "la cuarta parte"),
                 (lambda k: k % 10 == 0, "10\\,\\%=\\dfrac{1}{10}", "la décima parte"),
                 (lambda k: True, "100\\,\\%", "¡todo!")]
        notas("Algunos porcentajes que conviene saber de memoria")
        prev = None
        for cond, tex, txt in casos:
            m = VGroup(MathTex(tex, font_size=60, color=PCT), texto(txt, 30)).arrange(DOWN, buff=0.3).move_to([2.8, 0, 0])
            anims = [cg[k].animate.set_fill(PCT if cond(k) else VACIO) for k in range(100)]
            self.play(*anims, *([FadeOut(prev)] if prev else []), run_time=0.9)
            self.play(FadeIn(m))
            self.wait(1.8)
            prev = m
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("El 30 % de 80")
        enunciado(self, "Calcula el 30 % de 80", y=2.4, size=32)
        cg = cuadricula100([-3.6, 0.0, 0], s=0.28)
        tt = texto("Todo = 80", 30).next_to(cg, UP, buff=0.15)
        self.play(LaggedStart(*[FadeIn(q) for q in cg], lag_ratio=0.01), FadeIn(tt))
        notas("Repartimos 80 en 100 trozos iguales")
        p1 = MathTex("80:100=0{,}8", font_size=48).move_to([2.6, 1.0, 0])
        p1b = texto("cada cuadradito vale 0,8", 28).next_to(p1, DOWN, buff=0.25)
        self.play(Write(p1))
        self.play(FadeIn(p1b))
        self.wait(1.5)
        notas("El 30 % son 30 cuadraditos")
        self.play(LaggedStart(*[cg[k].animate.set_fill(PCT) for k in range(30)], lag_ratio=0.03))
        p2 = MathTex("30\\cdot 0{,}8=24", font_size=56, color=PCT).move_to([2.6, -1.0, 0])
        self.play(Write(p2))
        notas("30 cuadraditos de 0,8 suman 24", color=OK)
        self.wait(3)
        notas.fin()
        self.play(FadeOut(VGroup(cg, tt, p1, p1b, p2)))
        f1 = MathTex("1)\\ \\text{Repartiendo:}\\quad 80:100=0{,}8\\ \\rightarrow\\ 30\\cdot 0{,}8=24",
                     font_size=40).move_to([-6.3, 1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(f1))
        self.wait(1.5)
        f2 = MathTex("2)\\ \\text{Con la fracción:}\\quad \\dfrac{30}{100}\\cdot 80=\\dfrac{2400}{100}=24",
                     font_size=40).move_to([-6.3, -0.1, 0], aligned_edge=LEFT)
        self.play(Write(f2))
        self.wait(1.5)
        f3 = MathTex("3)\\ \\text{Con el decimal:}\\quad 0{,}30\\cdot 80=24", font_size=40)
        f3.move_to([-6.3, -1.4, 0], aligned_edge=LEFT)
        self.play(Write(f3))
        notas("Tres caminos, el mismo resultado: el 30 % de 80 es 24", color=OK)
        self.wait(3.5)
        notas.fin()


class AumentosDescuentos(Scene):
    def construct(self):
        cab = titulo(self, "Rebajas y subidas", "Porcentajes")
        notas = Notas(self)
        sub = Sub(self, cab)
        U = 0.12                           # ancho por euro

        sub("Una rebaja")
        enunciado(self, "Unas zapatillas cuestan 60 € y tienen un 20 % de descuento")
        x0, y = -4.6, 1.1
        azul = barra(x0, y, 48 * U, color=M1, opacidad=0.6)
        rojo = barra(x0 + 48 * U, y, 12 * U, color=M1, opacidad=0.6)
        t60 = eur("60", 36).next_to(VGroup(azul, rojo), UP, buff=0.12)
        self.play(GrowFromEdge(VGroup(azul, rojo), LEFT), FadeIn(t60))
        notas("En dos pasos. 1.º: ¿cuánto es el 20 % de 60?")
        p1 = eur("20\\,\\%\\ \\text{de}\\ 60=0{,}20\\cdot 60=12", 42).move_to([-0.5, -0.2, 0])
        p1[0][0][:3].set_color(PCT)
        t12 = eur("12", 30, MAL).next_to(rojo, DOWN, buff=0.12)
        self.play(Write(p1), rojo.animate.set_fill(MAL, 0.85), FadeIn(t12))
        self.wait(1.5)
        notas("2.º: se lo quitamos al precio")
        self.play(FadeOut(VGroup(rojo, t12), shift=RIGHT * 0.6))
        p2 = eur("60-12=48", 46, ACENTO).move_to([-0.5, -1.1, 0])
        self.play(Write(p2))
        t48 = eur("48", 36, ACENTO).next_to(azul, DOWN, buff=0.12)
        self.play(FadeIn(t48))
        self.wait(2)
        notas("Ahora, otra forma más directa: ¡en un solo paso!", color=OK)
        self.play(VGroup(p1, p2).animate.set_opacity(0.35))
        self.wait(1.5)
        notas("Miremos la barra entera: 60 € es el 100 %")
        rojo2 = barra(x0 + 48 * U, y, 12 * U, color=MAL, opacidad=0.35)
        l100 = texto("100 %", 26).next_to(VGroup(azul, rojo2), RIGHT, buff=0.2)
        self.play(FadeIn(rojo2), FadeIn(l100))
        l20 = texto("20 %", 24, MAL).move_to(rojo2)
        self.play(FadeIn(l20))
        notas("Quitamos el 20 %... lo que queda es el 80 %")
        l80 = texto("80 %", 30, ACENTO).move_to(azul)
        self.play(rojo2.animate.set_fill(opacity=0.1), l20.animate.set_opacity(0.4), FadeIn(l80, scale=1.3))
        self.play(Indicate(azul, color=ACENTO))
        self.wait(1)
        notas("En un paso: si me descuentan el 20 %, pago el 80 % (100 − 20)")
        p3 = eur("0{,}80\\cdot 60=48", 46, ACENTO).move_to([-0.5, -2.0, 0])
        self.play(Write(p3))
        self.play(Circumscribe(p3, color=ACENTO))
        notas("Pago 48 €", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Una subida")
        enunciado(self, "Un libro de 50 € sube un 10 %")
        total = barra(x0, y, 50 * U, color=M1, opacidad=0.6)
        t50 = eur("50", 36).next_to(total, UP, buff=0.12)
        self.play(GrowFromEdge(total, LEFT), FadeIn(t50))
        notas("1.º: el 10 % de 50 es 5 € (dividir entre 10)")
        p1 = eur("10\\,\\%\\ \\text{de}\\ 50=5", 42).move_to([-0.5, -0.2, 0])
        p1[0][0][:3].set_color(PCT)
        verde = barra(x0 + 50 * U, y, 5 * U, color=PCT, opacidad=0.85)
        t5 = eur("+5", 30, PCT).next_to(verde, DOWN, buff=0.12)
        t10 = texto("+10 %", 24, PCT).next_to(verde, DOWN, buff=0.12)
        self.play(GrowFromEdge(verde, LEFT), FadeIn(t10))
        self.wait(1)
        self.play(Write(p1))
        self.wait(0.5)
        self.play(ReplacementTransform(t10, t5))
        self.wait(1.5)
        notas("2.º: se lo sumamos al precio")
        p2 = eur("50+5=55", 46, ACENTO).move_to([-0.5, -1.1, 0])
        self.play(Write(p2))
        self.wait(1.5)
        notas("Ahora, otra forma más directa: ¡en un solo paso!", color=OK)
        self.play(VGroup(p1, p2).animate.set_opacity(0.35))
        self.wait(1.5)
        notas("La barra azul es el 100 %; le añadimos un 10 %")
        l100 = texto("100 %", 30).move_to(total)
        self.play(FadeIn(l100))
        self.wait(1)
        caja = SurroundingRectangle(VGroup(total, verde), color=ACENTO, buff=0.08)
        l110 = texto("110 %", 30, ACENTO).next_to(caja, RIGHT, buff=0.2)
        notas("Ahora el precio es la barra entera: el 110 %")
        self.play(Create(caja), FadeIn(l110))
        self.wait(1.5)
        notas("En un paso: ahora cuesta el 110 % del precio (100 + 10)")
        p3 = eur("1{,}10\\cdot 50=55", 46, ACENTO).move_to([-0.5, -2.0, 0])
        self.play(Write(p3))
        self.play(Circumscribe(p3, color=ACENTO))
        notas("Ahora cuesta 55 €", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Resumen")
        a = VGroup(texto("DESCUENTO del 20 %", 28, MAL), texto("pago el 80 %", 26), MathTex("0{,}80\\cdot\\text{precio}", font_size=44))
        b = VGroup(texto("SUBIDA del 10 %", 28, PCT), texto("pago el 110 %", 26), MathTex("1{,}10\\cdot\\text{precio}", font_size=44))
        a.arrange(DOWN, buff=0.35)
        b.arrange(DOWN, buff=0.35)
        ta = tarjeta(a, color=MAL, buff=0.4).move_to([-3.2, 0.2, 0])
        tb = tarjeta(b, color=PCT, buff=0.4).move_to([3.2, 0.2, 0])
        tb[0].stretch_to_fit_height(ta[0].height).move_to([3.2, 0.2, 0])
        self.play(Create(ta[0]), FadeIn(a))
        self.play(Create(tb[0]), FadeIn(b))
        notas("Con un descuento pagas menos del 100 %; con una subida, más del 100 %")
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
class Escalas(Scene):
    def construct(self):
        cab = titulo(self, "Escalas", "Mapas y planos")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Un mapa")
        mapa = RoundedRectangle(width=7.4, height=3.6, corner_radius=0.2, stroke_color=GREY_B,
                                fill_color="#2b3a2e", fill_opacity=0.9).move_to([-2.3, 0.3, 0])
        self.play(FadeIn(mapa))
        a = Dot([-5.0, -0.4, 0], color=ACENTO, radius=0.12)
        b = Dot([0.0, -0.4, 0], color=ACENTO, radius=0.12)
        la = texto("Pueblo A", 24).next_to(a, UP, buff=0.15)
        lb = texto("Pueblo B", 24).next_to(b, UP, buff=0.15)
        self.play(FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb))
        esc = MathTex("\\text{Escala } 1:100\\,000", font_size=40, color=ACENTO).move_to([3.9, 1.6, 0])
        self.play(Write(esc))
        notas("La escala dice cuántas veces es más grande la realidad que el mapa")
        self.wait(2)
        sig = VGroup(MathTex("1\\ \\text{cm del mapa}", font_size=34, color=M1),
                     MathTex("\\downarrow", font_size=34),
                     MathTex("100\\,000\\ \\text{cm reales}", font_size=34, color=M2),
                     MathTex("=1\\ \\text{km}", font_size=34, color=M2),
                     texto("1 km en la realidad", 30, ACENTO)).arrange(DOWN, buff=0.15).move_to([3.9, 0.0, 0])
        self.play(FadeIn(sig, shift=DOWN * 0.2))
        notas("1 cm en el mapa son 100 000 cm en la realidad: 1 km")
        self.wait(2.5)
        regla = VGroup(Line(a.get_center() + DOWN * 0.5, b.get_center() + DOWN * 0.5, color=WHITE, stroke_width=4))
        for k in range(6):
            p = a.get_center() + DOWN * 0.5 + RIGHT * k
            regla.add(Line(p + UP * 0.12, p + DOWN * 0.12, color=WHITE, stroke_width=3))
            regla.add(MathTex(str(k), font_size=24).next_to(p, DOWN, buff=0.18))
        notas("Medimos con la regla: entre A y B hay 5 cm")
        self.play(Create(regla))
        self.wait(1)
        m = MathTex("5\\ \\text{cm}\\ \\to\\ 5\\cdot 100\\,000=500\\,000\\ \\text{cm}=5\\ \\text{km}", font_size=40)
        m.move_to([-0.3, -2.3, 0])
        self.play(Write(m))
        notas("En la realidad están a 5 km. ¡Es una proporcionalidad directa!", color=OK)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Un plano")
        enunciado(self, "En el plano de una casa a escala 1 : 50, la cocina mide 8 cm de largo")
        plano = Rectangle(width=4.0, height=2.4, stroke_color=WHITE, stroke_width=3).move_to([-3.5, 0.0, 0])
        lc = texto("cocina", 26).move_to(plano)
        cota = DoubleArrow(plano.get_corner(DL) + DOWN * 0.35, plano.get_corner(DR) + DOWN * 0.35, buff=0,
                           color=M1, stroke_width=3, tip_length=0.15)
        tc = MathTex("8\\ \\text{cm}", font_size=34, color=M1).next_to(cota, DOWN, buff=0.1)
        self.play(Create(plano), FadeIn(lc), GrowFromCenter(cota), FadeIn(tc))
        preg = texto("¿Cuánto mide de largo en la realidad?", 30, ACENTO).move_to([0, 1.75, 0])
        self.play(FadeIn(preg))
        self.wait(1)
        notas("1 : 50 → cada centímetro del plano son 50 cm de verdad")
        pasos = VGroup(MathTex("8\\ \\text{cm del plano}\\cdot 50=400\\ \\text{cm reales}", font_size=38),
                       MathTex("400\\ \\text{cm}=4\\ \\text{m}", font_size=44),
                       texto("¡La cocina mide 4 m!", 34, ACENTO)).arrange(DOWN, buff=0.5)
        if pasos.width > 6.6:
            pasos.scale_to_fit_width(6.6)
        pasos.move_to([2.6, -0.1, 0])
        self.play(Write(pasos[0]))
        self.wait(1)
        self.play(Write(pasos[1]))
        self.wait(1)
        self.play(FadeIn(pasos[2], scale=1.2))
        notas("La cocina mide 4 m de largo", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("La escala gráfica")
        barra_e = VGroup(*[Rectangle(width=1.5, height=0.3, stroke_color=WHITE, stroke_width=2,
                                     fill_color=WHITE if k % 2 == 0 else FONDO, fill_opacity=1) for k in range(4)])
        barra_e.arrange(RIGHT, buff=0).move_to([0, 0.8, 0])
        nums = VGroup(*[MathTex(f"{2 * k}", font_size=30).next_to(barra_e.get_left() + RIGHT * 1.5 * k, DOWN, buff=0.25)
                        for k in range(5)])
        km = texto("km", 26).next_to(nums[-1], RIGHT, buff=0.2)
        self.play(FadeIn(barra_e), FadeIn(nums), FadeIn(km))
        notas("Muchos mapas traen una barra: cada trozo de la barra son 2 km")
        self.wait(2)
        self.play(FadeOut(VGroup(barra_e, nums, km)))

        # Un mapa inventado: una isla con dos pueblos y la barra en la esquina
        mar = RoundedRectangle(corner_radius=0.15, width=9.6, height=5.0, stroke_color=GREY_B, stroke_width=3,
                               fill_color="#1f4e6e", fill_opacity=1).move_to([0, 0.15, 0])
        pts = [[-4.0, 0.9], [-3.2, 2.1], [-1.6, 2.3], [-0.2, 1.9], [1.3, 2.2], [2.4, 1.3],
               [1.9, 0.2], [0.6, -0.5], [-1.0, -0.2], [-2.6, -0.6], [-3.8, -0.1]]
        isla = VMobject(stroke_color="#c9b57a", stroke_width=3, fill_color="#3d6b3a", fill_opacity=1)
        isla.set_points_smoothly([[x, y, 0] for x, y in pts + [pts[0]]])
        A, B = np.array([-2.6, 0.6, 0]), np.array([0.4, 0.6, 0])
        pueblos = VGroup(Dot(A, radius=0.1, color=ACENTO), Dot(B, radius=0.1, color=ACENTO),
                         texto("Villarriba", 22).next_to(A, UP, buff=0.12),
                         texto("Puertoazul", 22).next_to(B, UP, buff=0.12))
        bm = VGroup(*[Rectangle(width=1.0, height=0.2, stroke_color=WHITE, stroke_width=2,
                                fill_color=WHITE if k % 2 == 0 else FONDO, fill_opacity=1) for k in range(4)])
        bm.arrange(RIGHT, buff=0).move_to([2.0, -1.55, 0])
        bn = VGroup(*[MathTex(f"{2 * k}", font_size=24).next_to(bm.get_left() + RIGHT * k, DOWN, buff=0.15)
                      for k in range(5)])
        bk = texto("km", 20).next_to(bn[-1], RIGHT, buff=0.12)
        mapa = VGroup(mar, isla, pueblos, bm, bn, bk)
        self.play(FadeIn(mar), DrawBorderThenFill(isla), run_time=1.5)
        self.play(FadeIn(pueblos), FadeIn(VGroup(bm, bn, bk)))
        notas("Un mapa: ¿a qué distancia están Villarriba y Puertoazul?")
        self.wait(1.5)
        tira = Line(A, B, color=M2, stroke_width=6)
        self.play(Create(tira))
        notas("Copiamos la distancia (con una regla o un papel) y la llevamos a la barra")
        self.play(tira.animate.move_to(bm.get_left() + RIGHT * 1.5 + UP * 0.3), run_time=1.5)
        marcas = VGroup(*[DashedLine(bm.get_left() + RIGHT * k + UP * 0.45, bm.get_left() + RIGHT * k + DOWN * 0.1,
                                     color=M2, stroke_width=2) for k in (0, 3)])
        self.play(Create(marcas), Indicate(bn[3], color=M2, scale_factor=1.6))
        notas("Llega justo hasta el 6: están a 6 km", color=OK)
        self.wait(3)
        notas.fin()
        self.play(VGroup(mapa, tira, marcas).animate.scale(0.62).move_to([0, 0.75, 0]))
        expl = texto("Mides en el mapa, lo comparas con la barra... ¡y no hace falta hacer cuentas!\n"
                     "Además, si amplías o reduces el mapa, la barra cambia con él.", 26)
        caja = tarjeta(expl, color=ACENTO, buff=0.3).move_to([0, -2.4, 0])
        self.play(FadeIn(caja))
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios
def enunciados_1():
    return [
        ("1. En un equipo de 15 jugadores, 9 son chicas.",
         "a) Escribe la razón entre chicas y chicos.      b) ¿Qué fracción del equipo son chicas?"),
        ("2. ¿Forman proporción?", lista(["3/4 y 9/12", "2/5 y 6/14", "4/10 y 6/15"], 3)),
        ("3. Calcula el término que falta:", lista(["2/3 = 8/x", "x/5 = 12/20", "4/x = 6/9"], 3)),
        ("4. ¿Directa o inversa? Completa la tabla:",
         "a)  1, 2, 4, ?   →   5, 10, ?, 40            b)  2, 4, 8, ?   →   20, 10, ?, 4"),
    ]


def enunciados_2():
    return [
        ("5. 4 entradas de cine cuestan 26 €. ¿Cuánto cuestan 7 entradas?", ""),
        ("6. Si 6 amigos pagan 8 € cada uno por un regalo, ¿cuánto pagaría cada uno si fueran 4?", ""),
        ("7. Calcula:", lista(["25 % de 80", "10 % de 350", "15 % de 60"], 3)),
        ("8. Rebajas y subidas:",
         "a) Una camiseta de 25 € tiene un 20 % de descuento. ¿Cuánto pago?\n"
         "b) Una bicicleta de 200 € sube un 5 %. ¿Cuánto cuesta ahora?"),
    ]


PROP = [("\\dfrac{3}{4}\\ \\ \\mathrm{y}\\ \\ \\dfrac{9}{12}", "3\\cdot 12=36,\\quad 4\\cdot 9=36", True, "Sí: 36 = 36"),
        ("\\dfrac{2}{5}\\ \\ \\mathrm{y}\\ \\ \\dfrac{6}{14}", "2\\cdot 14=28,\\quad 5\\cdot 6=30", False, "No: 28 ≠ 30"),
        ("\\dfrac{4}{10}\\ \\ \\mathrm{y}\\ \\ \\dfrac{6}{15}", "4\\cdot 15=60,\\quad 10\\cdot 6=60", True, "Sí: 60 = 60")]
CUARTO = [("\\dfrac{2}{3}=\\dfrac{8}{x}", "x=\\dfrac{3\\cdot 8}{2}=\\dfrac{24}{2}=12"),
          ("\\dfrac{x}{5}=\\dfrac{12}{20}", "x=\\dfrac{5\\cdot 12}{20}=\\dfrac{60}{20}=3"),
          ("\\dfrac{4}{x}=\\dfrac{6}{9}", "x=\\dfrac{4\\cdot 9}{6}=\\dfrac{36}{6}=6")]
TABLAS = [
    ([["1", "2", "4", "?"], ["5", "10", "?", "40"]], False, "\\dfrac{5}{1}=\\dfrac{10}{2}=5",
     "El cociente no cambia: DIRECTA", [(1, 2, "20", "4\\cdot 5=20"), (0, 3, "8", "40:5=8")]),
    ([["2", "4", "8", "?"], ["20", "10", "?", "4"]], True, "2\\cdot 20=4\\cdot 10=40",
     "El producto no cambia: INVERSA", [(1, 2, "5", "40:8=5"), (0, 3, "10", "40:4=10")]),
]
PCT_EJ = {
    "7a": ("25\\,\\%\\ \\mathrm{de}\\ 80", "\\dfrac{1}{4}\\ \\mathrm{de}\\ 80=80:4=20", "25 % es la cuarta parte"),
    "7b": ("10\\,\\%\\ \\mathrm{de}\\ 350", "350:10=35", "10 %: dividir entre 10"),
    "7c": ("15\\,\\%\\ \\mathrm{de}\\ 60", "0{,}15\\cdot 60=9", "15 % = 0,15"),
    "8a": ("25\\cdot 0{,}80", "=20", "20 % de descuento: pago el 80 %"),
    "8b": ("200\\cdot 1{,}05", "=210", "Sube un 5 %: pago el 105 %"),
}


def ej_razon(scene, notas, apartado, ejemplo=False):
    if apartado == "a":
        g = VGroup(texto("a)", 28), MathTex("\\text{chicos}=15-9=6", font_size=44)).arrange(RIGHT, buff=0.3)
        g.move_to([-1.0, 1.4, 0])
        if ejemplo:
            notas("Primero: ¿cuántos chicos hay? 15 − 9 = 6")
        scene.play(FadeIn(g))
        r = VGroup(MathTex("\\dfrac{\\text{chicas}}{\\text{chicos}}=", font_size=44), frac(9, 6, CHICA, CHICO, 52),
                   MathTex("=", font_size=48), frac(3, 2, CHICA, CHICO, 52)).arrange(RIGHT, buff=0.2)
        r.next_to(g, DOWN, buff=0.6).align_to(g, LEFT).shift(RIGHT * 0.6)
        scene.play(Write(r))
        if ejemplo:
            notas("Por cada 3 chicas hay 2 chicos", color=OK)
        scene.wait(2)
        return VGroup(g, r)
    r = VGroup(texto("b)", 28), MathTex("\\dfrac{\\text{chicas}}{\\text{total}}=", font_size=44),
               frac(9, 15, CHICA, WHITE, 52), MathTex("=", font_size=48), frac(3, 5, CHICA, WHITE, 52)).arrange(RIGHT, buff=0.2)
    r.move_to([-0.6, -1.0, 0])
    scene.play(Write(r))
    notas("La fracción compara con el TOTAL: 3/5 del equipo son chicas", color=OK)
    scene.wait(2)
    return r


def ej_prop(scene, i, x, y, notas, ejemplo=False):
    enun, prod, ok, ver = PROP[i]
    g = cuenta(scene, X(enun, 44), [(prod, "Multiplicamos en cruz" if ejemplo else None)], x, y, notas,
               f"{'abc'[i]})", ejemplo, 40, dy=1.0)
    v = texto(ver, 28, OK if ok else MAL).next_to(g[-1], DOWN, buff=0.3).align_to(g[-1], LEFT)
    scene.play(FadeIn(v))
    scene.wait(1.2 if ejemplo else 0.6)
    return VGroup(g, v)


def ej_cuarto(scene, i, x, y, notas, ejemplo=False):
    enun, paso = CUARTO[i]
    nota = "Multiplicamos en cruz los que conocemos y dividimos entre el que queda" if ejemplo else None
    return cuenta(scene, X(enun, 48), [(paso, nota)], x, y, notas, f"{'abc'[i]})", ejemplo, 46, dy=1.3)


def ej_tabla(scene, i, notas, ejemplo=False):
    filas, inv, tex, txt, rellenos = TABLAS[i]
    marco, labs, cel, _ = tabla_h(["A", "B"], filas, 0, 1.4, w=1.2, wn=1.2)
    et = texto(f"{'ab'[i]})", 30).next_to(marco, LEFT, buff=0.4)
    scene.play(FadeIn(et), Create(marco), FadeIn(labs), *[FadeIn(c) for c in cel[0] + cel[1]])
    if ejemplo:
        notas("Miramos las columnas completas: ¿se mantiene el cociente o el producto?")
        scene.wait(1.5)
    c = MathTex(tex, font_size=44).move_to([0, -0.3, 0])
    scene.play(Write(c))
    t = texto(txt, 28, ROSA if inv else OK).next_to(c, DOWN, buff=0.25)
    scene.play(FadeIn(t))
    scene.wait(1.2)
    for k, (r, col, v, calc) in enumerate(rellenos):
        m = MathTex(calc, font_size=40, color=ACENTO).move_to([-2.6 + k * 5.2, -1.9, 0])
        scene.play(Write(m))
        nv = MathTex(v, font_size=40, color=ACENTO).move_to(cel[r][col])
        scene.play(Transform(cel[r][col], nv), Flash(nv, color=ACENTO))
        scene.wait(0.6)
    scene.wait(1.5)


def ej_regla(scene, notas, enun, nombres, f1, f2, inversa, calculo, unidad_txt, fin, ejemplo=False):
    t = texto(enun, 28).move_to([0, 2.4, 0])
    if t.width > 13:
        t.scale_to_fit_width(13)
    scene.play(FadeIn(t))
    cabs, filas, fl, tipo = esquema(nombres[0], nombres[1], f1, f2, -4.3, 1.4, inversa=inversa)
    scene.play(FadeIn(cabs), FadeIn(filas))
    if ejemplo:
        notas("Más entradas → más dinero: DIRECTA" if not inversa else "Menos amigos → más paga cada uno: INVERSA")
    scene.play(GrowArrow(fl[0]), GrowArrow(fl[1]))
    scene.play(FadeIn(tipo, scale=1.3))
    if inversa:
        marca = SurroundingRectangle(filas[0], color=M2, buff=0.15, corner_radius=0.12, stroke_width=4)
    else:
        marca = Line(filas[0][1].get_center(), filas[1][0].get_center(), buff=0.3, color=M2, stroke_width=5)
    scene.play(Create(marca))
    m = x_igual(*calculo, size=52).move_to([2.2, 0.9, 0])
    scene.play(Write(m))
    scene.play(Circumscribe(m[4], color=ACENTO))
    u = texto(unidad_txt, 26, GREY_B).move_to([1.3, -1.55, 0])
    scene.play(FadeIn(u))
    notas(fin, color=OK)
    scene.wait(3)
    notas.fin()


def ej_5(scene, notas, ejemplo=False):
    ej_regla(scene, notas, "4 entradas de cine cuestan 26 €. ¿Cuánto cuestan 7 entradas?", ("entradas", "€"),
             ("4", "26"), ("7", "x"), False, ("\\dfrac{26\\cdot 7}{4}", "45{,}50"),
             "Por la unidad: 1 entrada → 26 : 4 = 6,50 €;  7 · 6,50 = 45,50 €", "7 entradas cuestan 45,50 €", ejemplo)


def ej_6(scene, notas, ejemplo=False):
    ej_regla(scene, notas, "Si 6 amigos pagan 8 € cada uno por un regalo, ¿cuánto pagaría cada uno si fueran 4?",
             ("amigos", "€ cada uno"), ("6", "8"), ("4", "x"), True, ("\\dfrac{6\\cdot 8}{4}", "12"),
             "El regalo cuesta 6 · 8 = 48 €;  entre 4: 48 : 4 = 12 €", "Cada uno pagaría 12 €", ejemplo)


def ej_pct(scene, clave, x, y, notas, ejemplo=False, size=46):
    enun, paso, frase = PCT_EJ[clave]
    g = VGroup()
    f = texto(frase, 26, GREY_B).move_to([x, y + 0.75, 0], aligned_edge=LEFT)
    scene.play(FadeIn(f))
    g.add(f)
    if "\\text" in paso:               # X() pinta la «x» de \text y rompe el LaTeX: aquí no hay incógnita
        paso = MathTex(paso, font_size=size)
    g.add(cuenta(scene, X(enun, size), [(paso, None)], x, y, notas, f"{clave[1]})", ejemplo, size, dy=1.0))
    scene.wait(0.8)
    return g


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Proporcionalidad")
        notas = Notas(self)
        from t03_lenguaje_algebraico import pagina_enunciados
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        intro = texto("Resolvemos un apartado de cada tipo", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        ej_razon(self, notas, "a", ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        ej_prop(self, 0, -2.4, 1.2, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        ej_cuarto(self, 0, -2.4, 1.3, notas, ejemplo=True)
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 a)")
        ej_tabla(self, 0, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5")
        ej_5(self, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        ej_pct(self, "7a", -2.6, 1.0, notas, ejemplo=True, size=52)
        notas("El 25 % de 80 es 20", color=OK)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 4")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1 b)")
        ej_razon(self, notas, "b")
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2: b) y c)")
        ej_prop(self, 1, -5.8, 1.2, notas)
        ej_prop(self, 2, 0.9, 1.2, notas)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3: b) y c)")
        ej_cuarto(self, 1, -6.0, 1.5, notas)
        ej_cuarto(self, 2, 0.6, 1.5, notas)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 b)")
        ej_tabla(self, 1, notas)
        limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 5 a 8.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 5 a 8")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 6")
        ej_6(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7: b) y c)")
        ej_pct(self, "7b", -5.8, 1.2, notas, size=42)
        ej_pct(self, "7c", 0.9, 1.2, notas, size=42)
        notas("b) 35      c) 9", color=OK)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 8")
        ej_pct(self, "8a", -5.8, 1.2, notas, size=42)
        ej_pct(self, "8b", 0.9, 1.2, notas, size=42)
        notas("a) Pago 20 €      b) Ahora cuesta 210 €", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)


# Comprobaciones de los resultados (si algo no cuadra, falla al importar)
assert 26 * 7 / 4 == 45.5 and 6 * 8 / 4 == 12 and 3 * 8 / 2 == 12 and 5 * 12 / 20 == 3 and 4 * 9 / 6 == 6
assert 3 * 12 == 4 * 9 and 2 * 14 != 5 * 6 and 4 * 15 == 10 * 6
assert round(0.15 * 60, 6) == 9 and round(25 * 0.8, 6) == 20 and round(200 * 1.05, 6) == 210
