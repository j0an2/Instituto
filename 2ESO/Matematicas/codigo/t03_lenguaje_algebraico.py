"""Tema 3 · Lenguaje algebraico (2º ESO)

Sigue el índice del libro: expresiones algebraicas · monomios · polinomios · suma y resta de polinomios ·
multiplicación y potencias de polinomios · identidades notables (en el libro, con GeoGebra; aquí con áreas).

Escenas:
    ExpresionesAlgebraicas  – del lenguaje común al algebraico, el perímetro de un rectángulo, valor numérico
    Monomios                – coeficiente, parte literal, grado; semejantes (con fichas); producto y cociente
    Polinomios              – términos, grado, término independiente, ordenar y completar, valor numérico, raíz
    SumaRestaPolinomios     – en columnas por grado (con hueco si falta un término); restar = sumar el opuesto
    MultiplicarPolinomios   – monomio · polinomio (flechas), polinomio · polinomio (tabla de áreas), (x + 2)²
    IdentidadesNotables     – (a + b)², (a − b)² y (a + b)(a − b) con piezas de un cuadrado
    IdentidadesEjemplos     – usarlas con x, el error (x + 3)² ≠ x² + 9, al revés y cálculo mental (21², 31 · 29)
    EjerciciosEjemplo       – enunciados de los 10 ejercicios y el apartado a) de cada uno
    EjerciciosResueltos1/2  – el resto de apartados (1–5 y 6–10)

Página interactiva E2 (detrás de IdentidadesNotables): interactivos/identidades_notables.html
Página interactiva E1 (detrás de MultiplicarPolinomios): interactivos/multiplicar_polinomios.html

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t03_lenguaje_algebraico.py IdentidadesNotables
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t03_lenguaje_algebraico.py
"""
import os
import sys

COMUN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from t09_potencias_raices import Notas, limpiar, subtitulo  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 3 · Lenguaje algebraico"
TITULOS = {
    "ExpresionesAlgebraicas": "Expresiones algebraicas y valor numérico",
    "Monomios": "Monomios",
    "Polinomios": "Polinomios",
    "SumaRestaPolinomios": "Suma y resta de polinomios",
    "MultiplicarPolinomios": "Multiplicación y potencias de polinomios",
    "IdentidadesNotables": "Identidades notables con áreas",
    "IdentidadesEjemplos": "Identidades notables: ejemplos y trucos",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 5)",
    "EjerciciosResueltos2": "Ejercicios resueltos (6 a 10)",
}
INTERACTIVOS = [("E2", "Pruébalo tú: identidades notables", "interactivos/identidades_notables.html",
                 "IdentidadesNotables"),
               ("E1", "Pruébalo tú: multiplicar polinomios", "interactivos/multiplicar_polinomios.html",
                "MultiplicarPolinomios")]

ROSA = "#FF79C6"
LETRA = ACENTO                      # la x (y las letras) en amarillo
COEF = BASE                         # coeficiente azul
GRADO_COL = {4: "#C39BD3", 3: "#FF9F43", 2: "#5DADE2", 1: "#7BD88F", 0: "#E8E8E8"}
# identidades notables: a azul, b rosa, ab verde
A_COL, B_COL, AB_COL = "#5DADE2", ROSA, "#7BD88F"


def tarjeta(contenido, color=ACENTO, buff=0.3):
    r = SurroundingRectangle(contenido, color=color, buff=buff, corner_radius=0.15,
                             fill_color=color, fill_opacity=0.08)
    return VGroup(r, contenido)


def X(s, size=48, letras=("x",), color=LETRA):
    """MathTex con las letras coloreadas (no usar con \\frac ni \\text)."""
    t = MathTex(s, font_size=size, substrings_to_isolate=list(letras))
    for l in letras:
        t.set_color_by_tex(l, color)
    return t


def lineas(scene, textos, x, y, dy=0.9, size=48, rt=1.0, espera=0.6):
    """Escribe una columna de MathTex alineadas a la izquierda; devuelve el VGroup."""
    g = VGroup()
    for i, s in enumerate(textos):
        m = s if isinstance(s, Mobject) else MathTex(s, font_size=size)
        m.move_to([x, y - i * dy, 0], aligned_edge=LEFT)
        scene.play(Write(m), run_time=rt)
        scene.wait(espera)
        g.add(m)
    return g


# ---------------------------------------------------------------------------
# Polinomios: un término por grado, coloreado por grado
def term_tex(c, d, primero=False, letra="x"):
    s = "-" if c < 0 else ("" if primero else "+")
    a = abs(c)
    if d == 0:
        return s + str(a)
    return s + ("" if a == 1 else str(a)) + letra + ("" if d == 1 else "^{%d}" % d)


def term(c, d, primero=False, size=48):
    return MathTex(term_tex(c, d, primero), font_size=size, color=GRADO_COL[d])


def pol_tex(coefs):
    """'3x^{3}-2x^{2}+5x-1' a partir de {grado: coeficiente}."""
    s, primero = "", True
    for d in sorted(coefs, reverse=True):
        if coefs[d]:
            s += term_tex(coefs[d], d, primero)
            primero = False
    return s or "0"


def pol(coefs, size=48):
    """MathTex de un polinomio con cada término de su color."""
    partes, grados, primero = [], [], True
    for d in sorted(coefs, reverse=True):
        if coefs[d]:
            partes.append(term_tex(coefs[d], d, primero))
            grados.append(d)
            primero = False
    t = MathTex(*partes, font_size=size)
    for p, d in zip(t, grados):
        p.set_color(GRADO_COL[d])
    return t


def fila_pol(coefs, y, cols, size=48):
    """Términos colocados en columnas por grado: {grado: mobject}."""
    salida, primero = {}, True
    for d in sorted(cols, reverse=True):
        c = coefs.get(d, 0)
        if c:
            salida[d] = term(c, d, primero, size).move_to([cols[d], y, 0])
            primero = False
    return salida


def suma_columnas(scene, notas, P, Q, cols, etiquetas, y0=1.4, signo="+", nota_hueco=True):
    """P y Q en columnas, raya y resultado término a término. Devuelve el VGroup de todo."""
    fp = fila_pol(P, y0, cols)
    fq = fila_pol(Q, y0 - 1.0, cols)
    xe = min(cols.values()) - 1.9
    eP = MathTex(etiquetas[0], font_size=44).move_to([xe, y0, 0])
    eQ = MathTex(etiquetas[1], font_size=44).move_to([xe, y0 - 1.0, 0])
    sg = MathTex(signo, font_size=48).move_to([xe - 1.1, y0 - 1.0, 0])
    raya = Line([xe - 1.4, y0 - 1.55, 0], [max(cols.values()) + 0.9, y0 - 1.55, 0], stroke_width=3)
    scene.play(Write(eP), *[Write(m) for m in fp.values()])
    scene.play(Write(eQ), Write(sg), *[Write(m) for m in fq.values()])
    huecos = [d for d in cols if d not in Q or not Q[d]]
    if huecos and nota_hueco:
        d = huecos[0]
        caja = DashedVMobject(Square(0.8, color=GREY_B)).move_to([cols[d], y0 - 1.0, 0])
        scene.play(Create(caja))
        notas("Si falta un término, dejamos su hueco: así cada grado queda en su columna")
        scene.wait(1.5)
        scene.play(FadeOut(caja))
    else:
        notas("Cada grado en su columna: solo se suman los términos semejantes")
    scene.play(Create(raya))
    res, primero = VGroup(), True
    total = {d: P.get(d, 0) + Q.get(d, 0) for d in cols}
    for d in sorted(cols, reverse=True):
        col = VGroup(*[f[d] for f in (fp, fq) if d in f])
        scene.play(Indicate(col, color=GRADO_COL[d], scale_factor=1.15), run_time=0.6)
        if total[d]:
            r = term(total[d], d, primero).move_to([cols[d], y0 - 2.15, 0])
            primero = False
            scene.play(FadeIn(r, shift=DOWN * 0.2), run_time=0.6)
            res.add(r)
        else:
            cero = MathTex("0", font_size=40, color=GREY_B).move_to([cols[d], y0 - 2.15, 0])
            scene.play(FadeIn(cero), run_time=0.4)
            scene.play(FadeOut(cero), run_time=0.4)
    eR = MathTex(etiquetas[2], font_size=44).move_to([xe, y0 - 2.15, 0])
    scene.play(Write(eR))
    return VGroup(eP, eQ, sg, raya, eR, res, *fp.values(), *fq.values()), fq, total


# ---------------------------------------------------------------------------
# Tabla de áreas para multiplicar
def tabla_producto(scene, cab_col, cab_fil, celdas, centro, w=1.9, h=1.0, size=40, rt=0.7):
    """cab_col / cab_fil: listas de (tex, color); celdas[i][j]: (tex, color).
    Dibuja la tabla, rellena casilla a casilla y devuelve (VGroup tabla, lista de casillas)."""
    nf, nc = len(cab_fil), len(cab_col)
    x0, y0 = centro[0] - nc * w / 2, centro[1] + nf * h / 2
    rects = [[Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=2)
              .move_to([x0 + (j + 0.5) * w, y0 - (i + 0.5) * h, 0]) for j in range(nc)] for i in range(nf)]
    hc = [MathTex(t, font_size=size, color=c).move_to([x0 + (j + 0.5) * w, y0 + 0.4, 0])
          for j, (t, c) in enumerate(cab_col)]
    hf = [MathTex(t, font_size=size, color=c).move_to([x0 - 0.55, y0 - (i + 0.5) * h, 0], aligned_edge=RIGHT)
          for i, (t, c) in enumerate(cab_fil)]
    for m in hf:
        m.next_to([x0, m.get_center()[1], 0], LEFT, buff=0.25)
    todo = VGroup(*[r for f in rects for r in f], *hc, *hf)
    scene.play(LaggedStart(*[Create(r) for f in rects for r in f], lag_ratio=0.1),
               *[Write(m) for m in hc + hf], run_time=1.5)
    contenido = []
    for i in range(nf):
        for j in range(nc):
            t, c = celdas[i][j]
            m = MathTex(t, font_size=size, color=c).move_to(rects[i][j])
            scene.play(Indicate(hf[i], scale_factor=1.25), Indicate(hc[j], scale_factor=1.25),
                       rects[i][j].animate.set_fill(c, 0.18), run_time=rt)
            scene.play(FadeIn(m, scale=0.7), run_time=rt * 0.7)
            contenido.append(m)
            todo.add(m)
    return todo, contenido


class ExpresionesAlgebraicas(Scene):
    def construct(self):
        cab = titulo(self, "Expresiones algebraicas")
        notas = Notas(self)

        # --- Del lenguaje común al algebraico
        subtitulo(self, cab, "Letras en lugar de números")
        notas("Una letra representa un número que no conocemos o que puede cambiar")
        filas = [("El doble de un número", "2x"), ("Un número más 5", "x+5"),
                 ("El triple de un número menos 4", "3x-4"), ("El cuadrado de un número", "x^{2}"),
                 ("Dos números consecutivos", "x,\\ x+1"), ("La mitad de un número", None)]
        y = 2.0
        for frase, tex in filas:
            t = texto(frase, 30).move_to([-2.4, y, 0])
            fl = Arrow([0.7, y, 0], [1.9, y, 0], buff=0, stroke_width=4, color=GREY_B,
                       max_tip_length_to_length_ratio=0.25)
            if tex:
                m = X(tex, 50).move_to([2.3, y, 0], aligned_edge=LEFT)
            else:
                m = fraccion("x", 2, size=40, colores=False).move_to([2.3, y, 0], aligned_edge=LEFT)
                m[0].set_color(LETRA)
            self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.6)
            self.play(GrowArrow(fl), Write(m), run_time=0.7)
            self.wait(0.6)
            y -= 0.82
        notas("Entre un número y una letra no se escribe el punto: 2 · x = 2x")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- El perímetro de un rectángulo
        subtitulo(self, cab, "Una fórmula con letras")
        r = Rectangle(width=4.4, height=2.2, stroke_color=WHITE, fill_color=BASE, fill_opacity=0.25).move_to([-3.4, 0.2, 0])
        lx = X("x", 44).next_to(r, LEFT, buff=0.2)
        lx3 = X("x+3", 44).next_to(r, DOWN, buff=0.2)
        self.play(Create(r), Write(lx), Write(lx3))
        notas("Un lado mide x y el otro 3 cm más: x + 3")
        p = VGroup(X("P = x + (x+3) + x + (x+3)", 44), X("P = 2x + 2(x+3)", 44)).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        p.move_to([2.9, 1.0, 0])
        self.play(Write(p[0]))
        self.wait(1)
        self.play(Write(p[1]))
        notas("La expresión sirve para cualquier rectángulo de este tipo")
        self.wait(2)

        # --- Valor numérico
        notas("Si x = 4, sustituimos la letra por el número: es el valor numérico")
        lx_n = MathTex("4", font_size=44, color=LETRA).move_to(lx)
        lx3_n = MathTex("4+3=7", font_size=44, color=LETRA).move_to(lx3)
        self.play(ReplacementTransform(lx, lx_n), ReplacementTransform(lx3, lx3_n))
        v = VGroup(MathTex("P = 2\\cdot 4 + 2\\cdot(4+3)", font_size=44),
                   MathTex("= 8 + 14 = 22\\ \\text{cm}", font_size=44)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        v.next_to(p, DOWN, buff=0.6, aligned_edge=LEFT)
        for i, k in [(0, 2), (0, 9)]:
            pass
        self.play(Write(v[0]))
        self.play(Write(v[1]))
        self.play(Circumscribe(v[1], color=ACENTO))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Más valores numéricos
        subtitulo(self, cab, "Valor numérico")
        e = X("3x - 4", 60).move_to([0, 2.0, 0])
        self.play(Write(e))
        casos = [("x = 5", "3\\cdot 5 - 4 = 15 - 4 = 11"),
                 ("x = -2", "3\\cdot(-2) - 4 = -6 - 4 = -10"),
                 ("x = 0", "3\\cdot 0 - 4 = -4")]
        y = 0.7
        for c, cuenta in casos:
            a = X(c, 44).move_to([-4.6, y, 0])
            b = MathTex(cuenta, font_size=44).move_to([-2.4, y, 0], aligned_edge=LEFT)
            self.play(Write(a), run_time=0.6)
            self.play(Write(b), run_time=1.2)
            self.wait(0.8)
            y -= 1.0
        notas("Los números negativos, siempre entre paréntesis al sustituir")
        self.wait(2.5)
        notas.fin()


class Monomios(Scene):
    def construct(self):
        cab = titulo(self, "Monomios")
        notas = Notas(self)

        # --- Partes de un monomio
        subtitulo(self, cab, "Partes de un monomio")
        m = M(("-5", COEF), ("x", LETRA), ("^{2}", EXPONENTE), ("y", LETRA), size=110).move_to([0, 1.0, 0])
        self.play(Write(m))
        notas("Un monomio es un número multiplicado por letras: −5 · x · x · y")
        self.wait(1.5)
        b1 = Brace(m[0], DOWN, color=COEF)
        t1 = texto("coeficiente", 26, COEF).next_to(b1, DOWN, buff=0.1).shift(LEFT * 0.35)
        b2 = Brace(m[1:], DOWN, color=LETRA)
        t2 = texto("parte literal", 26, LETRA).next_to(b2, DOWN, buff=0.1).shift(RIGHT * 0.35)
        self.play(GrowFromCenter(b1), FadeIn(t1))
        self.play(GrowFromCenter(b2), FadeIn(t2))
        self.wait(1)
        g = MathTex("\\text{grado} = 2 + 1 = 3", font_size=48).move_to([0, -2.0, 0])
        g[0][6].set_color(EXPONENTE)
        uno = MathTex("1", font_size=44, color=EXPONENTE).next_to(m[3], UR, buff=0.08).shift(DOWN * 0.15)
        self.play(FadeIn(uno, scale=1.5))
        notas("El grado es la suma de los exponentes de las letras (la y lleva un 1 invisible)")
        self.play(Write(g))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Tabla de ejemplos
        subtitulo(self, cab, "Ejemplos")
        xs = [-4.5, -1.5, 1.5, 4.5]
        cabs = ["monomio", "coeficiente", "parte literal", "grado"]
        colores = [WHITE, COEF, LETRA, EXPONENTE]
        hdr = VGroup(*[texto(c, 26, col).move_to([x, 2.0, 0]) for c, x, col in zip(cabs, xs, colores)])
        raya = Line([-6, 1.65, 0], [6, 1.65, 0], color=GREY_B, stroke_width=2)
        self.play(FadeIn(hdr), Create(raya))
        filas = [("7x^{3}", "7", "x^{3}", "3", None),
                 ("-a", "-1", "a", "1", "−a: el coeficiente es −1 (el 1 no se escribe)"),
                 ("\\tfrac{2}{3}xy^{2}", "\\tfrac{2}{3}", "xy^{2}", "1+2=3", None),
                 ("4", "4", "\\text{---}", "0", "Un número solo también es un monomio, de grado 0")]
        y = 1.05
        for fila in filas:
            celdas = [MathTex(s, font_size=44, color=c).move_to([x, y, 0]) for s, x, c in zip(fila[:4], xs, colores)]
            self.play(Write(celdas[0]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in celdas[1:]], lag_ratio=0.3), run_time=1.2)
            if fila[4]:
                notas(fila[4])
            self.wait(1.2)
            y -= 0.85
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # --- Semejantes y suma
        subtitulo(self, cab, "Monomios semejantes")
        pares = [("3x^{2},\\quad -5x^{2}", True), ("4ab,\\quad 7ba", True), ("3x^{2},\\quad 3x", False)]
        y = 2.0
        marcas = VGroup()
        for s, ok in pares:
            t = MathTex(s, font_size=46).move_to([-2.2, y, 0])
            mk = MathTex("\\checkmark" if ok else "\\times", font_size=60, color=OK if ok else MAL).next_to(t, RIGHT, buff=0.6)
            self.play(Write(t), run_time=0.7)
            self.play(FadeIn(mk, scale=1.4), run_time=0.4)
            marcas.add(t, mk)
            y -= 0.8
        notas("Semejantes: tienen la misma parte literal (el coeficiente puede cambiar)")
        self.wait(2.5)
        self.play(FadeOut(marcas))

        notas("Solo se pueden sumar o restar los semejantes: como contar fichas iguales")

        def ficha_x2(col=BASE):
            return VGroup(Square(0.62, stroke_color=WHITE, stroke_width=2, fill_color=col, fill_opacity=0.8),
                          MathTex("x^{2}", font_size=26))

        def ficha_x(col=GREEN):
            r = Rectangle(width=0.3, height=0.62, stroke_color=WHITE, stroke_width=2, fill_color=col, fill_opacity=0.8)
            return VGroup(r, MathTex("x", font_size=26).move_to(r))

        def ponel(n, f):
            for i in range(n):
                f(i)

        a = VGroup(*[ficha_x2() for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to([-4.4, 1.6, 0])
        b = VGroup(*[ficha_x2() for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0.6, 1.6, 0])
        mas = MathTex("+", font_size=56).move_to([-2.65, 1.6, 0])
        self.play(LaggedStart(*[FadeIn(f, scale=0.6) for f in a], lag_ratio=0.15), Write(mas),
                  LaggedStart(*[FadeIn(f, scale=0.6) for f in b], lag_ratio=0.15))
        e1 = MathTex("3x^{2}", "+", "5x^{2}", "=", "8x^{2}", font_size=54).move_to([-2.6, 0.3, 0])
        self.play(Write(e1[:3]))
        junto = VGroup(*[ficha_x2() for _ in range(8)]).arrange(RIGHT, buff=0.12).move_to([3.3, 0.3, 0])
        self.play(ReplacementTransform(VGroup(*a, *b), junto), FadeOut(mas), run_time=1.2)
        self.play(Write(e1[3:]))
        self.play(Circumscribe(e1[4], color=ACENTO))
        self.wait(1)
        e2 = MathTex("7x - 2x = 5x", font_size=54).move_to([-2.6, -0.7, 0])
        self.play(Write(e2))
        self.wait(1)
        e3 = MathTex("3x^{2} + 5x", font_size=54).move_to([-2.5, -1.8, 0])
        fichas = VGroup(*[ficha_x2() for _ in range(3)], *[ficha_x() for _ in range(5)]).arrange(RIGHT, buff=0.12)
        fichas.move_to([2.6, -1.8, 0])
        self.play(Write(e3), FadeIn(fichas))
        notas("3x² y 5x no son semejantes: no se pueden juntar, se queda así", color=MAL)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Producto y cociente
        subtitulo(self, cab, "Multiplicar y dividir monomios")
        notas("Multiplicamos coeficientes por coeficientes y letras por letras (se suman los exponentes)")
        pr = VGroup(
            M(("(3x^{2})\\cdot(4x^{3})", None), ("=", None), ("(3\\cdot 4)", COEF), ("\\cdot", None),
              ("(x^{2}\\cdot x^{3})", LETRA), ("=", None), ("12x^{5}", ACENTO), size=48),
            M(("(-2ab)\\cdot(5a^{2})", None), ("=", None), ("-10", COEF), ("a^{3}b", LETRA), size=48),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, 1.3, 0])
        for f in pr:
            self.play(Write(f), run_time=2)
            self.wait(1.2)
        notas("Para dividir: coeficientes entre coeficientes y se restan los exponentes")
        co = VGroup(MathTex("12x^{5} : 4x^{2} = 3x^{3}", font_size=48),
                    MathTex("6x^{2}y : 2x = 3xy", font_size=48)).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        co.next_to(pr, DOWN, buff=0.7).align_to(pr, LEFT)
        for f in co:
            self.play(Write(f), run_time=1.5)
            self.wait(1.2)
        self.wait(2)
        notas.fin()


class Polinomios(Scene):
    def construct(self):
        cab = titulo(self, "Polinomios")
        notas = Notas(self)

        subtitulo(self, cab, "Partes de un polinomio")
        P = {4: 3, 2: -2, 1: 1, 0: -7}
        e = VGroup(MathTex("P(x) =", font_size=64), pol(P, 64)).arrange(RIGHT, buff=0.25).move_to([0, 1.3, 0])
        self.play(Write(e))
        notas("Un polinomio es una suma de monomios: cada uno es un término")
        cajas = VGroup(*[SurroundingRectangle(t, color=GRADO_COL[d], buff=0.08) for t, d in zip(e[1], [4, 2, 1, 0])])
        self.play(LaggedStart(*[Create(c) for c in cajas], lag_ratio=0.3))
        self.wait(1.5)
        self.play(FadeOut(cajas))
        datos = [("grado", "4", "el mayor de los grados de sus términos", e[1][0]),
                 ("coeficiente principal", "3", "el del término de mayor grado", e[1][0]),
                 ("término independiente", "-7", "el que no tiene letra", e[1][3])]
        y = -0.1
        for nombre, valor, expl, obj in datos:
            t = VGroup(texto(nombre + ":", 30, GREY_B), MathTex(valor, font_size=46, color=ACENTO),
                       texto("(" + expl + ")", 22, GREY_B)).arrange(RIGHT, buff=0.3).move_to([0, y, 0])
            self.play(Indicate(obj, color=ACENTO), FadeIn(t, shift=UP * 0.2))
            self.wait(1.2)
            y -= 0.75
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # --- Nombres según los términos
        subtitulo(self, cab, "Según el número de términos")
        nombres = [("monomio", "5x^{3}"), ("binomio", "x+1"), ("trinomio", "x^{2}-3x+2"),
                   ("polinomio", "3x^{4}-2x^{2}+x-7")]
        y = 1.8
        for n, s in nombres:
            a = texto(n, 32, ACENTO).move_to([-3.2, y, 0])
            b = X(s, 50).move_to([0.2, y, 0], aligned_edge=LEFT)
            self.play(FadeIn(a), Write(b), run_time=0.8)
            y -= 0.95
        self.wait(2)
        limpiar(self, cab)

        # --- Ordenar y completar
        subtitulo(self, cab, "Ordenar y completar")
        q = MathTex("Q(x) =", "5", "+2x^{3}", "-x", font_size=60).move_to([0, 1.6, 0])
        self.play(Write(q))
        notas("Lo escribimos ordenado: de mayor a menor grado")
        q2 = MathTex("Q(x) =", "2x^{3}", "-x", "+5", font_size=60).move_to([0, 0.3, 0])
        self.play(TransformFromCopy(q[0], q2[0]), TransformFromCopy(q[2], q2[1]),
                  TransformFromCopy(q[3], q2[2]), TransformFromCopy(q[1], q2[3]), run_time=1.5)
        self.wait(1.5)
        notas("Falta el término en x²: si lo escribimos con coeficiente 0, queda completo")
        q3 = MathTex("Q(x) =", "2x^{3}", "+0x^{2}", "-x", "+5", font_size=60).move_to([0, -1.0, 0])
        q3[2].set_color(ACENTO)
        self.play(TransformFromCopy(q2[0], q3[0]), TransformFromCopy(q2[1], q3[1]), TransformFromCopy(q2[2], q3[3]),
                  TransformFromCopy(q2[3], q3[4]), run_time=1.2)
        self.play(FadeIn(q3[2], scale=1.4))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Valor numérico
        subtitulo(self, cab, "Valor numérico")
        e = VGroup(MathTex("P(x) =", font_size=52), pol(P, 52)).arrange(RIGHT, buff=0.2).move_to([0, 2.1, 0])
        self.play(Write(e))
        notas("P(2): cambiamos cada x por 2 y operamos")
        lineas(self, ["P(2) = 3\\cdot 2^{4} - 2\\cdot 2^{2} + 2 - 7",
                      "= 3\\cdot 16 - 2\\cdot 4 + 2 - 7",
                      "= 48 - 8 + 2 - 7 = 35"], -4.6, 0.9, dy=0.85, size=44)
        notas("P(−1): el −1 entre paréntesis")
        lineas(self, ["P(-1) = 3\\cdot(-1)^{4} - 2\\cdot(-1)^{2} + (-1) - 7 = -7"], -4.6, -1.8, size=44)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        subtitulo(self, cab, "Raíces")
        r = VGroup(MathTex("R(x) = x^{2} - 4", font_size=56),
                   MathTex("R(2) = 2^{2} - 4 = 0", font_size=56)).arrange(DOWN, buff=0.6).move_to([0, 0.8, 0])
        self.play(Write(r[0]))
        self.play(Write(r[1]))
        notas("Si el valor numérico es 0, ese número es una raíz del polinomio: 2 es raíz de R(x)")
        self.play(Circumscribe(r[1], color=ACENTO))
        self.wait(3)
        notas.fin()


class SumaRestaPolinomios(Scene):
    def construct(self):
        cab = titulo(self, "Suma y resta de polinomios")
        notas = Notas(self)
        P = {3: 3, 2: -2, 1: 5, 0: -1}
        Q = {3: 1, 2: 4, 0: -6}
        cols = {3: -0.6, 2: 1.3, 1: 3.0, 0: 4.6}

        st = subtitulo(self, cab, "Suma")
        enun = VGroup(MathTex("P(x) =", font_size=42), pol(P, 42), MathTex("\\qquad Q(x) =", font_size=42),
                      pol(Q, 42)).arrange(RIGHT, buff=0.2).move_to([0, 2.4, 0])
        self.play(Write(enun))
        notas("Colocamos un polinomio debajo del otro, cada grado en su columna")
        todo, _, total = suma_columnas(self, notas, P, Q, cols, ("P(x)", "Q(x)", "P(x)+Q(x)"), y0=1.3)
        self.wait(1)
        notas("P(x) + Q(x) = 4x³ + 2x² + 5x − 7")
        self.wait(2.5)
        notas.fin()
        self.play(FadeOut(todo))

        # --- Resta
        self.play(FadeOut(st))
        st = subtitulo(self, cab, "Resta")
        notas("Restar es sumar el opuesto: cambiamos el signo de TODOS los términos de Q(x)")
        Qn = {d: -c for d, c in Q.items()}
        fq = fila_pol(Q, 1.3, cols)
        eq = MathTex("Q(x)", font_size=44).move_to([min(cols.values()) - 1.9, 1.3, 0])
        self.play(Write(eq), *[Write(m) for m in fq.values()])
        fqn = fila_pol(Qn, 0.3, cols)
        eqn = MathTex("-Q(x)", font_size=44).move_to([min(cols.values()) - 1.9, 0.3, 0])
        self.play(TransformFromCopy(eq, eqn), *[TransformFromCopy(fq[d], fqn[d]) for d in fq], run_time=1.5)
        self.play(*[Flash(m.get_left(), color=ACENTO, flash_radius=0.25) for m in fqn.values()])
        self.wait(1.5)
        self.play(FadeOut(VGroup(eq, *fq.values(), eqn, *fqn.values())))
        notas.fin()
        todo, _, total = suma_columnas(self, notas, P, Qn, cols, ("P(x)", "-Q(x)", "P(x)-Q(x)"), y0=1.3,
                                       nota_hueco=False)
        notas("P(x) − Q(x) = 2x³ − 6x² + 5x + 5")
        self.wait(2)
        notas("Cuidado: el −6 de Q(x) pasa a ser +6", color=ROSA)
        self.wait(2.5)
        notas.fin()
        self.play(FadeOut(todo))

        # --- En línea
        self.play(FadeOut(st), FadeOut(enun))
        subtitulo(self, cab, "Sin columnas")
        notas("También se puede hacer en línea: quitamos paréntesis y juntamos los semejantes")
        lineas(self, [
            "(2x^{2} - 3x + 1) - (x^{2} + 4x - 5)",
            "= 2x^{2} - 3x + 1 - x^{2} - 4x + 5",
            "= x^{2} - 7x + 6"], -4.6, 1.6, dy=1.0, size=50, rt=1.5, espera=1.2)
        self.wait(2.5)
        notas.fin()


class MultiplicarPolinomios(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicación de polinomios")
        notas = Notas(self)

        # --- Monomio por polinomio
        subtitulo(self, cab, "Monomio por polinomio")
        e = MathTex("2x", "\\cdot", "(", "3x^{2}", "-x", "+4", ")", font_size=64).move_to([0, 1.3, 0])
        e[0].set_color(ACENTO)
        self.play(Write(e))
        notas("Propiedad distributiva: el 2x multiplica a cada término del paréntesis")
        res = MathTex("=", "6x^{3}", "-2x^{2}", "+8x", font_size=64).move_to([0, -0.6, 0])
        for k, d in zip(range(3), [3, 2, 1]):
            res[k + 1].set_color(GRADO_COL[d])
        self.play(Write(res[0]))
        for k in range(3):
            fl = CurvedArrow(e[0].get_top() + UP * 0.1, e[3 + k].get_top() + UP * 0.1, angle=-PI / 2.2,
                             color=ACENTO, stroke_width=3)
            self.play(Create(fl), run_time=0.6)
            self.play(TransformFromCopy(VGroup(e[0], e[3 + k]), res[k + 1]), run_time=0.8)
            self.wait(0.4)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Polinomio por polinomio: tabla de áreas
        subtitulo(self, cab, "Polinomio por polinomio")
        e = MathTex("(x+3)\\cdot(2x-1)", font_size=56).move_to([0, 2.3, 0])
        self.play(Write(e))
        notas("Cada término del primero por cada término del segundo: lo vemos como áreas")
        c2 = GRADO_COL
        tab, _ = tabla_producto(self, [("2x", c2[1]), ("-1", c2[0])], [("x", c2[1]), ("+3", c2[0])],
                                [[("2x^{2}", c2[2]), ("-x", c2[1])], [("+6x", c2[1]), ("-3", c2[0])]],
                                [-3.4, -0.2, 0], w=2.2, h=1.1)
        r = VGroup(MathTex("2x^{2} - x + 6x - 3", font_size=50),
                   MathTex("= 2x^{2} + 5x - 3", font_size=50)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        r.move_to([3.4, -0.2, 0])
        self.play(Write(r[0]))
        notas("Y juntamos los semejantes: −x + 6x = 5x")
        self.play(Write(r[1]))
        self.play(Circumscribe(r[1], color=ACENTO))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        e = MathTex("(x^{2}-2x+3)\\cdot(x+2)", font_size=56).move_to([0, 2.5, 0])
        self.play(Write(e))
        tab, _ = tabla_producto(self, [("x^{2}", c2[2]), ("-2x", c2[1]), ("+3", c2[0])],
                                [("x", c2[1]), ("+2", c2[0])],
                                [[("x^{3}", c2[3]), ("-2x^{2}", c2[2]), ("+3x", c2[1])],
                                 [("+2x^{2}", c2[2]), ("-4x", c2[1]), ("+6", c2[0])]],
                                [-2.6, 0.2, 0], w=1.8, h=1.0, rt=0.5)
        r = VGroup(MathTex("x^{3} + 0x^{2} - x + 6", font_size=48),
                   MathTex("= x^{3} - x + 6", font_size=48)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        r.move_to([0, -2.0, 0])
        notas("Las casillas del mismo color son semejantes: −2x² + 2x² = 0 y 3x − 4x = −x")
        self.play(Write(r[0]))
        self.play(Write(r[1]))
        self.play(Circumscribe(r[1], color=ACENTO))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Potencias
        subtitulo(self, cab, "Potencias de polinomios")
        e = MathTex("(x+2)^{2} = (x+2)\\cdot(x+2)", font_size=56).move_to([0, 2.3, 0])
        self.play(Write(e))
        notas("Elevar al cuadrado es multiplicar el polinomio por sí mismo")
        tab, _ = tabla_producto(self, [("x", c2[1]), ("+2", c2[0])], [("x", c2[1]), ("+2", c2[0])],
                                [[("x^{2}", c2[2]), ("+2x", c2[1])], [("+2x", c2[1]), ("+4", c2[0])]],
                                [-3.4, -0.2, 0], w=2.0, h=1.1)
        r = VGroup(MathTex("x^{2} + 2x + 2x + 4", font_size=50),
                   MathTex("= x^{2} + 4x + 4", font_size=50)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        r.move_to([3.4, -0.2, 0])
        self.play(Write(r[0]))
        self.play(Write(r[1]))
        self.wait(1)
        notas("¡La tabla es un cuadrado! Esto tiene un atajo: las identidades notables")
        self.play(Circumscribe(tab, color=ACENTO, run_time=1.5))
        self.wait(3)
        notas.fin()


# ---------------------------------------------------------------------------
# Identidades notables con áreas
def pieza_rect(o, x, y, w, h, col, lab, op=0.6, size=40):
    r = Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=2.5, fill_color=col,
                  fill_opacity=op).move_to(np.array(o) + [x + w / 2, y + h / 2, 0])
    if not lab:
        return VGroup(r)
    t = MathTex(lab, font_size=size).move_to(r)
    if t.width > w * 0.9:
        t.scale_to_fit_width(w * 0.9)
    return VGroup(r, t)


def llave(p1, p2, lab, col, direc, size=40):
    b = BraceBetweenPoints(np.array(p1), np.array(p2), direction=direc, color=col)
    t = MathTex(lab, font_size=size, color=col)
    b.put_at_tip(t)
    return VGroup(b, t)


def cuadrado_suma(a, b, o):
    """Cuadrado de lado a + b partido en a², ab, ab, b² (o = esquina inferior izquierda) y sus lados."""
    o = np.array(o)
    piezas = VGroup(pieza_rect(o, 0, 0, a, a, A_COL, "a^{2}"), pieza_rect(o, a, 0, b, a, AB_COL, "ab"),
                    pieza_rect(o, 0, a, a, b, AB_COL, "ab"), pieza_rect(o, a, a, b, b, B_COL, "b^{2}"))
    lados = VGroup(llave(o, o + [a, 0, 0], "a", A_COL, DOWN), llave(o + [a, 0, 0], o + [a + b, 0, 0], "b", B_COL, DOWN),
                   llave(o + [0, a, 0], o, "a", A_COL, LEFT), llave(o + [0, a + b, 0], o + [0, a, 0], "b", B_COL, LEFT))
    return VGroup(piezas, lados)


def formula_ab(*partes, size=56):
    """MathTex con a azul, b rosa y ab verde, troceado por partes."""
    t = MathTex(*partes, font_size=size)
    return t


class IdentidadesNotables(Scene):
    def construct(self):
        cab = titulo(self, "Identidades notables", "con áreas")
        notas = Notas(self)
        O = [-5.2, -2.2, 0]
        A, B = 2.6, 1.3

        # ===== (a + b)²
        subtitulo(self, cab, "Cuadrado de una suma")
        fig = cuadrado_suma(A, B, O)
        borde = Square(A + B, color=WHITE, stroke_width=4).move_to(np.array(O) + [(A + B) / 2, (A + B) / 2, 0])
        lado_tot = llave(O, np.array(O) + [A + B, 0, 0], "a+b", WHITE, DOWN)
        self.play(Create(borde), FadeIn(lado_tot))
        notas("(a + b)² es el área de un cuadrado de lado a + b")
        f0 = MathTex("(a+b)^{2}", font_size=60).move_to([2.6, 1.6, 0])
        self.play(Write(f0))
        self.wait(1.5)
        notas("Partimos cada lado en un trozo a y un trozo b")
        self.play(FadeOut(lado_tot), FadeIn(fig[1]))
        for p in fig[0]:
            self.play(FadeIn(p), run_time=0.7)
        self.remove(borde)
        notas("Salen cuatro piezas: un cuadrado a², dos rectángulos ab y un cuadrado b²")
        self.wait(1.5)
        f1 = MathTex("=", "a^{2}", "+", "ab", "+", "ab", "+", "b^{2}", font_size=60)
        f1.next_to(f0, DOWN, buff=0.6).align_to(f0, LEFT).shift(LEFT * 0.3)
        self.play(Write(f1[0]))
        for k, p in zip([1, 3, 5, 7], fig[0]):
            if k > 1:
                self.play(Write(f1[k - 1]), run_time=0.3)
            f1[k].set_color(p[0].get_fill_color())
            self.play(TransformFromCopy(p[1], f1[k]), run_time=0.8)
        self.wait(1)
        f2 = MathTex("=", "a^{2}", "+", "2ab", "+", "b^{2}", font_size=60).next_to(f1, DOWN, buff=0.6).align_to(f1, LEFT)
        for k, c in [(1, A_COL), (3, AB_COL), (5, B_COL)]:
            f2[k].set_color(c)
        self.play(TransformFromCopy(f1, f2), run_time=1.2)
        caja = SurroundingRectangle(VGroup(f0, f1, f2), color=ACENTO, buff=0.2)
        self.play(Create(caja))
        self.wait(1.5)

        # da igual lo que midan a y b
        notas("Da igual lo que midan a y b: siempre salen las mismas cuatro piezas")
        ta, tb = ValueTracker(A), ValueTracker(B)
        dyn = always_redraw(lambda: cuadrado_suma(ta.get_value(), tb.get_value(), O))
        self.remove(fig, *fig[0], fig[1])
        self.add(dyn)
        self.play(ta.animate.set_value(1.6), tb.animate.set_value(2.2), run_time=2.5)
        self.play(ta.animate.set_value(3.0), tb.animate.set_value(0.9), run_time=2.5)
        self.play(ta.animate.set_value(A), tb.animate.set_value(B), run_time=2)
        dyn.clear_updaters()
        self.wait(0.5)

        # el error típico
        notas("Error típico: (a + b)² ≠ a² + b². ¡Faltarían los dos rectángulos!", color=MAL)
        rects = VGroup(dyn[0][1], dyn[0][2])
        self.play(rects.animate.set_opacity(0.08), run_time=1)
        tacha = MathTex("(a+b)^{2} \\neq a^{2} + b^{2}", font_size=48, color=MAL).next_to(caja, DOWN, buff=0.5)
        self.play(Write(tacha))
        self.wait(1.5)
        self.play(rects.animate.set_opacity(1), *[r[0].animate.set_fill(opacity=0.6) for r in rects], run_time=1)
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # ===== (a − b)²
        subtitulo(self, cab, "Cuadrado de una diferencia")
        A2, B2 = 3.6, 1.2
        o = np.array(O)
        grande = pieza_rect(o, 0, 0, A2, A2, A_COL, None, op=0.45)
        la = VGroup(llave(o, o + [A2, 0, 0], "a", A_COL, DOWN), llave(o + [0, A2, 0], o, "a", A_COL, LEFT))
        self.play(FadeIn(grande), FadeIn(la))
        g0 = MathTex("(a-b)^{2}", font_size=60).move_to([2.6, 1.6, 0])
        self.play(Write(g0))
        notas("Empezamos con un cuadrado de lado a: su área es a²")
        self.wait(1.5)
        interior = Square(A2 - B2, color=ACENTO, stroke_width=5).move_to(o + [(A2 - B2) / 2, (A2 - B2) / 2, 0])
        lb = VGroup(llave(o + [0, A2 + 0.05, 0], o + [A2 - B2, A2 + 0.05, 0], "a-b", ACENTO, UP),
                    llave(o + [A2 - B2, A2 + 0.05, 0], o + [A2, A2 + 0.05, 0], "b", B_COL, UP))
        self.play(Create(interior), FadeIn(lb))
        notas("Queremos el cuadrado amarillo, de lado a − b: hay que quitar dos franjas")
        self.wait(2)
        g1 = MathTex("=", "a^{2}", "-ab", "-ab", "+b^{2}", font_size=60)
        g1.next_to(g0, DOWN, buff=0.6).align_to(g0, LEFT).shift(LEFT * 0.3)
        g1[1].set_color(A_COL)
        g1[2].set_color(AB_COL)
        g1[3].set_color(AB_COL)
        g1[4].set_color(B_COL)
        self.play(Write(g1[:2]))
        arriba = pieza_rect(o, 0, A2 - B2, A2, B2, AB_COL, "ab", op=0.75)
        self.play(FadeIn(arriba, shift=DOWN * 0.3))
        self.play(Write(g1[2]))
        notas("Quitamos la franja de arriba (a por b) …")
        self.wait(1.2)
        derecha = pieza_rect(o, A2 - B2, 0, B2, A2, AB_COL, "ab", op=0.75)
        derecha[1].move_to(o + [A2 - B2 / 2, (A2 - B2) / 2, 0])
        self.play(FadeIn(derecha, shift=LEFT * 0.3))
        self.play(Write(g1[3]))
        notas("… y la de la derecha (otra vez a por b)")
        self.wait(1.2)
        esquina = pieza_rect(o, A2 - B2, A2 - B2, B2, B2, B_COL, "b^{2}", op=0.95)
        self.play(FadeIn(esquina, scale=1.3))
        notas("¡La esquina la hemos quitado dos veces! Hay que devolverla una vez: + b²", color=ROSA)
        self.play(Indicate(esquina, color=B_COL, scale_factor=1.15))
        self.play(Write(g1[4]))
        self.wait(1.5)
        g2 = MathTex("=", "a^{2}", "-2ab", "+b^{2}", font_size=60).next_to(g1, DOWN, buff=0.6).align_to(g1, LEFT)
        for k, c in [(1, A_COL), (2, AB_COL), (3, B_COL)]:
            g2[k].set_color(c)
        self.play(TransformFromCopy(g1, g2))
        self.play(Create(SurroundingRectangle(VGroup(g0, g1, g2), color=ACENTO, buff=0.2)),
                  Indicate(interior, color=ACENTO, scale_factor=1.05))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # ===== (a + b)(a − b)
        subtitulo(self, cab, "Suma por diferencia")
        p1 = pieza_rect(o, 0, 0, A2, A2 - B2, A_COL, None, op=0.55)
        p2 = pieza_rect(o, 0, A2 - B2, A2 - B2, B2, A_COL, None, op=0.55)
        esq = pieza_rect(o, A2 - B2, A2 - B2, B2, B2, B_COL, "b^{2}", op=0.8)
        la = VGroup(llave(o, o + [A2, 0, 0], "a", A_COL, DOWN), llave(o + [0, A2, 0], o, "a", A_COL, LEFT))
        h0 = MathTex("a^{2}", font_size=60, color=A_COL).move_to([2.6, 1.6, 0])
        entero = pieza_rect(o, 0, 0, A2, A2, A_COL, None, op=0.55)
        self.play(FadeIn(entero), FadeIn(la), Write(h0))
        notas("Otra vez un cuadrado de lado a: su área es a²")
        self.wait(1.5)
        lb = llave(o + [A2 - B2, A2 + 0.05, 0], o + [A2, A2 + 0.05, 0], "b", B_COL, UP)
        self.play(FadeIn(esq, scale=1.3), FadeIn(lb))
        notas("En una esquina marcamos un cuadradito de lado b …")
        self.wait(1.5)
        # el cuadrado entero se cambia por las dos piezas que quedan (misma imagen, ahora con la línea de corte)
        self.add(p1, p2, esq)
        self.remove(entero)
        notas("… y se lo quitamos")
        h1 = MathTex("a^{2}", "-", "b^{2}", font_size=60).move_to(h0, aligned_edge=LEFT)
        h1[0].set_color(A_COL)
        h1[2].set_color(B_COL)
        self.play(esq.animate.shift(RIGHT * 2.2 + UP * 0.6).set_opacity(0.0), FadeOut(lb),
                  ReplacementTransform(h0, h1[0]), Write(h1[1:]), run_time=1.5)
        self.remove(esq)
        self.wait(1)
        notas("Cortamos la pieza de arriba y la giramos para ponerla a la derecha")
        self.play(FadeOut(la))
        self.play(p2.animate.set_fill(AB_COL, 0.6), run_time=0.5)
        destino = o + [A2 + B2 / 2, (A2 - B2) / 2, 0]
        self.play(p2.animate.rotate(-PI / 2).move_to(destino), run_time=2)
        self.wait(0.5)
        lr = VGroup(llave(o, o + [A2 + B2, 0, 0], "a+b", WHITE, DOWN),
                    llave(o + [0, A2 - B2, 0], o, "a-b", WHITE, LEFT))
        self.play(FadeIn(lr))
        notas("¡Sale un rectángulo de lados a + b y a − b, con la misma área!")
        h2 = MathTex("(a+b)(a-b)", "=", "a^{2}", "-", "b^{2}", font_size=60)
        h2[2].set_color(A_COL)
        h2[4].set_color(B_COL)
        h2.move_to([3.5, 0.0, 0])
        self.play(Write(h2[:2]), ReplacementTransform(h1, h2[2:]), run_time=1.5)
        self.play(Create(SurroundingRectangle(h2, color=ACENTO, buff=0.2)))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # ===== Resumen
        subtitulo(self, cab, "Resumen")
        filas = [("(a+b)^{2}", "a^{2}", "+", "2ab", "+", "b^{2}", "Cuadrado de una suma"),
                 ("(a-b)^{2}", "a^{2}", "-", "2ab", "+", "b^{2}", "Cuadrado de una diferencia"),
                 ("(a+b)(a-b)", "a^{2}", "-", "b^{2}", None, None, "Suma por diferencia")]
        g = VGroup()
        for f in filas:
            partes = [f[0], "="] + [p for p in f[1:6] if p]
            t = MathTex(*partes, font_size=54)
            for i, p in enumerate(partes):
                if p == "a^{2}":
                    t[i].set_color(A_COL)
                elif p == "b^{2}":
                    t[i].set_color(B_COL)
                elif p == "2ab":
                    t[i].set_color(AB_COL)
            n = texto(f[6], 24, GREY_B)
            g.add(VGroup(n, t).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.1, 0])
        c = tarjeta(g, buff=0.4)
        self.play(Create(c[0]))
        for f in g:
            self.play(FadeIn(f, shift=RIGHT * 0.2))
            self.wait(1)
        notas("Pruébalo tú en la actividad interactiva: mueve a y b y mira las piezas")
        self.wait(3)
        notas.fin()


class IdentidadesEjemplos(Scene):
    def construct(self):
        cab = titulo(self, "Identidades notables", "ejemplos y trucos")
        notas = Notas(self)

        def ejemplo(enun, a, b, pasos, y, nota):
            e = MathTex(enun, font_size=60).move_to([-5.6, y, 0], aligned_edge=LEFT)
            self.play(Write(e))
            ab = VGroup(MathTex("a = " + a, font_size=40, color=A_COL),
                        MathTex("b = " + b, font_size=40, color=B_COL)).arrange(RIGHT, buff=0.6)
            ab.next_to(e, RIGHT, buff=0.8)
            self.play(FadeIn(ab, shift=LEFT * 0.2))
            notas(nota)
            prev = e
            g = VGroup(e, ab)
            for p in pasos:
                m = M(*p, size=56).next_to(prev, DOWN, buff=0.5).align_to(e, LEFT).shift(RIGHT * 0.6)
                self.play(Write(m), run_time=1.5)
                self.wait(1)
                prev = m
                g.add(m)
            self.play(Circumscribe(prev, color=ACENTO))
            self.wait(1.5)
            return g

        subtitulo(self, cab, "Con letras y números")
        g = ejemplo("(x+3)^{2}", "x", "3",
                    [[("="), ("x", A_COL), ("^{2}"), ("+ 2\\cdot"), ("x", A_COL), ("\\cdot"), ("3", B_COL), ("+"),
                      ("3", B_COL), ("^{2}")],
                     [("= x^{2} + 6x + 9")]], 1.4, "Cuadrado de una suma: a² + 2ab + b², con a = x y b = 3")
        self.wait(1)
        notas.fin()
        self.play(FadeOut(g))
        g = ejemplo("(2x-1)^{2}", "2x", "1",
                    [[("="), ("(2x)", A_COL), ("^{2}"), ("- 2\\cdot"), ("2x", A_COL), ("\\cdot"), ("1", B_COL), ("+"),
                      ("1", B_COL), ("^{2}")],
                     [("= 4x^{2} - 4x + 1")]], 1.4, "Si a = 2x, el cuadrado es (2x)² = 4x²: ¡el paréntesis es importante!")
        self.wait(1)
        notas.fin()
        self.play(FadeOut(g))
        g = ejemplo("(x+5)(x-5)", "x", "5",
                    [[("="), ("x", A_COL), ("^{2}"), ("-"), ("5", B_COL), ("^{2}")],
                     [("= x^{2} - 25")]], 1.4, "Suma por diferencia: a² − b²")
        notas.fin()
        limpiar(self, cab)

        # --- Error típico
        subtitulo(self, cab, "El error típico")
        mal = MathTex("(x+3)^{2}", "\\neq", "x^{2}+9", font_size=60).move_to([0, 1.7, 0])
        mal[1].set_color(MAL)
        self.play(Write(mal))
        notas("Lo comprobamos con un número, por ejemplo x = 1")
        c = VGroup(MathTex("(1+3)^{2} = 4^{2} = 16", font_size=50),
                   MathTex("1^{2} + 9 = 10", font_size=50)).arrange(DOWN, buff=0.5).move_to([0, -0.2, 0])
        self.play(Write(c[0]))
        self.play(Write(c[1]))
        notas("16 ≠ 10: falta el doble producto, 2 · x · 3 = 6x", color=MAL)
        self.play(Circumscribe(c, color=MAL))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Al revés
        subtitulo(self, cab, "Al revés: de polinomio a producto")
        notas("Reconocer una identidad permite escribir un polinomio como producto")
        lineas(self, [
            "x^{2} + 10x + 25 = x^{2} + 2\\cdot x\\cdot 5 + 5^{2} = (x+5)^{2}",
            "x^{2} - 49 = x^{2} - 7^{2} = (x+7)(x-7)",
            "4x^{2} - 12x + 9 = (2x)^{2} - 2\\cdot 2x\\cdot 3 + 3^{2} = (2x-3)^{2}"],
            -6.2, 1.6, dy=1.3, size=44, rt=2.0, espera=2.0)
        notas("Pista: busca dos cuadrados (a² y b²) y comprueba si el término del medio es 2ab")
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Cálculo mental
        subtitulo(self, cab, "Truco de cálculo mental")
        notas("21² sin calculadora: 21 = 20 + 1")
        lineas(self, ["21^{2} = (20+1)^{2} = 400 + 40 + 1 = 441"], -5.4, 1.6, size=52, rt=2.0, espera=1.5)
        notas("31 · 29: uno es 30 + 1 y el otro 30 − 1")
        lineas(self, ["31\\cdot 29 = (30+1)(30-1) = 900 - 1 = 899"], -5.4, 0.2, size=52, rt=2.0, espera=1.5)
        notas("49²: 49 = 50 − 1")
        lineas(self, ["49^{2} = (50-1)^{2} = 2500 - 100 + 1 = 2401"], -5.4, -1.2, size=52, rt=2.0, espera=1.5)
        self.wait(2.5)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios (propios, como en los temas 1 y 2)
def lista(items, por_linea=4, sep="      "):
    trozos = [f"{l}) {t}" for l, t in zip("abcdefgh", items)]
    return "\n".join(sep.join(trozos[i:i + por_linea]) for i in range(0, len(trozos), por_linea))


def pagina_enunciados(scene, cab, bloques, size=25):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 27, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
    if grupo.width > config.frame_width - 1.0:
        grupo.scale_to_fit_width(config.frame_width - 1.0).to_edge(LEFT, buff=0.5)
    if grupo.get_bottom()[1] < -3.0:
        grupo.scale(((cab.get_bottom()[1] - 0.4) + 3.0) / grupo.height).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


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
        ("6. Multiplica:", lista(["3x · (2x² − x + 4)", "(x + 3)(x − 2)", "(2x − 1)(x² + x + 3)"], 3)),
        ("7. Desarrolla con las identidades notables:", lista(["(x + 5)²", "(x − 4)²", "(x + 6)(x − 6)", "(3x + 2)²"])),
    ]


def enunciados_3():
    return [
        ("8. Escribe como un producto:", lista(["x² + 8x + 16", "x² − 81", "9x² − 6x + 1"], 3)),
        ("9. Calcula mentalmente con las identidades notables:", lista(["41²", "99²", "52 · 48"], 3)),
        ("10. Un rectángulo mide x + 3 de base y x − 1 de altura.",
         "a) Escribe su área como un polinomio.      b) ¿Cuánto vale el área si x = 5?"),
    ]


def cuenta(scene, enun, pasos, x, y, notas=None, etiqueta=None, ejemplo=False, size=50, dy=None,
           letras=("x",), tras_enun=None):
    """Enunciado y, debajo, los pasos [(tex o mobject, nota)]. Rodea el último. Devuelve el VGroup."""
    dy = dy or size / 52 * 0.95
    rt = 1.1 if ejemplo else 0.8
    g = VGroup()
    e = enun if isinstance(enun, Mobject) else X(enun, size, letras)
    e.move_to([x, y, 0], aligned_edge=LEFT)
    if etiqueta:
        et = texto(etiqueta, 28).next_to(e, LEFT, buff=0.3)
        scene.play(FadeIn(et), run_time=0.3)
        g.add(et)
    scene.play(Write(e), run_time=rt)
    g.add(e)
    if tras_enun:
        g.add(tras_enun(e))
    ultimo = e
    for i, (p, nota) in enumerate(pasos):
        m = p if isinstance(p, Mobject) else X(p, size, letras)
        # separación mínima dy entre centros, pero sin pisar la línea anterior (fracciones altas)
        yy = min(ultimo.get_center()[1] - dy, ultimo.get_bottom()[1] - 0.22 - m.height / 2)
        m.move_to([x + 0.5, yy, 0], aligned_edge=LEFT)
        if nota and notas:
            notas(nota)
            scene.wait(1.2 if ejemplo else 0.6)
        scene.play(Write(m), run_time=rt)
        scene.wait(0.8 if ejemplo else 0.4)
        g.add(m)
        ultimo = m
    scene.play(Circumscribe(ultimo, color=ACENTO), run_time=0.7)
    return g


# --- 1. Traducir
TRADUCE = [
    ("El doble de un número más 5", "2x+5", "El doble de x → 2x;  «más 5» → + 5"),
    ("El cuadrado de un número menos su triple", "x^{2}-3x", "El cuadrado → x²;  su triple → 3x"),
    ("La edad de Ana dentro de 7 años", "x+7", "Hoy tiene x años: dentro de 7 tendrá 7 más"),
    ("Tres números consecutivos", "x,\\ \\ x+1,\\ \\ x+2", "Consecutivos: cada uno es 1 más que el anterior"),
]


def ej_traduce(scene, i, y, notas, ejemplo=False):
    frase, expr, nota = TRADUCE[i]
    et = texto(f"{'abcd'[i]})", 28).move_to([-6.4, y, 0])
    f = texto(frase, 30).next_to(et, RIGHT, buff=0.3)
    scene.play(FadeIn(et), FadeIn(f, shift=RIGHT * 0.2))
    notas(nota)
    scene.wait(1.5 if ejemplo else 0.8)
    fl = MathTex("\\longrightarrow", font_size=48).next_to(f, RIGHT, buff=0.35)
    m = X(expr, 50).next_to(fl, RIGHT, buff=0.35)
    scene.play(GrowFromEdge(fl, LEFT), Write(m))
    scene.play(Circumscribe(m, color=ACENTO), run_time=0.7)
    scene.wait(1.2 if ejemplo else 0.6)
    return VGroup(et, f, fl, m)


# --- 2. Valor numérico de P(x) = 2x² − 3x + 1
VALOR = [
    ("2", "2", ["=8-6+1", "=3"], ["Cambiamos cada x por 2", "Primero la potencia: 2² = 4, y 2 · 4 = 8"]),
    ("-1", "(-1)", ["=2+3+1", "=6"], ["Si el número es negativo, lo escribimos entre paréntesis",
                                      "(−1)² = 1  y  −3 · (−1) = +3"]),
    ("0", "0", ["=0-0+1", "=1"], ["Cambiamos cada x por 0", "Con x = 0 solo queda el término independiente"]),
    ("3", "3", ["=18-9+1", "=10"], ["Cambiamos cada x por 3", "3² = 9, y 2 · 9 = 18"]),
]


def p_valor(size=46):
    return X("P(x)=2x^{2}-3x+1", size).move_to([0, 2.2, 0])


def ej_valor(scene, i, x, y, notas, ejemplo=False, size=50):
    v, vp, resto, ns = VALOR[i]
    enun = M("P(", (v, LETRA), ")", size=size)
    sust = M("=2\\cdot", (vp, LETRA), "^{2}-3\\cdot", (vp, LETRA), "+1", size=size)
    pasos = [(sust, ns[0]), (MathTex(resto[0], font_size=size), ns[1]), (MathTex(resto[1], font_size=size), None)]
    return cuenta(scene, enun, pasos, x, y, notas, f"{'abcd'[i]})", ejemplo, size)


# --- 3. Coeficiente, parte literal y grado
MONOMIOS_EJ = [
    ("-5x^{3}", "-5", "x^{3}", "3", "El coeficiente es el número (con su signo); la parte literal, las letras"),
    ("7x^{2}y", "7", "x^{2}y", "2+1=3", "Con varias letras, el grado es la suma de todos los exponentes"),
    ("-x", "-1", "x", "1", "−x es (−1) · x: el 1 no se escribe, pero está"),
    ("6", "6", None, "0", "Un número solo es un monomio de grado 0, sin parte literal"),
]


def tabla_monomios(scene, notas, filas, ejemplo=False):
    xs = [-4.3, -1.3, 1.7, 4.7]
    cabe = VGroup(*[texto(t, 28, GREY_B).move_to([x, 1.9, 0])
                    for t, x in zip(("Monomio", "Coeficiente", "Parte literal", "Grado"), xs)])
    raya = Line([-6.4, 1.45, 0], [6.4, 1.45, 0], stroke_width=2, color=GREY_B)
    scene.play(FadeIn(cabe), Create(raya))
    g = VGroup(cabe, raya)
    for k, i in enumerate(filas):
        mon, co, pl, gr, nota = MONOMIOS_EJ[i]
        y = 0.7 - k * 1.05
        et = texto(f"{'abcd'[i]})", 28).move_to([-6.2, y, 0])
        m = X(mon, 50, ("x", "y")).move_to([xs[0], y, 0])
        scene.play(FadeIn(et), Write(m))
        notas(nota)
        scene.wait(1.2 if ejemplo else 0.6)
        celdas = [MathTex(co, font_size=46, color=COEF).move_to([xs[1], y, 0]),
                  (X(pl, 46, ("x", "y")) if pl else texto("no tiene", 26, GREY_B)).move_to([xs[2], y, 0]),
                  MathTex(gr, font_size=46, color=ROSA).move_to([xs[3], y, 0])]
        for c in celdas:
            scene.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.6)
            scene.wait(0.6 if ejemplo else 0.3)
        g.add(et, m, *celdas)
    scene.wait(1.5)
    notas.fin()
    return g


# --- 4. Reducir
REDUCE = [
    ("3x+5x-2x", [("=(3+5-2)\\,x", "Todos son semejantes (parte literal x): operamos los coeficientes"),
                  ("=6x", None)]),
    ("4x^{2}-x+2x^{2}+3x", [("=(4x^{2}+2x^{2})+(-x+3x)", "Juntamos los semejantes: x² con x², y x con x"),
                            ("=6x^{2}+2x", "x² y x no son semejantes: aquí ya no se puede juntar más")]),
    ("5x\\cdot(-2x^{2})", [("=5\\cdot(-2)\\cdot x\\cdot x^{2}", "Números con números y letras con letras"),
                           ("=-10x^{3}", "x · x² = x¹⁺² = x³")]),
    ("12x^{5}:4x^{2}", [("=(12:4)\\cdot x^{5-2}", "Dividimos los coeficientes y restamos los exponentes"),
                        ("=3x^{3}", None)]),
]


def ej_reduce(scene, i, x, y, notas, ejemplo=False, size=50):
    enun, pasos = REDUCE[i]
    return cuenta(scene, enun, pasos, x, y, notas, f"{'abcd'[i]})", ejemplo, size)


# --- 5. Suma y resta de P(x) = 3x³ − 2x + 5 y Q(x) = x³ + 4x² − 6
P5 = {3: 3, 1: -2, 0: 5}
Q5 = {3: 1, 2: 4, 0: -6}
COLS5 = {3: -0.6, 2: 1.3, 1: 3.0, 0: 4.6}


def enun5(scene):
    e = VGroup(MathTex("P(x) =", font_size=42), pol(P5, 42), MathTex("\\qquad Q(x) =", font_size=42),
               pol(Q5, 42)).arrange(RIGHT, buff=0.2)
    e[2:].shift(RIGHT * 0.5)
    e.move_to([0, 2.4, 0])
    scene.play(Write(e))
    return e


def ej5_suma(scene, notas, ejemplo=False):
    e = enun5(scene)
    notas("Un polinomio debajo del otro, cada grado en su columna")
    scene.wait(1.0 if ejemplo else 0.5)
    todo, _, _ = suma_columnas(scene, notas, P5, Q5, COLS5, ("P(x)", "Q(x)", "P(x)+Q(x)"), y0=1.3)
    notas("P(x) + Q(x) = 4x³ + 4x² − 2x − 1")
    scene.wait(2.5)
    notas.fin()
    return VGroup(e, todo)


def ej5_resta(scene, notas):
    e = enun5(scene)
    notas("Restar es sumar el opuesto: cambiamos el signo de todos los términos de Q(x)")
    Qn = {d: -c for d, c in Q5.items()}
    xe = min(COLS5.values()) - 1.9
    fq = fila_pol(Q5, 1.3, COLS5)
    eq = MathTex("Q(x)", font_size=44).move_to([xe, 1.3, 0])
    scene.play(Write(eq), *[Write(m) for m in fq.values()])
    fqn = fila_pol(Qn, 0.3, COLS5)
    eqn = MathTex("-Q(x)", font_size=44).move_to([xe, 0.3, 0])
    scene.play(TransformFromCopy(eq, eqn), *[TransformFromCopy(fq[d], fqn[d]) for d in fq], run_time=1.5)
    scene.play(*[Flash(m.get_left(), color=ACENTO, flash_radius=0.25) for m in fqn.values()])
    scene.wait(1.2)
    scene.play(FadeOut(VGroup(eq, *fq.values(), eqn, *fqn.values())))
    notas.fin()
    todo, _, _ = suma_columnas(scene, notas, P5, Qn, COLS5, ("P(x)", "-Q(x)", "P(x)-Q(x)"), y0=1.3,
                               nota_hueco=False)
    notas("P(x) − Q(x) = 2x³ − 4x² − 2x + 11")
    scene.wait(2)
    notas("Cuidado: el −6 de Q(x) pasa a ser +6, y 5 + 6 = 11", color=ROSA)
    scene.wait(2.5)
    notas.fin()
    return VGroup(e, todo)


def ej5_inversa(scene, notas):
    pasos = [("=-\\,(2x^{3}-4x^{2}-2x+11)", "Q − P es el opuesto de P − Q: ¡ya lo tenemos calculado!"),
             ("=-2x^{3}+4x^{2}+2x-11", "Cambiamos el signo de todos los términos")]
    g = cuenta(scene, "Q(x)-P(x)", pasos, -3.6, 1.2, notas, "c)", size=54, dy=1.1)
    scene.wait(1.5)
    notas.fin()
    return g


# --- 6. Multiplicar
C2 = GRADO_COL


def ej6_a(scene, notas, ejemplo=False):
    pasos = [("=3x\\cdot 2x^{2}-3x\\cdot x+3x\\cdot 4", "El 3x multiplica a cada término del paréntesis"),
             ("=6x^{3}-3x^{2}+12x", "En cada producto: coeficientes por coeficientes y se suman los exponentes")]
    g = cuenta(scene, "3x\\cdot(2x^{2}-x+4)", pasos, -5.0, 1.4, notas, "a)", ejemplo, 54, dy=1.15)
    scene.wait(1.5)
    notas.fin()
    return g


def ej6_b(scene, notas):
    e = MathTex("(x+3)\\cdot(x-2)", font_size=56).move_to([0, 2.3, 0])
    scene.play(Write(e))
    notas("Cada término del primero por cada término del segundo")
    tabla_producto(scene, [("x", C2[1]), ("-2", C2[0])], [("x", C2[1]), ("+3", C2[0])],
                   [[("x^{2}", C2[2]), ("-2x", C2[1])], [("+3x", C2[1]), ("-6", C2[0])]],
                   [-3.4, -0.2, 0], w=2.2, h=1.1)
    r = VGroup(MathTex("x^{2} - 2x + 3x - 6", font_size=50),
               MathTex("= x^{2} + x - 6", font_size=50)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    r.move_to([3.4, -0.2, 0])
    scene.play(Write(r[0]))
    notas("Juntamos los semejantes: −2x + 3x = x")
    scene.play(Write(r[1]))
    scene.play(Circumscribe(r[1], color=ACENTO))
    scene.wait(2)
    notas.fin()


def ej6_c(scene, notas):
    e = MathTex("(2x-1)\\cdot(x^{2}+x+3)", font_size=56).move_to([0, 2.5, 0])
    scene.play(Write(e))
    notas("Ahora la tabla tiene 2 filas y 3 columnas: 6 productos")
    tabla_producto(scene, [("x^{2}", C2[2]), ("+x", C2[1]), ("+3", C2[0])], [("2x", C2[1]), ("-1", C2[0])],
                   [[("2x^{3}", C2[3]), ("+2x^{2}", C2[2]), ("+6x", C2[1])],
                    [("-x^{2}", C2[2]), ("-x", C2[1]), ("-3", C2[0])]],
                   [-2.6, 0.2, 0], w=1.8, h=1.0, rt=0.5)
    r = VGroup(MathTex("2x^{3} + 2x^{2} - x^{2} + 6x - x - 3", font_size=46),
               MathTex("= 2x^{3} + x^{2} + 5x - 3", font_size=46)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    r.move_to([0, -2.0, 0])
    notas("Las casillas del mismo color son semejantes: 2x² − x² = x²  y  6x − x = 5x")
    scene.play(Write(r[0]))
    scene.play(Write(r[1]))
    scene.play(Circumscribe(r[1], color=ACENTO))
    scene.wait(2)
    notas.fin()


# --- 7. Identidades notables
IDENT = [
    ("(x+5)^{2}", "x", "5", "+", "x^{2}+10x+25", "Cuadrado de una suma: a² + 2ab + b², con a = x y b = 5"),
    ("(x-4)^{2}", "x", "4", "-", "x^{2}-8x+16", "Cuadrado de una diferencia: a² − 2ab + b²"),
    ("(x+6)(x-6)", "x", "6", "sd", "x^{2}-36", "Suma por diferencia: a² − b²"),
    ("(3x+2)^{2}", "3x", "2", "+", "9x^{2}+12x+4", "Con a = 3x, el cuadrado es (3x)² = 9x²: ¡con paréntesis!"),
]


def ej_ident(scene, i, notas, ejemplo=False):
    enun, a, b, s, res, nota = IDENT[i]
    a2 = f"({a})" if len(a) > 1 else a
    if s == "sd":
        medio = M("=", (a2, A_COL), "^{2}", "-", (b, B_COL), "^{2}", size=56)
    else:
        medio = M("=", (a2, A_COL), "^{2}", f"{s} 2\\cdot", (a, A_COL), "\\cdot", (b, B_COL), "+", (b, B_COL),
                  "^{2}", size=56)

    def ab(e):
        g = VGroup(MathTex("a = " + a, font_size=40, color=A_COL),
                   MathTex("b = " + b, font_size=40, color=B_COL)).arrange(RIGHT, buff=0.6)
        g.next_to(e, RIGHT, buff=0.9)
        scene.play(FadeIn(g, shift=LEFT * 0.2))
        return g

    g = cuenta(scene, MathTex(enun, font_size=60), [(medio, nota), ("=" + res, None)], -5.4, 1.4, notas,
               f"{'abcd'[i]})", ejemplo, 56, dy=1.15, tras_enun=ab)
    scene.wait(1.5)
    notas.fin()
    return g


# --- 8. Factorizar
FACTOR = [
    ("x^{2}+8x+16", [("=x^{2}+2\\cdot x\\cdot 4+4^{2}", "Dos cuadrados: x² y 16 = 4². ¿Es 8x = 2 · x · 4? ¡Sí!"),
                     ("=(x+4)^{2}", "Es el cuadrado de una suma")]),
    ("x^{2}-81", [("=x^{2}-9^{2}", "Una resta de dos cuadrados: 81 = 9²"),
                  ("=(x+9)(x-9)", "a² − b² = (a + b)(a − b)")]),
    ("9x^{2}-6x+1", [("=(3x)^{2}-2\\cdot 3x\\cdot 1+1^{2}", "9x² = (3x)² y 1 = 1²;  2 · 3x · 1 = 6x, con signo −"),
                     ("=(3x-1)^{2}", "Es el cuadrado de una diferencia")]),
]


def ej_factor(scene, i, x, y, notas, ejemplo=False, size=54):
    enun, pasos = FACTOR[i]
    return cuenta(scene, enun, pasos, x, y, notas, f"{'abc'[i]})", ejemplo, size, dy=1.1)


# --- 9. Cálculo mental
MENTAL = [
    ("41^{2}", [("=(40+1)^{2}", "41 = 40 + 1, y 40 es fácil de elevar al cuadrado"),
                ("=1600+80+1", "40² + 2 · 40 · 1 + 1²"), ("=1681", None)]),
    ("99^{2}", [("=(100-1)^{2}", "99 = 100 − 1"), ("=10000-200+1", "100² − 2 · 100 · 1 + 1²"), ("=9801", None)]),
    ("52\\cdot 48", [("=(50+2)(50-2)", "52 y 48 están a la misma distancia de 50: suma por diferencia"),
                     ("=2500-4", "50² − 2²"), ("=2496", None)]),
]


def ej_mental(scene, i, x, y, notas, ejemplo=False, size=54):
    enun, pasos = MENTAL[i]
    return cuenta(scene, enun, pasos, x, y, notas, f"{'abc'[i]})", ejemplo, size, dy=1.05)


# --- 10. Problema del rectángulo
def figura_rect(scene):
    r = Rectangle(width=3.4, height=2.0, color=AB_COL, fill_color=AB_COL, fill_opacity=0.25).move_to([3.4, 0.3, 0])
    b = Brace(r, DOWN, color=GREY_B)
    lb = X("x+3", 42).next_to(b, DOWN, buff=0.12)
    h = Brace(r, RIGHT, color=GREY_B)
    lh = X("x-1", 42).next_to(h, RIGHT, buff=0.12)
    g = VGroup(r, b, lb, h, lh)
    scene.play(Create(r), FadeIn(VGroup(b, lb, h, lh)))
    return g


def ej10_a(scene, notas, ejemplo=False):
    f = figura_rect(scene)
    notas("Área de un rectángulo = base · altura")
    scene.wait(1.2 if ejemplo else 0.6)
    pasos = [("=x^{2}-x+3x-3", "Multiplicamos cada término por cada término"),
             ("=x^{2}+2x-3", "Juntamos los semejantes: −x + 3x = 2x")]
    g = cuenta(scene, "A=(x+3)(x-1)", pasos, -6.0, 1.3, notas, None, ejemplo, 50, dy=1.1)
    scene.wait(1.5)
    notas.fin()
    return VGroup(f, g)


def ej10_b(scene, notas):
    f = figura_rect(scene)
    scene.play(f.animate.shift(UP * 1.2))
    e0 = X("A=x^{2}+2x-3", 46).move_to([-6.0, 2.2, 0], aligned_edge=LEFT)
    scene.play(FadeIn(e0))
    notas("Sustituimos x = 5 en el polinomio del apartado a)")
    pasos = [(MathTex("=25+10-3", font_size=50), None), (MathTex("=32", font_size=50), None)]
    enun = M("A=", ("5", LETRA), "^{2}+2\\cdot", ("5", LETRA), "-3", size=50)
    g = cuenta(scene, enun, pasos, -6.0, 1.0, notas, None, False, 50, dy=1.05)
    lados = VGroup(MathTex("5+3=8", font_size=40), MathTex("5-1=4", font_size=40)).arrange(RIGHT, buff=0.8)
    lados.next_to(f, DOWN, buff=0.5)
    notas("Comprobación: con x = 5 la base mide 8 y la altura 4")
    scene.play(Write(lados))
    ok = MathTex("8\\cdot 4 = 32", "\\ \\checkmark", font_size=48).next_to(lados, DOWN, buff=0.35)
    ok[1].set_color(OK)
    scene.play(Write(ok))
    scene.wait(2.5)
    notas.fin()
    return VGroup(f, e0, g, lados, ok)


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
        ej_traduce(self, 0, 0.8, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        self.play(Write(p_valor()))
        ej_valor(self, 0, -3.0, 1.0, notas, ejemplo=True, size=54)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        tabla_monomios(self, notas, [0], ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 a)")
        ej_reduce(self, 0, -3.0, 1.2, notas, ejemplo=True, size=56)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 a)")
        ej5_suma(self, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        ej6_a(self, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        ej_ident(self, 0, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 8 a)")
        ej_factor(self, 0, -4.4, 1.2, notas, ejemplo=True, size=56)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9 a)")
        ej_mental(self, 0, -3.0, 1.4, notas, ejemplo=True, size=56)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 10 a)")
        ej10_a(self, notas, ejemplo=True)
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
            ej_traduce(self, i, y, notas)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2 b)")
        self.play(Write(p_valor()))
        ej_valor(self, 1, -3.0, 1.0, notas, size=54)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2: c) y d)")
        self.play(Write(p_valor()))
        ej_valor(self, 2, -5.8, 1.0, notas, size=48)
        ej_valor(self, 3, 1.0, 1.0, notas, size=48)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        tabla_monomios(self, notas, [1, 2, 3])
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 4 b)")
        ej_reduce(self, 1, -4.4, 1.2, notas, size=54)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4: c) y d)")
        ej_reduce(self, 2, -5.8, 1.2, notas, size=46)
        ej_reduce(self, 3, 1.2, 1.2, notas, size=46)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 b)")
        ej5_resta(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 c)")
        ej5_inversa(self, notas)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo: ejercicios 6 a 10.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 6 a 10")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 6 b)")
        ej6_b(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 c)")
        ej6_c(self, notas)
        limpiar(self, cab)

        for i in (1, 2, 3):
            subtitulo(self, cab, f"Ejercicio 7 {'abcd'[i]})")
            ej_ident(self, i, notas)
            limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 8: b) y c)")
        ej_factor(self, 1, -6.0, 1.4, notas, size=46)
        ej_factor(self, 2, 0.6, 1.4, notas, size=46)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 9: b) y c)")
        ej_mental(self, 1, -5.8, 1.4, notas, size=50)
        ej_mental(self, 2, 1.0, 1.4, notas, size=50)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 10 b)")
        ej10_b(self, notas)
        limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
