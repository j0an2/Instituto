"""Tema 1 · Números naturales y potencias (1º ESO) — unidad 1 del libro, un vídeo por apartado

Escenas (mismo orden que el libro):
    SistemasNumeracion      – 1. numeración romana (sumar, restar, no repetir más de 3) y decimal (posicional)
    NumeroNatural           – 2. contar y ordenar, la recta, siguiente/anterior, comparar (< y >)
    PropiedadesOperaciones  – 3. conmutativa, asociativa y distributiva con fichas; la división: D = d · c + r
    PotenciasNaturales      – 4. base y exponente, cuadrado y cubo, potencias de 10
    CuadradosRaiz           – 5. cuadrados perfectos, raíz cuadrada exacta y entera
    RedondearEstimar        – 6. redondear en la recta (mirar la cifra siguiente) y estimar resultados

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t01_naturales.py SistemasNumeracion
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t01_naturales.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403
from potencias_raices import (pot, producto, cuadricula, cubo_iso, fichas_cuadrado,  # noqa: E402
                                  Notas, fila, pagina_enunciados, t_a_potencia, t_calcula,
                                  t_raiz, t_raiz_entera, t_perfecto)

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 1 · Números naturales y potencias"
TITULOS = {
    "SistemasNumeracion": "Sistemas de numeración romano y decimal",
    "NumeroNatural": "El número natural",
    "PropiedadesOperaciones": "Operaciones con números naturales",
    "PotenciasNaturales": "Potencias",
    "CuadradosRaiz": "Cuadrados perfectos y raíz cuadrada",
    "RedondearEstimar": "Estimación",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

ROSA = "#FF79C6"
AZUL = "#5DADE2"
ROMANO = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def miles(n):
    """3487 -> '3\\,487' (LaTeX, separador de miles con espacio)."""
    s = f"{n:,}".replace(",", r"\,")
    return s


def valores_romano(s):
    v = [ROMANO[c] for c in s]
    return [-x if i + 1 < len(v) and x < v[i + 1] else x for i, x in enumerate(v)]


def romano(s, size=64):
    """VGroup(letras, valores) con el valor de cada letra debajo (en rojo si resta)."""
    letras = VGroup(*[Text(c, font_size=size, weight=BOLD) for c in s]).arrange(RIGHT, buff=0.3)
    vals = VGroup()
    for i, (l, v) in enumerate(zip(letras, valores_romano(s))):
        signo = "-" if v < 0 else ("+" if i > 0 else "")
        vals.add(MathTex(signo + str(abs(v)), font_size=size * 0.5, color=MAL if v < 0 else OK)
                 .next_to(l, DOWN, buff=0.3))
    return VGroup(letras, vals)


def fichas(filas, cols, r=0.16, buff=0.12, color=ACENTO):
    g = VGroup(*[Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5)
                 for _ in range(filas * cols)])
    g.arrange_in_grid(rows=filas, cols=cols, buff=buff)
    return g


# ---------------------------------------------------------------------------
class SistemasNumeracion(Scene):
    def construct(self):
        cab = titulo(self, "Sistemas de numeración", "Romano y decimal")

        # 1. Los símbolos romanos
        subtitulo(self, cab, "Los romanos usaban 7 letras")
        cartas = VGroup()
        for c, v in ROMANO.items():
            l = Text(c, font_size=60, weight=BOLD)
            n = MathTex(miles(v), font_size=34, color=ACENTO).next_to(l, DOWN, buff=0.3)
            caja = SurroundingRectangle(VGroup(l, n), color=GREY_B, buff=0.22, corner_radius=0.1)
            caja.stretch_to_fit_width(1.35)
            cartas.add(VGroup(caja, l, n))
        cartas.arrange(RIGHT, buff=0.3).move_to([0, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cartas], lag_ratio=0.15))
        self.wait(2)
        self.play(cartas.animate.scale(0.6).to_edge(DOWN, buff=0.3))

        # Regla 1: sumar
        r1 = texto("1) De mayor a menor: se SUMAN", 30, OK).move_to([-3.2, 2.0, 0])
        self.play(FadeIn(r1))
        ej = romano("XVI").move_to([-3.2, 0.5, 0])
        self.play(Write(ej[0]))
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in ej[1]], lag_ratio=0.3))
        res = MathTex("= 16", font_size=60, color=ACENTO).next_to(ej[0], RIGHT, buff=0.5)
        self.play(Write(res))
        self.wait(1)

        # Regla 2: restar
        r2 = texto("2) Uno menor DELANTE: RESTA", 30, MAL).move_to([3.3, 2.0, 0])
        self.play(FadeIn(r2))
        ej2 = romano("IX").move_to([2.6, 0.5, 0])
        self.play(Write(ej2[0]))
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in ej2[1]], lag_ratio=0.3))
        res2 = MathTex("= 9", font_size=60, color=ACENTO).next_to(ej2[0], RIGHT, buff=0.5)
        self.play(Write(res2))
        solo = texto("Solo: IV 4 · IX 9 · XL 40 · XC 90 · CD 400 · CM 900", 22, GREY_B).move_to([3.0, -0.9, 0])
        self.play(FadeIn(solo))
        self.wait(2)
        self.play(FadeOut(VGroup(r1, ej, res, r2, ej2, res2, solo)))

        # Regla 3: no más de 3 veces
        r3 = texto("3) Una letra no se repite más de 3 veces", 30, AZUL).move_to([0, 2.0, 0])
        self.play(FadeIn(r3))
        bien = Text("III = 3", font_size=54, weight=BOLD).move_to([-3, 0.6, 0])
        mal = Text("IIII", font_size=54, weight=BOLD, color=MAL).move_to([1.4, 0.6, 0])
        cruz = Cross(mal, stroke_color=MAL, stroke_width=6)
        bueno = Text("IV = 4", font_size=54, weight=BOLD, color=OK).next_to(mal, RIGHT, buff=0.9)
        self.play(Write(bien))
        self.play(Write(mal), Create(cruz))
        self.play(Write(bueno))
        self.wait(2)
        self.play(FadeOut(VGroup(r3, bien, mal, cruz, bueno)))

        # Ejemplo grande: el año
        q = texto("¿Qué año es MMXXVI?", 32, ACENTO).move_to([0, 2.0, 0])
        self.play(FadeIn(q))
        ej = romano("MMXXVI", 72).move_to([-1.2, 0.6, 0])
        self.play(Write(ej[0]))
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in ej[1]], lag_ratio=0.25))
        res = MathTex(r"= 2\,026", font_size=66, color=ACENTO).next_to(ej[0], RIGHT, buff=0.5)
        self.play(Write(res), Circumscribe(res, color=ACENTO))
        self.wait(2.5)
        limpiar(self, cab)

        # 2. Sistema decimal: posicional
        subtitulo(self, cab, "Nuestro sistema: 10 cifras y POSICIONAL")
        cifras = MathTex(*[str(k) for k in range(10)], font_size=56).arrange(RIGHT, buff=0.45).move_to([0, 1.9, 0])
        self.play(LaggedStart(*[FadeIn(c) for c in cifras], lag_ratio=0.1))
        tres = MathTex("3", "3", "3", font_size=110).arrange(RIGHT, buff=0.25).move_to([0, 0.5, 0])
        for t, pos in zip(tres, "CDU"):
            t.set_color(COLOR_POS[pos])
        self.play(Write(tres))
        vals = VGroup()
        for i, (t, (v, pos)) in enumerate(zip(tres, ((300, "C"), (30, "D"), (3, "U")))):
            v_ = MathTex(str(v), font_size=48, color=COLOR_POS[pos]).move_to([-3.0 + i * 3.0, -1.0, 0])
            nom = texto(NOMBRE_POS[pos], 22, COLOR_POS[pos]).next_to(v_, DOWN, buff=0.2)
            fl = Arrow(t.get_bottom(), v_.get_top(), buff=0.15, color=COLOR_POS[pos], stroke_width=3,
                       max_tip_length_to_length_ratio=0.15)
            self.play(GrowArrow(fl), FadeIn(v_), FadeIn(nom), run_time=0.8)
            vals.add(VGroup(fl, v_, nom))
        msg = texto("La misma cifra vale distinto según su POSICIÓN\n"
                    "(en romano, X siempre vale 10)", 28, ACENTO).move_to([0, -2.8, 0])
        self.play(FadeIn(msg))
        self.wait(3)
        limpiar(self, cab)

        # 3. 2026 en la tabla y el cero
        subtitulo(self, cab, "Cada posición vale 10 veces más que la de su derecha")
        tabla, centros = tabla_posiciones(["M", "C", "D", "U"], centro=[-3.0, 0.3, 0], w=1.2)
        self.play(FadeIn(tabla))
        num = tex_decimal("2026", 64)
        for c, pos in zip(num, "MCDU"):
            c.move_to(centros[(0, pos)])
        self.play(Write(num))
        desc = MathTex(r"2\,026", "=", r"2\,000", "+", "0", "+", "20", "+", "6", font_size=48)
        for i, pos in ((2, "M"), (4, "C"), (6, "D"), (8, "U")):
            desc[i].set_color(COLOR_POS[pos])
        desc.move_to([2.6, 0.3, 0])
        self.play(Write(desc), run_time=2)
        cero = texto("El 0 dice «aquí no hay centenas»:\nsin él, 2026 y 226 se confundirían", 26, GREY_B)
        cero.move_to([0, -2.2, 0])
        self.play(FadeIn(cero), Indicate(num[1], color=ACENTO))
        self.wait(3)


# ---------------------------------------------------------------------------
class NumeroNatural(Scene):
    def construct(self):
        cab = titulo(self, "El número natural", "Para contar y para ordenar")

        # Contar y ordenar
        manz = VGroup(*[Circle(radius=0.3, fill_color=MAL, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
                        for _ in range(5)]).arrange(RIGHT, buff=0.25).move_to([-3.4, 1.0, 0])
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in manz], lag_ratio=0.15))
        n5 = MathTex("5", font_size=80, color=ACENTO).next_to(manz, DOWN, buff=0.4)
        t5 = texto("CONTAR: ¿cuántos hay?", 26, ACENTO).next_to(n5, DOWN, buff=0.3)
        self.play(Write(n5), FadeIn(t5))
        alturas = (1.0, 1.5, 0.7)
        podio = VGroup(*[Rectangle(width=1.1, height=h, fill_color=AZUL, fill_opacity=0.7, stroke_color=WHITE)
                         for h in alturas]).arrange(RIGHT, buff=0, aligned_edge=DOWN).move_to([3.4, 0.6, 0])
        etq = VGroup(*[texto(t, 28, WHITE).move_to(podio[i]) for i, t in ((0, "2.º"), (1, "1.º"), (2, "3.º"))])
        self.play(FadeIn(podio), Write(etq))
        to = texto("ORDENAR: ¿en qué lugar?", 26, ACENTO).move_to([3.4, -1.0, 0])
        self.play(FadeIn(to))
        self.wait(2)
        limpiar(self, cab)

        # La recta: siguiente y anterior
        subtitulo(self, cab, "En la recta: todos a la misma distancia")
        recta = NumberLine(x_range=[0, 10, 1], length=12, include_tip=True, stroke_width=3,
                           tick_size=0.12).move_to([0, 0.3, 0])
        nums = VGroup(*[MathTex(str(k), font_size=36).next_to(recta.n2p(k), DOWN, buff=0.25) for k in range(11)])
        self.play(Create(recta), LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.08))
        p = Dot(recta.n2p(6), radius=0.13, color=ACENTO)
        self.play(FadeIn(p, scale=2), nums[6].animate.set_color(ACENTO))
        a1 = CurvedArrow(recta.n2p(6) + UP * 0.25, recta.n2p(7) + UP * 0.25, angle=-PI / 2, color=OK)
        a2 = CurvedArrow(recta.n2p(6) + UP * 0.25, recta.n2p(5) + UP * 0.25, angle=PI / 2, color=POSITIVO)
        l1 = texto("siguiente: 7", 24, OK).next_to(a1, UP, buff=0.15).shift(RIGHT * 0.5)
        l2 = texto("anterior: 5", 24, POSITIVO).next_to(a2, UP, buff=0.15).shift(LEFT * 0.5)
        self.play(Create(a1), FadeIn(l1))
        self.play(Create(a2), FadeIn(l2))
        inf = texto("Siempre hay un siguiente: los naturales no se acaban nunca", 26, GREY_B).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(inf), Indicate(recta.tip))
        self.wait(2)
        limpiar(self, cab)

        # Comparar
        subtitulo(self, cab, "Comparar: cifra a cifra, desde la izquierda")
        a = MathTex(*list("3487"), font_size=90).arrange(RIGHT, buff=0.08).move_to([-2.0, 1.2, 0])
        b = MathTex(*list("3478"), font_size=90).arrange(RIGHT, buff=0.08).move_to([-2.0, -0.3, 0])
        self.play(Write(a), Write(b))
        for i in range(2):
            self.play(Indicate(VGroup(a[i], b[i]), color=GREY_B), run_time=0.5)
        self.play(a[2].animate.set_color(OK), b[2].animate.set_color(MAL))
        nota = texto("iguales... hasta las decenas: 8 > 7", 26, ACENTO).move_to([3.3, 0.45, 0])
        self.play(FadeIn(nota))
        r = MathTex(r"3\,487 > 3\,478", font_size=60, color=ACENTO).move_to([0, -1.8, 0])
        self.play(Write(r))
        signos = texto("«>» mayor que   ·   «<» menor que   ·   la punta señala al menor", 24, GREY_B)
        signos.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(signos))
        self.wait(2.5)


# ---------------------------------------------------------------------------
class PropiedadesOperaciones(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones con naturales", "Propiedades y división con resto")

        # 1. Conmutativa con fichas
        subtitulo(self, cab, "Conmutativa: el orden no importa")
        g = fichas(3, 4).move_to([-3.2, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(f, scale=0.5) for f in g], lag_ratio=0.04))
        e1 = MathTex(r"3 \cdot 4 = 12", font_size=56).move_to([2.5, 1.0, 0])
        self.play(Write(e1))
        self.play(Rotate(g, PI / 2), run_time=1.3)
        e2 = MathTex(r"4 \cdot 3 = 12", font_size=56).next_to(e1, DOWN, buff=0.5)
        self.play(Write(e2))
        txt = texto("Giramos el rectángulo: las mismas fichas", 24, GREY_B).next_to(g, DOWN, buff=0.4)
        self.play(FadeIn(txt))
        suma = MathTex(r"5 + 3 = 3 + 5", font_size=48, color=ACENTO).next_to(e2, DOWN, buff=0.7)
        nota = texto("También con la suma (¡pero no con la resta ni la división!)", 22, GREY_B).to_edge(DOWN, buff=0.5)
        self.play(Write(suma), FadeIn(nota))
        self.wait(2.5)
        limpiar(self, cab)

        # 2. Asociativa
        subtitulo(self, cab, "Asociativa: podemos agrupar como nos convenga")
        a = MathTex(r"(2 \cdot 5) \cdot 7", "=", r"10 \cdot 7", "=", "70", font_size=54).move_to([0, 1.2, 0])
        b = MathTex(r"2 \cdot (5 \cdot 7)", "=", r"2 \cdot 35", "=", "70", font_size=54).move_to([0, -0.2, 0])
        b.align_to(a, LEFT)
        self.play(Write(a[0]))
        self.play(Write(a[1:]))
        self.play(Write(b[0]))
        self.play(Write(b[1:]))
        self.play(Indicate(a[4]), Indicate(b[4]))
        truco = texto("Truco: busca parejas que den 10, 100...  →  25 · 7 · 4 = 7 · (25 · 4) = 700", 24, ACENTO)
        truco.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(truco))
        self.wait(3)
        limpiar(self, cab)

        # 3. Distributiva con fichas
        subtitulo(self, cab, "Distributiva: repartir la multiplicación")
        izq = fichas(3, 4, color=AZUL)
        der = fichas(3, 2, color=ROSA)
        bloque = VGroup(izq, der).arrange(RIGHT, buff=0.12).move_to([-3.4, 0.4, 0])
        self.play(FadeIn(bloque))
        e = MathTex(r"3 \cdot (4 + 2)", "=", r"3 \cdot 6", "=", "18", font_size=50).move_to([2.6, 1.3, 0])
        self.play(Write(e))
        self.play(der.animate.shift(RIGHT * 0.6))
        e2 = MathTex(r"3 \cdot 4", "+", r"3 \cdot 2", "=", "12", "+", "6", "=", "18", font_size=50)
        e2[0].set_color(AZUL)
        e2[2].set_color(ROSA)
        e2.next_to(e, DOWN, buff=0.7).align_to(e, LEFT)
        self.play(Write(e2))
        regla = MathTex(r"a \cdot (b + c) = a \cdot b + a \cdot c", font_size=50, color=ACENTO).to_edge(DOWN, buff=0.7)
        self.play(Write(regla))
        self.wait(3)
        limpiar(self, cab)

        # 4. La división con resto
        subtitulo(self, cab, "La división: repartimos 23 caramelos entre 5")
        cars = VGroup(*[Circle(radius=0.17, fill_color=ACENTO, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5)
                        for _ in range(23)]).arrange_in_grid(rows=3, buff=0.15).move_to([0, 1.3, 0])
        self.play(FadeIn(cars))
        cajas = VGroup(*[RoundedRectangle(width=1.3, height=2.0, corner_radius=0.1, stroke_color=GREY_B)
                         for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([-1.4, -1.3, 0])
        self.play(FadeIn(cajas))
        k = 0
        for ronda in range(4):
            anims = []
            for j in range(5):
                pos = cajas[j].get_top() + DOWN * (0.3 + 0.45 * ronda)
                anims.append(cars[k].animate.move_to(pos))
                k += 1
            self.play(*anims, run_time=0.6)
        sobra = VGroup(*cars[20:])
        self.play(sobra.animate.arrange(RIGHT, buff=0.15).move_to([3.4, -1.3, 0]).set_color(POSITIVO))
        ts = texto("sobran 3", 24, POSITIVO).next_to(sobra, DOWN, buff=0.3)
        tc = texto("4 cada uno", 24, ACENTO).next_to(cajas, DOWN, buff=0.2)
        self.play(FadeIn(ts), FadeIn(tc))
        self.wait(1)
        self.play(FadeOut(VGroup(cars[:20], cajas, ts, tc, sobra)))
        nombres = VGroup(texto("dividendo", 22, WHITE), texto("divisor", 22, AZUL),
                         texto("cociente", 22, ACENTO), texto("resto", 22, POSITIVO))
        f = MathTex("23", "=", "5", r"\cdot", "4", "+", "3", font_size=80).arrange(RIGHT, buff=0.45).move_to([0, 0.8, 0])
        f[2].set_color(AZUL)
        f[4].set_color(ACENTO)
        f[6].set_color(POSITIVO)
        self.play(Write(f))
        for nm, i in zip(nombres, (0, 2, 4, 6)):
            nm.next_to(f[i], DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(n) for n in nombres], lag_ratio=0.2))
        regla = MathTex(r"D = d \cdot c + r", font_size=56, color=ACENTO).move_to([0, -1.3, 0])
        cond = texto("El resto siempre es MENOR que el divisor (3 < 5). Si el resto es 0, la división es exacta.",
                     22, GREY_B).to_edge(DOWN, buff=0.5)
        self.play(Write(regla))
        self.play(FadeIn(cond))
        self.wait(3)


# ---------------------------------------------------------------------------
class PotenciasNaturales(Scene):
    def construct(self):
        cab = titulo(self, "Potencias", "Multiplicar un número por sí mismo")

        largo = MathTex(producto(2, 5), font_size=64).move_to([0, 1.6, 0])
        self.play(Write(largo))
        llave = Brace(largo, DOWN, buff=0.15)
        lt = texto("5 veces", 26, EXPONENTE).next_to(llave, DOWN, buff=0.1)
        self.play(GrowFromCenter(llave), FadeIn(lt))
        p = pot(2, 5, 110).move_to([-1.2, -1.0, 0])
        igual = MathTex("= 32", font_size=80).next_to(p, RIGHT, buff=0.3)
        self.play(TransformFromCopy(largo, p))
        self.play(Write(igual))
        eb = texto("base: el número\nque se repite", 24, BASE).next_to(p, LEFT, buff=0.6)
        ee = texto("exponente:\ncuántas veces", 24, EXPONENTE).next_to(p, UP, buff=0.2).shift(RIGHT * 2.6)
        self.play(FadeIn(eb), FadeIn(ee))
        lee = texto("Se lee: «dos elevado a cinco»", 26, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(lee))
        self.wait(2)
        cuidado = texto("¡Cuidado! 2⁵ no es 2 · 5 = 10", 26, MAL).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(lee, cuidado))
        self.wait(2)
        limpiar(self, cab)

        # Cuadrado y cubo
        subtitulo(self, cab, "Exponente 2: al cuadrado · exponente 3: al cubo")
        cu = cuadricula(3, s=0.5).move_to([-3.5, 0.2, 0])
        c3 = cubo_iso(3, s=0.5).move_to([3.0, 0.2, 0])
        self.play(FadeIn(cu))
        e1 = VGroup(pot(3, 2, 56), MathTex("= 9", font_size=56)).arrange(RIGHT, buff=0.2).next_to(cu, DOWN, buff=0.4)
        self.play(Write(e1), FadeIn(texto("«tres al cuadrado»", 22, GREY_B).next_to(e1, DOWN, buff=0.15)))
        self.play(LaggedStart(*[FadeIn(c) for c in c3], lag_ratio=0.03), run_time=1.5)
        e2 = VGroup(pot(3, 3, 56), MathTex("= 27", font_size=56)).arrange(RIGHT, buff=0.2).next_to(c3, DOWN, buff=0.4)
        self.play(Write(e2), FadeIn(texto("«tres al cubo»", 22, GREY_B).next_to(e2, DOWN, buff=0.15)))
        self.wait(2)
        limpiar(self, cab)

        # Potencias de 10
        subtitulo(self, cab, "Potencias de 10: un 1 y tantos ceros como diga el exponente")
        filas = [(2, r"100"), (3, r"1\,000"), (6, r"1\,000\,000")]
        g = VGroup()
        for e, v in filas:
            g.add(VGroup(pot(10, e, 56), MathTex("=", v, font_size=56)).arrange(RIGHT, buff=0.25))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.0, 0.3, 0])
        for f in g:
            self.play(Write(f), run_time=0.8)
        desc = MathTex(r"2\,026", "=", r"2 \cdot 10^3", "+", r"2 \cdot 10", "+", "6", font_size=50)
        desc[2].set_color(COLOR_POS["M"])
        desc[4].set_color(COLOR_POS["D"])
        desc.move_to([2.8, 0.3, 0])
        self.play(Write(desc))
        n = texto("Así se descompone un número con potencias de 10", 22, GREY_B).next_to(desc, DOWN, buff=0.3)
        self.play(FadeIn(n))
        self.wait(2.5)


# ---------------------------------------------------------------------------
class CuadradosRaiz(Scene):
    def construct(self):
        cab = titulo(self, "Cuadrados perfectos", "y raíz cuadrada")

        # Cuadrados perfectos
        subtitulo(self, cab, "¿Con cuántas fichas se puede hacer un cuadrado?")
        xs = [-5.2, -3.4, -1.0, 2.0]
        g = VGroup()
        for n, x in zip((1, 2, 3, 4), xs):
            c = cuadricula(n, s=0.45).move_to([x, 0.6, 0]).align_to([0, 1.8, 0], UP)
            t = MathTex(str(n * n), font_size=48, color=ACENTO).next_to(c, DOWN, buff=0.3)
            self.play(FadeIn(c), Write(t), run_time=0.7)
            g.add(VGroup(c, t))
        doce = fichas_cuadrado(12, lado=4, r=0.16, buff=0.12).move_to([5.0, 1.0, 0])
        t12 = MathTex("12", font_size=48, color=MAL).next_to(doce, DOWN, buff=0.3)
        self.play(FadeIn(doce), Write(t12))
        x12 = texto("no hay cuadrado", 22, MAL).next_to(t12, DOWN, buff=0.15)
        self.play(FadeIn(x12))
        lista = MathTex(r"1,\ 4,\ 9,\ 16,\ 25,\ 36,\ 49,\ 64,\ 81,\ 100 \dots", font_size=44, color=ACENTO)
        lista.to_edge(DOWN, buff=1.0)
        lt = texto("Cuadrados perfectos: los que son un número al cuadrado", 24, GREY_B).next_to(lista, DOWN, buff=0.2)
        self.play(Write(lista), FadeIn(lt))
        self.wait(2)
        limpiar(self, cab)

        # Raíz cuadrada exacta
        subtitulo(self, cab, "La raíz cuadrada es el LADO del cuadrado")
        c = cuadricula(7, s=0.4).move_to([-3.5, 0.0, 0])
        self.play(FadeIn(c))
        t49 = texto("49 casillas", 24, ACENTO).next_to(c, UP, buff=0.2)
        lado = Brace(c, DOWN, buff=0.1)
        l7 = MathTex("7", font_size=44, color=BASE).next_to(lado, DOWN, buff=0.1)
        self.play(FadeIn(t49))
        self.play(GrowFromCenter(lado), Write(l7))
        r = MathTex(r"\sqrt{49} = 7", font_size=80, color=ACENTO).move_to([2.6, 0.8, 0])
        por = VGroup(MathTex(r"\text{porque }", font_size=44), pot(7, 2, 44), MathTex("= 49", font_size=44))
        por.arrange(RIGHT, buff=0.15).next_to(r, DOWN, buff=0.4)
        self.play(Write(r))
        self.play(FadeIn(por))
        self.wait(2)
        limpiar(self, cab)

        # Raíz entera
        subtitulo(self, cab, "Si no es cuadrado perfecto: raíz entera y resto")
        f = VGroup(cuadricula(5, s=0.4))
        sobra = VGroup(*[Square(0.4, stroke_color=WHITE, stroke_width=1.5, fill_color=POSITIVO, fill_opacity=0.9)
                         for _ in range(5)]).arrange(DOWN, buff=0)
        grupo = VGroup(f, sobra).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([-3.4, 0.0, 0])
        self.play(FadeIn(f))
        self.play(FadeIn(sobra))
        t = texto("30 fichas: cuadrado de 5 × 5 y sobran 5", 24, GREY_B).next_to(grupo, DOWN, buff=0.35)
        self.play(FadeIn(t))
        r = MathTex(r"\sqrt{30} \to 5", font_size=64, color=ACENTO).move_to([2.8, 1.0, 0])
        rr = MathTex(r"\text{resto } 5", font_size=48, color=POSITIVO).next_to(r, DOWN, buff=0.3)
        comp = MathTex(r"30 = 5^2 + 5", font_size=48).next_to(rr, DOWN, buff=0.4)
        self.play(Write(r))
        self.play(Write(rr))
        self.play(Write(comp))
        self.wait(2.5)


# ---------------------------------------------------------------------------
class RedondearEstimar(Scene):
    def construct(self):
        cab = titulo(self, "Estimación", "Redondear y calcular aproximadamente")

        # 1. Redondear en la recta
        subtitulo(self, cab, "Redondear 3 487 a las centenas")
        recta = NumberLine(x_range=[3400, 3500, 10], length=11, include_tip=False, stroke_width=3,
                           tick_size=0.1).move_to([0, 0.2, 0])
        ext = VGroup(MathTex(r"3\,400", font_size=40).next_to(recta.n2p(3400), DOWN, buff=0.3),
                     MathTex(r"3\,500", font_size=40).next_to(recta.n2p(3500), DOWN, buff=0.3))
        self.play(Create(recta), FadeIn(ext))
        mitad = DashedLine(recta.n2p(3450) + UP * 0.8, recta.n2p(3450) + DOWN * 0.5, color=GREY_B)
        tm = MathTex(r"3\,450", font_size=30, color=GREY_B).next_to(mitad, DOWN, buff=0.1)
        tmt = texto("la mitad", 20, GREY_B).next_to(mitad, UP, buff=0.1)
        self.play(Create(mitad), FadeIn(tm), FadeIn(tmt))
        p = Dot(recta.n2p(3487), radius=0.13, color=ACENTO)
        tp = MathTex(r"3\,487", font_size=40, color=ACENTO).next_to(p, UP, buff=0.35)
        self.play(FadeIn(p, scale=2), Write(tp))
        d1 = Line(recta.n2p(3487) + DOWN * 0.9, recta.n2p(3500) + DOWN * 0.9, color=OK, stroke_width=6)
        d2 = Line(recta.n2p(3400) + DOWN * 1.4, recta.n2p(3487) + DOWN * 1.4, color=MAL, stroke_width=6)
        self.play(Create(d1), FadeIn(texto("13", 22, OK).next_to(d1, DOWN, buff=0.1)))
        self.play(Create(d2), FadeIn(texto("87", 22, MAL).next_to(d2, DOWN, buff=0.1)))
        r = MathTex(r"3\,487 \approx 3\,500", font_size=54, color=ACENTO).to_edge(DOWN, buff=0.5)
        self.play(Write(r))
        self.wait(2.5)
        limpiar(self, cab)

        # 2. La regla: mirar la cifra siguiente
        subtitulo(self, cab, "Sin dibujar la recta: mira la cifra SIGUIENTE")
        reg = texto("0, 1, 2, 3, 4  →  se queda igual          5, 6, 7, 8, 9  →  sube uno", 28, GREY_B)
        reg.move_to([0, 1.8, 0])
        self.play(FadeIn(reg))
        filas = [("a las centenas", "3487", 1, r"3\,500"), ("a las decenas", "3487", 2, r"3\,490"),
                 ("a los millares", "3487", 0, r"3\,000")]
        y = 0.6
        for nombre, n, i, res in filas:
            t = texto(nombre, 28).move_to([-4.6, y, 0])
            m = MathTex(*list(n), font_size=56).arrange(RIGHT, buff=0.05).move_to([-1.2, y, 0])
            m[i].set_color(ACENTO)
            m[i + 1].set_color(POSITIVO)
            fl = Arrow(m[i + 1].get_top() + UP * 0.35 + RIGHT * 0.3, m[i + 1].get_top() + UP * 0.05,
                       buff=0, color=POSITIVO, stroke_width=3, max_tip_length_to_length_ratio=0.4)
            rr = MathTex(r"\approx", res, font_size=56).next_to(m, RIGHT, buff=0.4)
            rr[1].set_color(ACENTO)
            sig = int(n[i + 1])
            nota = texto(f"{sig} {'≥' if sig >= 5 else '<'} 5 → {'sube' if sig >= 5 else 'se queda'}", 22,
                         POSITIVO).next_to(rr, RIGHT, buff=0.5)
            self.play(FadeIn(t), Write(m))
            self.play(GrowArrow(fl), FadeIn(nota))
            self.play(Write(rr))
            self.wait(0.8)
            y -= 1.25
        self.wait(2)
        limpiar(self, cab)

        # 3. Estimar
        subtitulo(self, cab, "Estimar: redondear antes de calcular")
        p1 = texto("28 alumnos pagan 12 € cada uno para una excursión. ¿Unos 300 €?", 28).move_to([0, 1.9, 0])
        self.play(FadeIn(p1))
        est = MathTex(r"28 \cdot 12", r"\approx", r"30 \cdot 10", "=", "300", font_size=56).move_to([0, 0.8, 0])
        est[4].set_color(ACENTO)
        self.play(Write(est))
        exacto = MathTex(r"28 \cdot 12 = 336", font_size=44, color=GREY_B).next_to(est, DOWN, buff=0.4)
        self.play(FadeIn(exacto))
        n1 = texto("La estimación no es exacta, pero da una idea rápida", 24, GREY_B).next_to(exacto, DOWN, buff=0.3)
        self.play(FadeIn(n1))
        self.wait(2.5)
        self.play(FadeOut(VGroup(p1, est, exacto, n1)))

        p2 = texto("Sirve para detectar errores:", 30, ACENTO).move_to([0, 1.9, 0])
        self.play(FadeIn(p2))
        mal = MathTex(r"49 \cdot 21 = 10\,290", font_size=60).move_to([0, 0.8, 0])
        self.play(Write(mal))
        est = MathTex(r"49 \cdot 21 \approx 50 \cdot 20 = 1\,000", font_size=50, color=ACENTO).move_to([0, -0.4, 0])
        self.play(Write(est))
        cruz = Cross(mal, stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        bien = MathTex(r"49 \cdot 21 = 1\,029", font_size=50, color=OK).move_to([0, -1.6, 0])
        self.play(Write(bien))
        fin = texto("10 290 está muy lejos de 1 000: ¡sobraba un cero!", 26, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(fin))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
ORDENES = ["unidades", "decenas", "centenas", "unidades de millar", "decenas de millar", "centenas de millar"]
ROM_TABLA = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
             (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
PROBLEMAS = [
    "a) 150 alumnos van de excursión en autobuses de 40 plazas.\n     ¿Cuántos autobuses hacen falta?",
    "b) Un cubo está hecho con cubitos: 4 de largo, 4 de ancho y 4 de alto.\n     ¿Cuántos cubitos tiene?",
    "c) Un huerto cuadrado tiene 81 m² de superficie. ¿Cuánto mide su lado?",
]


def a_romano(n):
    s = ""
    for v, l in ROM_TABLA:
        while n >= v:
            s, n = s + l, n - v
    return s


def num_tex(n, colores=None):
    """Partes de MathTex de un número, cifra a cifra (para colorear), con espacio de miles."""
    colores = colores or {}
    cif = str(n)
    partes = []
    for i, c in enumerate(cif):
        pos = len(cif) - 1 - i
        t = c + (r"\," if pos % 3 == 0 and pos > 0 else "")
        partes.append((t, colores.get(pos)))
    return partes


def t_rom_a_dec(s, size):
    v = [ROMANO[c] for c in s]
    trozos, i = [], 0
    while i < len(v):
        if i + 1 < len(v) and v[i] < v[i + 1]:
            trozos.append(f"({v[i + 1]} - {v[i]})")
            i += 2
        else:
            trozos.append(str(v[i]))
            i += 1
    resta = any(t.startswith("(") for t in trozos)
    return [(M(rf"\mathrm{{{s}}}", size=size), None),
            (M("= " + " + ".join(trozos), size=size),
             "Una letra delante de otra mayor se resta" if resta else "Las letras se suman"),
            (M("= " + miles(sum(valores_romano(s))), size=size).set_color(ACENTO), None)]


def t_dec_a_rom(n, size):
    cif = str(n)
    trozos = [int(c) * 10 ** (len(cif) - 1 - i) for i, c in enumerate(cif) if c != "0"]
    return [(M(miles(n), "=", " + ".join(miles(t) for t in trozos), size=size),
             "Separamos el número en millares, centenas, decenas y unidades"),
            (M("= " + " + ".join(rf"\mathrm{{{a_romano(t)}}}" for t in trozos), size=size),
             "Escribimos cada parte en romano"),
            (M(rf"= \mathrm{{{a_romano(n)}}}", size=size).set_color(ACENTO), None)]


def t_valor(n, size, cifra="7"):
    pos = len(str(n)) - 1 - str(n).index(cifra)
    return [(M(*num_tex(n, {pos: ACENTO}), size=size), f"El {cifra} está en el lugar de las {ORDENES[pos]}"),
            (M(r"\rightarrow", rf"{cifra} \text{{ {ORDENES[pos]}}} =", (miles(int(cifra) * 10 ** pos), ACENTO),
               size=size), None)]


def t_ordena_1(size):
    return [(M(r"3\,095,\ 3\,509,\ 3\,059,\ 3\,950", size=size),
             "Todos tienen 3 millares: comparamos las centenas")]


def t_ordena_2(size):
    return [(M(r"3\,059 < 3\,095", size=size),
             "3 059 y 3 095 empatan en centenas: deciden las decenas (5 < 9)"),
            (M(r"< 3\,509 < 3\,950", size=size).set_color(ACENTO), "3 509 y 3 950: 5 centenas < 9 centenas")]


def t_distrib(a, b, op, c, size):
    r = a * b + a * c if op == "+" else a * b - a * c
    return [(M(rf"{a} \cdot ({b} {op} {c})", size=size), None),
            (M(rf"= {a} \cdot {b} {op} {a} \cdot {c}", size=size), f"El {a} multiplica a cada número del paréntesis"),
            (M(rf"= {a * b} {op} {a * c}", size=size), None),
            (M(f"= {r}", size=size).set_color(ACENTO), None)]


def t_division(D, d, size):
    c, r = divmod(D, d)
    return [(M(rf"{D} : {d}", size=size), None),
            (M(r"\rightarrow", rf"c = {c},\ r = {r}", size=size).set_color(ACENTO),
             f"¿Cuántas veces cabe el {d} en {D}?  {d} · {c} = {d * c} y sobran {r}"),
            (M(rf"\text{{Prueba: }} {d} \cdot {c} + {r} = {D}", size=int(size * 0.85)).set_color(OK),
             "Comprobamos: dividendo = divisor · cociente + resto")]


def t_descomp(n, size):
    cif = str(n)
    trozos = []
    for i, c in enumerate(cif):
        e = len(cif) - 1 - i
        if c == "0":
            continue
        trozos.append(c if e == 0 else (rf"{c} \cdot 10" if e == 1 else rf"{c} \cdot 10^{{{e}}}"))
    return [(M(miles(n), size=size), None),
            (M("= " + " + ".join(trozos), size=size).set_color(ACENTO),
             "Cada cifra multiplica a una potencia de 10 (si vale 0, no se escribe)")]


def t_redondeo(n, orden, size):
    mira = orden - 1
    paso10 = 10 ** orden
    d = int(str(n)[len(str(n)) - 1 - mira])
    r = (n + paso10 // 2) // paso10 * paso10
    regla = "5 o más: subimos" if d >= 5 else "menos de 5: se queda igual"
    return [(M(*num_tex(n, {mira: ROSA}), size=size), f"Miramos la cifra de las {ORDENES[mira]}: {d}, {regla}"),
            (M(r"\approx", (miles(r), ACENTO), size=size), None)]


def t_estima(a, op, b, ra, rb, size):
    sim = r"\cdot" if op == "·" else op
    exacto = a * b if op == "·" else a + b
    apr = ra * rb if op == "·" else ra + rb
    return [(M(rf"{a} {sim} {b}", size=size), None),
            (M(rf"\approx {ra} {sim} {rb}", size=size), f"Redondeamos: {a} → {ra} y {b} → {rb}"),
            (M("= " + miles(apr), size=size).set_color(ACENTO), None),
            (M(rf"(\text{{exacto: }} {miles(exacto)})", size=int(size * 0.75)).set_color(GREY_B),
             "La estimación se acerca mucho al resultado exacto")]


def resolver(scene, items, notas, ejemplo=False):
    ys = {1: [0.6], 2: [1.2, -0.9], 3: [1.7, 0.2, -1.3]}[len(items)]
    s = 60 if ejemplo else 50
    for (lab, build), y in zip(items, ys):
        fila(scene, lab, build(s), y, notas=notas, ejemplo=ejemplo)
    notas.fin()
    scene.wait(1.2)


def it(lab, f, *args):
    return (lab, lambda s: f(*args, s))


EJ = {
    1: [it("a)", t_rom_a_dec, "XIV"), it("b)", t_rom_a_dec, "XLIX"),
        it("c)", t_rom_a_dec, "CCXC"), it("d)", t_rom_a_dec, "MCMXC")],
    2: [it("a)", t_dec_a_rom, 27), it("b)", t_dec_a_rom, 94),
        it("c)", t_dec_a_rom, 409), it("d)", t_dec_a_rom, 1500)],
    3: [it("a)", t_valor, 4172), it("b)", t_valor, 7305), it("c)", t_valor, 170438)],
    4: [(None, t_ordena_1), (None, t_ordena_2)],
    5: [it("a)", t_distrib, 5, 6, "+", 4), it("b)", t_distrib, 7, 10, "-", 2)],
    6: [it("a)", t_division, 47, 6), it("b)", t_division, 100, 8)],
    7: [it("a)", t_a_potencia, 7, 3), it("b)", t_calcula, 2, 4),
        it("c)", t_calcula, 10, 4), it("d)", t_descomp, 5308)],
    8: [it("a)", t_raiz, 64), it("b)", t_raiz, 144),
        it("c)", t_perfecto, 50), it("d)", t_raiz_entera, 40)],
    9: [it("a) decenas:", t_redondeo, 6748, 1), it("b) centenas:", t_redondeo, 6748, 2),
        it("c) millares:", t_redondeo, 6748, 3)],
    10: [it("a)", t_estima, 52, "·", 19, 50, 20), it("b)", t_estima, 38, "·", 41, 40, 40),
         it("c)", t_estima, 198, "+", 403, 200, 400)],
}


def enunciados():
    return [
        [("1. Escribe en el sistema decimal:", "a) XIV      b) XLIX      c) CCXC      d) MCMXC"),
         ("2. Escribe en números romanos:", "a) 27      b) 94      c) 409      d) 1 500"),
         ("3. ¿Qué valor tiene la cifra 7 en cada número?", "a) 4 172      b) 7 305      c) 170 438"),
         ("4. Ordena de menor a mayor:", "3 095,   3 509,   3 059,   3 950")],
        [("5. Aplica la propiedad distributiva y calcula:", f"a) 5 · (6 + 4)      b) 7 · (10 {MENOS} 2)"),
         ("6. Divide y haz la prueba:", "a) 47 : 6      b) 100 : 8"),
         ("7. Potencias:", "a) Escribe como potencia y calcula: 7 · 7 · 7      b) Calcula 2⁴      c) Calcula 10⁴\n"
                           "d) Descompón 5 308 con potencias de 10"),
         ("8. Cuadrados y raíces:", "a) √64      b) √144      c) ¿Es 50 un cuadrado perfecto?\n"
                                    "d) Raíz entera y resto de √40")],
        [("9. Redondea 6 748:", "a) a las decenas      b) a las centenas      c) a los millares"),
         ("10. Estima el resultado y compáralo con el exacto:", "a) 52 · 19      b) 38 · 41      c) 198 + 403"),
         ("11. Problemas:", "\n".join(PROBLEMAS))],
    ]


def problema(scene, notas, i, ilus, filas_tr, sol):
    e = texto(PROBLEMAS[i][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    if e.width > config.frame_width - 1.0:
        e.scale_to_fit_width(config.frame_width - 1.0)
    scene.play(Write(e), run_time=1.5)
    x, ancho = -6.4, 13.0
    if ilus is not None:
        ilus.move_to([-4.3, -0.5, 0])
        scene.play(FadeIn(ilus), run_time=1.2)
        x, ancho = -1.4, 7.6
    ys = {1: [0.4], 2: [0.9, -0.9]}[len(filas_tr)]
    for tr, y in zip(filas_tr, ys):
        fila(scene, None, tr, y, notas=notas, ejemplo=True, x=x, ancho_max=ancho)
    notas.fin()
    s = texto(sol, 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(s))
    scene.wait(2.5)


def problema_autobuses(scene, notas):
    filas_tr = [
        [(M("150 : 40", size=56), None),
         (M(r"\rightarrow c = 3,\ r = 30", size=56), "En 3 autobuses caben 40 · 3 = 120 alumnos; sobran 30")],
        [(M(r"3 + 1 =", size=56), "Los 30 que sobran también necesitan autobús"),
         (M("4", size=56).set_color(ACENTO), None)],
    ]
    problema(scene, notas, 0, None, filas_tr, "Hacen falta 4 autobuses (en el último van 30)")


def problema_cubo(scene, notas):
    problema(scene, notas, 1, cubo_iso(4, s=0.38), [t_calcula(4, 3, 56)], "El cubo tiene 4³ = 64 cubitos")


def problema_huerto(scene, notas):
    problema(scene, notas, 2, cuadricula(9, 0.3, color=OK, op=0.6), [t_raiz(81, 56)], "El lado mide 9 m")


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Números naturales y potencias")
        notas = Notas(self)
        for pagina in enunciados():
            pagina_enunciados(self, cab, pagina)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))
        for n in range(1, 11):
            items = EJ[n] if n == 4 else EJ[n][:1]
            subtitulo(self, cab, f"Ejercicio {n}" + ("" if n == 4 else " a)"))
            resolver(self, items, notas, ejemplo=True)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 11 a)")
        problema_autobuses(self, notas)
        limpiar(self, cab)
        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Números naturales y potencias")
        notas = Notas(self, size=24)
        pantallas = [
            ("Ejercicio 1: b) y c)", 1, 1, 3), ("Ejercicio 1 d)", 1, 3, 4),
            ("Ejercicio 2: b), c) y d)", 2, 1, 4),
            ("Ejercicio 3: b) y c)", 3, 1, 3),
            ("Ejercicio 5 b)", 5, 1, 2),
            ("Ejercicio 6 b)", 6, 1, 2),
            ("Ejercicio 7: b), c) y d)", 7, 1, 4),
            ("Ejercicio 8: b) y c)", 8, 1, 3), ("Ejercicio 8 d)", 8, 3, 4),
            ("Ejercicio 9: b) y c)", 9, 1, 3),
            ("Ejercicio 10: b) y c)", 10, 1, 3),
        ]
        for sub, n, i0, i1 in pantallas:
            subtitulo(self, cab, sub)
            resolver(self, EJ[n][i0:i1], notas)
            limpiar(self, cab)
        for sub, f in (("Ejercicio 11 b)", problema_cubo), ("Ejercicio 11 c)", problema_huerto)):
            subtitulo(self, cab, sub)
            f(self, notas)
            limpiar(self, cab)
        fin = texto("¡Muy bien! Ya dominas los números naturales.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
