r"""Tema 2 · Divisibilidad (1º ESO) — unidad 2 del libro (antes temas 1 y 2)

Escenas (orden del libro: múltiplos y divisores, criterios, primos, M.C.D. y m.c.m.):
    Divisores            – múltiplos y divisores con rectángulos de fichas
    Criterios            – criterios de divisibilidad por 2, 3, 5 y 10
    PrimosCompuestos     – un número primo no forma rectángulos
    CribaEratostenes     – criba de Eratóstenes del 1 al 100
    ArbolFactores        – árbol de factores de 60 (dos caminos, mismo resultado)
    DivisionesSucesivas  – método de la columna con 60 y 84
    ComunesRecta         – múltiplos comunes (ranas en la recta) y divisores comunes (Venn)
    McdMcmFactores       – M.C.D. y m.c.m. de 12 y 18 con fichas de colores
    ProblemasMcdMcm      – cintas y baldosas (M.C.D.), autobuses (m.c.m.) y regla final
    EjerciciosEjemplo / EjerciciosResueltos

Renderizar (desde esta carpeta):
    ~\venvs\manim\Scripts\python.exe -m manim -pql t02_divisibilidad.py Divisores
    ~\venvs\manim\Scripts\python.exe publicar.py t02_divisibilidad.py
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 2 · Divisibilidad"
TITULOS = {
    "Divisores": "Múltiplos y divisores",
    "Criterios": "Criterios de divisibilidad",
    "PrimosCompuestos": "Números primos y compuestos",
    "CribaEratostenes": "Criba de Eratóstenes",
    "ArbolFactores": "Árbol de factores",
    "DivisionesSucesivas": "Divisiones sucesivas",
    "ComunesRecta": "Múltiplos y divisores comunes",
    "McdMcmFactores": "M.C.D. y m.c.m. con factores",
    "ProblemasMcdMcm": "Problemas: ¿M.C.D. o m.c.m.?",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplo resuelto",
    "EjerciciosResueltos": "Ejercicios resueltos (b – h)",
}
# Extras que no son vídeos (publicar.py los pone en la web):
#   (etiqueta, título, ruta desde la carpeta de la asignatura, detrás de qué escena)
INTERACTIVOS = [
    ("E1", "Pruébalo tú: factores, M.C.D. y m.c.m.", "interactivos/factores_mcd_mcm.html?m=mcd", "McdMcmFactores"),
]

ROSA = "#FF79C6"
RANA_A = TEAL
RANA_B = ROSA


def tex_factores(n, factores, size=48):
    """MathTex 'n = 2 · 2 · 3 · 5' con cada primo coloreado. Devuelve (tex, índices de factores)."""
    partes = [str(n), "="]
    idx = []
    for i, p in enumerate(factores):
        if i:
            partes.append(r"\cdot")
        idx.append(len(partes))
        partes.append(str(p))
    t = MathTex(*partes, font_size=size)
    for i, p in zip(idx, factores):
        t[i].set_color(COLOR_PRIMO[p])
    return t, idx


def tex_potencias(factores, size=48, prefijo="="):
    """MathTex '= 2^{2} · 3 · 5' coloreado."""
    cuenta = {}
    for p in factores:
        cuenta[p] = cuenta.get(p, 0) + 1
    partes = [prefijo] if prefijo else []
    colores = []
    for i, (p, e) in enumerate(sorted(cuenta.items())):
        if i:
            partes.append(r"\cdot")
            colores.append(None)
        partes.append(f"{p}^{{{e}}}" if e > 1 else str(p))
        colores.append(COLOR_PRIMO[p])
    t = MathTex(*partes, font_size=size)
    off = 1 if prefijo else 0
    for i, c in enumerate(colores):
        if c:
            t[i + off].set_color(c)
    return t


# ---------------------------------------------------------------------------
# Múltiplos, divisores, criterios y primos (antes tema 1)

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


# ---------------------------------------------------------------------------
class ArbolFactores(Scene):
    def construct(self):
        cab = titulo(self, "Factores primos", "Descomposición de un número")

        idea = texto("Todo número compuesto se puede escribir\ncomo producto de números primos", 32)
        idea.shift(UP * 1.2)
        ladrillos = VGroup(*[pieza(p, 0.45) for p in (2, 3, 5, 7)]).arrange(RIGHT, buff=0.5)
        ladrillos.next_to(idea, DOWN, buff=0.8)
        frase = texto("Los primos son los «ladrillos» de los números", 30, ACENTO)
        frase.next_to(ladrillos, DOWN, buff=0.8)
        self.play(Write(idea))
        self.play(LaggedStart(*[GrowFromCenter(l) for l in ladrillos], lag_ratio=0.2))
        self.play(FadeIn(frase, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(VGroup(idea, ladrillos, frase)))

        # Dos árboles distintos para el 60
        hojas1 = self.arbol(60, {60: (6, 10), 6: (2, 3), 10: (2, 5)}, -3.5, 2.0, 1.4)
        res1 = self.resultado(60, hojas1, -3.5)
        self.wait(0.8)

        otra = texto("¿Y si empezamos de otra forma?", 28, GREY_B).move_to([3.5, 2.9, 0])
        self.play(FadeIn(otra))
        hojas2 = self.arbol(60, {60: (4, 15), 4: (2, 2), 15: (3, 5)}, 3.5, 2.0, 1.4)
        self.play(FadeOut(otra))
        res2 = self.resultado(60, hojas2, 3.5)

        msg = texto("¡Siempre sale lo mismo!", 36, ACENTO).to_edge(DOWN, buff=0.3)
        self.play(Write(msg), Circumscribe(res1[1], color=ACENTO), Circumscribe(res2[1], color=ACENTO))
        self.wait(2.5)

    def arbol(self, n, split, cx, y, dx, dy=1.3):
        """Dibuja el árbol recursivamente. Devuelve lista de (valor, MathTex) de las hojas."""
        nodo = MathTex(str(n), font_size=48).move_to([cx, y, 0])
        self.play(FadeIn(nodo, scale=0.8), run_time=0.4)
        if es_primo(n):
            col = COLOR_PRIMO[n]
            aro = Circle(radius=0.36, color=col, stroke_width=4).move_to(nodo)
            self.play(Create(aro), nodo.animate.set_color(col), run_time=0.4)
            return [(n, nodo)]
        a, b = split[n]
        hojas = []
        lineas = []
        for sx in (-1, 1):
            fin = np.array([cx + sx * dx, y - dy, 0])
            lineas.append(Line(nodo.get_bottom() + DOWN * 0.1, fin + UP * 0.38,
                               stroke_width=3, color=GREY_B))
        prod = MathTex(rf"{a} \times {b}", font_size=30, color=GREY_B).next_to(nodo, RIGHT, buff=0.25)
        self.play(*[Create(l) for l in lineas], FadeIn(prod), run_time=0.5)
        self.play(FadeOut(prod), run_time=0.2)
        hojas += self.arbol(a, split, cx - dx, y - dy, dx / 2, dy)
        hojas += self.arbol(b, split, cx + dx, y - dy, dx / 2, dy)
        return hojas

    def resultado(self, n, hojas, cx):
        hojas = sorted(hojas, key=lambda h: h[0])
        fila, idx = tex_factores(n, [h[0] for h in hojas])
        fila.move_to([cx, -2.0, 0])
        self.play(Write(fila[:2]))
        self.play(*[TransformFromCopy(h[1], fila[i]) for h, i in zip(hojas, idx)],
                  *[FadeIn(fila[i - 1]) for i in idx[1:]], run_time=1.2)
        pot = tex_potencias([h[0] for h in hojas], 52).next_to(fila, DOWN, buff=0.35).align_to(fila[1], LEFT)
        self.play(Write(pot))
        return VGroup(fila, pot)


# ---------------------------------------------------------------------------
class DivisionesSucesivas(Scene):
    def construct(self):
        cab = titulo(self, "Divisiones sucesivas")
        regla = texto("Dividimos siempre por el primo más pequeño posible", 28, GREY_B)
        regla.next_to(cab, DOWN, buff=0.3).to_edge(LEFT)
        self.play(FadeIn(regla))

        self.columna(60, np.array([-4.6, 1.9, 0]))
        self.columna(84, np.array([1.7, 1.9, 0]), rapido=True)
        self.wait(2.5)

    @staticmethod
    def motivo(num, p):
        if p == 2:
            return f"{num} es par"
        if p == 3:
            cif = [int(c) for c in str(num)]
            return f"{' + '.join(map(str, cif))} = {sum(cif)}, múltiplo de 3"
        if p == 5:
            return f"{num} acaba en {str(num)[-1]}"
        return f"{num} : {p} = {num // p} exacto"

    def columna(self, n, origen, rapido=False):
        rt = 0.5 if rapido else 0.8
        dy = 0.72
        factores, nums, x = [], [n], n
        while x > 1:
            p = next(d for d in range(2, x + 1) if x % d == 0)
            factores.append(p)
            x //= p
            nums.append(x)

        linea = Line(origen + UP * 0.35, origen + DOWN * ((len(nums) - 1) * dy + 0.35),
                     stroke_width=3)
        self.play(Create(linea), run_time=rt)
        for i, num in enumerate(nums):
            fila_y = origen + DOWN * i * dy
            izq = MathTex(str(num), font_size=46).next_to(fila_y, LEFT, buff=0.3)
            self.play(FadeIn(izq, shift=DOWN * 0.15), run_time=rt * 0.6)
            if i < len(factores):
                p = factores[i]
                der = MathTex(str(p), font_size=46, color=COLOR_PRIMO[p]).next_to(fila_y, RIGHT, buff=0.3)
                por = texto(self.motivo(num, p), 20, GREY_B)
                por.move_to(fila_y + RIGHT * 1.2, aligned_edge=LEFT)
                self.play(FadeIn(der, scale=1.3), FadeIn(por), run_time=rt)
        res = tex_factores(n, factores, 46)[0]
        pot = tex_potencias(factores, 46)
        grupo = VGroup(res, pot).arrange(RIGHT, buff=0.2)
        grupo.next_to(origen + DOWN * (len(nums) - 1) * dy, DOWN, buff=0.8).align_to(origen + LEFT * 1.0, LEFT)
        self.play(Write(grupo), run_time=rt * 2)
        self.play(Circumscribe(grupo, color=ACENTO), run_time=rt * 1.5)


# ---------------------------------------------------------------------------
class ComunesRecta(Scene):
    def construct(self):
        cab = titulo(self, "Múltiplos y divisores comunes")
        self.multiplos(cab)
        self.divisores(cab)

    def multiplos(self, cab):
        sub = texto("Múltiplos comunes de 4 y 6", 32, ACENTO).next_to(cab, DOWN, buff=0.3).to_edge(LEFT)
        self.play(FadeIn(sub))

        def recta(y):
            r = NumberLine(x_range=[0, 37, 1], length=12.6, include_numbers=True,
                           font_size=18, tick_size=0.06, stroke_width=2)
            return r.move_to([0, y, 0])

        ra, rb = recta(0.5), recta(-1.6)
        la = texto("Rana A: salta de 4 en 4", 24, RANA_A).next_to(ra, UP, buff=0.9).to_edge(LEFT)
        lb = texto("Rana B: salta de 6 en 6", 24, RANA_B).next_to(rb, UP, buff=0.9).to_edge(LEFT)
        self.play(Create(ra), Create(rb), FadeIn(la), FadeIn(lb))

        marcas = {}
        for r, paso, col in ((ra, 4, RANA_A), (rb, 6, RANA_B)):
            rana = Dot(radius=0.14, color=col).move_to(r.n2p(0) + UP * 0.15)
            self.play(FadeIn(rana, scale=2), run_time=0.3)
            marcas[paso] = {}
            for m in range(paso, 37, paso):
                arco = ArcBetweenPoints(r.n2p(m - paso) + UP * 0.15, r.n2p(m) + UP * 0.15, angle=-PI / 1.6)
                huella = Dot(radius=0.09, color=col).move_to(r.n2p(m) + UP * 0.15)
                self.play(MoveAlongPath(rana, arco), Create(DashedVMobject(arco.copy().set_stroke(col, 2, 0.6))),
                          run_time=0.35 if paso == 4 else 0.5, rate_func=linear)
                self.add(huella)
                marcas[paso][m] = huella
            self.play(FadeOut(rana), run_time=0.3)

        comunes = [12, 24, 36]
        uniones = VGroup(*[DashedLine(ra.n2p(m) + UP * 0.3, rb.n2p(m) + DOWN * 0.35, color=ACENTO)
                           for m in comunes])
        aros = VGroup(*[Circle(radius=0.22, color=ACENTO, stroke_width=4).move_to(marcas[p][m])
                        for m in comunes for p in (4, 6)])
        self.play(LaggedStart(*[Create(u) for u in uniones], lag_ratio=0.3), Create(aros))

        t1 = MathTex(r"\text{Multiplos comunes: } 12,\ 24,\ 36,\ \dots", font_size=40).to_edge(DOWN, buff=1.1)
        t2 = MathTex(r"\text{El menor: } \text{m.c.m.}(4, 6) = 12", font_size=44, color=ACENTO).to_edge(DOWN, buff=0.35)
        self.play(Write(t1))
        self.play(Write(t2), Indicate(aros[0]), Indicate(aros[1]))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not cab])

    def divisores(self, cab):
        sub = texto("Divisores comunes de 12 y 18", 32, ACENTO).next_to(cab, DOWN, buff=0.3).to_edge(LEFT)
        self.play(FadeIn(sub))

        c = DOWN * 0.4
        ea = Ellipse(width=5.2, height=3.8, color=RANA_A, fill_opacity=0.12).move_to(c + LEFT * 1.4)
        eb = Ellipse(width=5.2, height=3.8, color=RANA_B, fill_opacity=0.12).move_to(c + RIGHT * 1.4)
        la = texto("Divisores de 12", 28, RANA_A).next_to(ea, UP, buff=0.15).shift(LEFT * 0.8)
        lb = texto("Divisores de 18", 28, RANA_B).next_to(eb, UP, buff=0.15).shift(RIGHT * 0.8)

        pos = {
            1: c + UL * 0.55, 2: c + UR * 0.55, 3: c + DL * 0.55, 6: c + DR * 0.55,
            4: c + LEFT * 2.9 + UP * 0.5, 12: c + LEFT * 2.9 + DOWN * 0.5,
            9: c + RIGHT * 2.9 + UP * 0.5, 18: c + RIGHT * 2.9 + DOWN * 0.5,
        }
        nums = {d: MathTex(str(d), font_size=48).move_to(p) for d, p in pos.items()}

        self.play(Create(ea), FadeIn(la))
        self.play(LaggedStart(*[FadeIn(nums[d], scale=1.4) for d in (1, 2, 3, 4, 6, 12)], lag_ratio=0.25))
        self.wait(0.5)
        self.play(Create(eb), FadeIn(lb))
        anims = []
        for d in (1, 2, 3, 6, 9, 18):
            anims.append(Indicate(nums[d], color=ACENTO) if d in (1, 2, 3, 6) else FadeIn(nums[d], scale=1.4))
        self.play(LaggedStart(*anims, lag_ratio=0.3), run_time=3)

        self.play(*[nums[d].animate.set_color(ACENTO) for d in (1, 2, 3, 6)])
        t1 = MathTex(r"\text{Divisores comunes: } 1,\ 2,\ 3,\ 6", font_size=40).to_edge(DOWN, buff=1.1)
        t2 = MathTex(r"\text{El mayor: } \text{M.C.D.}(12, 18) = 6", font_size=44, color=ACENTO).to_edge(DOWN, buff=0.35)
        self.play(Write(t1))
        self.play(Write(t2), Circumscribe(nums[6], shape=Circle, color=ACENTO))
        self.wait(3)


# ---------------------------------------------------------------------------
class McdMcmFactores(Scene):
    def construct(self):
        cab = titulo(self, "M.C.D. y m.c.m.", "Con factores primos")

        y12, y18 = 2.0, 0.8
        x2, x3 = [-3.4, -2.6], [-1.4, -0.6]

        def fila(n, y, n2, n3):
            lab = MathTex(f"{n} =", font_size=48).move_to([-5.0, y, 0])
            dos = [pieza(2).move_to([x2[i], y, 0]) for i in range(n2)]
            tres = [pieza(3).move_to([x3[i], y, 0]) for i in range(n3)]
            return lab, dos, tres

        l12, d12, t12 = fila(12, y12, 2, 1)
        l18, d18, t18 = fila(18, y18, 1, 2)
        p12 = tex_potencias([2, 2, 3], 44).move_to([0.6, y12, 0], aligned_edge=LEFT)
        p18 = tex_potencias([2, 3, 3], 44).move_to([0.6, y18, 0], aligned_edge=LEFT)

        for lab, dos, tres, pot in ((l12, d12, t12, p12), (l18, d18, t18, p18)):
            self.play(Write(lab))
            self.play(LaggedStart(*[GrowFromCenter(m) for m in dos + tres], lag_ratio=0.2))
            self.play(Write(pot))
        self.wait(0.8)

        # --- M.C.D.
        reg_mcd = texto("M.C.D. → factores COMUNES, con el MENOR exponente", 26, OK)
        reg_mcd.move_to([0, -0.3, 0]).to_edge(LEFT, buff=0.6)
        cajas = VGroup(
            SurroundingRectangle(VGroup(d12[0], d18[0]), color=OK, buff=0.1),
            SurroundingRectangle(VGroup(t12[0], t18[0]), color=OK, buff=0.1),
        )
        self.play(Write(reg_mcd))
        self.play(Create(cajas))
        lab_mcd = MathTex(r"\text{M.C.D.}(12, 18) =", font_size=40).move_to([-6.6, -1.2, 0], aligned_edge=LEFT)
        self.play(Write(lab_mcd))
        piezas_mcd = [d18[0].copy(), t12[0].copy()]
        destinos = [lab_mcd.get_right() + RIGHT * (0.55 + 0.8 * i) for i in range(2)]
        self.play(*[m.animate.move_to(d) for m, d in zip(piezas_mcd, destinos)])
        r_mcd = MathTex(r"= 2 \cdot 3 = 6", font_size=44, color=ACENTO).next_to(piezas_mcd[-1], RIGHT, buff=0.3)
        self.play(Write(r_mcd))
        nota1 = texto("(6 divide a 12 y a 18)", 20, GREY_B).next_to(r_mcd, DOWN, buff=0.1, aligned_edge=LEFT)
        self.play(FadeIn(nota1))
        self.play(FadeOut(cajas))
        self.wait(0.8)

        # --- m.c.m.
        reg_mcm = texto("m.c.m. → TODOS los factores, con el MAYOR exponente", 26, ROSA)
        reg_mcm.move_to([0, -2.1, 0]).to_edge(LEFT, buff=0.6)
        cajas2 = VGroup(
            SurroundingRectangle(VGroup(*d12), color=ROSA, buff=0.1),
            SurroundingRectangle(VGroup(*t18), color=ROSA, buff=0.1),
        )
        self.play(Write(reg_mcm))
        self.play(Create(cajas2))
        lab_mcm = MathTex(r"\text{m.c.m.}(12, 18) =", font_size=40).move_to([-6.6, -3.0, 0], aligned_edge=LEFT)
        self.play(Write(lab_mcm))
        piezas_mcm = [m.copy() for m in d12 + t18]
        destinos = [lab_mcm.get_right() + RIGHT * (0.55 + 0.8 * i) for i in range(4)]
        self.play(*[m.animate.move_to(d) for m, d in zip(piezas_mcm, destinos)])
        r_mcm = MathTex(r"= 2^2 \cdot 3^2 = 36", font_size=44, color=ACENTO).next_to(piezas_mcm[-1], RIGHT, buff=0.3)
        self.play(Write(r_mcm))
        nota2 = texto("(36 es múltiplo de 12 y de 18)", 20, GREY_B).next_to(r_mcm, DOWN, buff=0.1, aligned_edge=LEFT)
        self.play(FadeIn(nota2))
        self.play(FadeOut(cajas2))
        self.wait(2)

        # --- Resumen
        self.play(*[FadeOut(m) for m in self.mobjects if m is not cab])
        tarjetas = VGroup()
        for nombre, l1, l2, col in (("M.C.D.", "factores comunes", "al menor exponente", OK),
                                    ("m.c.m.", "todos los factores", "al mayor exponente", ROSA)):
            caja = RoundedRectangle(width=5.4, height=3.0, corner_radius=0.3, color=col, fill_opacity=0.12)
            txt = VGroup(texto(nombre, 44, col, weight=BOLD), texto(l1, 30), texto(l2, 30)).arrange(DOWN, buff=0.25)
            tarjetas.add(VGroup(caja, txt.move_to(caja)))
        tarjetas.arrange(RIGHT, buff=0.8)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tarjetas], lag_ratio=0.4))
        self.wait(3)


# ---------------------------------------------------------------------------
class ProblemasMcdMcm(Scene):
    def construct(self):
        cab = titulo(self, "¿M.C.D. o m.c.m.?", "Problemas")
        self.cintas(cab)
        self.baldosas(cab)
        self.autobuses(cab)
        self.regla(cab)

    def limpiar(self, cab):
        self.play(*[FadeOut(m) for m in self.mobjects if m is not cab])

    def enunciado(self, cab, cadena):
        t = texto(cadena, 28).next_to(cab, DOWN, buff=0.35).to_edge(LEFT)
        self.play(Write(t), run_time=1.5)
        return t

    def cintas(self, cab):
        self.enunciado(cab, "Tenemos dos cintas de 12 m y 18 m. Queremos cortarlas en\n"
                            "trozos iguales, lo más largos posible, sin que sobre nada.")
        u = 0.38
        x0 = -4.8
        ca = Rectangle(width=12 * u, height=0.5, fill_color=RANA_A, fill_opacity=0.7, stroke_width=0)
        cb = Rectangle(width=18 * u, height=0.5, fill_color=RANA_B, fill_opacity=0.7, stroke_width=0)
        ca.move_to([x0, 0.8, 0], aligned_edge=LEFT)
        cb.move_to([x0, -0.4, 0], aligned_edge=LEFT)
        la = texto("12 m", 26).next_to(ca, LEFT)
        lb = texto("18 m", 26).next_to(cb, LEFT)
        self.play(GrowFromEdge(ca, LEFT), GrowFromEdge(cb, LEFT), FadeIn(la), FadeIn(lb))

        def cortes(trozo, col):
            g = VGroup()
            for cinta, largo in ((ca, 12), (cb, 18)):
                for k in range(trozo, largo, trozo):
                    p = cinta.get_left() + RIGHT * k * u
                    g.add(Line(p + UP * 0.4, p + DOWN * 0.4, color=col, stroke_width=4))
            return g

        # Intento con 4
        c4 = cortes(4, WHITE)
        sobra = Rectangle(width=2 * u, height=0.5, fill_color=MAL, fill_opacity=0.8, stroke_width=0)
        sobra.move_to(cb.get_right(), aligned_edge=RIGHT)
        m4 = texto("Trozos de 4 m: ¡sobran 2 m!", 28, MAL).move_to([0, -1.5, 0])
        self.play(Create(c4))
        self.play(FadeIn(sobra), Write(m4))
        self.wait(1)
        self.play(FadeOut(c4), FadeOut(sobra), FadeOut(m4))

        # Con 6
        c6 = cortes(6, ACENTO)
        m6 = texto("Trozos de 6 m: ¡exacto! (2 + 3 = 5 trozos)", 28, OK).move_to([0, -1.5, 0])
        self.play(Create(c6))
        self.play(Write(m6))
        r = MathTex(r"\text{El mayor divisor comun: } \text{M.C.D.}(12, 18) = 6",
                    font_size=42, color=ACENTO).move_to([0, -2.6, 0])
        self.play(Write(r))
        self.wait(2.5)
        self.limpiar(cab)

    def baldosas(self, cab):
        self.enunciado(cab, "Un suelo mide 12 m × 18 m. Queremos cubrirlo con baldosas\n"
                            "cuadradas iguales, lo más grandes posible.")
        u = 0.24
        suelo = Rectangle(width=18 * u, height=12 * u, color=WHITE).move_to([-2.5, -0.5, 0])
        a = texto("18 m", 24).next_to(suelo, UP, buff=0.15)
        b = texto("12 m", 24).next_to(suelo, LEFT, buff=0.15)
        self.play(Create(suelo), FadeIn(a), FadeIn(b))
        lado = 6 * u
        tiles = VGroup()
        for fila in range(2):
            for col in range(3):
                sq = Square(lado, fill_color=OK, fill_opacity=0.5, stroke_color=WHITE, stroke_width=3)
                sq.move_to(suelo.get_corner(UL) + RIGHT * (col + 0.5) * lado + DOWN * (fila + 0.5) * lado)
                tiles.add(sq)
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.2))
        etiq = texto("6 m", 22).move_to(tiles[0])
        self.play(FadeIn(etiq))
        txt = VGroup(
            texto("Baldosas de 6 m × 6 m", 30, OK),
            texto("2 · 3 = 6 baldosas", 28),
            MathTex(r"\text{M.C.D.}(12, 18) = 6", font_size=44, color=ACENTO),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(suelo, RIGHT, buff=0.9)
        self.play(LaggedStart(*[Write(t) for t in txt], lag_ratio=0.5))
        self.wait(2.5)
        self.limpiar(cab)

    def autobuses(self, cab):
        self.enunciado(cab, "Un autobús pasa cada 12 minutos y otro cada 18. Si salen\n"
                            "juntos ahora, ¿cuándo vuelven a coincidir?")

        def linea(y):
            return NumberLine(x_range=[0, 42, 6], length=11.5, include_numbers=True,
                              font_size=22, stroke_width=2).move_to([0.6, y, 0])

        la, lb = linea(0.5), linea(-1.4)
        ta = texto("Bus A: cada 12 min", 24, RANA_A).next_to(la, UP, buff=0.35).to_edge(LEFT)
        tb = texto("Bus B: cada 18 min", 24, RANA_B).next_to(lb, UP, buff=0.35).to_edge(LEFT)
        self.play(Create(la), Create(lb), FadeIn(ta), FadeIn(tb))

        t = ValueTracker(0)
        cursor = always_redraw(lambda: DashedLine(la.n2p(t.get_value()) + UP * 0.45,
                                                  lb.n2p(t.get_value()) + DOWN * 0.15, color=ACENTO))
        reloj = always_redraw(lambda: Text(f"{int(round(t.get_value()))} min", font_size=24, color=ACENTO)
                              .next_to(la.n2p(t.get_value()) + UP * 0.45, UP, buff=0.05))
        self.add(cursor, reloj)
        puntos = {}
        for linea_, col, key in ((la, RANA_A, "A"), (lb, RANA_B, "B")):
            puntos[(key, 0)] = Dot(linea_.n2p(0) + UP * 0.2, radius=0.12, color=col)
        self.play(FadeIn(puntos[("A", 0)]), FadeIn(puntos[("B", 0)]))

        eventos = [(12, "A"), (18, "B"), (24, "A"), (36, "AB")]
        prev = 0
        for tiempo, quien in eventos:
            self.play(t.animate.set_value(tiempo), run_time=(tiempo - prev) / 9, rate_func=linear)
            prev = tiempo
            anims = []
            for key in quien:
                linea_, col = (la, RANA_A) if key == "A" else (lb, RANA_B)
                d = Dot(linea_.n2p(tiempo) + UP * 0.2, radius=0.12, color=col)
                puntos[(key, tiempo)] = d
                anims += [FadeIn(d, scale=2), Flash(d, color=col)]
            self.play(*anims, run_time=0.6)

        aros = VGroup(*[Circle(radius=0.25, color=ACENTO, stroke_width=4).move_to(puntos[(k, 36)]) for k in "AB"])
        self.play(Create(aros))
        r1 = texto("¡Vuelven a coincidir a los 36 minutos!", 30, OK).move_to([0, -2.5, 0])
        r2 = MathTex(r"\text{El menor multiplo comun: } \text{m.c.m.}(12, 18) = 36",
                     font_size=42, color=ACENTO).move_to([0, -3.3, 0])
        self.play(Write(r1))
        self.play(Write(r2))
        self.wait(2.5)
        self.remove(cursor, reloj)
        self.limpiar(cab)

    def regla(self, cab):
        filas = VGroup()
        for preg, resp, col in (
            ("¿Repartir o cortar en partes iguales,\nlo más GRANDES posible?", "M.C.D.", OK),
            ("¿Coincidir o volver a repetirse,\nlo ANTES posible?", "m.c.m.", ROSA),
        ):
            caja = RoundedRectangle(width=11, height=1.9, corner_radius=0.3, color=col, fill_opacity=0.12)
            p = texto(preg, 30).move_to(caja).shift(LEFT * 1.6)
            flecha = Arrow(LEFT * 0.5, RIGHT * 0.5, color=col).next_to(p, RIGHT, buff=0.5)
            r = texto(resp, 46, col, weight=BOLD).next_to(flecha, RIGHT, buff=0.4)
            filas.add(VGroup(caja, p, flecha, r))
        filas.arrange(DOWN, buff=0.6).shift(DOWN * 0.4)
        for f in filas:
            self.play(FadeIn(f[0]), Write(f[1]))
            self.play(GrowArrow(f[2]), FadeIn(f[3], scale=1.4))
            self.wait(1)
        self.wait(2.5)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
PROBLEMAS = [(60, 90), (24, 36), (18, 30), (20, 50), (28, 42), (45, 75), (16, 40), (12, 18, 30)]
LETRAS = "abcdefgh"


def nombre_numeros(nums):
    return ", ".join(map(str, nums[:-1])) + " y " + str(nums[-1])


def descomponer(n, primero=None):
    """Lista de factores en el orden de las divisiones (opcionalmente forzando el primer divisor)."""
    fs, x = [], n
    while x > 1:
        p = primero if (primero and not fs) else next(d for d in range(2, x + 1) if x % d == 0)
        fs.append(p)
        x //= p
    return fs


def mcd_mcm(nums):
    cs = [Counter(descomponer(n)) for n in nums]
    mcd, mcm = [], []
    for p in sorted(set().union(*cs)):
        mcd += [p] * min(c[p] for c in cs)
        mcm += [p] * max(c[p] for c in cs)
    return mcd, mcm


def motivo(num, p):
    if num == p:
        return f"{p} es primo"
    if p == 2:
        return f"{num} es par"
    if p == 3:
        cif = [int(c) for c in str(num)]
        return " + ".join(map(str, cif)) + f" = {sum(cif)}, múltiplo de 3"
    if p == 5:
        return f"{num} acaba en {str(num)[-1]}"
    return f"{num} : {p} = {num // p}"


def columna(scene, n, origen, primero=None, motivos=False, rt=0.6, dy=0.62, size=42):
    """Anima la columna de divisiones sucesivas. Devuelve (VGroup, factores)."""
    fs = descomponer(n, primero)
    nums, x = [n], n
    for p in fs:
        x //= p
        nums.append(x)
    g = VGroup()
    linea = Line(origen + UP * 0.3, origen + DOWN * ((len(nums) - 1) * dy + 0.3), stroke_width=3)
    scene.play(Create(linea), run_time=rt)
    g.add(linea)
    for i, num in enumerate(nums):
        pt = origen + DOWN * i * dy
        izq = MathTex(str(num), font_size=size).next_to(pt, LEFT, buff=0.25)
        scene.play(FadeIn(izq, shift=DOWN * 0.1), run_time=rt * 0.5)
        g.add(izq)
        if i < len(fs):
            p = fs[i]
            der = MathTex(str(p), font_size=size, color=COLOR_PRIMO[p]).next_to(pt, RIGHT, buff=0.25)
            anims = [FadeIn(der, scale=1.3)]
            g.add(der)
            if motivos:
                m = texto(motivo(num, p), 18, GREY_B).move_to(pt + RIGHT * 0.9, aligned_edge=LEFT)
                anims.append(FadeIn(m))
                g.add(m)
            scene.play(*anims, run_time=rt)
    return g, fs


def linea_factorizacion(n, fs, size=40):
    return VGroup(MathTex(f"{n} =", font_size=size), tex_potencias(fs, size, prefijo="")).arrange(RIGHT, buff=0.15)


def fila_resultado(nombre, nums, fs, regla=None, size=40):
    valor = 1
    for p in fs:
        valor *= p
    args = ", ".join(map(str, nums))
    partes = [MathTex(r"\text{" + nombre + "}(" + args + ") =", font_size=size)]
    if len(fs) > 1:
        partes.append(tex_potencias(fs, size, prefijo=""))
        partes.append(MathTex("=", str(valor), font_size=size, color=ACENTO))
    else:
        partes.append(MathTex(str(valor), font_size=size, color=ACENTO))
    partes[-1].valor = partes[-1][-1]  # el número, para enmarcarlo
    if regla:
        partes.append(texto(regla, 20, GREY_B))
    return VGroup(*partes).arrange(RIGHT, buff=0.18)


def resolver_mcd_mcm(scene, nums, y_mcd, y_mcm, reglas=False, rt=1.0):
    mcd, mcm = mcd_mcm(nums)
    f1 = fila_resultado("M.C.D.", nums, mcd, "(comunes, al menor exponente)" if reglas else None)
    f2 = fila_resultado("m.c.m.", nums, mcm, "(todos, al mayor exponente)" if reglas else None)
    f1.move_to([0, y_mcd, 0])
    f2.move_to([0, y_mcm, 0])
    for f in (f1, f2):
        scene.play(Write(f), run_time=rt * 1.5)
    idx_valor = -2 if reglas else -1
    cajas = VGroup(*[SurroundingRectangle(f[idx_valor].valor, color=ACENTO, buff=0.1) for f in (f1, f2)])
    scene.play(Create(cajas), run_time=rt * 0.6)
    return VGroup(f1, f2, cajas)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Factores primos, M.C.D. y m.c.m.")

        # --- Enunciados
        ins = texto("Descompón en factores primos y calcula el M.C.D. y el m.c.m.:", 28)
        ins.next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        items = VGroup(*[texto(f"{l})   {nombre_numeros(p)}", 36) for l, p in zip(LETRAS, PROBLEMAS)])
        items.arrange_in_grid(rows=4, cols=2, flow_order="dr", col_alignments="ll", buff=(2.5, 0.5))
        items.next_to(ins, DOWN, buff=0.6).set_x(0)
        self.play(Write(ins))
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.15))
        pausa = texto("¡Pausa el vídeo e inténtalo!", 28, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(pausa))
        self.wait(2.5)
        self.play(Indicate(items[0], color=ACENTO, scale_factor=1.3))
        self.play(*[FadeOut(m) for m in [ins, pausa, *items[1:]]])

        sub = texto("Ejemplo resuelto:  a)  60 y 90", 32, ACENTO).next_to(cab, RIGHT, buff=0.6)
        self.play(ReplacementTransform(items[0], sub))

        # --- 60 por dos caminos
        l1 = texto("Camino 1: empezamos dividiendo por 2", 24, COLOR_PRIMO[2]).move_to([-3.5, 2.5, 0])
        l2 = texto("Camino 2: empezamos dividiendo por 5", 24, COLOR_PRIMO[5]).move_to([3.5, 2.5, 0])
        self.play(FadeIn(l1))
        col1, f1 = columna(self, 60, np.array([-4.6, 1.7, 0]), primero=2, motivos=True)
        self.play(FadeIn(l2))
        col2, f2 = columna(self, 60, np.array([2.4, 1.7, 0]), primero=5, motivos=True)

        r1 = tex_factores(60, f1, 40)[0].move_to([-3.5, -1.6, 0])
        r2 = tex_factores(60, f2, 40)[0].move_to([3.5, -1.6, 0])
        self.play(Write(r1), Write(r2))
        self.wait(0.5)
        p1 = linea_factorizacion(60, sorted(f1), 44).move_to([-3.5, -2.5, 0])
        p2 = linea_factorizacion(60, sorted(f2), 44).move_to([3.5, -2.5, 0])
        ordenar = texto("ordenamos", 22, GREY_B).move_to([0, -2.05, 0])
        self.play(FadeIn(ordenar), TransformFromCopy(r1, p1), TransformFromCopy(r2, p2))
        msg = texto("¡Los mismos factores! No importa por dónde empecemos.", 30, ACENTO).to_edge(DOWN, buff=0.3)
        self.play(Write(msg), Circumscribe(p1, color=ACENTO), Circumscribe(p2, color=ACENTO))
        self.wait(2.5)

        # --- 90
        self.play(*[FadeOut(m) for m in [l1, l2, col1, col2, r1, r2, p2, ordenar, msg]])
        self.play(p1.animate.scale(0.9).move_to([3.0, 1.2, 0]))
        col3, f3 = columna(self, 90, np.array([-4.6, 1.9, 0]), motivos=True)
        p3 = linea_factorizacion(90, sorted(f3), 40).next_to(p1, DOWN, buff=0.4).align_to(p1, LEFT)
        self.play(TransformFromCopy(col3, p3))
        self.wait(0.8)

        # --- M.C.D. y m.c.m.
        self.play(FadeOut(col3), VGroup(p1, p3).animate.move_to([0, 1.4, 0]))
        resolver_mcd_mcm(self, (60, 90), -0.3, -1.5, reglas=True)
        self.wait(1)
        sig = texto("En el siguiente vídeo resolvemos el resto.", 26, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(sig))
        self.wait(2.5)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Apartados b) a h)")
        for letra, nums in list(zip(LETRAS, PROBLEMAS))[1:]:
            sub = texto(f"{letra})  {nombre_numeros(nums)}", 34, ACENTO).next_to(cab, RIGHT, buff=0.6)
            self.play(FadeIn(sub, shift=DOWN * 0.2))
            xs = [-2.8, 3.2] if len(nums) == 2 else [-4.4, 0.4, 5.2]
            objs = VGroup()
            for x, n in zip(xs, nums):
                col, fs = columna(self, n, np.array([x, 2.2, 0]), rt=0.4, dy=0.6)
                fac = linea_factorizacion(n, sorted(fs), 40).move_to([x, -0.9, 0])
                self.play(Write(fac), run_time=0.8)
                objs.add(col, fac)
            res = resolver_mcd_mcm(self, nums, -2.1, -3.1, rt=0.8)
            self.wait(2)
            self.play(FadeOut(objs), FadeOut(res), FadeOut(sub))
        fin = texto("¡Muy bien! Ahora ya sabes calcular el M.C.D. y el m.c.m.", 32, ACENTO)
        self.play(Write(fin))
        self.wait(2)
