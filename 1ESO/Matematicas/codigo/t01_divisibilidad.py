"""Tema 1 · Divisibilidad (1º ESO)

Escenas:
    Divisores          – múltiplos y divisores con rectángulos de fichas
    PrimosCompuestos   – un número primo no forma rectángulos
    Criterios          – criterios de divisibilidad por 2, 3, 5 y 10
    CribaEratostenes   – criba de Eratóstenes del 1 al 100

Renderizar (desde esta carpeta):
    python -m manim -pql t01_divisibilidad.py Divisores
    python -m manim -pqh t01_divisibilidad.py -a        (todas, alta calidad)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 1 · Divisibilidad"
TITULOS = {
    "Divisores": "Múltiplos y divisores",
    "PrimosCompuestos": "Números primos y compuestos",
    "Criterios": "Criterios de divisibilidad",
    "CribaEratostenes": "Criba de Eratóstenes",
}

BUFF = 0.25


def huecos(n_fichas, filas, cols, centro=ORIGIN):
    """Posiciones de una cuadrícula filas x cols (devuelve VGroup de Dots invisibles)."""
    g = VGroup(*[Dot(radius=0.15) for _ in range(filas * cols)])
    g.arrange_in_grid(rows=filas, cols=cols, buff=BUFF).move_to(centro)
    return g


def colocar(fichas, rejilla):
    return AnimationGroup(*[f.animate.move_to(rejilla[i]) for i, f in enumerate(fichas)])


class Divisores(Scene):
    def construct(self):
        cab = titulo(self, "Divisibilidad", "Múltiplos y divisores")

        pregunta = texto("¿De cuántas formas podemos colocar\n12 fichas formando un rectángulo?", 30)
        pregunta.next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(pregunta))

        fichas = VGroup(*[Dot(radius=0.15, color=ACENTO) for _ in range(12)])
        fichas.arrange(RIGHT, buff=BUFF).shift(UP * 0.5)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in fichas], lag_ratio=0.08))

        formas = [(1, 12), (2, 6), (3, 4)]
        etiquetas = VGroup()
        for filas, cols in formas:
            rej = huecos(12, filas, cols, UP * 0.5)
            self.play(colocar(fichas, rej), run_time=1.2)
            et = MathTex(rf"{filas} \times {cols} = 12", font_size=44)
            et.next_to(fichas, DOWN, buff=0.5)
            self.play(Write(et))
            self.wait(0.6)
            etiquetas.add(et.copy())
            self.play(FadeOut(et))

        # Resumen de los productos
        etiquetas.arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=1.6)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in etiquetas], lag_ratio=0.3))
        self.wait(0.5)

        divs = MathTex(r"\text{Divisores de } 12:\; 1,\ 2,\ 3,\ 4,\ 6,\ 12",
                       font_size=46, color=ACENTO).to_edge(DOWN, buff=0.6)
        self.play(Write(divs))
        self.wait(1)

        # Definición
        self.play(*[FadeOut(m) for m in [fichas, etiquetas, pregunta]], divs.animate.to_edge(UP, buff=1.2))
        defi = VGroup(
            MathTex(r"12 = 3 \times 4", font_size=60),
            texto("3 es divisor de 12", 38, OK),
            texto("12 es múltiplo de 3", 38, BLUE),
            texto("(12 entre 3 da exacto: resto 0)", 28, GREY_B),
        ).arrange(DOWN, buff=0.4).shift(DOWN * 0.5)
        for m in defi:
            self.play(FadeIn(m, shift=UP * 0.2))
            self.wait(0.4)
        self.wait(2)


class PrimosCompuestos(Scene):
    def construct(self):
        cab = titulo(self, "Números primos")

        pregunta = texto("¿Y con 7 fichas?", 36).next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(pregunta))

        fichas = VGroup(*[Dot(radius=0.15, color=ACENTO) for _ in range(7)])
        fichas.arrange(RIGHT, buff=BUFF).shift(UP * 0.3)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in fichas], lag_ratio=0.1))

        for filas in (2, 3):
            cols = -(-7 // filas)  # techo
            rej = huecos(7, filas, cols, UP * 0.3)
            self.play(colocar(fichas, rej), run_time=1.2)
            vacios = VGroup(*[DashedVMobject(Circle(radius=0.15, color=MAL)).move_to(rej[i])
                              for i in range(7, filas * cols)])
            msg = texto(f"{filas} filas: ¡no sale! Sobra hueco.", 32, MAL).next_to(rej, DOWN, buff=0.6)
            self.play(Create(vacios), Write(msg))
            self.wait(0.8)
            self.play(FadeOut(vacios), FadeOut(msg))

        rej = huecos(7, 1, 7, UP * 0.3)
        self.play(colocar(fichas, rej))
        solo = MathTex(r"7 = 1 \times 7", font_size=50).next_to(fichas, DOWN, buff=0.6)
        self.play(Write(solo))
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in [fichas, solo, pregunta]])

        primo = VGroup(
            texto("Número PRIMO", 44, OK),
            texto("Solo tiene 2 divisores: el 1 y él mismo", 30),
            MathTex(r"2,\ 3,\ 5,\ 7,\ 11,\ 13,\ \dots", font_size=44, color=OK),
        ).arrange(DOWN, buff=0.3)
        compuesto = VGroup(
            texto("Número COMPUESTO", 44, BLUE),
            texto("Tiene más de 2 divisores", 30),
            MathTex(r"4,\ 6,\ 8,\ 9,\ 10,\ 12,\ \dots", font_size=44, color=BLUE),
        ).arrange(DOWN, buff=0.3)
        VGroup(primo, compuesto).arrange(DOWN, buff=0.8).shift(DOWN * 0.3)
        self.play(FadeIn(primo, shift=UP * 0.3))
        self.wait(1)
        self.play(FadeIn(compuesto, shift=UP * 0.3))
        self.wait(1)
        nota = texto("Ojo: el 1 no es ni primo ni compuesto.", 28, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(Write(nota))
        self.wait(2)


class Criterios(Scene):
    def construct(self):
        cab = titulo(self, "Criterios de divisibilidad")

        filas = [
            ("2", "Acaba en cifra par (0, 2, 4, 6, 8)", "348", BLUE),
            ("3", "La suma de sus cifras es múltiplo de 3", "471", GREEN),
            ("5", "Acaba en 0 o en 5", "835", ORANGE),
            ("10", "Acaba en 0", "760", PURPLE),
        ]
        tabla = VGroup()
        for d, regla, ej, col in filas:
            caja = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.15, color=col, fill_opacity=0.25)
            num = texto(d, 36, col).move_to(caja)
            r = texto(regla, 28).next_to(caja, RIGHT, buff=0.4)
            fila = VGroup(VGroup(caja, num), r)
            fila.ej, fila.col = ej, col
            tabla.add(fila)
        tabla.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(cab, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)

        for f in tabla:
            self.play(FadeIn(f[0], scale=0.8), Write(f[1]), run_time=1)
            self.wait(0.6)
        self.wait(1)

        # Ejemplo detallado del 3
        self.play(tabla.animate.scale(0.6).to_corner(UR).shift(DOWN * 0.6))
        ej = MathTex("4", "7", "1", font_size=90).shift(LEFT * 2.5 + DOWN * 0.3)
        self.play(Write(ej))
        suma = MathTex("4", "+", "7", "+", "1", "=", "12", font_size=70).next_to(ej, DOWN, buff=0.8)
        self.play(*[TransformFromCopy(ej[i], suma[2 * i]) for i in range(3)], FadeIn(suma[1]), FadeIn(suma[3]))
        self.play(Write(suma[5:]))
        check = MathTex(r"12 = 3 \times 4 \;\Rightarrow\; 471 \text{ es divisible por } 3",
                        font_size=42, color=OK).to_edge(DOWN, buff=0.8)
        self.play(Write(check))
        self.wait(1)
        comprob = MathTex(r"471 : 3 = 157", font_size=48, color=ACENTO).next_to(ej, RIGHT, buff=1.2)
        self.play(FadeIn(comprob, shift=LEFT * 0.3))
        self.wait(2)


class CribaEratostenes(Scene):
    def construct(self):
        cab = titulo(self, "Criba de Eratóstenes", "Buscamos los primos del 1 al 100")

        lado = 0.62
        celdas = {}
        grid = VGroup()
        for n in range(1, 101):
            cuad = Square(lado, stroke_width=1.5, stroke_color=GREY_B, fill_opacity=0)
            num = Text(str(n), font_size=20).set_z_index(2)  # siempre por encima del relleno
            celda = VGroup(cuad, num)
            celdas[n] = celda
            grid.add(celda)
        grid.arrange_in_grid(rows=10, cols=10, buff=0)
        for c in grid:
            c[1].move_to(c[0])
        grid.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01), run_time=2)

        def explicar(cadena, color=TEXTO):
            t = texto(cadena, 28, color)
            t.next_to(grid, RIGHT, buff=0.6).align_to(grid, UP)
            return t

        info = explicar("El 1 no es primo")
        self.play(Write(info), celdas[1].animate.set_opacity(0.2))
        tachado = {1}

        leyenda = VGroup()
        for p in (2, 3, 5, 7):
            col = COLOR_PRIMO[p]
            nuevo = explicar(f"{p} es primo.\nTachamos sus múltiplos:\n{2*p}, {3*p}, {4*p}, ...", col)
            self.play(Transform(info, nuevo),
                      celdas[p][0].animate.set_fill(col, 0.9),
                      Circumscribe(celdas[p], color=col))
            multiplos = [m for m in range(2 * p, 101, p) if m not in tachado]
            self.play(LaggedStart(*[
                AnimationGroup(celdas[m][0].animate.set_fill(col, 0.25),
                               celdas[m][1].animate.set_opacity(0.25))
                for m in multiplos], lag_ratio=0.06), run_time=2.5)
            tachado.update(multiplos)
            item = VGroup(Square(0.3, fill_color=col, fill_opacity=0.9, stroke_width=0),
                          texto(f"múltiplos de {p}", 24))
            item[1].next_to(item[0], RIGHT, buff=0.2)
            leyenda.add(item)
            self.wait(0.5)

        leyenda.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(grid, RIGHT, buff=0.6).align_to(grid, DOWN)
        self.play(FadeIn(leyenda))

        fin = explicar("Los que quedan\nson todos PRIMOS", ACENTO)
        primos = [n for n in range(2, 101) if n not in tachado]
        self.play(Transform(info, fin))
        self.play(LaggedStart(*[
            celdas[n][0].animate.set_fill(ACENTO, 0.85) for n in primos if n > 7
        ], lag_ratio=0.05), *[celdas[n][1].animate.set_color(BLACK) for n in primos if n > 7], run_time=2.5)

        total = texto(f"¡Hay {len(primos)} primos\nmenores que 100!", 32, ACENTO)
        total.next_to(info, DOWN, buff=0.6).align_to(info, LEFT)
        self.play(Write(total))
        self.wait(3)
