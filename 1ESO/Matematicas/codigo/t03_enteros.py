"""Tema 3 · Números enteros (1º ESO)

Escenas:
    NegativosVidaReal    – termómetro, ascensor y dinero
    RectaEnteros         – el termómetro tumbado: la recta de los enteros
    OpuestoValorAbsoluto – opuesto (espejo en el 0) y valor absoluto (distancia al 0)
    OrdenarEnteros       – más a la derecha = mayor; comparar y ordenar

Renderizar (desde esta carpeta):
    python -m manim -pql t03_enteros.py RectaEnteros
    python publicar.py t03_enteros.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 3 · Números enteros"
TITULOS = {
    "NegativosVidaReal": "¿Para qué sirven los negativos?",
    "RectaEnteros": "La recta de los números enteros",
    "OpuestoValorAbsoluto": "Opuesto y valor absoluto",
    "OrdenarEnteros": "Comparar y ordenar enteros",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

MERCURIO = "#E74C3C"


def tex_entero(n, mas=True, size=40):
    s = "0" if n == 0 else (f"+{n}" if mas else str(n)) if n > 0 else str(n)
    return MathTex(s, font_size=size, color=color_entero(n))


def recta_enteros(a=-6, b=6, largo=12.0, y=0.0, size=32):
    """NumberLine con etiquetas coloreadas. Devuelve (VGroup(linea, etiquetas), linea)."""
    linea = NumberLine(x_range=[a, b, 1], length=largo, include_tip=False, stroke_width=3,
                       tick_size=0.1).move_to([0, y, 0])
    etiquetas = VGroup(*[tex_entero(n, mas=False, size=size).next_to(linea.n2p(n), DOWN, buff=0.22)
                         for n in range(a, b + 1)])
    return VGroup(linea, etiquetas), linea


def saltar(scene, punto, linea, desde, hasta, rt=0.25, alto=0.25):
    paso = 1 if hasta > desde else -1
    for k in range(desde, hasta, paso):
        a, b = linea.n2p(k) + UP * alto, linea.n2p(k + paso) + UP * alto
        arco = ArcBetweenPoints(a, b, angle=-PI / 1.5 * paso)
        scene.play(MoveAlongPath(punto, arco), run_time=rt, rate_func=linear)


# ---------------------------------------------------------------------------
class NegativosVidaReal(Scene):
    def construct(self):
        cab = titulo(self, "Números enteros", "¿Para qué sirven los negativos?")
        self.termometro()
        self.ascensor()
        self.dinero()
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not cab])

        c1 = texto("Los números negativos indican cantidades\npor debajo del cero.", 36)
        c2 = VGroup(texto("Se escriben con el signo", 34),
                    texto(MENOS, 48, NEGATIVO, weight=BOLD),
                    texto(":", 34),
                    texto(f"{MENOS}3 °C,  {MENOS}2,  {MENOS}10 €", 34, NEGATIVO)).arrange(RIGHT, buff=0.2)
        VGroup(c1, c2).arrange(DOWN, buff=0.8)
        self.play(Write(c1))
        self.play(FadeIn(c2, shift=UP * 0.2))
        self.wait(2.5)

    # -- Panel 1
    def termometro(self):
        cx, tmin, tmax, alto = -4.8, -20, 30, 4.0
        tit = texto("Temperatura", 28, ACENTO).move_to([cx, 2.5, 0])
        escala = Line([cx, -2.0, 0], [cx, -2.0 + alto, 0])

        def y(t):
            return escala.point_from_proportion((t - tmin) / (tmax - tmin))[1]

        tubo = RoundedRectangle(width=0.45, height=alto + 0.5, corner_radius=0.22,
                                stroke_color=WHITE).move_to([cx, -2.0 + alto / 2, 0])
        bulbo = Circle(radius=0.38, color=WHITE, fill_color=MERCURIO, fill_opacity=1).move_to([cx, -2.55, 0])
        marcas = VGroup()
        for t in range(tmin, tmax + 1, 5):  # marca cada 5 °C, número cada 10 °C
            principal = t % 10 == 0
            m = Line([cx - 0.22, y(t), 0], [cx - (0.42 if principal else 0.32), y(t), 0],
                     stroke_width=2.5 if principal else 1.5)
            marcas.add(m)
            if principal:
                marcas.add(Text(fmt_entero(t, mas=False), font_size=20, color=color_entero(t))
                           .next_to(m, LEFT, buff=0.08))
        cero = DashedLine([cx - 0.9, y(0), 0], [cx + 0.9, y(0), 0], color=GREY_B)

        temp = ValueTracker(25)
        mercurio = always_redraw(lambda: Rectangle(
            width=0.2, height=max(0.01, y(temp.get_value()) + 2.3), fill_color=MERCURIO, fill_opacity=1,
            stroke_width=0).move_to([cx, (y(temp.get_value()) - 2.3) / 2, 0]))
        lectura = always_redraw(lambda: Text(
            f"{fmt_entero(round(temp.get_value()))} °C", font_size=30,
            color=color_entero(round(temp.get_value()))).move_to([cx + 1.2, y(temp.get_value()), 0]))

        self.play(FadeIn(tit), Create(tubo), FadeIn(bulbo), FadeIn(marcas), Create(cero))
        self.add(mercurio, lectura)
        cap = texto("Hace calor: +25 °C", 22).move_to([cx, -3.3, 0])
        self.play(FadeIn(cap))
        self.wait(0.6)
        for t, frase in ((0, "Cero grados: 0 °C"), (-3, f"3 grados bajo cero: {MENOS}3 °C")):
            nueva = texto(frase, 22, color_entero(t) if t else WHITE).move_to(cap)
            self.play(temp.animate.set_value(t), Transform(cap, nueva), run_time=1.8)
            self.wait(0.6)
        self.remove(mercurio, lectura)
        self.add(mercurio.copy().clear_updaters(), lectura.copy().clear_updaters())

    # -- Panel 2
    def ascensor(self):
        cx, y0, h = 0.0, -2.2, 0.62
        tit = texto("Ascensor", 28, ACENTO).move_to([cx, 2.5, 0])
        plantas = VGroup()
        for f in range(-2, 4):
            r = Rectangle(width=1.8, height=h, stroke_color=GREY_B, stroke_width=2,
                          fill_color="#6B4F3A" if f < 0 else GREY_D, fill_opacity=0.5 if f < 0 else 0.25)
            r.move_to([cx, y0 + (f + 2) * h + h / 2, 0])
            lab = tex_entero(f, size=30).next_to(r, LEFT, buff=0.15)
            plantas.add(VGroup(r, lab))
        suelo_y = y0 + 2 * h
        calle = Line([cx - 1.3, suelo_y, 0], [cx + 1.3, suelo_y, 0], color=GREEN, stroke_width=6)
        calle_t = texto("calle", 18, GREEN).next_to(calle, RIGHT, buff=0.1)
        self.play(FadeIn(tit), LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in plantas], lag_ratio=0.1),
                  Create(calle), FadeIn(calle_t))

        def centro(f):
            return [cx + 0.35, y0 + (f + 2) * h + h / 2, 0]

        cabina = Rectangle(width=0.5, height=0.45, fill_color=ACENTO, fill_opacity=0.9, stroke_width=0)
        cabina.move_to(centro(3))
        cap = texto("Planta 3  →  +3", 22, POSITIVO).move_to([cx, -3.3, 0])
        self.play(FadeIn(cabina), FadeIn(cap))
        self.wait(0.5)
        for f, frase in ((0, "Planta baja  →  0"), (-2, f"2.º sótano  →  {MENOS}2")):
            nueva = texto(frase, 22, color_entero(f) if f else WHITE).move_to(cap)
            self.play(cabina.animate.move_to(centro(f)), Transform(cap, nueva), run_time=1.5)
            self.wait(0.6)

    # -- Panel 3
    def dinero(self):
        cx, base, k = 4.7, -0.6, 0.075
        tit = texto("Dinero", 28, ACENTO).move_to([cx, 2.5, 0])
        eje = Line([cx - 1.2, base, 0], [cx + 1.2, base, 0], stroke_width=3)
        cero = texto("0 €", 20).next_to(eje, RIGHT, buff=0.1)
        saldo = ValueTracker(0)

        def barra():
            v = saldo.get_value()
            return Rectangle(width=0.8, height=max(0.01, abs(v) * k), stroke_width=0,
                             fill_color=POSITIVO if v >= 0 else NEGATIVO, fill_opacity=0.85
                             ).move_to([cx, base + v * k / 2, 0])

        b = always_redraw(barra)
        lab = always_redraw(lambda: Text(f"{fmt_entero(round(saldo.get_value()))} €", font_size=26,
                                         color=color_entero(round(saldo.get_value())))
                            .move_to([cx - 1.0, base + saldo.get_value() * k, 0]))
        self.play(FadeIn(tit), Create(eje), FadeIn(cero))
        self.add(b, lab)
        cap = texto("Tienes 20 €", 22, POSITIVO).move_to([cx, -3.3, 0])
        self.play(saldo.animate.set_value(20), FadeIn(cap), run_time=1.2)
        self.wait(0.5)
        nueva = texto("Gastas 30 €...", 22).move_to(cap)
        self.play(Transform(cap, nueva))
        self.play(saldo.animate.set_value(-10), run_time=2)
        nueva = texto(f"Debes 10 €: saldo {MENOS}10 €", 22, NEGATIVO).move_to(cap)
        self.play(Transform(cap, nueva))
        self.wait(1.5)
        self.remove(b, lab)
        self.add(b.copy().clear_updaters(), lab.copy().clear_updaters())


# ---------------------------------------------------------------------------
class RectaEnteros(Scene):
    def construct(self):
        cab = titulo(self, "La recta de los enteros")

        grupo, linea = recta_enteros(-6, 6, y=-0.2)
        idea = texto("Si «tumbamos» el termómetro...", 30, GREY_B).next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        vertical = linea.copy().rotate(PI / 2).scale(0.45)
        self.play(FadeIn(idea), Create(vertical))
        self.play(Transform(vertical, linea), run_time=1.5)
        self.remove(vertical)
        self.add(linea)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in grupo[1]], lag_ratio=0.05))

        cero = Dot(linea.n2p(0), radius=0.1)
        origen = texto("origen", 22).next_to(linea.n2p(0), UP, buff=0.3)
        self.play(FadeIn(cero, scale=2), FadeIn(origen))

        pos = Line(linea.n2p(0), linea.n2p(6), color=POSITIVO, stroke_width=8)
        neg = Line(linea.n2p(0), linea.n2p(-6), color=NEGATIVO, stroke_width=8)
        tpos = texto("POSITIVOS →", 28, POSITIVO).next_to(pos, UP, buff=0.6)
        tneg = texto("← NEGATIVOS", 28, NEGATIVO).next_to(neg, UP, buff=0.6)
        self.play(Create(pos), FadeIn(tpos))
        self.play(Create(neg), FadeIn(tneg))
        nota0 = texto("El 0 no es positivo ni negativo", 24, GREY_B).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(nota0))
        self.wait(1.2)
        self.play(FadeOut(VGroup(pos, neg, tpos, tneg, origen, nota0, idea)))

        # Representar puntos
        for n in (4, -3):
            p = Dot(linea.n2p(0) + UP * 0.25, radius=0.13, color=color_entero(n))
            self.play(FadeIn(p, scale=2), run_time=0.3)
            saltar(self, p, linea, 0, n)
            self.play(p.animate.move_to(linea.n2p(n)), run_time=0.3)
            lab = tex_entero(n, size=44).next_to(p, UP, buff=0.3)
            self.play(Write(lab), Flash(p, color=color_entero(n)))
            self.wait(0.4)

        # Definición
        partes = [r"\mathbb{Z} = \{\, \dots,"]
        valores = [-3, -2, -1, 0, 1, 2, 3]
        for v in valores:
            partes.append("0" if v == 0 else (f"+{v}" if v > 0 else str(v)))
            partes.append(",")
        partes.append(r"\dots \,\}")
        z = MathTex(*partes, font_size=48).to_edge(DOWN, buff=1.3)
        for i, v in enumerate(valores):
            z[1 + 2 * i].set_color(color_entero(v))
        self.play(Write(z), run_time=2)
        nat = texto("Los enteros positivos son los números naturales de siempre: 1, 2, 3...", 24, GREY_B)
        nat.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(nat))
        self.wait(3)


# ---------------------------------------------------------------------------
class OpuestoValorAbsoluto(Scene):
    def construct(self):
        cab = titulo(self, "Opuesto y valor absoluto")
        grupo, linea = recta_enteros(-6, 6, y=-0.6)
        self.play(Create(linea), FadeIn(grupo[1]))

        # --- Opuesto
        sub = texto("El opuesto: el «reflejo» en el 0", 30, ACENTO).next_to(cab, DOWN, buff=0.35).to_edge(LEFT)
        espejo = DashedLine(linea.n2p(0) + DOWN * 0.15, linea.n2p(0) + UP * 1.7, color=GREY_B)
        self.play(FadeIn(sub), Create(espejo))

        for n in (4, 2):
            a = Dot(linea.n2p(n), radius=0.13, color=POSITIVO)
            la = tex_entero(n, size=40).next_to(a, UP, buff=0.25)
            self.play(FadeIn(a, scale=2), Write(la))
            b = a.copy()
            arco = ArcBetweenPoints(linea.n2p(n), linea.n2p(-n), angle=PI / 2)
            self.play(MoveAlongPath(b, arco),
                      UpdateFromAlphaFunc(b, lambda m, t: m.set_color(interpolate_color(
                          ManimColor(POSITIVO), ManimColor(NEGATIVO), t))), run_time=1.3)
            lb = tex_entero(-n, size=40).next_to(b, UP, buff=0.25)
            self.play(Write(lb))
            dist = VGroup(
                BraceBetweenPoints(linea.n2p(-n), linea.n2p(0), DOWN).shift(DOWN * 0.45),
                BraceBetweenPoints(linea.n2p(0), linea.n2p(n), DOWN).shift(DOWN * 0.45),
            )
            dl = VGroup(*[texto(str(n), 22, GREY_B).next_to(d, DOWN, buff=0.08) for d in dist])
            frase = MathTex(r"\text{Opuesto de }", f"+{n}", r"\text{ es }", f"-{n}", font_size=44)
            frase[1].set_color(POSITIVO)
            frase[3].set_color(NEGATIVO)
            frase.move_to([0, 2.0, 0])
            self.play(GrowFromCenter(dist), FadeIn(dl), Write(frase))
            self.wait(1)
            if n == 4:
                self.play(FadeOut(VGroup(a, b, la, lb, dist, dl, frase)))
        misma = texto("Están a la misma distancia del 0, pero en lados contrarios.", 26).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(misma))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (cab, linea, grupo[1])])

        # --- Valor absoluto
        sub = texto("El valor absoluto: la distancia al 0", 30, ACENTO).next_to(cab, DOWN, buff=0.35).to_edge(LEFT)
        self.play(FadeIn(sub))
        for n, y in ((-5, 1.0), (3, 1.0)):
            p = Dot(linea.n2p(n), radius=0.13, color=color_entero(n))
            tramo = Line(linea.n2p(0), linea.n2p(n), color=ACENTO, stroke_width=8)
            br = BraceBetweenPoints(*sorted([linea.n2p(0), linea.n2p(n)], key=lambda v: v[0]), UP)
            br.shift(UP * 0.15)
            pasos = texto(f"{abs(n)} unidades", 22, ACENTO).next_to(br, UP, buff=0.08)
            self.play(FadeIn(p, scale=2))
            self.play(Create(tramo), GrowFromCenter(br), FadeIn(pasos))
            s = f"+{n}" if n > 0 else str(n)
            eq = MathTex(r"|", s, r"| =", str(abs(n)), font_size=52)
            eq[1].set_color(color_entero(n))
            eq[3].set_color(ACENTO)
            eq.move_to([-4.8 if n < 0 else 4.8, y + 0.4, 0])
            self.play(Write(eq))
            self.wait(1)
            self.play(FadeOut(VGroup(tramo, br, pasos, p)))
        cero = MathTex(r"|0| = 0", font_size=52).move_to([0, 1.4, 0])
        self.play(Write(cero))
        regla = texto("El valor absoluto nunca es negativo: es una distancia.", 28, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(Write(regla))
        self.wait(3)


# ---------------------------------------------------------------------------
class OrdenarEnteros(Scene):
    def construct(self):
        cab = titulo(self, "Comparar y ordenar")
        grupo, linea = recta_enteros(-6, 6, y=-0.8)
        self.play(Create(linea), FadeIn(grupo[1]))

        menor = texto("← menor", 28, NEGATIVO).next_to(linea, UP, buff=1.0).to_edge(LEFT, buff=0.6)
        mayor = texto("mayor →", 28, POSITIVO).next_to(linea, UP, buff=1.0).to_edge(RIGHT, buff=0.6)
        regla = texto("En la recta, el que está más a la DERECHA es MAYOR", 28, ACENTO)
        regla.next_to(cab, DOWN, buff=0.4).set_x(0)
        self.play(Write(regla))
        self.play(FadeIn(menor, shift=LEFT * 0.3), FadeIn(mayor, shift=RIGHT * 0.3))
        self.wait(0.8)

        # Comparaciones
        for a, b, extra in ((2, -5, None), (-1, -4, "¡Aunque 4 > 1!  −1 °C hace menos frío que −4 °C")):
            da = Dot(linea.n2p(a), radius=0.13, color=color_entero(a))
            db = Dot(linea.n2p(b), radius=0.13, color=color_entero(b))
            la = tex_entero(a, size=40).next_to(da, UP, buff=0.25)
            lb = tex_entero(b, size=40).next_to(db, UP, buff=0.25)
            self.play(FadeIn(da, scale=2), FadeIn(db, scale=2), Write(la), Write(lb))
            flecha = CurvedArrow(linea.n2p(b) + UP * 0.9, linea.n2p(a) + UP * 0.9, angle=-PI / 3, color=ACENTO)
            self.play(Create(flecha))
            sa = f"+{a}" if a > 0 else str(a)
            res = MathTex(sa, ">", str(b), font_size=60).move_to([0, 1.6, 0])
            res[0].set_color(color_entero(a))
            res[2].set_color(color_entero(b))
            self.play(Write(res))
            nota = None
            if extra:
                nota = texto(extra, 26, GREY_B).to_edge(DOWN, buff=0.4)
                self.play(FadeIn(nota))
            self.wait(1.8)
            self.play(FadeOut(VGroup(da, db, la, lb, flecha, res, *([nota] if nota else []))))

        # Ordenar una lista
        self.play(FadeOut(regla))
        enun = texto("Ordena de menor a mayor:", 30, ACENTO).next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        nums = [3, -2, 0, -5, 1, -1]
        fichas = VGroup(*[tex_entero(n, mas=False, size=48) for n in nums]).arrange(RIGHT, buff=0.9)
        fichas.next_to(enun, DOWN, buff=0.4).set_x(0)
        self.play(FadeIn(enun), LaggedStart(*[FadeIn(f, shift=DOWN * 0.2) for f in fichas], lag_ratio=0.15))
        self.wait(0.6)

        puntos = VGroup()
        for n, f in zip(nums, fichas):
            d = Dot(linea.n2p(n), radius=0.12, color=color_entero(n))
            self.play(f.animate.next_to(linea.n2p(n), UP, buff=0.4), FadeIn(d, scale=2), run_time=0.7)
            puntos.add(d)
        self.wait(0.8)

        orden = sorted(nums)
        partes = []
        for i, n in enumerate(orden):
            if i:
                partes.append("<")
            partes.append(str(n))
        fila = MathTex(*partes, font_size=56).to_edge(DOWN, buff=0.5)
        for i, n in enumerate(orden):
            fila[2 * i].set_color(color_entero(n))
        anims = [TransformFromCopy(fichas[nums.index(n)], fila[2 * i]) for i, n in enumerate(orden)]
        self.play(LaggedStart(*anims, lag_ratio=0.2), run_time=2)
        self.play(LaggedStart(*[FadeIn(fila[2 * i + 1]) for i in range(len(orden) - 1)], lag_ratio=0.1))
        self.play(Circumscribe(fila, color=ACENTO))
        truco = texto("Truco: ordenar de menor a mayor = leer la recta de izquierda a derecha", 24, GREY_B)
        truco.next_to(fila, UP, buff=0.35)
        self.play(FadeIn(truco))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
EXPRESA = [  # (frase, palabra clave, solución)
    ("5 grados bajo cero", "bajo cero", -5),
    ("Planta 4", "Planta", 4),
    ("Una deuda de 20 €", "deuda", -20),
    ("Bucear a 10 m de profundidad", "profundidad", -10),
    ("Ganar 15 €", "Ganar", 15),
    ("Tercer sótano", "sótano", -3),
]
REPRESENTA = [-4, 2, 0, -1, 5]
OPUESTOS = [-7, 3, -12, 0, 9]
COMPARA = [(-3, 1), (-6, -2), (0, -5), (-10, -1), (4, -8)]
ORDENA_MENOR = [4, -3, 0, -7, 2, -1]
ORDENA_MAYOR = [-5, 6, -2, 1, -9, 3]
CIUDADES = [("Madrid", 2), ("Moscú", -15), ("Valencia", 12), ("Oslo", -6), ("Teruel", -3)]


def s_ent(n, mas=True):
    """Cadena LaTeX de un entero."""
    s = "0" if n == 0 else (f"+{n}" if mas else str(n)) if n > 0 else str(n)
    return "{" + s + "}"  # llaves: signo pegado al número (no como resta)


def lista_txt(nums, mas=True):
    return ",  ".join(fmt_entero(n, mas) for n in nums)


def apartado(scene, cab, cadena):
    t = texto(cadena, 30, ACENTO).next_to(cab, RIGHT, buff=0.6)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def pagina_enunciados(scene, cab, bloques):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 28, ACENTO), texto(cuerpo, 24))
        b.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(cab, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.35)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


ENUNCIADOS_1 = [
    ("1. Expresa con un número entero:",
     "a) 5 grados bajo cero    b) Planta 4    c) Una deuda de 20 €\n"
     "d) Bucear a 10 m de profundidad    e) Ganar 15 €    f) Tercer sótano"),
    ("2. Representa en la recta:", lista_txt(REPRESENTA)),
    ("3. Escribe el opuesto y el valor absoluto de:", lista_txt(OPUESTOS)),
]
ENUNCIADOS_2 = [
    ("4. Escribe < o > entre cada pareja:",
     "    ".join(f"{l}) {fmt_entero(a)}  ?  {fmt_entero(b)}" for l, (a, b) in zip("abcde", COMPARA))),
    ("5. Ordena:",
     f"a) De menor a mayor:  {lista_txt(ORDENA_MENOR, False)}\n"
     f"b) De mayor a menor:  {lista_txt(ORDENA_MAYOR, False)}"),
    ("6. Temperaturas de un día de invierno:",
     ",  ".join(f"{c} {fmt_entero(t, False)} °C" for c, t in CIUDADES) + "\n"
     "¿Cuál es la ciudad más fría? ¿Y la más cálida?\nOrdénalas de más fría a más cálida."),
]


# --- 1. Expresa
def resolver_expresa(scene, items, letras, ejemplo=False):
    filas = VGroup()
    for i, ((frase, clave, n), letra) in enumerate(zip(items, letras)):
        y = 1.9 - i * 0.85
        t = Text(f"{letra})  {frase}", font_size=32, t2c={clave: color_entero(n)})
        t.move_to([-6.0, y, 0], aligned_edge=LEFT)
        flecha = Arrow([2.2, y, 0], [3.2, y, 0], buff=0, color=GREY_B)
        num = tex_entero(n, size=48).move_to([4.1, y, 0])
        scene.play(Write(t), run_time=0.9)
        scene.play(GrowArrow(flecha), Write(num), run_time=0.7)
        filas.add(t, flecha, num)
    if ejemplo:
        n = items[0][2]
        ex = texto(f"«{items[0][1]}» = por debajo del 0  →  número negativo", 28, color_entero(n))
        ex.to_edge(DOWN, buff=1.2)
        scene.play(FadeIn(ex))
    else:
        ex = texto("Por debajo del 0 (bajo cero, deuda, profundidad, sótano) → negativo\n"
                   "Por encima del 0 (planta, ganar) → positivo", 24, GREY_B).to_edge(DOWN, buff=0.4)
        scene.play(FadeIn(ex))
    scene.wait(2.5)


# --- 2. Representa
def resolver_representa(scene, nums, ejemplo=False):
    grupo, linea = recta_enteros(-6, 6, y=-0.5)
    scene.play(Create(linea), FadeIn(grupo[1]))
    for n in nums:
        p = Dot(linea.n2p(0) + UP * 0.25, radius=0.13, color=color_entero(n))
        scene.play(FadeIn(p, scale=2), run_time=0.3)
        if ejemplo and n:
            saltar(scene, p, linea, 0, n, rt=0.3)
            nota = texto(f"Desde el 0, {abs(n)} pasos hacia la {'derecha' if n > 0 else 'izquierda'}",
                         28, color_entero(n)).to_edge(DOWN, buff=1.0)
            scene.play(FadeIn(nota))
        elif n:
            arco = ArcBetweenPoints(linea.n2p(0) + UP * 0.25, linea.n2p(n) + UP * 0.25,
                                    angle=-PI / 2 if n > 0 else PI / 2)
            scene.play(MoveAlongPath(p, arco), run_time=0.8)
        scene.play(p.animate.move_to(linea.n2p(n)), run_time=0.25)
        lab = tex_entero(n, size=44).next_to(p, UP, buff=0.3)
        scene.play(Write(lab), Flash(p, color=color_entero(n)), run_time=0.6)
    scene.wait(2.5)


# --- 3. Opuesto y valor absoluto
def resolver_opuestos(scene, nums):
    xs = [-3.5, 0.3, 4.2]
    cab = VGroup(*[texto(t, 28, ACENTO).move_to([x, 2.0, 0])
                   for t, x in zip(("Número", "Opuesto", "Valor absoluto"), xs)])
    raya = Line([-5.5, 1.65, 0], [6.0, 1.65, 0], color=GREY_B)
    scene.play(FadeIn(cab), Create(raya))
    for i, n in enumerate(nums):
        y = 1.1 - i * 0.7
        a = tex_entero(n, size=44).move_to([xs[0], y, 0])
        b = tex_entero(-n, size=44).move_to([xs[1], y, 0])
        c = MathTex("|", s_ent(n), "| =", str(abs(n)), font_size=44).move_to([xs[2], y, 0])
        c[1].set_color(color_entero(n))
        c[3].set_color(ACENTO)
        scene.play(Write(a), run_time=0.5)
        scene.play(TransformFromCopy(a, b), run_time=0.7)
        scene.play(Write(c), run_time=0.8)
    reglas = texto("Opuesto: cambiamos el signo  ·  Valor absoluto: quitamos el signo", 26, GREY_B)
    reglas.to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(reglas))
    scene.wait(2.5)


# --- 4. Compara
def resolver_compara(scene, pares, letras, ejemplo=False):
    grupo, linea = recta_enteros(-11, 5, largo=12.8, y=-1.4, size=26)
    scene.play(Create(linea), FadeIn(grupo[1]))
    n = len(pares)
    slots = [np.array([(-4.8 + 3.2 * i) if n > 1 else 0, 1.9, 0]) for i in range(n)]
    for (a, b), letra, slot in zip(pares, letras, slots):
        da = Dot(linea.n2p(a), radius=0.12, color=color_entero(a))
        db = Dot(linea.n2p(b), radius=0.12, color=color_entero(b))
        la = tex_entero(a, size=36).next_to(da, UP, buff=0.25)
        lb = tex_entero(b, size=36).next_to(db, UP, buff=0.25)
        expr = MathTex(rf"\text{{{letra})}}\;", s_ent(a), r"\;\square\;", s_ent(b), font_size=52).move_to([0, 0.6, 0])
        expr[1].set_color(color_entero(a))
        expr[3].set_color(color_entero(b))
        scene.play(Write(expr), FadeIn(da, scale=2), FadeIn(db, scale=2), Write(la), Write(lb), run_time=1)
        simbolo = MathTex(">" if a > b else "<", font_size=52, color=ACENTO).move_to(expr[2])
        anims = [Transform(expr[2], simbolo), Indicate(da if a > b else db, scale_factor=1.8)]
        nota = None
        if ejemplo:
            mayor = a if a > b else b
            nota = texto(f"{fmt_entero(mayor)} está más a la derecha → es el mayor", 26, ACENTO)
            nota.to_edge(DOWN, buff=0.3)
            anims.append(FadeIn(nota))
        scene.play(*anims, run_time=1)
        scene.wait(1.2)
        scene.play(FadeOut(VGroup(da, db, la, lb, *([nota] if nota else []))),
                   expr.animate.scale(0.85).move_to(slot), run_time=0.8)
    scene.wait(2)


# --- 5. Ordena
def resolver_ordena(scene, nums, creciente, letra):
    grupo, linea = recta_enteros(-10, 7, largo=12.8, y=-0.9, size=26)
    modo = "De menor a mayor" if creciente else "De mayor a menor"
    enun = texto(f"{letra}) {modo}:", 30).move_to([-4.5, 2.2, 0])
    fichas = VGroup(*[tex_entero(n, mas=False, size=46) for n in nums]).arrange(RIGHT, buff=0.7)
    fichas.next_to(enun, RIGHT, buff=0.6)
    scene.play(Create(linea), FadeIn(grupo[1]), FadeIn(enun),
               LaggedStart(*[FadeIn(f, shift=DOWN * 0.2) for f in fichas], lag_ratio=0.1))
    for n, f in zip(nums, fichas):
        d = Dot(linea.n2p(n), radius=0.11, color=color_entero(n))
        scene.play(f.animate.next_to(linea.n2p(n), UP, buff=0.35), FadeIn(d, scale=2), run_time=0.6)
    orden = sorted(nums, reverse=not creciente)
    signo = "<" if creciente else ">"
    partes = []
    for i, n in enumerate(orden):
        if i:
            partes.append(signo)
        partes.append(str(n))
    fila = MathTex(*partes, font_size=54).to_edge(DOWN, buff=0.5)
    for i, n in enumerate(orden):
        fila[2 * i].set_color(color_entero(n))
    lectura = texto("Leemos la recta de " + ("izquierda a derecha →" if creciente else "← derecha a izquierda"),
                    26, GREY_B).next_to(fila, UP, buff=0.35)
    scene.play(FadeIn(lectura))
    scene.play(LaggedStart(*[TransformFromCopy(fichas[nums.index(n)], fila[2 * i]) for i, n in enumerate(orden)],
                           lag_ratio=0.2), run_time=2)
    scene.play(LaggedStart(*[FadeIn(fila[2 * i + 1]) for i in range(len(orden) - 1)], lag_ratio=0.1))
    scene.play(Circumscribe(fila, color=ACENTO))
    scene.wait(2.5)


# --- 6. Ciudades
def mini_termo(nombre, t, x, tmin=-20, tmax=20, alto=2.8, y0=-1.3):
    def y(v):
        return y0 + (v - tmin) / (tmax - tmin) * alto
    tubo = RoundedRectangle(width=0.36, height=alto + 0.3, corner_radius=0.18, stroke_color=WHITE)
    tubo.move_to([x, y0 + alto / 2, 0])
    bulbo = Circle(radius=0.28, color=WHITE, fill_color=MERCURIO, fill_opacity=1).move_to([x, y0 - 0.25, 0])
    base = y0 - 0.15
    merc = Rectangle(width=0.15, height=y(t) - base, fill_color=MERCURIO, fill_opacity=1, stroke_width=0)
    merc.move_to([x, (y(t) + base) / 2, 0])
    cero = DashedLine([x - 0.35, y(0), 0], [x + 0.35, y(0), 0], color=GREY_B, stroke_width=1.5)
    lab = Text(f"{fmt_entero(t, False)} °C", font_size=26, color=color_entero(t)).next_to(tubo, UP, buff=0.15)
    nom = Text(nombre, font_size=24).next_to(bulbo, DOWN, buff=0.15)
    g = VGroup(tubo, merc, bulbo, cero, lab, nom)
    g.temp = t
    return g


def resolver_ciudades(scene):
    xs = [-5.2, -2.6, 0, 2.6, 5.2]
    termos = [mini_termo(c, t, x) for (c, t), x in zip(CIUDADES, xs)]
    scene.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in termos], lag_ratio=0.15))
    scene.wait(1)

    fria = min(termos, key=lambda g: g.temp)
    calida = max(termos, key=lambda g: g.temp)
    for g, txt, col in ((fria, "La más fría", NEGATIVO), (calida, "La más cálida", POSITIVO)):
        caja = SurroundingRectangle(g, color=col, buff=0.12)
        t = texto(txt, 24, col).next_to(caja, UP, buff=0.1)
        scene.play(Create(caja), FadeIn(t))
        scene.wait(0.8)
        scene.play(FadeOut(caja), FadeOut(t))

    orden = sorted(termos, key=lambda g: g.temp)
    scene.play(*[g.animate.shift(RIGHT * (x - g[0].get_x())) for g, x in zip(orden, xs)], run_time=1.8)
    nombres = "  <  ".join(g[5].text for g in orden)
    fila1 = texto(nombres, 28).to_edge(DOWN, buff=1.0)
    partes = []
    for i, g in enumerate(orden):
        if i:
            partes.append("<")
        partes.append(str(g.temp))
    fila2 = MathTex(*partes, font_size=46).to_edge(DOWN, buff=0.3)
    for i, g in enumerate(orden):
        fila2[2 * i].set_color(color_entero(g.temp))
    scene.play(Write(fila1))
    scene.play(Write(fila2))
    scene.wait(3)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Números enteros")
        pagina_enunciados(self, cab, ENUNCIADOS_1)
        pagina_enunciados(self, cab, ENUNCIADOS_2)

        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        sub = apartado(self, cab, "Ejercicio 1 a)")
        resolver_expresa(self, EXPRESA[:1], "a", ejemplo=True)
        limpiar(self, cab)
        sub = apartado(self, cab, f"Ejercicio 2: representa {fmt_entero(REPRESENTA[0])}")
        resolver_representa(self, REPRESENTA[:1], ejemplo=True)
        limpiar(self, cab)
        sub = apartado(self, cab, f"Ejercicio 3: {fmt_entero(OPUESTOS[0])}")
        resolver_opuestos(self, OPUESTOS[:1])
        limpiar(self, cab)
        sub = apartado(self, cab, "Ejercicio 4 a)")
        resolver_compara(self, COMPARA[:1], "a", ejemplo=True)
        limpiar(self, cab)
        sub = apartado(self, cab, "Ejercicio 5 a)")
        resolver_ordena(self, ORDENA_MENOR, True, "a")
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Números enteros")

        apartado(self, cab, "Ejercicio 1: b) a f)")
        resolver_expresa(self, EXPRESA[1:], "bcdef")
        limpiar(self, cab)
        apartado(self, cab, "Ejercicio 2")
        resolver_representa(self, REPRESENTA[1:])
        limpiar(self, cab)
        apartado(self, cab, "Ejercicio 3")
        resolver_opuestos(self, OPUESTOS[1:])
        limpiar(self, cab)
        apartado(self, cab, "Ejercicio 4: b) a e)")
        resolver_compara(self, COMPARA[1:], "bcde")
        limpiar(self, cab)
        apartado(self, cab, "Ejercicio 5 b)")
        resolver_ordena(self, ORDENA_MAYOR, False, "b")
        limpiar(self, cab)
        apartado(self, cab, "Ejercicio 6")
        resolver_ciudades(self)
        limpiar(self, cab)

        fin = texto("¡Muy bien! Ya dominas los números enteros.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
