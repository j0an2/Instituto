"""Tema 7 · Operaciones con fracciones (1º ESO)

Escenas:
    SumaRestaMismoDenominador     – juntar/quitar trozos iguales; error típico 2/7 + 3/7 ≠ 5/14
    SumaRestaDistintoDenominador  – común denominador con el m.c.m.; simplificar el resultado; entero + fracción
    FraccionDeUnaCantidad         – 3/4 de 20 caramelos; 2/5 de 30 €
    MultiplicarFracciones         – el rectángulo: 2/3 · 4/5 = 8/15
    DividirFracciones             – ¿cuántos octavos caben en 3/4?; la inversa
    EjerciciosEjemplo             – enunciados (2 páginas) + primer apartado de cada ejercicio resuelto
    EjerciciosResueltos           – el resto de apartados

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t07_operaciones_fracciones.py MultiplicarFracciones
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t07_operaciones_fracciones.py
"""
import os
import sys
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 7 · Operaciones con fracciones"
TITULOS = {
    "SumaRestaMismoDenominador": "Sumar y restar con el mismo denominador",
    "SumaRestaDistintoDenominador": "Sumar y restar con distinto denominador",
    "FraccionDeUnaCantidad": "Fracción de una cantidad",
    "MultiplicarFracciones": "Multiplicar fracciones",
    "DividirFracciones": "Dividir fracciones",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

ROSA = "#FF79C6"
AZUL = "#5DADE2"


def mcm(a, b):
    return a * b // gcd(a, b)


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def nota_op(f_ini, f_fin, s, color=ACENTO, size=26):
    """Etiquetas '×k' arriba y abajo entre dos fracciones."""
    g = VGroup()
    for i, lado in ((0, UP), (2, DOWN)):
        p = (f_ini[i].get_right() + f_fin[i].get_left()) / 2
        g.add(MathTex(s, font_size=size, color=color).move_to(p))
    return g


def juntar(scene, origenes, destino, inicio=0, rt=0.35):
    """Mueve copias de los trozos 'origenes' a las casillas de la barra 'destino' a partir de 'inicio'."""
    copias = []
    for k, pieza in enumerate(origenes):
        c = pieza.copy()
        scene.play(c.animate.move_to(destino[inicio + k]), run_time=rt)
        copias.append(c)
    return copias


# ---------------------------------------------------------------------------
class SumaRestaMismoDenominador(Scene):
    def construct(self):
        cab = titulo(self, "Sumar y restar fracciones", "Con el mismo denominador")

        e = cadena((2, 7), "+", (3, 7), "=", size=64).move_to([-0.6, 2.0, 0])
        self.play(Write(e))
        ancho, xb = 7.0, 1.0
        b1 = barra(7, 2, ancho=ancho, alto=0.7).move_to([xb, 0.6, 0])
        b2 = barra(7, 3, ancho=ancho, alto=0.7, color=ROSA).move_to([xb, -0.4, 0])
        br = barra(7, 0, ancho=ancho, alto=0.7).move_to([xb, -1.8, 0])
        l1 = fraccion(2, 7, 40).next_to(b1, LEFT, buff=0.5)
        l2 = fraccion(3, 7, 40).next_to(b2, LEFT, buff=0.5)
        self.play(FadeIn(b1), FadeIn(l1))
        self.play(FadeIn(b2), FadeIn(l2))
        tam = texto("Los trozos son del mismo tamaño (séptimos): solo hay que juntarlos", 24, GREY_B)
        tam.move_to([0, -1.0, 0])
        self.play(FadeIn(tam), FadeIn(br))
        juntar(self, list(b1[:2]), br, 0)
        juntar(self, list(b2[:3]), br, 2)
        res = fraccion(5, 7, 64).next_to(e, RIGHT, buff=0.3)
        lr = fraccion(5, 7, 40).next_to(br, LEFT, buff=0.5)
        self.play(Write(res), FadeIn(lr))
        regla = texto("Se suman los numeradores y se deja el mismo denominador", 28, ACENTO).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(regla), Indicate(VGroup(e[0][0], e[2][0], res[0]), color=NUMERADOR))
        self.wait(2.5)
        limpiar(self, cab)

        # Error típico
        subtitulo(self, cab, "¡Cuidado con este error!")
        mal = cadena((2, 7), "+", (3, 7), r"\neq", (5, 14), size=64).move_to([0, 1.9, 0])
        self.play(Write(mal))
        cruz = Cross(mal[4], stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        b7 = barra(7, 5, ancho=8, alto=0.6).move_to([0.9, 0.2, 0])
        b14 = barra(14, 5, ancho=8, alto=0.6).move_to([0.9, -0.8, 0])
        self.play(FadeIn(b7), FadeIn(fraccion(5, 7, 36).next_to(b7, LEFT, buff=0.4)))
        self.play(FadeIn(b14), FadeIn(fraccion(5, 14, 36).next_to(b14, LEFT, buff=0.4)))
        exp = texto("Los denominadores NO se suman: los trozos siguen siendo séptimos.\n"
                    "5/14 es mucho menos de lo que tenemos.", 26, MAL).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(exp))
        self.wait(3)
        limpiar(self, cab)

        # Resta
        subtitulo(self, cab, "Restar: quitamos trozos")
        e = cadena((5, 8), "-", (2, 8), "=", size=64).move_to([-0.6, 1.8, 0])
        b = barra(8, 5, ancho=8, alto=0.8).move_to([0.6, 0.0, 0])
        self.play(Write(e), FadeIn(b))
        self.play(*[b[i].animate.set_fill(MAL) for i in (3, 4)])
        quita = texto("quitamos 2 octavos", 24, MAL).next_to(VGroup(b[3], b[4]), DOWN, buff=0.25)
        self.play(FadeIn(quita))
        self.play(*[b[i].animate.set_fill(VACIO) for i in (3, 4)], FadeOut(quita))
        res = fraccion(3, 8, 64).next_to(e, RIGHT, buff=0.3)
        self.play(Write(res), Indicate(VGroup(*b[:3]), scale_factor=1.05))
        regla = texto("Se restan los numeradores y se deja el mismo denominador", 28, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(regla))
        self.wait(2.5)


# ---------------------------------------------------------------------------
class SumaRestaDistintoDenominador(Scene):
    def construct(self):
        cab = titulo(self, "Sumar y restar fracciones", "Con distinto denominador")
        self.suma_visual(cab)
        self.resta(cab)
        self.simplificar(cab)
        self.entero(cab)

    def suma_visual(self, cab):
        e = cadena((1, 2), "+", (1, 3), "=", size=60).move_to([-0.8, 2.3, 0])
        self.play(Write(e))
        ancho, xb = 6.0, 1.6
        b1 = barra(2, 1, ancho=ancho, alto=0.65).move_to([xb, 1.1, 0])
        b2 = barra(3, 1, ancho=ancho, alto=0.65, color=ROSA).move_to([xb, 0.2, 0])
        f1 = fraccion(1, 2, 40).move_to([-5.4, 1.1, 0])
        f2 = fraccion(1, 3, 40).move_to([-5.4, 0.2, 0])
        self.play(FadeIn(b1), FadeIn(f1), FadeIn(b2), FadeIn(f2))
        p = texto("Trozos de distinto tamaño: así no los podemos juntar", 24, MAL).move_to([0, -0.6, 0])
        self.play(FadeIn(p))
        self.wait(1)

        paso1 = texto("1.º  m.c.m. de los denominadores:", 24, ACENTO)
        m = MathTex(r"\text{m.c.m.}(2, 3) = 6", font_size=40, color=ACENTO)
        g1 = VGroup(paso1, m).arrange(RIGHT, buff=0.3).move_to([0, -0.6, 0])
        self.play(ReplacementTransform(p, g1))
        self.wait(1)
        paso2 = texto("2.º  Pasamos las dos a sextos (fracciones equivalentes)", 24, ACENTO).move_to(g1)
        self.play(ReplacementTransform(g1, paso2))
        nuevas = []
        for f, b, (n, d), col in ((f1, b1, (1, 2), ACENTO), (f2, b2, (1, 3), ROSA)):
            k = 6 // d
            f_new = fraccion(n * k, 6, 40).move_to(f.get_center() + RIGHT * 2.4)
            ops = nota_op(f, f_new, rf"\times {k}", size=24)
            b_new = barra(6, n * k, ancho=ancho, alto=0.65, color=col).move_to(b)
            self.play(FadeIn(ops), TransformFromCopy(f, f_new), ReplacementTransform(b, b_new), run_time=1.3)
            nuevas.append(b_new)
        b1, b2 = nuevas
        self.wait(0.5)
        paso3 = texto("3.º  Ya son trozos iguales: los juntamos", 24, ACENTO).move_to(paso2)
        self.play(ReplacementTransform(paso2, paso3))
        br = barra(6, 0, ancho=ancho, alto=0.65).move_to([xb, -1.5, 0])
        self.play(FadeIn(br))
        juntar(self, list(b1[:3]), br, 0)
        juntar(self, list(b2[:2]), br, 3)
        res = fraccion(5, 6, 60).next_to(e, RIGHT, buff=0.3)
        self.play(Write(res), FadeIn(fraccion(5, 6, 40).move_to([-3.0, -1.5, 0])))
        cuenta = cadena((1, 2), "+", (1, 3), "=", (3, 6), "+", (2, 6), "=", (5, 6), size=44).to_edge(DOWN, buff=0.3)
        self.play(Write(cuenta))
        self.wait(3)
        limpiar(self, cab)

    def lineas(self, filas, x=-5.8, y0=1.7, dy=1.25, size=56):
        objs = []
        for i, items in enumerate(filas):
            l = cadena(*items, size=size).move_to([x, y0 - i * dy, 0], aligned_edge=LEFT)
            self.play(Write(l), run_time=1.2)
            objs.append(l)
        return objs

    def resta(self, cab):
        subtitulo(self, cab, "Restar: igual, pero quitando")
        filas = self.lineas([[(3, 4), "-", (1, 6)]])
        m = MathTex(r"\text{m.c.m.}(4, 6) = 12", font_size=40, color=ACENTO).move_to([2.8, 1.7, 0])
        self.play(Write(m))
        filas += self.lineas([["=", (9, 12), "-", (2, 12)], ["=", (7, 12)]], y0=0.45)
        n = texto("3/4 = 9/12  (×3)      1/6 = 2/12  (×2)", 22, GREY_B).next_to(filas[1], RIGHT, buff=0.6)
        self.play(FadeIn(n))
        self.play(Circumscribe(filas[2][1], color=ACENTO))
        self.wait(2.5)
        limpiar(self, cab)

    def simplificar(self, cab):
        subtitulo(self, cab, "Al final, simplificamos si se puede")
        filas = self.lineas([[(1, 4), "+", (1, 12)], ["=", (3, 12), "+", (1, 12)], ["=", (4, 12)]], dy=1.15)
        f2 = cadena("=", (1, 3), size=56).next_to(filas[2], RIGHT, buff=0.3)
        mcd = texto("dividimos arriba y abajo\npor el M.C.D.(4, 12) = 4", 24, ACENTO).next_to(f2, RIGHT, buff=0.7)
        self.play(Write(mcd))
        self.play(Write(f2))
        irr = texto("1/3 es irreducible: el resultado se da siempre simplificado", 26, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(irr), Circumscribe(f2[1], color=ACENTO))
        self.wait(2.5)
        limpiar(self, cab)

    def entero(self, cab):
        subtitulo(self, cab, "Un número entero más una fracción")
        e = cadena("2", "+", (1, 3), "=", size=64).move_to([-1.0, 1.5, 0])
        self.play(Write(e))
        bs = VGroup(barra(3, 3, ancho=3, alto=0.7), barra(3, 3, ancho=3, alto=0.7),
                    barra(3, 1, ancho=3, alto=0.7, color=ROSA)).arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        self.play(FadeIn(bs[0]), FadeIn(bs[1]))
        dos = texto("2 unidades = 6 tercios", 26, ACENTO).next_to(VGroup(bs[0], bs[1]), DOWN, buff=0.3)
        self.play(FadeIn(dos))
        self.play(FadeIn(bs[2]), FadeIn(fraccion(1, 3, 36).next_to(bs[2], DOWN, buff=0.3)))
        l = cadena("2", "+", (1, 3), "=", (6, 3), "+", (1, 3), "=", (7, 3), size=52).move_to([0, -1.7, 0])
        self.play(Write(l))
        truco = texto("El entero se escribe con el mismo denominador: 2 = 6/3", 26, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(truco), Write(fraccion(7, 3, 64).next_to(e, RIGHT, buff=0.3)))
        self.wait(3)


# ---------------------------------------------------------------------------
class FraccionDeUnaCantidad(Scene):
    def construct(self):
        cab = titulo(self, "Fracción de una cantidad", "¿Cuánto son 3/4 de 20?")
        caramelos = VGroup(*[Circle(radius=0.17, color=ROSA, fill_color=ROSA, fill_opacity=0.85) for _ in range(20)])
        caramelos.arrange(RIGHT, buff=0.15).move_to([0, 1.6, 0])
        t = texto("Tenemos 20 caramelos", 28).next_to(caramelos, UP, buff=0.3)
        self.play(FadeIn(t), LaggedStart(*[GrowFromCenter(c) for c in caramelos], lag_ratio=0.04))
        self.wait(0.5)

        # Paso 1: repartir en 4 grupos
        grupos = VGroup(*[VGroup(*caramelos[5 * g:5 * g + 5]) for g in range(4)])
        destino = VGroup(*[VGroup(*[c.copy() for c in gr]).arrange(DOWN, buff=0.12) for gr in grupos])
        destino.arrange(RIGHT, buff=1.0).move_to([-2.0, -0.4, 0])
        p1 = texto("1.º  El denominador (4) dice en cuántos grupos iguales repartimos", 24, DENOMINADOR)
        p1.move_to([0, 2.65, 0])
        self.play(FadeOut(t), FadeIn(p1))
        self.play(*[c.animate.move_to(d) for gr, dg in zip(grupos, destino) for c, d in zip(gr, dg)], run_time=1.5)
        cajas = VGroup(*[SurroundingRectangle(gr, color=GREY_B, buff=0.12) for gr in grupos])
        self.play(Create(cajas))
        c1 = MathTex("20 : 4 = 5", font_size=48, color=DENOMINADOR).move_to([4.2, 0.6, 0])
        c1n = texto("caramelos en cada grupo", 22, GREY_B).next_to(c1, DOWN, buff=0.15)
        self.play(Write(c1), FadeIn(c1n))
        self.wait(1)

        # Paso 2: tomar 3 grupos
        p2 = texto("2.º  El numerador (3) dice cuántos grupos tomamos", 24, NUMERADOR).move_to(p1)
        self.play(ReplacementTransform(p1, p2))
        self.play(*[cajas[g].animate.set_stroke(ACENTO, 5) for g in range(3)],
                  *[c.animate.set_fill(ACENTO) .set_stroke(ACENTO) for g in range(3) for c in grupos[g]])
        c2 = MathTex(r"5 \cdot 3 = 15", font_size=48, color=NUMERADOR).move_to([4.2, -0.9, 0])
        self.play(Write(c2))
        res = VGroup(fraccion(3, 4, 56), MathTex(r"\text{de } 20 = 15", font_size=56)).arrange(RIGHT, buff=0.25)
        res.to_edge(DOWN, buff=0.5)
        self.play(Write(res), Circumscribe(res, color=ACENTO))
        regla = texto("Dividimos por el denominador y multiplicamos por el numerador", 26, ACENTO)
        regla.next_to(res, UP, buff=0.3)
        self.play(FadeIn(regla))
        self.wait(3)
        limpiar(self, cab)

        # Dinero
        subtitulo(self, cab, "Otro ejemplo: 2/5 de 30 €")
        b = barra(5, 0, ancho=10, alto=0.9).move_to([0, 0.8, 0])
        llave = Brace(b, UP)
        total = texto("30 €", 30).next_to(llave, UP, buff=0.1)
        self.play(FadeIn(b), GrowFromCenter(llave), FadeIn(total))
        c1 = MathTex(r"30 : 5 = 6", font_size=48, color=DENOMINADOR).move_to([-3.0, -0.8, 0])
        self.play(Write(c1))
        seis = VGroup(*[Text("6 €", font_size=26).move_to(p) for p in b])
        self.play(LaggedStart(*[FadeIn(s) for s in seis], lag_ratio=0.15))
        self.play(*[b[i].animate.set_fill(ACENTO) for i in range(2)], *[seis[i].animate.set_color(BLACK) for i in range(2)])
        c2 = MathTex(r"6 \cdot 2 = 12", font_size=48, color=NUMERADOR).move_to([3.0, -0.8, 0])
        self.play(Write(c2))
        res = VGroup(fraccion(2, 5, 56), Text("de 30 € = 12 €", font_size=40)).arrange(RIGHT, buff=0.25)
        res.to_edge(DOWN, buff=0.6)
        self.play(Write(res), Circumscribe(res, color=ACENTO))
        self.wait(3)


# ---------------------------------------------------------------------------
class MultiplicarFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicar fracciones", "El truco del rectángulo")
        lado, c0 = 4.2, np.array([-3.4, -0.4, 0])
        cuadro = Square(lado, stroke_color=WHITE, fill_color=VACIO, fill_opacity=1).move_to(c0)
        e = cadena((2, 3), r"\cdot", (4, 5), "=", size=64).move_to([3.0, 2.0, 0])
        self.play(Write(e), FadeIn(cuadro))
        izq, arr = cuadro.get_left()[0], cuadro.get_top()[1]

        # 2/3: columnas
        cols = VGroup(*[Line([izq + lado * k / 3, arr, 0], [izq + lado * k / 3, arr - lado, 0], stroke_width=2)
                        for k in (1, 2)])
        f_col = Rectangle(width=lado * 2 / 3, height=lado, stroke_width=0, fill_color=AZUL, fill_opacity=0.45)
        f_col.move_to([izq + lado / 3, c0[1], 0])
        t1 = VGroup(fraccion(2, 3, 36), texto("de las columnas", 24, AZUL)).arrange(RIGHT, buff=0.2)
        t1.next_to(cuadro, UP, buff=0.3)
        self.play(Create(cols), Indicate(e[0], color=AZUL))
        self.play(FadeIn(f_col), FadeIn(t1))
        self.wait(0.6)

        # 4/5: filas
        filas = VGroup(*[Line([izq, arr - lado * k / 5, 0], [izq + lado, arr - lado * k / 5, 0], stroke_width=2)
                         for k in range(1, 5)])
        f_fil = Rectangle(width=lado, height=lado * 4 / 5, stroke_width=0, fill_color=ACENTO, fill_opacity=0.35)
        f_fil.move_to([c0[0], arr - lado * 2 / 5, 0])
        t2 = VGroup(fraccion(4, 5, 36), texto("de las filas", 24, ACENTO)).arrange(RIGHT, buff=0.2)
        t2.next_to(cuadro, DOWN, buff=0.3)
        self.play(Create(filas), Indicate(e[2], color=ACENTO))
        self.play(FadeIn(f_fil), FadeIn(t2))
        self.wait(0.6)

        # Cruce
        w, h = lado / 3, lado / 5
        celdas = VGroup(*[Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=2, fill_color=VERDE_CRUCE,
                                    fill_opacity=0.95).move_to([izq + w * (c + 0.5), arr - h * (r + 0.5), 0])
                          for r in range(4) for c in range(2)])
        cruce = texto("Donde se cruzan: 8 cuadraditos", 26, VERDE_CRUCE).move_to([3.0, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in celdas], lag_ratio=0.1), FadeIn(cruce))
        total = texto("En total hay 3 · 5 = 15 cuadraditos", 26, GREY_B).next_to(cruce, DOWN, buff=0.3)
        self.play(FadeIn(total))
        res = fraccion(8, 15, 64).next_to(e, RIGHT, buff=0.3)
        self.play(Write(res))
        formula = MathTex(r"\frac{2}{3}\cdot\frac{4}{5}=\frac{2\cdot 4}{3\cdot 5}=\frac{8}{15}", font_size=52)
        formula.move_to([3.0, -1.4, 0])
        self.play(Write(formula))
        regla = texto("Numerador por numerador\ny denominador por denominador", 28, ACENTO).move_to([3.0, -2.8, 0])
        self.play(FadeIn(regla))
        self.wait(3)
        limpiar(self, cab)

        # «de» = por, y simplificar
        subtitulo(self, cab, "Más ejemplos")
        l1 = VGroup(texto("«2/3 de 4/5» es lo mismo que", 30), cadena((2, 3), r"\cdot", (4, 5), size=52))
        l1.arrange(RIGHT, buff=0.3).move_to([0, 1.8, 0])
        self.play(FadeIn(l1))
        l2 = cadena((3, 4), r"\cdot", (2, 9), "=", (6, 36), "=", (1, 6), size=52).move_to([0, 0.3, 0])
        self.play(Write(l2))
        n2 = texto("simplificamos al final (M.C.D. = 6)", 22, GREY_B).next_to(l2, DOWN, buff=0.2)
        self.play(FadeIn(n2))
        l3 = cadena("3", r"\cdot", (2, 5), "=", (3, 1), r"\cdot", (2, 5), "=", (6, 5), size=52).move_to([0, -1.6, 0])
        self.play(Write(l3))
        n3 = texto("un entero es una fracción con denominador 1", 22, GREY_B).next_to(l3, DOWN, buff=0.2)
        self.play(FadeIn(n3))
        self.wait(3)


VERDE_CRUCE = "#58D68D"


# ---------------------------------------------------------------------------
class DividirFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Dividir fracciones", "¿Cuántas veces cabe?")
        e = cadena((3, 4), ":", (1, 8), "=", size=64).move_to([-0.6, 2.2, 0])
        q = texto("¿Cuántos octavos caben en 3/4?", 30, ACENTO).move_to([0, 1.2, 0])
        self.play(Write(e), FadeIn(q))
        ancho = 10.0
        b4 = barra(4, 3, ancho=ancho, alto=0.8).move_to([0, 0.0, 0])
        b8 = barra(8, 0, ancho=ancho, alto=0.8).move_to([0, -1.1, 0])
        self.play(FadeIn(b4), FadeIn(fraccion(3, 4, 32).next_to(b4, LEFT, buff=0.25)))
        self.play(FadeIn(b8), FadeIn(fraccion(1, 8, 32).next_to(b8, LEFT, buff=0.25)))
        guia = DashedLine(b4[2].get_corner(UR) + UP * 0.1, b8[5].get_corner(DR) + DOWN * 0.1, color=ACENTO)
        self.play(Create(guia))
        nums = VGroup()
        for k in range(6):
            n = MathTex(str(k + 1), font_size=36, color=BLACK).move_to(b8[k])
            self.play(b8[k].animate.set_fill(ROSA), FadeIn(n), run_time=0.35)
            nums.add(n)
        r = MathTex("6", font_size=64, color=ACENTO).next_to(e, RIGHT, buff=0.3)
        self.play(Write(r), FadeIn(texto("¡Caben 6!", 30, ACENTO).to_edge(DOWN, buff=0.6)))
        self.wait(2.5)
        limpiar(self, cab)

        # La inversa
        subtitulo(self, cab, "La fracción inversa: le damos la vuelta")
        ejemplos = [(1, 8), (2, 3), (5, 1)]
        xs = [-4.0, 0.0, 4.0]
        for (n, d), x in zip(ejemplos, xs):
            f = fraccion(n, d, 72).move_to([x, 0.8, 0])
            self.play(Write(f), run_time=0.7)
            self.play(Swap(f[0], f[2]), run_time=1.0)
            self.play(f[0].animate.set_color(NUMERADOR), f[2].animate.set_color(DENOMINADOR), run_time=0.3)
            if d == 1:
                nota = texto("5 = 5/1  →  1/5", 24, GREY_B).next_to(f, DOWN, buff=0.4)
            else:
                nota = texto(f"{n}/{d}  →  {d}/{n}", 24, GREY_B).next_to(f, DOWN, buff=0.4)
            self.play(FadeIn(nota))
        self.wait(2)
        limpiar(self, cab)

        # Regla
        subtitulo(self, cab, "Dividir es multiplicar por la inversa")
        regla = MathTex(r"\frac{a}{b} : \frac{c}{d} = \frac{a}{b}\cdot\frac{d}{c}", font_size=64, color=ACENTO)
        regla.move_to([0, 1.9, 0])
        self.play(Write(regla))
        l1 = cadena((3, 4), ":", (1, 8), "=", (3, 4), r"\cdot", (8, 1), "=", (24, 4), "=", "6", size=52).move_to([0, 0.3, 0])
        self.play(Write(l1), run_time=2)
        ok = texto("¡Igual que en el dibujo! ✓", 26, OK).next_to(l1, DOWN, buff=0.2)
        self.play(FadeIn(ok))
        l2 = cadena((2, 3), ":", (4, 5), "=", (2, 3), r"\cdot", (5, 4), "=", (10, 12), "=", (5, 6), size=52)
        l2.move_to([0, -1.6, 0])
        self.play(Write(l2), run_time=2)
        n2 = texto("y simplificamos al final", 22, GREY_B).next_to(l2, DOWN, buff=0.2)
        self.play(FadeIn(n2), Circumscribe(l2[-1], color=ACENTO))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
from fractions import Fraction  # noqa: E402

# Las operaciones se escriben como (a, op, b): a y b son enteros o tuplas (n, d); op es "+", "-", "x" o ":".
MISMO_DEN = [((3, 8), "+", (2, 8)), ((7, 9), "-", (4, 9)), ((2, 5), "+", (4, 5)), ((5, 6), "-", (1, 6))]
DISTINTO_DEN = [((1, 2), "+", (1, 4)), ((2, 3), "+", (1, 6)), ((3, 4), "-", (2, 3)),
                ((5, 6), "+", (3, 8)), (1, "-", (3, 5)), (2, "+", (3, 4))]
DE_CANTIDAD = [(2, 3, 18), (3, 5, 40), (5, 8, 72), (3, 10, 250)]
MULTIPLICA = [((2, 5), "x", (3, 7)), ((4, 9), "x", (3, 8)), (5, "x", (2, 15)), ((6, 5), "x", (10, 3))]
DIVIDE = [((3, 5), ":", (2, 7)), ((4, 9), ":", (2, 3)), (6, ":", (3, 4)), ((5, 8), ":", 10)]
PROBLEMAS = [
    "a) Un depósito de 60 L está lleno en sus 3/4 partes. ¿Cuántos litros tiene?",
    "b) Juan se come 1/3 de una pizza y Marta 1/4.\n"
    "     ¿Qué fracción se comen entre los dos? ¿Cuánta pizza queda?",
    "c) ¿Cuántos vasos de 1/4 L se llenan con una botella de 3/2 L?",
    "d) Laura tiene 30 €. Gasta 2/5 en un libro y 1/3 de lo que le queda en el cine.\n"
    "     ¿Cuánto dinero le queda?",
]

SIMB_TEX = {"+": "+", "-": "-", "x": r"\cdot", ":": ":"}
SIMB_TXT = {"+": "+", "-": MENOS, "x": "·", ":": ":"}


def como_frac(x):
    """Entero -> (x, 1); tupla -> la misma tupla."""
    return (x, 1) if isinstance(x, int) else x


def item(x):
    """Lo que se dibuja: los enteros como número, las fracciones como fracción."""
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else (x.numerator, x.denominator)
    return str(x) if isinstance(x, int) else x


def op_txt(a, op, b):
    def t(x):
        return str(x) if isinstance(x, int) else f"{x[0]}/{x[1]}"
    return f"{t(a)} {SIMB_TXT[op]} {t(b)}"


def pasos_op(a, op, b, ejemplo=False):
    """Pasos de 'a op b': lista de (elementos de la cadena, nota). Los resultados salen de Fraction."""
    (na, da), (nb, db) = como_frac(a), como_frac(b)
    segs = [([item(a), SIMB_TEX[op], item(b)], None)]
    if op in "+-":
        signo = 1 if op == "+" else -1
        verbo = "suman" if op == "+" else "restan"
        if da == db:
            raw = (na + signo * nb, da)
            segs.append((["=", raw], f"Mismo denominador: se {verbo} los numeradores y se deja el {da}"))
        else:
            m = mcm(da, db)
            a2, b2 = (na * m // da, m), (nb * m // db, m)
            if isinstance(a, int):
                nota = f"El entero con denominador {m}: {a} = {a2[0]}/{m}"
            elif ejemplo:
                nota = f"1.º m.c.m.({da}, {db}) = {m}: pasamos las dos a denominador {m}"
            else:
                nota = f"m.c.m.({da}, {db}) = {m}"
            segs.append((["=", a2, SIMB_TEX[op], b2], nota))
            raw = (a2[0] + signo * b2[0], m)
            segs.append((["=", raw], ("2.º " if ejemplo else "") + f"Mismo denominador: se {verbo} los numeradores"))
    else:
        A = (na, da)
        B = (nb, db) if op == "x" else (db, nb)
        if op == "x" and (isinstance(a, int) or isinstance(b, int)):
            segs.append((["=", A, r"\cdot", B], "Un entero es una fracción con denominador 1"))
        if op == ":":
            nota = f"La inversa de {nb}/{db} es {db}/{nb}" if db != 1 else f"La inversa de {nb} es 1/{nb}"
            segs.append((["=", A, r"\cdot", B], "Dividir es multiplicar por la inversa. " + nota))
        segs.append((["=", (rf"{A[0]} \cdot {B[0]}", rf"{A[1]} \cdot {B[1]}")],
                     "Numerador por numerador y denominador por denominador"))
        raw = (A[0] * B[0], A[1] * B[1])
        segs.append((["=", raw], None))
    r = Fraction(*raw)
    if (r.numerator, r.denominator) != raw:
        segs.append((["=", item(r)], f"Simplificamos: M.C.D.({raw[0]}, {raw[1]}) = {gcd(*raw)}"))
    return segs


def resolver_cadena(scene, segs, etiqueta, y, x=-6.5, size=50, ejemplo=False, ancho_max=13.0):
    """Escribe la cadena de pasos de izquierda a derecha, con la nota de cada paso abajo."""
    elementos = [e for s, _ in segs for e in s]
    fila = cadena(*elementos, size=size)
    partes = [texto(etiqueta, 30)] if etiqueta else []
    grupo = VGroup(*partes, fila).arrange(RIGHT, buff=0.4)
    if grupo.width > ancho_max:
        grupo.scale_to_fit_width(ancho_max)
    grupo.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    k, nota_vieja = 0, None
    for i, (s, nota) in enumerate(segs):
        trozo = fila[k:k + len(s)]
        k += len(s)
        anims = [Write(trozo)]
        if i == 0 and partes:
            anims.append(FadeIn(partes[0]))
        if nota_vieja:
            anims.append(FadeOut(nota_vieja))
            nota_vieja = None
        if nota:
            nota_vieja = texto(nota, 28 if ejemplo else 24, ACENTO).to_edge(DOWN, buff=0.4)
            anims.append(FadeIn(nota_vieja))
        scene.play(*anims, run_time=1.2 if ejemplo else 0.9)
        scene.wait(1.6 if ejemplo else 0.7)
    if nota_vieja:
        scene.play(FadeOut(nota_vieja))
    scene.play(Circumscribe(fila[-1], color=ACENTO))
    return grupo


def resolver_ops(scene, ops, letras, ejemplo=False):
    """Varias operaciones en filas (1, 2 o 3 por pantalla)."""
    ys = {1: [0.6], 2: [1.2, -1.1], 3: [1.7, 0.0, -1.7]}[len(ops)]
    for (a, op, b), l, y in zip(ops, letras, ys):
        resolver_cadena(scene, pasos_op(a, op, b, ejemplo), f"{l})", y, size=60 if ejemplo else 50, ejemplo=ejemplo)
    scene.wait(1.5)


def resolver_cantidad(scene, n, d, total, etiqueta, y, unidad="", ejemplo=False):
    """«n/d de total» con una barra de d partes: total : d en cada parte y tomamos n partes."""
    parte = total // d
    res = parte * n
    u = rf"\text{{ {unidad}}}" if unidad else ""
    frac = fraccion(n, d, 44)
    lab = VGroup(*([texto(etiqueta, 30)] if etiqueta else []), frac,
                 MathTex(rf"\text{{de }} {total}" + u, font_size=44)).arrange(RIGHT, buff=0.2)
    lab.move_to([-4.9, y, 0])
    b = barra(d, 0, ancho=5.0, alto=0.7).move_to([0.8, y, 0])
    llave = Brace(b, UP, buff=0.08)
    tot = MathTex(str(total) + u, font_size=30).next_to(llave, UP, buff=0.05)
    scene.play(FadeIn(lab), FadeIn(b), GrowFromCenter(llave), FadeIn(tot))
    nota = None
    if ejemplo:
        nota = texto(f"1.º Dividimos entre el denominador: {d} partes iguales", 28, DENOMINADOR)
        nota.to_edge(DOWN, buff=0.4)
        scene.play(FadeIn(nota), Indicate(frac[2], color=DENOMINADOR, scale_factor=1.4))
    c1 = MathTex(f"{total} : {d} = {parte}", font_size=38, color=DENOMINADOR).move_to([5.5, y + 0.35, 0])
    vals = VGroup(*[MathTex(str(parte), font_size=26 if d <= 8 else 20).move_to(p) for p in b])
    scene.play(Write(c1))
    scene.play(LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.08))
    if ejemplo:
        scene.wait(1)
        nota2 = texto(f"2.º Multiplicamos por el numerador: tomamos {n} partes", 28, NUMERADOR)
        nota2.to_edge(DOWN, buff=0.4)
        scene.play(ReplacementTransform(nota, nota2), Indicate(frac[0], color=NUMERADOR, scale_factor=1.4))
        nota = nota2
    c2 = MathTex(rf"{parte} \cdot {n} = {res}", font_size=38, color=NUMERADOR).move_to([5.5, y - 0.35, 0])
    scene.play(*[b[i].animate.set_fill(ACENTO) for i in range(n)],
               *[vals[i].animate.set_color(BLACK) for i in range(n)], Write(c2))
    r = MathTex(rf"= {res}" + u, font_size=48, color=ACENTO).next_to(lab, DOWN, buff=0.25).align_to(frac, LEFT)
    scene.play(Write(r), Circumscribe(r, color=ACENTO))
    scene.wait(1.5 if ejemplo else 0.8)
    if nota:
        scene.play(FadeOut(nota))


def resolver_cantidades(scene, items, letras):
    ys = {1: [0.4], 2: [1.2, -1.3], 3: [1.6, -0.35, -2.3]}[len(items)]
    for (n, d, total), l, y in zip(items, letras, ys):
        resolver_cantidad(scene, n, d, total, f"{l})", y)
    scene.wait(1.5)


def pagina_enunciados(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 28, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cab, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def lista_ops(ops, por_linea=4):
    trozos = [f"{l}) {op_txt(*o)}" for l, o in zip("abcdef", ops)]
    return "\n".join("     ".join(trozos[i:i + por_linea]) for i in range(0, len(trozos), por_linea))


def enunciados_1():
    return [
        ("1. Suma o resta (mismo denominador) y simplifica:", lista_ops(MISMO_DEN)),
        ("2. Suma o resta (distinto denominador) y simplifica:", lista_ops(DISTINTO_DEN, 3)),
        ("3. Calcula:", "     ".join(f"{l}) {n}/{d} de {t}" for l, (n, d, t) in zip("abcd", DE_CANTIDAD))),
    ]


def enunciados_2():
    return [
        ("4. Multiplica y simplifica:", lista_ops(MULTIPLICA)),
        ("5. Divide y simplifica:", lista_ops(DIVIDE)),
        ("6. Problemas:", "\n".join(PROBLEMAS)),
    ]


# --- 6. Problemas
def enunciado(scene, i):
    e = texto(PROBLEMAS[i][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    return e


def problema_deposito(scene):
    enunciado(scene, 0)
    resolver_cantidad(scene, 3, 4, 60, "", 0.2, unidad="L", ejemplo=True)
    sol = texto("El depósito tiene 45 litros", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_pizza(scene):
    enunciado(scene, 1)
    p = pizza(12, 0, r=1.35).move_to([-5.2, -0.2, 0])
    scene.play(FadeIn(p))
    resolver_cadena(scene, pasos_op((1, 3), "+", (1, 4)), "Comen:", 0.8, x=-3.3, size=46, ancho_max=10)
    nj = texto("Juan: 4/12", 24, ACENTO).next_to(p, DOWN, buff=0.25)
    nm = texto("Marta: 3/12", 24, ROSA).next_to(nj, DOWN, buff=0.12)
    scene.play(*[p[i].animate.set_fill(ACENTO) for i in range(4)], FadeIn(nj))
    scene.play(*[p[i].animate.set_fill(ROSA) for i in range(4, 7)], FadeIn(nm))
    resolver_cadena(scene, pasos_op(1, "-", (7, 12)), "Queda:", -1.1, x=-3.3, size=46, ancho_max=10)
    scene.play(LaggedStart(*[Indicate(p[i], scale_factor=1.1) for i in range(7, 12)], lag_ratio=0.1))
    sol = texto("Se comen 7/12 de la pizza y queda 5/12", 30, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_vasos(scene):
    enunciado(scene, 2)
    resolver_cadena(scene, pasos_op((3, 2), ":", (1, 4)), "", 1.0, x=-4.5, size=50)
    bs = VGroup(barra(4, 4, ancho=4.0, alto=0.75), barra(4, 2, ancho=4.0, alto=0.75)).arrange(RIGHT, buff=0.5)
    bs.move_to([0, -1.0, 0])
    litros = VGroup(*[texto("1 L", 22, GREY_B).next_to(b, DOWN, buff=0.15) for b in bs])
    bot = texto("3/2 L = una botella y media", 24, GREY_B).next_to(bs, UP, buff=0.2)
    scene.play(FadeIn(bs), FadeIn(litros), FadeIn(bot))
    trozos = list(bs[0]) + list(bs[1][:2])
    nums = VGroup(*[MathTex(str(i + 1), font_size=34, color=BLACK).move_to(t) for i, t in enumerate(trozos)])
    scene.play(LaggedStart(*[FadeIn(n, scale=1.5) for n in nums], lag_ratio=0.2))
    sol = texto("Cada trozo es un vaso de 1/4 L: se llenan 6 vasos", 30, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_laura(scene):
    enunciado(scene, 3)
    b = barra(5, 0, ancho=10, alto=0.8).move_to([0, 0.85, 0])
    llave = Brace(b, UP, buff=0.08)
    tot = texto("30 €", 26).next_to(llave, UP, buff=0.05)
    seis = VGroup(*[texto("6 €", 24).move_to(p) for p in b])
    scene.play(FadeIn(b), GrowFromCenter(llave), FadeIn(tot))
    scene.play(LaggedStart(*[FadeIn(s) for s in seis], lag_ratio=0.15))
    l1 = texto("Libro: 2/5 de 30 € = 12 €   →   le quedan 30 − 12 = 18 €", 28).move_to([0, -0.9, 0])
    scene.play(*[b[i].animate.set_fill(ACENTO) for i in range(2)], *[seis[i].animate.set_color(BLACK) for i in range(2)],
               FadeIn(l1))
    queda = Brace(VGroup(*b[2:]), DOWN, buff=0.08, color=GREY_B)
    tq = texto("quedan 18 €", 22, GREY_B).next_to(queda, DOWN, buff=0.05)
    scene.play(GrowFromCenter(queda), FadeIn(tq))
    scene.wait(1)
    trampa = texto("¡Ojo! Es 1/3 de lo que le queda (18 €), no de los 30 €", 24, ACENTO).move_to([0, -1.6, 0])
    scene.play(FadeIn(trampa))
    scene.wait(1.5)
    l2 = texto("Cine: 1/3 de 18 € = 6 €", 28).move_to([0, -1.6, 0])
    scene.play(ReplacementTransform(trampa, l2), b[2].animate.set_fill(ROSA), seis[2].animate.set_color(BLACK))
    sol = texto("Le quedan 18 − 6 = 12 €", 32, OK).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(sol), Indicate(VGroup(*b[3:]), scale_factor=1.05))
    scene.wait(3)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Operaciones con fracciones")
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2(), size=22)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        for sub, ops, letra in (("Ejercicio 1 a)", MISMO_DEN[:1], "a"), ("Ejercicio 2 a)", DISTINTO_DEN[:1], "a"),
                                ("Ejercicio 2 f): un entero más una fracción", DISTINTO_DEN[5:], "f")):
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, letra, ejemplo=True)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        resolver_cantidad(self, *DE_CANTIDAD[0], "a)", 0.4, ejemplo=True)
        limpiar(self, cab)
        for sub, ops in (("Ejercicio 4 a)", MULTIPLICA[:1]), ("Ejercicio 5 a)", DIVIDE[:1])):
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, "a", ejemplo=True)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        problema_deposito(self)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Operaciones con fracciones")
        pantallas = [
            ("Ejercicio 1: b), c) y d)", MISMO_DEN[1:], "bcd"),
            ("Ejercicio 2: b) y c)", DISTINTO_DEN[1:3], "bc"),
            ("Ejercicio 2: d) y e)", DISTINTO_DEN[3:5], "de"),
        ]
        for sub, ops, letras in pantallas:
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, letras)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        resolver_cantidades(self, DE_CANTIDAD[1:], "bcd")
        limpiar(self, cab)
        for sub, ops in (("Ejercicio 4: b), c) y d)", MULTIPLICA[1:]), ("Ejercicio 5: b), c) y d)", DIVIDE[1:])):
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, "bcd")
            limpiar(self, cab)
        for sub, f in (("Ejercicio 6 b)", problema_pizza), ("Ejercicio 6 c)", problema_vasos),
                       ("Ejercicio 6 d)", problema_laura)):
            subtitulo(self, cab, sub)
            f(self)
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes operar con fracciones.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
