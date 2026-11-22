"""Tema 6 · Números decimales (1º ESO) — unidad 5 del libro (antes temas 6 y 8)

Escenas:
    QueEsUnDecimal      – décimas y centésimas con el cuadrado unidad; decimal = fracción; dinero
    ValorPosicional     – tabla C D U , d c m; 34,072; el 0 importa
    DecimalesEnLaRecta  – zoom: décimas → centésimas → milésimas
    CompararDecimales   – cifra a cifra; la trampa 0,5 vs 0,45; ceros a la derecha
    OrdenarDecimales    – igualar cifras con ceros y colocar en la recta

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t06_decimales.py QueEsUnDecimal
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t06_decimales.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 6 · Números decimales"
TITULOS = {
    "QueEsUnDecimal": "¿Qué es un número decimal?",
    "ValorPosicional": "El valor de cada cifra",
    "DecimalesEnLaRecta": "Decimales en la recta",
    "CompararDecimales": "Comparar decimales",
    "OrdenarDecimales": "Ordenar decimales",
    "EjerciciosDecimalesEjemplo": "Ejercicios (decimales): enunciados y ejemplos resueltos",
    "EjerciciosDecimalesResueltos": "Ejercicios (decimales) resueltos",
    "SumaRestaDecimales": "Sumar y restar decimales",
    "PorDiezCienMil": "Multiplicar y dividir por 10, 100, 1000",
    "MultiplicarDecimales": "Multiplicar decimales",
    "DividirDecimales": "Dividir decimales",
    "FraccionADecimal": "De fracción a decimal y redondeo",
    "DecimalesPeriodicos": "Decimales periódicos",
    "EjerciciosEjemplo": "Ejercicios (operaciones): enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios (operaciones) resueltos",
}

CD, CC, CM = COLOR_POS["d"], COLOR_POS["c"], COLOR_POS["m"]


def limpiar_a(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo_a(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def igual_fraccion_decimal(n, d, s, size=60):
    return VGroup(fraccion(n, d, size=size), MathTex("=", font_size=size), tex_decimal(s, size=size)).arrange(RIGHT, buff=0.3)


# ---------------------------------------------------------------------------
class QueEsUnDecimal(Scene):
    def construct(self):
        cab = titulo(self, "¿Qué es un número decimal?", "Partes de la unidad")
        lado, c0 = 4.0, np.array([-3.4, -0.4, 0])

        unidad = Square(lado, stroke_color=WHITE, fill_color=VACIO, fill_opacity=1).move_to(c0)
        t1 = texto("La unidad: 1", 28).next_to(unidad, UP, buff=0.25)
        self.play(FadeIn(unidad), FadeIn(t1))
        self.wait(0.5)

        # Décimas: 10 tiras
        tiras = VGroup(*[Rectangle(width=lado / 10, height=lado, stroke_color=WHITE, stroke_width=2,
                                   fill_color=VACIO, fill_opacity=1) for _ in range(10)]).arrange(RIGHT, buff=0).move_to(c0)
        t2 = texto("La partimos en 10 tiras iguales", 28).move_to(t1)
        self.play(Transform(t1, t2), Create(tiras), run_time=1.5)
        self.remove(unidad)
        self.play(tiras[0].animate.set_fill(CD, 1))
        e1 = igual_fraccion_decimal(1, 10, "0,1").move_to([2.8, 1.2, 0])
        n1 = texto("una DÉCIMA", 30, CD).next_to(e1, DOWN, buff=0.3)
        self.play(Write(e1), FadeIn(n1))
        self.wait(1)
        self.play(*[tiras[i].animate.set_fill(CD, 1) for i in (1, 2)])
        e2 = igual_fraccion_decimal(3, 10, "0,3").move_to([2.8, -1.2, 0])
        n2 = texto("tres décimas", 28, CD).next_to(e2, DOWN, buff=0.3)
        self.play(Write(e2), FadeIn(n2))
        self.wait(2)
        self.play(FadeOut(VGroup(e1, n1, e2, n2)))

        # Centésimas: 100 cuadraditos
        celdas = VGroup(*[Square(lado / 10, stroke_color=WHITE, stroke_width=1.2, fill_color=VACIO, fill_opacity=1)
                          for _ in range(100)]).arrange_in_grid(rows=10, cols=10, buff=0).move_to(c0)
        t3 = texto("Cada tira en 10: 100 cuadraditos", 28).move_to(t1)
        self.play(Transform(t1, t3), FadeOut(tiras), FadeIn(celdas), run_time=1.5)
        self.play(celdas[0].animate.set_fill(CC, 1))
        e1 = igual_fraccion_decimal(1, 100, "0,01").move_to([2.8, 1.2, 0])
        n1 = texto("una CENTÉSIMA", 30, CC).next_to(e1, DOWN, buff=0.3)
        self.play(Write(e1), FadeIn(n1))
        self.wait(1)
        # 25 centésimas = 2 columnas enteras + 5 cuadraditos
        indices = [r * 10 + c for c in range(2) for r in range(10)] + [r * 10 + 2 for r in range(5)]
        self.play(LaggedStart(*[celdas[i].animate.set_fill(CC, 1) for i in indices[1:]], lag_ratio=0.04), run_time=2)
        e2 = igual_fraccion_decimal(25, 100, "0,25").move_to([2.8, -1.2, 0])
        n2 = texto("25 centésimas\n(= 2 décimas y 5 centésimas)", 24, CC).next_to(e2, DOWN, buff=0.3)
        self.play(Write(e2), FadeIn(n2))
        self.wait(2)
        idea = texto("Un decimal es una fracción con denominador 10, 100, 1000...", 28, ACENTO).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(idea))
        self.wait(2.5)
        limpiar_a(self, cab)

        # Dinero: 2,45 €
        sub = subtitulo_a(self, cab, "Lo usamos cada día: el dinero")
        num = VGroup(tex_decimal("2,45", size=110), MathTex(r"\text{€}", font_size=90)).arrange(RIGHT, buff=0.25)
        num = VGroup(tex_decimal("2,45", size=110), Text("€", font_size=70)).arrange(RIGHT, buff=0.25).move_to([0, 1.5, 0])
        self.play(Write(num))

        def moneda(etq, r, col):
            c = Circle(radius=r, color=col, fill_color=col, fill_opacity=0.35, stroke_width=3)
            return VGroup(c, Text(etq, font_size=int(r * 34), color=WHITE).move_to(c))

        grupos = [
            (VGroup(*[moneda("1 €", 0.5, COLOR_POS["U"]) for _ in range(2)]).arrange(RIGHT, buff=0.15), 0, "2 euros"),
            (VGroup(*[moneda("10 c", 0.38, CD) for _ in range(4)]).arrange(RIGHT, buff=0.1), 2, "4 monedas de 10 cént.\n= 4 décimas de euro"),
            (VGroup(*[moneda("1 c", 0.25, CC) for _ in range(5)]).arrange(RIGHT, buff=0.08), 3, "5 monedas de 1 cént.\n= 5 centésimas de euro"),
        ]
        xs = [-4.3, 0, 4.3]
        for (g, idx, lab), x in zip(grupos, xs):
            g.move_to([x, -0.6, 0])
            t = texto(lab, 22, num[0][idx].get_color()).next_to(g, DOWN, buff=0.3)
            self.play(Indicate(num[0][idx], scale_factor=1.3), LaggedStart(*[GrowFromCenter(m) for m in g], lag_ratio=0.15),
                      FadeIn(t))
            self.play(Create(Arrow(num[0][idx].get_bottom(), g.get_top(), buff=0.15, color=num[0][idx].get_color(),
                                   stroke_width=3)), run_time=0.5)
        self.wait(3)


# ---------------------------------------------------------------------------
class ValorPosicional(Scene):
    def construct(self):
        cab = titulo(self, "El valor de cada cifra", "La tabla de posiciones")
        cols = ["C", "D", "U", ",", "d", "c", "m"]
        tabla, centros = tabla_posiciones(cols, filas=2, centro=np.array([0, 0.0, 0]))
        num = tex_decimal("34,072", size=80).move_to([0, 2.4, 0])
        self.play(Write(num))
        self.play(FadeIn(tabla))
        destino = ["D", "U", ",", "d", "c", "m"]
        for parte, pos in zip(num, destino):
            self.play(parte.copy().animate.move_to(centros[(0, pos)]).scale(0.9), run_time=0.6)
        self.wait(0.5)
        coma = texto("La coma separa la parte entera de la parte decimal", 24, GREY_B).next_to(tabla, DOWN, buff=0.3)
        self.play(FadeIn(coma))
        self.wait(1.5)

        lect = texto("Se lee: «34 unidades y 72 milésimas»", 30, ACENTO).next_to(coma, DOWN, buff=0.3)
        self.play(Write(lect))
        self.wait(1.5)
        self.play(FadeOut(VGroup(coma, lect)))

        # El 0 importa: 34,72 en la segunda fila
        otro = tex_decimal("34,72", size=80)
        destino2 = ["D", "U", ",", "d", "c"]
        aviso = texto("¿Y si quitamos el 0?", 28, MAL).next_to(tabla, DOWN, buff=0.3)
        self.play(FadeIn(aviso))
        for parte, pos in zip(otro, destino2):
            parte.move_to(centros[(1, pos)]).scale(0.9)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in otro], lag_ratio=0.15))
        res = VGroup(tex_decimal("34,072", 50), MathTex(r"\neq", font_size=50), tex_decimal("34,72", 50))
        res.arrange(RIGHT, buff=0.3).next_to(aviso, DOWN, buff=0.25)
        exp = texto("El 7 pasa de las centésimas a las décimas: ¡vale 10 veces más!", 24, GREY_B).next_to(res, DOWN, buff=0.2)
        self.play(Write(res), FadeIn(exp))
        self.wait(3)
        limpiar_a(self, cab)

        # Descomposición
        sub = subtitulo_a(self, cab, "Cada cifra vale según su posición")
        n = tex_decimal("34,072", 72).move_to([0, 1.7, 0])
        self.play(Write(n))
        partes = [("3", "D", "30"), ("4", "U", "4"), ("0", "d", "0"), ("7", "c", "0,07"), ("2", "m", "0,002")]
        filas_a = VGroup()
        for cif, pos, val in partes:
            f = VGroup(MathTex(cif, font_size=44, color=COLOR_POS[pos]),
                       Text(f"{NOMBRE_POS[pos]}", font_size=24, color=COLOR_POS[pos]),
                       MathTex(r"\rightarrow", font_size=40), MathTex(val.replace(",", "{,}"), font_size=44,
                                                                       color=COLOR_POS[pos])).arrange(RIGHT, buff=0.3)
            filas_a.add(f)
        filas_a.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.2, -1.0, 0])
        for f in filas_a:
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.6)
        suma = MathTex("34{,}072", "=", "30", "+", "4", "+", "0{,}07", "+", "0{,}002", font_size=46)
        for i, pos in ((2, "D"), (4, "U"), (6, "c"), (8, "m")):
            suma[i].set_color(COLOR_POS[pos])
        suma.move_to([0, -3.2, 0])
        self.play(Write(suma))
        self.wait(3)


# ---------------------------------------------------------------------------
class DecimalesEnLaRecta(Scene):
    def construct(self):
        cab = titulo(self, "Decimales en la recta", "Haciendo zoom")
        L = 12.0

        def recta(a, b, paso, y, n_dec, color, cada=1):
            r = NumberLine(x_range=[a, b, paso], length=L, include_tip=False, stroke_width=3,
                           tick_size=0.09).move_to([0, y, 0])
            labs = VGroup()
            k = 0
            v = a
            while v <= b + 1e-9:
                if k % cada == 0:
                    s = str(round(v)) if abs(v - round(v)) < 1e-9 else dec_txt(v, n_dec)
                    labs.add(Text(s, font_size=16, color=color).next_to(r.n2p(v), DOWN, buff=0.15))
                v += paso
                k += 1
            return VGroup(r, labs), r

        g1, r1 = recta(0, 1, 0.1, 1.9, 1, CD)
        self.play(Create(r1), FadeIn(g1[1]))
        t = texto("De 0 a 1, en décimas", 24, CD).next_to(r1, UP, buff=0.35).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(t))
        p1 = Dot(r1.n2p(0.3), radius=0.1, color=ACENTO)
        l1 = tex_decimal("0,3", 36).next_to(p1, UP, buff=0.2)
        self.play(FadeIn(p1, scale=2), Write(l1))
        self.wait(0.8)

        # Zoom 1: de 0,3 a 0,4
        g2, r2 = recta(0.3, 0.4, 0.01, 0.0, 2, CC)
        self.zoom(r1, 0.3, 0.4, r2, CC)
        self.play(FadeIn(g2[1]))
        t2 = texto("Entre 0,3 y 0,4, en centésimas", 24, CC).next_to(r2, UP, buff=0.35).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(t2))
        p2 = Dot(r2.n2p(0.37), radius=0.1, color=ACENTO)
        l2 = tex_decimal("0,37", 36).next_to(p2, UP, buff=0.2)
        self.play(FadeIn(p2, scale=2), Write(l2))
        self.wait(0.8)

        # Zoom 2: de 0,37 a 0,38
        g3, r3 = recta(0.37, 0.38, 0.001, -1.9, 3, CM, cada=2)
        self.zoom(r2, 0.37, 0.38, r3, CM)
        self.play(FadeIn(g3[1]))
        t3 = texto("Entre 0,37 y 0,38, en milésimas", 24, CM).next_to(r3, UP, buff=0.35).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(t3))
        p3 = Dot(r3.n2p(0.375), radius=0.1, color=ACENTO)
        l3 = tex_decimal("0,375", 36).next_to(p3, UP, buff=0.2)
        self.play(FadeIn(p3, scale=2), Write(l3))
        idea = texto("Entre dos decimales siempre caben más decimales", 28, ACENTO).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(idea))
        self.wait(3)

    def zoom(self, r_arriba, a, b, r_abajo, color):
        marco = Rectangle(width=r_arriba.n2p(b)[0] - r_arriba.n2p(a)[0], height=0.35, color=color, stroke_width=3)
        marco.move_to((r_arriba.n2p(a) + r_arriba.n2p(b)) / 2)
        self.play(Create(marco))
        guias = VGroup(DashedLine(r_arriba.n2p(a) + DOWN * 0.18, r_abajo.n2p(a) + UP * 0.1, color=color),
                       DashedLine(r_arriba.n2p(b) + DOWN * 0.18, r_abajo.n2p(b) + UP * 0.1, color=color))
        trozo = Line(r_arriba.n2p(a), r_arriba.n2p(b), color=color, stroke_width=6)
        self.play(Create(guias))
        self.play(ReplacementTransform(trozo, r_abajo), run_time=1.3)


# ---------------------------------------------------------------------------
class CompararDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Comparar decimales", "Cifra a cifra, de izquierda a derecha")
        self.comparar(cab, "3,47", "3,52", "Mismas unidades → miramos las décimas: 4 < 5")
        self.trampa(cab)
        self.ceros(cab)

    def colocar(self, s, fila, centros, size=64):
        t = tex_decimal(s, size)
        ent, _, dec = s.partition(",")
        pos = ["UDC"[len(ent) - 1 - i] for i in range(len(ent))] + [","] + ["dcm"[i] for i in range(len(dec))]
        for p, c in zip(t, pos):
            p.move_to(centros[(fila, c)])
        return t, pos

    def comparar(self, cab, a, b, explicacion, extra=None):
        subtitulo_a(self, cab, f"¿Qué es mayor, {a} o {b}?")
        cols = ["U", ",", "d", "c", "m"]
        tabla, centros = tabla_posiciones(cols, filas=2, centro=np.array([-2.0, 0.3, 0]))
        self.play(FadeIn(tabla))
        ta, pa = self.colocar(a, 0, centros)
        tb, pb = self.colocar(b, 1, centros)
        self.play(LaggedStart(*[FadeIn(p) for p in ta], lag_ratio=0.1), LaggedStart(*[FadeIn(p) for p in tb], lag_ratio=0.1))
        # Recorremos las columnas
        flecha = Arrow(UP * 0.6, DOWN * 0.1, color=ACENTO).next_to(centros[(0, "U")], UP, buff=0.75)
        self.play(GrowArrow(flecha))
        da = dict(zip(pa, ta))
        db = dict(zip(pb, tb))
        for c in ["U", "d", "c", "m"]:
            self.play(flecha.animate.next_to(centros[(0, c)], UP, buff=0.75), run_time=0.5)
            va = da[c].get_tex_string() if c in da else "0"
            vb = db[c].get_tex_string() if c in db else "0"
            caja = SurroundingRectangle(VGroup(da.get(c, Dot(centros[(0, c)])), db.get(c, Dot(centros[(1, c)]))),
                                        color=ACENTO if va != vb else GREY_B, buff=0.12)
            self.play(Create(caja), run_time=0.4)
            if va != vb:
                break
            self.play(FadeOut(caja), run_time=0.3)
        mayor, menor = (a, b) if float(a.replace(",", ".")) > float(b.replace(",", ".")) else (b, a)
        r = VGroup(tex_decimal(a, 60), MathTex(">" if mayor == a else "<", font_size=60, color=ACENTO), tex_decimal(b, 60))
        r.arrange(RIGHT, buff=0.3).move_to([3.9, 0.3, 0])
        exp = texto(explicacion, 24, GREY_B).to_edge(DOWN, buff=0.5)
        self.play(Write(r), FadeIn(exp))
        if extra:
            self.play(FadeIn(extra))
        self.wait(2.5)
        limpiar_a(self, cab)

    def trampa(self, cab):
        subtitulo_a(self, cab, "¡Cuidado! ¿Qué es mayor, 0,5 o 0,45?")
        piensa = texto("Mucha gente piensa: «45 es mayor que 5, así que 0,45 es mayor»", 26, MAL).move_to([0, 1.8, 0])
        self.play(FadeIn(piensa))
        self.wait(1.5)
        no = texto("¡FALSO!", 40, MAL).next_to(piensa, DOWN, buff=0.3)
        self.play(Write(no))
        self.wait(1)
        self.play(FadeOut(VGroup(piensa, no)))
        cols = ["U", ",", "d", "c"]
        tabla, centros = tabla_posiciones(cols, filas=2, centro=np.array([-3.0, 0.5, 0]))
        self.play(FadeIn(tabla))
        ta, _ = self.colocar("0,5", 0, centros)
        tb, _ = self.colocar("0,45", 1, centros)
        self.play(FadeIn(ta), FadeIn(tb))
        cero = MathTex("0", font_size=64, color=GREY_B).move_to(centros[(0, "c")])
        nota = texto("Rellenamos con un 0: no cambia el valor", 22, GREY_B).next_to(tabla, DOWN, buff=0.25)
        self.play(FadeIn(cero, scale=1.5), FadeIn(nota))
        caja = SurroundingRectangle(VGroup(ta[2], tb[2]), color=ACENTO, buff=0.12)
        dec = texto("décimas: 5 > 4", 26, ACENTO).next_to(nota, DOWN, buff=0.2)
        self.play(Create(caja), FadeIn(dec))
        # Con la cuadrícula se ve
        g1 = self.cuadricula(50).scale(0.5).move_to([4.4, 1.0, 0])
        g2 = self.cuadricula(45).scale(0.5).move_to([4.4, -1.35, 0])
        l1 = tex_decimal("0,50", 40).next_to(g1, LEFT, buff=0.3)
        l2 = tex_decimal("0,45", 40).next_to(g2, LEFT, buff=0.3)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2))
        r = VGroup(tex_decimal("0,5", 60), MathTex(">", font_size=60, color=ACENTO), tex_decimal("0,45", 60))
        r.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9).shift(LEFT * 3)
        regla = texto("Tener MÁS cifras NO significa ser mayor", 26, ACENTO).to_edge(DOWN, buff=0.3)
        self.play(Write(r), FadeIn(regla))
        self.wait(3)
        limpiar_a(self, cab)

    def cuadricula(self, n):
        celdas = VGroup(*[Square(0.4, stroke_color=WHITE, stroke_width=1, fill_color=VACIO, fill_opacity=1)
                          for _ in range(100)]).arrange_in_grid(rows=10, cols=10, buff=0)
        for k in range(n):
            c, r = divmod(k, 10)
            celdas[r * 10 + c].set_fill(CC, 1)
        return celdas

    def ceros(self, cab):
        subtitulo_a(self, cab, "Los ceros a la derecha no cambian el valor")
        ancho = 9.0
        filas_a = [(10, 5, "0,5", (5, 10)), (100, 50, "0,50", (50, 100)), (1000, 500, "0,500", (500, 1000))]
        grupo = VGroup()
        for i, (partes, tomadas, s, (n, d)) in enumerate(filas_a):
            y = 1.5 - i * 1.25
            if partes <= 100:
                b = barra(partes, tomadas, ancho=ancho, alto=0.7)
            else:  # 1000 trozos: dibujamos solo el relleno con rayitas finas
                b = VGroup(Rectangle(width=ancho, height=0.7, stroke_color=WHITE, fill_color=VACIO, fill_opacity=1),
                           Rectangle(width=ancho / 2, height=0.7, stroke_width=0, fill_color=ACENTO, fill_opacity=1))
                b[1].align_to(b[0], LEFT)
                b.add(*[Line(UP * 0.35, DOWN * 0.35, stroke_width=0.4, color=WHITE).move_to(
                    b[0].get_left() + RIGHT * ancho * k / 200) for k in range(1, 200)])
            b.move_to([1.3, y, 0])
            lab = VGroup(tex_decimal(s, 48), MathTex("=", font_size=40), fraccion(n, d, size=36)).arrange(RIGHT, buff=0.15)
            lab.next_to(b, LEFT, buff=0.4)
            self.play(FadeIn(b), Write(lab), run_time=1)
            grupo.add(VGroup(b, lab))
        guia = DashedLine([1.3, 2.1, 0], [1.3, -1.6, 0], color=ACENTO)
        self.play(Create(guia))
        res = VGroup(tex_decimal("0,5", 56), MathTex("=", font_size=56), tex_decimal("0,50", 56),
                     MathTex("=", font_size=56), tex_decimal("0,500", 56)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9)
        nota = texto("¡Como las fracciones equivalentes!", 24, GREY_B).to_edge(DOWN, buff=0.35)
        self.play(Write(res), FadeIn(nota))
        self.wait(3)


# ---------------------------------------------------------------------------
class OrdenarDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Ordenar decimales")
        enun = texto("Ordena de menor a mayor:", 30, ACENTO).next_to(cab, DOWN, buff=0.35).to_edge(LEFT)
        nums = ["2,3", "2,03", "2,33", "2,13"]
        xs = [-4.5, -1.5, 1.5, 4.5]
        orig = [tex_decimal(s, 60).move_to([x, 1.6, 0]) for s, x in zip(nums, xs)]
        self.play(FadeIn(enun), LaggedStart(*[Write(o) for o in orig], lag_ratio=0.2))
        self.wait(0.8)

        paso = texto("1.º  Igualamos el número de decimales con ceros", 26, GREY_B).move_to([0, 0.5, 0])
        self.play(FadeIn(paso))
        nuevos = []
        for s, o, x in zip(nums, orig, xs):
            n_dec = len(s.split(",")[1])
            s2 = s + "0" * (2 - n_dec)
            t = tex_decimal(s2, 60).move_to([x, 1.6, 0])
            if len(s2) > len(s):
                t[-1].set_color(GREY_B)
            self.play(Transform(o, t), run_time=0.6)
            nuevos.append(s2)
        self.wait(1)
        self.play(FadeOut(paso))

        paso = texto("2.º  Los colocamos en la recta", 26, GREY_B).move_to([0, 0.5, 0])
        self.play(FadeIn(paso))
        recta = NumberLine(x_range=[2, 2.4, 0.01], length=12, include_tip=False, stroke_width=3,
                           tick_size=0.07).move_to([0, -1.2, 0])
        marcas = VGroup(*[Text(dec_txt(v, 1), font_size=20).next_to(recta.n2p(v), DOWN, buff=0.2)
                          for v in (2.0, 2.1, 2.2, 2.3, 2.4)])
        largas = VGroup(*[Line(recta.n2p(v) + UP * 0.15, recta.n2p(v) + DOWN * 0.15, stroke_width=3)
                          for v in (2.0, 2.1, 2.2, 2.3, 2.4)])
        self.play(Create(recta), FadeIn(marcas), FadeIn(largas))
        sobre = []
        for s, o in zip(nuevos, orig):
            v = float(s.replace(",", "."))
            d = Dot(recta.n2p(v), radius=0.1, color=ACENTO)
            c = o.copy()
            self.play(c.animate.scale(0.6).next_to(recta.n2p(v), UP, buff=0.3), FadeIn(d, scale=2), run_time=0.8)
            sobre.append((v, c, s))
        self.play(FadeOut(paso))

        orden = sorted(zip(nums, sobre), key=lambda t: t[1][0])
        partes = []
        for i, (s, _) in enumerate(orden):
            if i:
                partes.append(MathTex("<", font_size=56))
            partes.append(tex_decimal(s, 56))
        fila = VGroup(*partes).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in fila], lag_ratio=0.15), run_time=2)
        truco = texto("Ordenar de menor a mayor = leer la recta de izquierda a derecha", 24, ACENTO).move_to([0, 0.5, 0])
        self.play(FadeIn(truco), Circumscribe(fila, color=ACENTO))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
from decimal import Decimal  # noqa: E402

FRAC_A_DEC = [(7, 10), (35, 100), (8, 100), (125, 1000)]
DEC_A_FRAC = ["0,9", "0,47", "0,06", "1,3"]
VALOR_5 = ["5,2", "0,5", "3,05", "1,205"]
ESCRIBE = [("4 unidades y 8 décimas", "4,8"), ("2 unidades y 35 centésimas", "2,35"),
           ("7 centésimas", "0,07"), ("12 unidades y 9 milésimas", "12,009")]
RECTA = [(0, 1, ["0,2", "0,5", "0,9"]), (2, 3, ["2,4", "2,75"])]
COMPARA = [("4,7", "4,2"), ("0,8", "0,75"), ("3,06", "3,6"), ("1,5", "1,50"), ("0,099", "0,1")]
ORDENA = [(["0,7", "0,07", "0,77", "0,707"], True), (["5,1", "5,01", "5,11", "5,101"], False)]
INTERCALA = [("0,3", "0,4"), ("1,25", "1,26"), ("2", "2,1")]
ATLETAS = [("Laia", "13,08"), ("Marc", "13,8"), ("Nil", "12,95")]
ALTURAS = [("Pau", "1,6"), ("Julia", "1,58"), ("Ona", "1,605")]
PRECIOS = [("Libro A", "12,5"), ("Libro B", "12,45")]


def D_a(s):
    return Decimal(s.replace(",", "."))


def ndec_a(s):
    return len(s.partition(",")[2])


def fmt_a(v, k):
    return f"{v:.{k}f}".replace(".", ",") if k else str(int(v))


def pad_a(s, k):
    ent, _, dec = s.partition(",")
    return ent if k == 0 else ent + "," + dec + "0" * (k - len(dec))


def tex_pad(s, k, size=52):
    """Decimal con ceros añadidos hasta k decimales (los ceros nuevos en gris)."""
    t = tex_decimal(pad_a(s, k), size)
    extra = k - ndec_a(s)
    if extra:
        for p in t[-extra:]:
            p.set_color(GREY_B)
    return t


def filas_a(scene, rows, y0=1.9, dy=1.0, x0=-6.2, size_nota=22):
    """rows: lista de (mobject, nota o None). Notas alineadas en columna a la derecha."""
    for i, (m, _) in enumerate(rows):
        m.move_to([x0, y0 - i * dy, 0], aligned_edge=LEFT)
    x = max(m.get_right()[0] for m, _ in rows) + 0.6
    for m, nota in rows:
        scene.play(Write(m), run_time=1.0)
        if nota:
            n = texto(nota, size_nota, GREY_B).move_to([x, m.get_y(), 0], aligned_edge=LEFT)
            if n.get_right()[0] > config.frame_width / 2 - 0.2:
                n.next_to(m, DOWN, buff=0.08).align_to(m, LEFT)
            scene.play(FadeIn(n, shift=LEFT * 0.2), run_time=0.5)
    scene.wait(2.5)


def pagina_enunciados_a(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 27, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.25)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar_a(scene, cab)


ENUN_1 = [
    ("1. Fracciones y decimales:",
     "a) Escribe como decimal:   " + "    ".join(f"{n}/{d}" for n, d in FRAC_A_DEC) + "\n"
     "b) Escribe como fracción:   " + "    ".join(DEC_A_FRAC)),
    ("2. Valor de posición:",
     "a) ¿Cuánto vale la cifra 5 en cada número?   " + "    ".join(VALOR_5) + "\n"
     "b) Escribe el número:   " + "  ·  ".join(f"«{t}»" for t, _ in ESCRIBE[:2]) + "\n"
     "                                " + "  ·  ".join(f"«{t}»" for t, _ in ESCRIBE[2:])),
    ("3. Representa en la recta:",
     "a) Entre 0 y 1:   " + ";   ".join(RECTA[0][2]) + "\n"
     "b) Entre 2 y 3:   " + ";   ".join(RECTA[1][2])),
]
ENUN_2 = [
    ("4. Compara con <, > o =:", "    ".join(f"{l}) {a}  ?  {b}" for l, (a, b) in zip("abcde", COMPARA))),
    ("5. Ordena:", "a) De menor a mayor:   " + ";  ".join(ORDENA[0][0]) + "\n"
                   "b) De mayor a menor:   " + ";  ".join(ORDENA[1][0])),
    ("6. Escribe un decimal que esté entre:", "    ".join(f"{l}) {a} y {b}" for l, (a, b) in zip("abc", INTERCALA))),
    ("7. Problemas:",
     "a) En los 100 m, Laia hace 13,08 s, Marc 13,8 s y Nil 12,95 s.\n"
     "     ¿Quién gana? Haz la clasificación.\n"
     "b) Pau mide 1,6 m, Julia 1,58 m y Ona 1,605 m. Ordénalos de más alto a más bajo.\n"
     "c) Un libro cuesta 12,5 € y otro 12,45 €. ¿Cuál es más caro?"),
]


def con_letra(l, m, size=40):
    return VGroup(MathTex(rf"\text{{{l})}}", font_size=size), m).arrange(RIGHT, buff=0.3)


# --- 1a. Fracción → decimal
def resolver_frac_dec(scene, items, letras, ejemplo=False):
    rows = []
    for (n, d), l in zip(items, letras):
        k = len(str(d)) - 1
        s = fmt_a(Decimal(n) / Decimal(d), k)
        m = con_letra(l, VGroup(fraccion(n, d, size=44), MathTex("=", font_size=48), tex_decimal(s, 52))
                      .arrange(RIGHT, buff=0.25))
        nota = f"denominador {d}  →  {k} cifra{'s' if k > 1 else ''} decimal{'es' if k > 1 else ''}"
        if len(str(n)) < k:
            nota += " (con un 0)"
        rows.append((m, nota))
    filas_a(scene, rows, y0=1.8 if len(rows) > 1 else 0.6, dy=1.3)
    if ejemplo:
        regla = texto("Denominador 10 → 1 cifra decimal · 100 → 2 cifras · 1000 → 3 cifras", 26, ACENTO)
        scene.play(FadeIn(regla.to_edge(DOWN, buff=0.5)))
        scene.wait(2)


# --- 1b. Decimal → fracción
def resolver_dec_frac(scene, items, letras, ejemplo=False):
    rows = []
    for s, l in zip(items, letras):
        k = ndec_a(s)
        d = 10 ** k
        n = int(s.replace(",", ""))
        m = con_letra(l, VGroup(tex_decimal(s, 52), MathTex("=", font_size=48), fraccion(n, d, size=44))
                      .arrange(RIGHT, buff=0.25))
        rows.append((m, f"{k} cifra{'s' if k > 1 else ''} decimal{'es' if k > 1 else ''}  →  denominador {d}"))
    filas_a(scene, rows, y0=1.8 if len(rows) > 1 else 0.6, dy=1.3)
    if ejemplo:
        regla = texto("Se lee «nueve décimas» → 9/10", 26, ACENTO).to_edge(DOWN, buff=0.5)
        scene.play(FadeIn(regla))
        scene.wait(2)


# --- 2a. ¿Cuánto vale el 5?
def valor_del_5(s):
    ent, _, dec = s.partition(",")
    if "5" in ent:
        i = ent.index("5")
        pos = "UDC"[len(ent) - 1 - i]
        return s.index("5"), pos, "5" + "0" * (len(ent) - 1 - i)
    i = dec.index("5")
    return len(ent) + 1 + i, "dcm"[i], "0," + "0" * i + "5"


def resolver_valor5(scene, items, letras, ejemplo=False):
    rows = []
    for s, l in zip(items, letras):
        idx, pos, val = valor_del_5(s)
        num = tex_decimal(s, 56)
        caja = SurroundingRectangle(num[idx], color=ACENTO, buff=0.08)
        m = con_letra(l, VGroup(num, caja), 44)
        res = VGroup(MathTex(r"\rightarrow", font_size=44), Text(f"5 {NOMBRE_POS[pos]}", font_size=28, color=COLOR_POS[pos]),
                     MathTex("=", font_size=44), tex_decimal(val, 52)).arrange(RIGHT, buff=0.25)
        rows.append((VGroup(m, res).arrange(RIGHT, buff=0.4), None))
    filas_a(scene, rows, y0=1.9 if len(rows) > 1 else 0.6, dy=1.1)
    if ejemplo:
        regla = texto("Miramos en qué columna está el 5: unidades, décimas, centésimas...", 26, ACENTO)
        scene.play(FadeIn(regla.to_edge(DOWN, buff=0.5)))
        scene.wait(2)


# --- 2b. Escribe el número
def resolver_escribe(scene, items, letras, ejemplo=False):
    rows = []
    for (desc, s), l in zip(items, letras):
        m = con_letra(l, VGroup(texto(f"«{desc}»", 30), MathTex(r"\rightarrow", font_size=44), tex_decimal(s, 56))
                      .arrange(RIGHT, buff=0.3))
        nota = None
        ent, _, dec = s.partition(",")
        if "0" in dec:
            nota = "(ceros en los huecos)"
        rows.append((m, nota))
    filas_a(scene, rows, y0=1.9 if len(rows) > 1 else 0.6, dy=1.1)
    if ejemplo:
        s = items[0][1]
        cols = ["U", ",", "d", "c"]
        tabla, centros = tabla_posiciones(cols, filas=1, centro=np.array([0, -1.6, 0]))
        t = tex_decimal(s, 56)
        for p, pos in zip(t, t.posiciones):
            p.move_to(centros[(0, pos)])
        scene.play(FadeIn(tabla), FadeIn(t))
        scene.wait(2)


# --- 3. Recta
def resolver_recta(scene, a, b, vals, letra, ejemplo=False):
    lab = texto(f"{letra}) Entre {a} y {b}", 30).move_to([-4.5, 2.2, 0])
    r = NumberLine(x_range=[a, b, 0.1], length=11.5, include_tip=False, stroke_width=3,
                   tick_size=0.1).move_to([0, -0.4, 0])
    etiquetas = VGroup()
    for i in range(11):
        v = Decimal(a) + Decimal(i) / Decimal(10)
        s = str(a) if i == 0 else str(b) if i == 10 else fmt_a(v, 1)
        etiquetas.add(Text(s, font_size=18, color=CD if 0 < i < 10 else WHITE).next_to(r.n2p(float(v)), DOWN, buff=0.18))
    scene.play(FadeIn(lab), Create(r), FadeIn(etiquetas))
    for s in vals:
        v = float(D_a(s))
        if ejemplo:
            p = Dot(r.n2p(a) + UP * 0.22, radius=0.11, color=ACENTO)
            scene.play(FadeIn(p, scale=2))
            pasos = int(round((v - a) * 10))
            for k in range(pasos):
                arco = ArcBetweenPoints(r.n2p(a + k / 10) + UP * 0.22, r.n2p(a + (k + 1) / 10) + UP * 0.22, angle=-PI / 1.5)
                scene.play(MoveAlongPath(p, arco), run_time=0.45, rate_func=linear)
            scene.play(p.animate.move_to(r.n2p(v)))
            nota = texto(f"{pasos} décimas: {pasos} rayitas desde el {a}", 26, ACENTO).move_to([0, -1.8, 0])
            scene.play(FadeIn(nota))
        else:
            p = Dot(r.n2p(v), radius=0.11, color=ACENTO)
            scene.play(FadeIn(p, scale=2))
        t = tex_decimal(s, 40).next_to(r.n2p(v), UP, buff=0.4)
        scene.play(Write(t), Flash(p, color=ACENTO), run_time=0.8)
        if ndec_a(s) == 2:
            abajo = fmt_a(D_a(s).quantize(Decimal("0.1"), rounding="ROUND_FLOOR"), 1)
            arriba = fmt_a(D_a(abajo.replace(",", ".")) + Decimal("0.1"), 1) if False else fmt_a(D_a(abajo) + Decimal("0.1"), 1)
            nota = texto(f"{s} está justo a mitad de camino entre {abajo} y {arriba}", 24, GREY_B).move_to([0, -1.8, 0])
            scene.play(FadeIn(nota))
    scene.wait(2.5)


# --- 4. Comparar
def colocar_a(s, k, fila, centros, size=60):
    t = tex_pad(s, k, size)
    for p, pos in zip(t, t.posiciones):
        p.move_to(centros[(fila, pos)])
    return t


def resolver_compara(scene, a, b, letra, ejemplo=False):
    k = max(ndec_a(a), ndec_a(b))
    ne = max(len(a.partition(",")[0]), len(b.partition(",")[0]))
    cols = ["C", "D", "U"][3 - ne:] + [","] + ["d", "c", "m"][:k]
    lab = texto(f"{letra})", 34).move_to([-6.3, 0.3, 0])
    tabla, centros = tabla_posiciones(cols, filas=2, centro=np.array([-2.6, 0.2, 0]))
    scene.play(FadeIn(lab), FadeIn(tabla))
    ta = colocar_a(a, k, 0, centros)
    tb = colocar_a(b, k, 1, centros)
    scene.play(FadeIn(ta), FadeIn(tb))
    if k > min(ndec_a(a), ndec_a(b)):
        n = texto("rellenamos con ceros (en gris)", 22, GREY_B).next_to(tabla, DOWN, buff=0.25)
        scene.play(FadeIn(n))
    da, db = dict(zip(ta.posiciones, ta)), dict(zip(tb.posiciones, tb))
    flecha = Arrow(UP * 0.6, DOWN * 0.1, color=ACENTO).next_to(centros[(0, cols[0])], UP, buff=0.75)
    scene.play(GrowArrow(flecha))
    for c in cols:
        if c == ",":
            continue
        scene.play(flecha.animate.next_to(centros[(0, c)], UP, buff=0.75), run_time=0.45)
        va, vb = da[c].get_tex_string(), db[c].get_tex_string()
        caja = SurroundingRectangle(VGroup(da[c], db[c]), color=ACENTO if va != vb else GREY_B, buff=0.1)
        scene.play(Create(caja), run_time=0.35)
        if va != vb:
            break
        scene.play(FadeOut(caja), run_time=0.25)
    sig = ">" if D_a(a) > D_a(b) else "<" if D_a(a) < D_a(b) else "="
    r = VGroup(tex_decimal(a, 64), MathTex(sig, font_size=64, color=ACENTO), tex_decimal(b, 64)).arrange(RIGHT, buff=0.3)
    r.move_to([4.3, 0.2, 0])
    scene.play(Write(r))
    if sig == "=":
        exp = "Todas las cifras son iguales: ¡es el mismo número!"
    else:
        exp = f"La primera cifra distinta decide: {va} {sig} {vb}"
    scene.play(FadeIn(texto(exp, 26, ACENTO).to_edge(DOWN, buff=0.45)))
    scene.wait(2.5)


# --- 5 y 7. Ordenar (con ceros)
def ordenar(scene, items, creciente, nombres=None, unidad="", y0=1.6, conclusion=None):
    k = max(ndec_a(s) for s in items)
    paso = texto("Igualamos las cifras decimales con ceros", 24, GREY_B).move_to([0, y0 + 0.75, 0])
    scene.play(FadeIn(paso))
    for i, s in enumerate(items):
        y = y0 - i * 0.82
        parts = []
        if nombres:
            parts.append(texto(nombres[i], 28, ACENTO))
        orig = tex_decimal(s, 48)
        parts += [orig]
        g = VGroup(*parts).arrange(RIGHT, buff=0.5).move_to([-3.6, y, 0])
        fl = MathTex(r"\rightarrow", font_size=44).move_to([-0.9, y, 0])
        p = tex_pad(s, k, 48).move_to([0.9, y, 0])
        scene.play(FadeIn(g), run_time=0.5)
        scene.play(FadeIn(fl), TransformFromCopy(orig, p), run_time=0.7)
    signo = "<" if creciente else ">"
    orden = sorted(range(len(items)), key=lambda i: D_a(items[i]), reverse=not creciente)
    if nombres:
        cad = f"  {signo}  ".join(f"{nombres[i]} ({pad_a(items[i], k)}{unidad})" for i in orden)
        fila = texto(cad, 28, OK)
    else:
        partes = []
        for j, i in enumerate(orden):
            if j:
                partes.append(MathTex(signo, font_size=54))
            partes.append(tex_decimal(items[i], 54))
        fila = VGroup(*partes).arrange(RIGHT, buff=0.28)
    fila.move_to([0, y0 - len(items) * 0.82 - 0.35, 0])
    scene.play(FadeOut(paso))
    scene.play(FadeIn(fila, shift=UP * 0.2), run_time=1.5)
    scene.play(Circumscribe(fila, color=ACENTO))
    if conclusion:
        scene.play(FadeIn(texto(conclusion, 28, ACENTO).next_to(fila, DOWN, buff=0.35)))
    scene.wait(2.5)


# --- 6. Intercalar
def resolver_intercala(scene, a, b, letra, ejemplo=False):
    k = max(ndec_a(a), ndec_a(b)) + 1
    t1 = texto(f"{letra}) Entre {a} y {b}", 30).move_to([0, 2.2, 0])
    scene.play(FadeIn(t1))
    t2 = VGroup(texto("Añadimos una cifra decimal más:", 26, GREY_B), tex_pad(a, k, 44), texto("y", 26, GREY_B),
                tex_pad(b, k, 44)).arrange(RIGHT, buff=0.25).move_to([0, 1.3, 0])
    scene.play(FadeIn(t2))
    va, vb = D_a(a), D_a(b)
    r = NumberLine(x_range=[0, 10, 1], length=11, include_tip=False, stroke_width=3, tick_size=0.1).move_to([0, -0.4, 0])
    ext = VGroup(tex_decimal(pad_a(a, k), 32).next_to(r.n2p(0), DOWN, buff=0.2),
                 tex_decimal(pad_a(b, k), 32).next_to(r.n2p(10), DOWN, buff=0.2))
    nota_z = texto("hacemos zoom: el trozo se divide en 10 partes", 22, GREY_B).next_to(r, UP, buff=0.35)
    scene.play(Create(r), FadeIn(ext), FadeIn(nota_z))
    m = (va + vb) / 2
    sm = fmt_a(m, k)
    p = Dot(r.n2p(5), radius=0.12, color=ACENTO)
    lp = tex_decimal(sm, 40).next_to(p, UP, buff=0.3)
    scene.play(FadeOut(nota_z), FadeIn(p, scale=2), Write(lp))
    res = VGroup(tex_decimal(a, 56), MathTex("<", font_size=56), tex_decimal(sm, 56), MathTex("<", font_size=56),
                 tex_decimal(b, 56)).arrange(RIGHT, buff=0.25).move_to([0, -1.9, 0])
    scene.play(Write(res))
    if ejemplo:
        otras = [fmt_a(va + (vb - va) * j / 10, k) for j in (1, 2, 8, 9)]
        n = texto("También valen " + ";  ".join(otras[:2]) + " ...  " + ";  ".join(otras[2:]), 24, GREY_B)
        scene.play(FadeIn(n.to_edge(DOWN, buff=0.4)))
    scene.wait(2.5)


# --- 7. Problemas
def problema(scene, enunciado, datos, creciente, unidad, conclusion, aviso=None):
    enun = texto(enunciado, 26).move_to([0, 2.5, 0])
    scene.play(Write(enun), run_time=1.5)
    if aviso:
        a = texto(aviso, 26, MAL).next_to(enun, DOWN, buff=0.2)
        scene.play(FadeIn(a))
        scene.wait(1)
        scene.play(FadeOut(a))
    ordenar(scene, [s for _, s in datos], creciente, nombres=[n for n, _ in datos], unidad=unidad,
            y0=1.2, conclusion=conclusion)


class EjerciciosDecimalesEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Números decimales")
        pagina_enunciados_a(self, cab, ENUN_1)
        pagina_enunciados_a(self, cab, ENUN_2, size=22)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        pasos = [
            ("Ejercicio 1 a): fracción → decimal", lambda: resolver_frac_dec(self, FRAC_A_DEC[:1], "a", True)),
            ("Ejercicio 1 b): decimal → fracción", lambda: resolver_dec_frac(self, DEC_A_FRAC[:1], "a", True)),
            ("Ejercicio 2 a): ¿cuánto vale el 5?", lambda: resolver_valor5(self, VALOR_5[:1], "a", True)),
            ("Ejercicio 2 b): escribe el número", lambda: resolver_escribe(self, ESCRIBE[:1], "a", True)),
            ("Ejercicio 3 a)", lambda: resolver_recta(self, RECTA[0][0], RECTA[0][1], RECTA[0][2][:1], "a", True)),
            ("Ejercicio 4 a)", lambda: resolver_compara(self, *COMPARA[0], "a", True)),
            ("Ejercicio 5 a): de menor a mayor", lambda: ordenar(self, *ORDENA[0])),
            ("Ejercicio 6 a)", lambda: resolver_intercala(self, *INTERCALA[0], "a", True)),
            ("Ejercicio 7 a)", lambda: problema(
                self, "En los 100 m, Laia hace 13,08 s, Marc 13,8 s y Nil 12,95 s. ¿Quién gana?",
                ATLETAS, True, " s", "Gana Nil: 1.º Nil, 2.º Laia, 3.º Marc",
                aviso="¡Ojo! En una carrera gana quien tarda MENOS tiempo")),
        ]
        for sub, f in pasos:
            subtitulo_a(self, cab, sub)
            f()
            limpiar_a(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosDecimalesResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Números decimales")
        pasos = [
            ("Ejercicio 1 a): b), c) y d)", lambda: resolver_frac_dec(self, FRAC_A_DEC[1:], "bcd")),
            ("Ejercicio 1 b): b), c) y d)", lambda: resolver_dec_frac(self, DEC_A_FRAC[1:], "bcd")),
            ("Ejercicio 2 a): b), c) y d)", lambda: resolver_valor5(self, VALOR_5[1:], "bcd")),
            ("Ejercicio 2 b): b), c) y d)", lambda: resolver_escribe(self, ESCRIBE[1:], "bcd")),
            ("Ejercicio 3 a)", lambda: resolver_recta(self, RECTA[0][0], RECTA[0][1], RECTA[0][2][1:], "a")),
            ("Ejercicio 3 b)", lambda: resolver_recta(self, RECTA[1][0], RECTA[1][1], RECTA[1][2], "b")),
        ]
        for l, (a, b) in zip("bcde", COMPARA[1:]):
            pasos.append((f"Ejercicio 4 {l})", lambda a=a, b=b, l=l: resolver_compara(self, a, b, l)))
        pasos += [
            ("Ejercicio 5 b): de mayor a menor", lambda: ordenar(self, *ORDENA[1])),
        ]
        for l, (a, b) in zip("bc", INTERCALA[1:]):
            pasos.append((f"Ejercicio 6 {l})", lambda a=a, b=b, l=l: resolver_intercala(self, a, b, l)))
        pasos += [
            ("Ejercicio 7 b)", lambda: problema(
                self, "Pau mide 1,6 m, Julia 1,58 m y Ona 1,605 m.\nOrdénalos de más alto a más bajo.",
                ALTURAS, False, " m", "Ona es la más alta y Julia la más baja")),
            ("Ejercicio 7 c)", lambda: problema(
                self, "Un libro cuesta 12,5 € y otro 12,45 €. ¿Cuál es más caro?",
                PRECIOS, False, " €", "El libro A es más caro (5 céntimos más)")),
        ]
        for sub, f in pasos:
            subtitulo_a(self, cab, sub)
            f()
            limpiar_a(self, cab)

        fin = texto("¡Muy bien! Ya sabes leer, comparar y ordenar decimales.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)


# ===========================================================================
# Antes t08_operaciones_decimales.py
from decimal import ROUND_HALF_UP, Decimal



ROSA = "#FF79C6"
ORDEN_POS = ["M", "C", "D", "U", "d", "c", "m", "x"]
SINGULAR = {"M": "millar", "C": "centena", "D": "decena", "U": "unidad",
            "d": "décima", "c": "centésima", "m": "milésima", "x": "diezmilésima"}


# ---------------------------------------------------------------------------
# Utilidades
def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def D(s):
    return Decimal(str(s).replace(",", "."))


def ndec(s):
    return len(s.partition(",")[2])


def norm(v):
    """Decimal -> texto con coma y sin ceros sobrantes: 3.90 -> '3,9'; 750.0 -> '750'."""
    return format(v.normalize(), "f").replace(".", ",")


def fmt(v, k):
    """Decimal -> texto con k decimales exactos."""
    return format(v.quantize(Decimal(1).scaleb(-k)), "f").replace(".", ",") if k else str(int(v))


def pad(s, k):
    ent, _, dec = s.partition(",")
    return ent if k == 0 else ent + "," + dec + "0" * (k - len(dec))


def tx(s):
    """Coma decimal para MathTex."""
    return str(s).replace(",", "{,}")


def posiciones(s):
    ent, coma, dec = s.partition(",")
    return ["UDCM"[len(ent) - 1 - i] for i in range(len(ent))] + ([","] if coma else []) + \
        ["dcmx"[i] for i in range(len(dec))]


def colocar(s, fila, centros, size=56):
    """tex_decimal con cada cifra en su casilla de la tabla."""
    t = tex_decimal(s, size)
    for p, c in zip(t, posiciones(s)):
        p.move_to(centros[(fila, c)])
    return t


def filas(scene, rows, y0=1.9, dy=1.0, x0=-6.2, size_nota=22, espera=2.5):
    """rows: lista de (mobject, nota o None). Notas alineadas en columna a la derecha."""
    for i, (m, _) in enumerate(rows):
        m.move_to([x0, y0 - i * dy, 0], aligned_edge=LEFT)
    x = max(m.get_right()[0] for m, _ in rows) + 0.6
    for m, nota in rows:
        scene.play(Write(m), run_time=1.0)
        if nota:
            n = texto(nota, size_nota, GREY_B).move_to([x, m.get_y(), 0], aligned_edge=LEFT)
            if n.get_right()[0] > config.frame_width / 2 - 0.2:
                n.next_to(m, DOWN, buff=0.08).align_to(m, LEFT)
            scene.play(FadeIn(n, shift=LEFT * 0.2), run_time=0.5)
    scene.wait(espera)


class Notas:
    """Una sola nota a la vez en la parte de abajo."""

    def __init__(self, scene, size=26, color=ACENTO, buff=0.4):
        self.scene, self.size, self.color, self.buff, self.actual = scene, size, color, buff, None

    def __call__(self, cadena_txt, color=None):
        nueva = texto(cadena_txt, self.size, color or self.color)
        if nueva.width > config.frame_width - 1.0:
            nueva.scale_to_fit_width(config.frame_width - 1.0)
        nueva.to_edge(DOWN, buff=self.buff)
        if self.actual:
            self.scene.play(FadeOut(self.actual), FadeIn(nueva), run_time=0.6)
        else:
            self.scene.play(FadeIn(nueva), run_time=0.6)
        self.actual = nueva

    def fin(self):
        if self.actual:
            self.scene.play(FadeOut(self.actual), run_time=0.4)
            self.actual = None


# ---------------------------------------------------------------------------
# Suma y resta en columnas (coma debajo de coma)
def operar_columnas(scene, a, b, op, centro, tabla=True, w=0.85, h=0.8, size=52, notas=None, nombres=True):
    k = max(ndec(a), ndec(b))
    res = D(a) + D(b) if op == "+" else D(a) - D(b)
    ra, rb, rr = pad(a, k), pad(b, k), fmt(res, k)
    ent = max(len(x.partition(",")[0]) for x in (ra, rb, rr))
    cols = ["UDCM"[i] for i in range(ent - 1, -1, -1)] + ([","] + list("dcmx"[:k]) if k else [])
    grupo, centros = tabla_posiciones(cols, filas=3, centro=np.array([centro[0], centro[1], 0]), w=w, h=h,
                                      nombres=nombres)
    if tabla:
        scene.play(FadeIn(grupo))
    ta, tb = colocar(ra, 0, centros, size), colocar(rb, 1, centros, size)
    extra = []
    for t, s, orig in ((ta, ra, a), (tb, rb, b)):
        n_extra = len(s) - len(orig)
        for p in (t[len(t) - n_extra:] if n_extra else []):
            p.set_color(GREY_B)
            extra.append(p)
    originales = [p for p in list(ta) + list(tb) if p not in extra]
    xs = [centros[(0, c)][0] for c in cols]
    signo = MathTex("+" if op == "+" else "-", font_size=size).move_to(
        [min(xs) - w * 0.9, centros[(1, cols[0])][1], 0])
    y_raya = (centros[(1, cols[0])][1] + centros[(2, cols[0])][1]) / 2
    raya = Line([min(xs) - w * 1.3, y_raya, 0], [max(xs) + w * 0.5, y_raya, 0], stroke_width=3)
    scene.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in originales], lag_ratio=0.08), FadeIn(signo),
               run_time=1.5)
    if notas:
        notas("Coma debajo de coma: cada cifra en su columna")
    if extra:
        scene.play(*[FadeIn(p, scale=1.5) for p in extra])
        if notas:
            notas("Completamos con ceros para tener las mismas cifras decimales")
    scene.play(Create(raya))

    tr = colocar(rr, 2, centros, size).set_color(ACENTO)
    dig_r = {c: p for c, p in zip(posiciones(rr), tr)}
    da = {c: int(p.get_tex_string()) for c, p in zip(posiciones(ra), ta) if c != ","}
    db = {c: int(p.get_tex_string()) for c, p in zip(posiciones(rb), tb) if c != ","}
    columnas = [c for c in cols if c != ","][::-1]
    marco = Rectangle(width=w, height=3 * h, stroke_color=ACENTO, stroke_width=3)
    llevo = 0
    dig_a = {c: p for c, p in zip(posiciones(ra), ta)}
    actual, marcas, cambios = {}, {}, {}
    sitios = [LEFT * w * 0.3 + UP * h * 0.3, RIGHT * w * 0.3 + UP * h * 0.3, UP * h * 0.55]

    def cambiar(col, v):
        """Tacha la cifra de arriba de 'col' y escribe encima su nuevo valor."""
        actual[col] = v
        viejo = marcas.get(col, dig_a[col])
        tacha = Line(viejo.get_corner(DL), viejo.get_corner(UR), color=MAL, stroke_width=3)
        n = cambios.get(col, 0)
        nuevo_m = MathTex(str(v), font_size=int(size * 0.5), color=ACENTO).move_to(centros[(0, col)] + sitios[min(n, 2)])
        scene.play(Create(tacha), FadeIn(nuevo_m, shift=DOWN * 0.15), run_time=0.6)
        marcas[col], cambios[col] = nuevo_m, n + 1
    for j, c in enumerate(columnas):
        x, y = centros[(1, c)][0], centros[(1, c)][1]
        if j == 0:
            marco.move_to([x, y, 0])
            scene.play(Create(marco), run_time=0.4)
        else:
            scene.play(marco.animate.move_to([x, y, 0]), run_time=0.35)
        if c == "U" and "," in rr:
            scene.play(FadeIn(dig_r[","], shift=DOWN * 0.3), run_time=0.4)
            if notas and j == len([q for q in columnas if q in "dcmx"]):
                notas("La coma del resultado baja recta")
        x1, x2 = da.get(c, 0), db.get(c, 0)
        nuevo = 0
        if op == "+":
            s = x1 + x2 + llevo
            dig, nuevo = s % 10, s // 10
            frase = f"{x1} + {x2}" + (f" + {llevo}" if llevo else "") + f" = {s}"
            if nuevo:
                frase += f": escribo {dig} y me llevo 1"
        else:
            # Desagrupar: si arriba no llega, pedimos 1 a la columna de la izquierda (1 décima = 10 centésimas...)
            x1 = actual.setdefault(c, x1)
            if x1 < x2:
                k = j + 1
                while actual.get(columnas[k], da.get(columnas[k], 0)) == 0:
                    k += 1
                izq = columnas[j + 1]
                if k == j + 1:
                    pide = (f"{x1} − {x2} no se puede: deshacemos 1 {SINGULAR[izq]} en 10 {NOMBRE_POS[c]}")
                else:
                    pide = (f"{x1} − {x2} no se puede y al lado hay un 0: pedimos a las {NOMBRE_POS[columnas[k]]}")
                if notas:
                    notas(pide)
                fuente = columnas[k]
                cambiar(fuente, actual.setdefault(fuente, da.get(fuente, 0)) - 1)
                for m in reversed(columnas[j + 1:k]):
                    cambiar(m, 9)
                cambiar(c, x1 + 10)
                x1 = actual[c]
                if notas:
                    scene.wait(0.8)
            dig = x1 - x2
            frase = f"{x1} − {x2} = {dig}"
        anims = []
        if c in dig_r:
            anims.append(Write(dig_r[c]))
        if notas:
            notas(frase)
        if anims:
            scene.play(*anims, run_time=0.6)
        sig = columnas[j + 1] if j + 1 < len(columnas) else None
        if nuevo and sig:
            uno = MathTex("1", font_size=28, color=ACENTO).move_to(centros[(0, sig)] + UP * h * 0.55)
            scene.play(FadeIn(uno, scale=1.5), run_time=0.4)
        llevo = nuevo
        if notas:
            scene.wait(0.8)
    scene.play(FadeOut(marco), Circumscribe(tr, color=ACENTO))
    if notas:
        notas.fin()
    return rr, VGroup(grupo if tabla else VGroup(), ta, tb, tr, signo, raya)


# ---------------------------------------------------------------------------
# División larga (a la española: dividendo | divisor, cociente debajo)
W_DIG, W_COMA, H_FILA = 0.42, 0.13, 0.62


def simular_division(dividendo, divisor, max_dec=3):
    ent, _, dec = dividendo.partition(",")
    digs = [int(c) for c in ent + dec]
    k = len(ent)
    i0 = 0
    while i0 < k - 1 and int(ent[:i0 + 1]) < divisor:
        i0 += 1
    pasos, i, cur, q = [], i0, int(ent[:i0 + 1]), ""
    while True:
        cq, r = divmod(cur, divisor)
        q += str(cq)
        pasos.append((i, cur, cq, r))
        i += 1
        if i >= len(digs):
            if r == 0 or i - k >= max_dec:
                break
            digs.append(0)
        if i == k:
            q += ","
        cur = r * 10 + digs[i]
    return digs, k, i0, pasos, q


def division_larga(scene, dividendo, divisor, x0, y0, size=46, max_dec=3, notas=None, lateral=False, rt=0.5):
    """Dibuja y resuelve dividendo : divisor (divisor natural). Devuelve el cociente (texto)."""
    digs, k, i0, pasos, q = simular_division(dividendo, divisor, max_dec)
    n_orig = len(dividendo.replace(",", ""))
    tiene_coma = "," in dividendo

    def cx(i):
        return x0 + i * W_DIG + (W_COMA if i >= k else 0)

    cifras = [MathTex(str(d), font_size=size, color=WHITE if i < n_orig else GREY_B).move_to([cx(i), y0, 0])
              for i, d in enumerate(digs)]
    coma = MathTex(",", font_size=size, color=WHITE if tiene_coma else GREY_B)
    coma.move_to([x0 + (k - 1) * W_DIG + W_DIG / 2 + W_COMA / 2, y0 - 0.12, 0])
    xd = cx(len(digs) - 1) + W_DIG / 2 + 0.3
    dv = MathTex(str(divisor), font_size=size).move_to([xd + 0.2, y0, 0], aligned_edge=LEFT)
    ancho = max(dv.width, len(q) * W_DIG) + 0.4
    llave = VGroup(Line([xd, y0 + 0.35, 0], [xd, y0 - 0.35, 0]), Line([xd, y0 - 0.35, 0], [xd + ancho, y0 - 0.35, 0]))
    visibles = cifras[:n_orig] + ([coma] if tiene_coma else [])
    scene.play(*[FadeIn(c) for c in visibles], FadeIn(dv), Create(llave), run_time=0.8)

    yq = y0 - H_FILA - 0.05
    xq = [xd + 0.2]

    def escribir_cociente(ch):
        m = MathTex("," if ch == "," else ch, font_size=size, color=ACENTO)
        ancho_c = W_COMA if ch == "," else W_DIG
        m.move_to([xq[0] + ancho_c / 2, yq - (0.12 if ch == "," else 0), 0])
        xq[0] += ancho_c
        return m

    lado = None
    caja = SurroundingRectangle(VGroup(*cifras[:i0 + 1]), color=ACENTO, buff=0.08)
    scene.play(Create(caja), run_time=0.4)
    if notas and i0 > 0:
        notas(f"{int(dividendo.partition(',')[0][:i0])} < {divisor}: cogemos una cifra más")
    resto_prev = None
    for j, (i, cur, cq, r) in enumerate(pasos):
        if j > 0:
            y = y0 - j * H_FILA
            if i >= n_orig:
                aparecer = [FadeIn(cifras[i], scale=1.5)]
                if not tiene_coma and i == k:
                    aparecer.append(FadeIn(coma))
                if notas:
                    notas("No quedan cifras: añadimos un 0" + (" (y la coma)" if not tiene_coma and i == k else ""))
                scene.play(*aparecer, run_time=0.5)
            baja = cifras[i].copy().set_color(WHITE)
            scene.play(baja.animate.move_to([cx(i), y, 0]), run_time=rt)
            if i == k:
                c = escribir_cociente(",")
                if notas:
                    notas("Bajamos la primera cifra decimal: ponemos la coma en el cociente")
                scene.play(FadeIn(c, scale=2), run_time=0.5)
            grupo_cur = VGroup(resto_prev, baja) if resto_prev is not None else baja
            scene.play(caja.animate.become(SurroundingRectangle(grupo_cur, color=ACENTO, buff=0.08)), run_time=0.3)
        if lateral:
            nuevo = MathTex(rf"{cur} : {divisor} = {cq}", r"\quad \text{resto } " + str(r), font_size=30, color=GREY_B)
            nuevo.move_to([xd + 0.2, y0 - 2.4 * H_FILA, 0], aligned_edge=LEFT)
            if lado:
                scene.play(ReplacementTransform(lado, nuevo), run_time=0.4)
            else:
                scene.play(FadeIn(nuevo), run_time=0.4)
            lado = nuevo
        scene.play(Write(escribir_cociente(str(cq))), run_time=rt)
        y_r = y0 - (j + 1) * H_FILA
        rs = str(r)
        resto = VGroup(*[MathTex(ch, font_size=size).move_to([cx(i - len(rs) + 1 + t), y_r, 0])
                         for t, ch in enumerate(rs)])
        scene.play(FadeIn(resto), run_time=rt)
        resto_prev = resto
        if notas:
            scene.wait(0.6)
    fin = [FadeOut(caja)] + ([FadeOut(lado)] if lado else [])
    scene.play(*fin, run_time=0.4)
    return q


def con_divisor_natural(a, b):
    """a : b con b decimal -> (a·10^n, b·10^n, 10^n)."""
    n = ndec(b)
    f = 10 ** n
    return norm(D(a) * f), int(D(b) * f), f


# ---------------------------------------------------------------------------
# Multiplicar en una fila: sin comas -> contar decimales -> poner la coma
def con_n_dec(p, n):
    s = str(p).rjust(n + 1, "0")
    return s if n == 0 else s[:-n] + "," + s[-n:]


def mult_fila(scene, a, b, letra, y, x=-6.4, size=44, notas=None, ancho_max=13.2):
    ia, ib = int(a.replace(",", "")), int(b.replace(",", ""))
    na, nb = ndec(a), ndec(b)
    n, p = na + nb, ia * ib
    exacto, final = con_n_dec(p, n), norm(D(a) * D(b))
    piezas = [
        MathTex(rf"{tx(a)} \cdot {tx(b)}", font_size=size),
        MathTex(rf"\rightarrow\; {ia} \cdot {ib} = {p}", font_size=size, color=GREY_A),
        MathTex(rf"\rightarrow\; {na} + {nb} = {n}" + r"\text{ dec.}", font_size=size, color=COLOR_POS["d"]),
        MathTex(rf"\rightarrow\; {tx(exacto)}" + (rf" = {tx(final)}" if final != exacto else ""), font_size=size,
                color=ACENTO),
    ]
    partes = ([texto(f"{letra})", 30)] if letra else []) + piezas
    g = VGroup(*partes).arrange(RIGHT, buff=0.3)
    ancho_max = min(ancho_max, config.frame_width / 2 - 0.3 - x)
    if g.width > ancho_max:
        g.scale_to_fit_width(ancho_max)
    g.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    frases = [None, "1.º Multiplicamos sin comas",
              f"2.º Contamos los decimales de los dos factores: {na} + {nb} = {n}",
              f"3.º Separamos {n} cifra{'s' if n != 1 else ''} decimal{'es' if n != 1 else ''} desde la derecha"]
    if final != exacto:
        frases[3] += " (y quitamos los ceros del final)"
    if letra:
        scene.play(FadeIn(partes[0]), run_time=0.3)
    for pz, fr in zip(piezas, frases):
        if notas and fr:
            notas(fr)
        scene.play(Write(pz), run_time=0.9)
        if notas:
            scene.wait(1)
    scene.play(Circumscribe(piezas[-1], color=ACENTO), run_time=0.8)
    if notas:
        notas.fin()
    return g


# ---------------------------------------------------------------------------
# Redondear
def redondear(scene, s, pos, letra, y, x=-6.2, size=60, notas=None):
    k = "dcm".index(pos) + 1
    t = tex_decimal(s, size)
    ps = posiciones(s)
    idx = ps.index(pos)
    res = fmt(D(s).quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP), k)
    lab = texto(f"{letra}) a las {NOMBRE_POS[pos]}:" if letra else f"A las {NOMBRE_POS[pos]}:", 26, COLOR_POS[pos])
    g = VGroup(lab, t).arrange(RIGHT, buff=0.4).move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    scene.play(FadeIn(lab), Write(t), run_time=0.9)
    caja = SurroundingRectangle(t[idx], color=COLOR_POS[pos], buff=0.08)
    scene.play(Create(caja), run_time=0.5)
    sig = int(t[idx + 1].get_tex_string())
    flecha = Arrow(t[idx + 1].get_top() + UP * 0.55, t[idx + 1].get_top() + UP * 0.05, buff=0, color=ACENTO,
                   stroke_width=4, max_tip_length_to_length_ratio=0.35)
    if notas:
        notas(f"Miramos la cifra siguiente: {sig}" + (" ≥ 5 → la cifra de la caja sube 1" if sig >= 5
                                                         else " < 5 → la cifra de la caja se queda igual"))
    scene.play(GrowArrow(flecha), Indicate(t[idx + 1], color=ACENTO, scale_factor=1.4))
    r = VGroup(MathTex(r"\approx", font_size=size), tex_decimal(res, size)).arrange(RIGHT, buff=0.25)
    r.next_to(t, RIGHT, buff=0.4)
    nota = texto("sube 1" if sig >= 5 else "igual", 22, OK if sig >= 5 else GREY_B).next_to(flecha, UP, buff=0.05)
    scene.play(Write(r), FadeIn(nota))
    scene.play(Circumscribe(r[1], color=ACENTO), run_time=0.8)
    if notas:
        scene.wait(1)
        notas.fin()
    return res


# ---------------------------------------------------------------------------
# ×10, ×100... en la tabla
def mover_en_tabla(scene, s, op, n, centros, fila=0, size=60, notas=None, linea_y=2.2):
    k = len(str(n)) - 1
    res = D(s) * n if op == "x" else D(s) / n
    rs = norm(res)
    simb = r"\cdot" if op == "x" else ":"
    enun = MathTex(rf"{tx(s)} {simb} {n} =", font_size=58).move_to([-1.0, linea_y, 0])
    scene.play(Write(enun))
    t = colocar(s, fila, centros, size)
    scene.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in t], lag_ratio=0.1))
    if notas:
        lugares = f"{k} lugar{'es' if k > 1 else ''}"
        notas(f"Cada cifra se mueve {lugares} a la " + ("IZQUIERDA: vale " if op == "x" else "DERECHA: vale ")
              + f"{n} veces " + ("más" if op == "x" else "menos") + ". La coma no se mueve.")
    movs = []
    ocupadas = set()
    cero_inicial = s.partition(",")[0].strip("0") == ""  # 0,5 -> el 0 de las unidades no cuenta
    for p, c in zip(t, posiciones(s)):
        if c == ",":
            continue
        if cero_inicial and c in "UDCM":
            movs.append(FadeOut(p))
            continue
        nuevo = ORDEN_POS[ORDEN_POS.index(c) + (-k if op == "x" else k)]
        ocupadas.add(nuevo)
        movs.append(p.animate.move_to(centros[(fila, nuevo)]).set_color(COLOR_POS[nuevo]))
    scene.play(*movs, run_time=1.6)
    ceros = VGroup()
    for c in posiciones(rs):
        if c != "," and c not in ocupadas:
            ceros.add(MathTex("0", font_size=size, color=GREY_B).move_to(centros[(fila, c)]))
    if len(ceros):
        scene.play(FadeIn(ceros, scale=1.5))
        if notas:
            notas("Rellenamos los huecos con ceros", GREY_B)
    if "," not in rs:
        scene.play(t[posiciones(s).index(",")].animate.set_opacity(0.25))
    r = tex_decimal(rs, 58).next_to(enun, RIGHT, buff=0.3)
    scene.play(Write(r), Circumscribe(r, color=ACENTO))
    scene.wait(1.5)
    if notas:
        notas.fin()
    return VGroup(enun, t, ceros, r)


# ===========================================================================
class SumaRestaDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Sumar y restar decimales", "Coma debajo de coma")
        notas = Notas(self)
        ctx = texto("Un cuaderno cuesta 3,45 € y un libro 12,8 €. ¿Cuánto pagamos?", 28).move_to([0, 2.5, 0])
        self.play(FadeIn(ctx))
        operar_columnas(self, "3,45", "12,8", "+", (0, -0.2), w=1.0, h=0.85, notas=notas)
        sol = texto("Pagamos 16,25 €", 32, OK).move_to([4.6, -0.2, 0])
        self.play(FadeIn(sol))
        self.wait(2.5)
        limpiar(self, cab)

        # Error típico: alinear por la derecha
        subtitulo(self, cab, "¡Cuidado con este error!")
        mal = VGroup(MathTex(r"3{,}45", font_size=64), MathTex(r"+\;12{,}8", font_size=64)).arrange(DOWN, buff=0.25,
                                                                                                    aligned_edge=RIGHT)
        raya = Line(mal.get_corner(DL) + DOWN * 0.15, mal.get_corner(DR) + DOWN * 0.15)
        malg = VGroup(mal, raya).move_to([-3.2, 0.4, 0])
        self.play(Write(mal), Create(raya))
        cruz = Cross(malg, stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        exp = texto("Alineando por la derecha sumaríamos\ncentésimas con décimas: ¡NO!", 28, MAL).move_to([3.0, 1.0, 0])
        self.play(FadeIn(exp))
        bien = VGroup(tex_decimal("3,45", 64), tex_decimal("12,80", 64)).arrange(DOWN, buff=0.25)
        bien[0].shift(RIGHT * (bien[1][2].get_x() - bien[0][1].get_x()))
        bien[1][-1].set_color(GREY_B)
        okm = texto("Coma debajo de coma ✓", 28, OK).next_to(bien, UP, buff=0.3)
        VGroup(bien, okm).move_to([3.0, -1.4, 0])
        self.play(FadeIn(okm), Write(bien))
        self.wait(3)
        limpiar(self, cab)

        # Resta llevando
        subtitulo(self, cab, "Restar: igual, coma debajo de coma")
        operar_columnas(self, "7,2", "3,85", "-", (0, 0.0), w=1.0, h=0.85, notas=notas)
        regla = texto("Si faltan cifras decimales, completamos con ceros", 26, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(regla))
        self.wait(3)


# ===========================================================================
class PorDiezCienMil(Scene):
    def construct(self):
        cab = titulo(self, "Por 10, 100, 1000", "Las cifras se mueven, la coma se queda quieta")
        notas = Notas(self, size=24)
        cols = ["C", "D", "U", ",", "d", "c", "m"]
        tabla, centros = tabla_posiciones(cols, filas=1, centro=np.array([0, 0.1, 0]), w=1.05, h=1.0)
        self.play(FadeIn(tabla))
        for s, op, n in (("3,47", "x", 10), ("3,47", "x", 100), ("0,5", "x", 1000)):
            g = mover_en_tabla(self, s, op, n, centros, notas=notas)
            self.play(FadeOut(g))
        for s, op, n in (("45,2", ":", 10), ("3,1", ":", 100)):
            g = mover_en_tabla(self, s, op, n, centros, notas=notas)
            self.play(FadeOut(g))
        limpiar(self, cab)

        subtitulo(self, cab, "Resumen")
        r1 = VGroup(MathTex(r"\cdot 10,\ \cdot 100,\ \cdot 1000", font_size=48, color=OK),
                    texto("las cifras pasan 1, 2 o 3 lugares a la IZQUIERDA\n(es como mover la coma a la derecha)", 26))
        r2 = VGroup(MathTex(r": 10,\ : 100,\ : 1000", font_size=48, color=COLOR_POS["d"]),
                    texto("las cifras pasan 1, 2 o 3 lugares a la DERECHA\n(es como mover la coma a la izquierda)", 26))
        for r in (r1, r2):
            r.arrange(RIGHT, buff=0.5)
        VGroup(r1, r2).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to([0, 0.4, 0])
        self.play(FadeIn(r1, shift=RIGHT * 0.2))
        self.play(FadeIn(r2, shift=RIGHT * 0.2))
        truco = texto("Tantos lugares como ceros tiene el 10, 100, 1000", 28, ACENTO).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(truco))
        self.wait(3)


# ===========================================================================
class MultiplicarDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicar decimales", "El rectángulo de 2,3 × 1,4")
        s = 1.75
        a, b = 2.3, 1.4
        c0 = np.array([-3.1, -0.4, 0])
        rect = Rectangle(width=a * s, height=b * s, stroke_color=WHITE, stroke_width=3, fill_color=ACENTO,
                         fill_opacity=0.25).move_to(c0)
        izq, abajo = rect.get_left()[0], rect.get_bottom()[1]
        finas = VGroup(*[Line([izq + s * i / 10, abajo, 0], [izq + s * i / 10, abajo + b * s, 0], stroke_width=0.8,
                              color=GREY_B) for i in range(1, 23)],
                       *[Line([izq, abajo + s * j / 10, 0], [izq + a * s, abajo + s * j / 10, 0], stroke_width=0.8,
                              color=GREY_B) for j in range(1, 14)])
        gruesas = VGroup(*[Line([izq + s * i, abajo, 0], [izq + s * i, abajo + b * s, 0], stroke_width=3) for i in (1, 2)],
                         Line([izq, abajo + s, 0], [izq + a * s, abajo + s, 0], stroke_width=3))
        la = MathTex(r"2{,}3", font_size=40).next_to(Brace(rect, DOWN), DOWN, buff=0.1)
        lb = MathTex(r"1{,}4", font_size=40).next_to(Brace(rect, LEFT), LEFT, buff=0.1)
        self.play(FadeIn(rect), GrowFromCenter(Brace(rect, DOWN)), GrowFromCenter(Brace(rect, LEFT)), FadeIn(la), FadeIn(lb))
        p1 = texto("Lados: 2,3 y 1,4.\nEl área es 2,3 × 1,4", 26).move_to([3.4, 2.0, 0])
        self.play(FadeIn(p1))
        self.play(Create(gruesas))
        uni = texto("Los cuadrados grandes son de 1 × 1", 24, GREY_B).move_to([3.4, 0.9, 0])
        self.play(FadeIn(uni))
        self.play(Create(finas), run_time=2)
        cuad = Square(s / 10, stroke_color=ACENTO, fill_color=ACENTO, fill_opacity=1).move_to(
            [izq + s / 20, abajo + s / 20, 0])
        c1 = VGroup(texto("Cada cuadradito:", 24), MathTex(r"0{,}1 \cdot 0{,}1 = 0{,}01", font_size=40, color=ACENTO))
        c1.arrange(DOWN, buff=0.12).move_to([3.4, -0.2, 0])
        self.play(FadeIn(cuad, scale=3), FadeIn(c1))
        c2 = VGroup(texto("Cuadraditos:", 24), MathTex(r"23 \cdot 14 = 322", font_size=40))
        c2.arrange(DOWN, buff=0.12).move_to([3.4, -1.5, 0])
        self.play(FadeIn(c2))
        res = MathTex(r"2{,}3 \cdot 1{,}4 = 322 \text{ centésimas} = 3{,}22", font_size=44, color=ACENTO)
        res.to_edge(DOWN, buff=0.35)
        self.play(Write(res))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "La regla")
        notas = Notas(self)
        mult_fila(self, "2,3", "1,4", "", 1.4, x=-5.5, size=52, notas=notas)
        mult_fila(self, "0,25", "0,4", "", -0.3, x=-5.5, size=52, notas=notas)
        regla = texto("El resultado lleva tantos decimales\ncomo los dos factores juntos", 30, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(regla))
        self.wait(3)


# ===========================================================================
class DividirDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Dividir decimales", "La coma del cociente")
        notas = Notas(self)
        ctx = texto("Tres amigos se reparten 7,5 €. ¿Cuánto le toca a cada uno?", 28).move_to([0, 2.5, 0])
        self.play(FadeIn(ctx))
        q = division_larga(self, "7,5", 3, -2.2, 1.2, size=60, notas=notas, lateral=True, rt=0.7)
        sol = texto(f"A cada uno le tocan {q} €", 32, OK).to_edge(DOWN, buff=1.2)
        notas.fin()
        self.play(FadeIn(sol))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Si no es exacta, añadimos ceros")
        q = division_larga(self, "7", 4, -2.2, 1.6, size=60, notas=notas, lateral=True, rt=0.6)
        notas.fin()
        r = MathTex(rf"7 : 4 = {tx(q)}", font_size=56, color=ACENTO).to_edge(DOWN, buff=1.0)
        self.play(Write(r))
        self.wait(2.5)
        limpiar(self, cab)

        # Divisor decimal
        subtitulo(self, cab, "Si el divisor tiene coma")
        e = MathTex(r"4{,}8 : 0{,}6 = \ ?", font_size=60).move_to([0, 2.3, 0])
        q1 = texto("¿Cuántas veces cabe 0,6 en 4,8?", 28, ACENTO).next_to(e, DOWN, buff=0.25)
        self.play(Write(e), FadeIn(q1))
        k = 2.0
        recta = NumberLine(x_range=[0, 5, 1], length=5 * k, include_numbers=False, include_tip=False).move_to([0, 0.0, 0])
        nums = VGroup(*[MathTex(str(i), font_size=30).next_to(recta.n2p(i), DOWN, buff=0.15) for i in range(6)])
        total = Line(recta.n2p(0), recta.n2p(4.8), stroke_width=10, color=COLOR_POS["U"]).shift(UP * 0.35)
        self.play(Create(recta), FadeIn(nums), Create(total))
        trozos = VGroup()
        for i in range(8):
            t = Line(recta.n2p(0.6 * i), recta.n2p(0.6 * (i + 1)), stroke_width=12,
                     color=ACENTO if i % 2 == 0 else ROSA).shift(UP * 0.75)
            n = MathTex(str(i + 1), font_size=28, color=t.get_color()).next_to(t, UP, buff=0.08)
            self.play(Create(t), FadeIn(n), run_time=0.3)
            trozos.add(t, n)
        cabe = texto("¡Cabe 8 veces!", 30, OK).move_to([0, -1.3, 0])
        self.play(FadeIn(cabe))
        self.wait(1)
        truco = MathTex(r"4{,}8 : 0{,}6", r"=", r"48 : 6", "=", "8", font_size=56).move_to([0, -2.3, 0])
        truco[2].set_color(ACENTO)
        truco[4].set_color(OK)
        self.play(Write(truco))
        notas("Multiplicamos los dos por 10: el divisor queda sin coma y el resultado no cambia")
        self.wait(3)
        notas.fin()


# ===========================================================================
class FraccionADecimal(Scene):
    def construct(self):
        cab = titulo(self, "De fracción a decimal", "Dividimos el numerador entre el denominador")
        notas = Notas(self)
        f = VGroup(fraccion(3, 4, 72), MathTex("= 3 : 4", font_size=60)).arrange(RIGHT, buff=0.3).move_to([-4.0, 1.5, 0])
        self.play(Write(f))
        q = division_larga(self, "3", 4, 0.0, 1.6, size=56, notas=notas, rt=0.5)
        notas.fin()
        r = VGroup(fraccion(3, 4, 60), MathTex("=", font_size=56), tex_decimal(q, 60)).arrange(RIGHT, buff=0.25)
        r.move_to([-4.0, -1.0, 0])
        self.play(Write(r))
        ex = texto("Decimal exacto: la división termina (resto 0)", 26, OK).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ex))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "A veces no termina nunca")
        f = VGroup(fraccion(1, 3, 72), MathTex("= 1 : 3", font_size=60)).arrange(RIGHT, buff=0.3).move_to([-4.0, 1.5, 0])
        self.play(Write(f))
        q = division_larga(self, "1", 3, 0.0, 1.6, size=56, max_dec=4, rt=0.4)
        r = VGroup(fraccion(1, 3, 60), MathTex(r"= 0{,}3333\ldots", font_size=56)).arrange(RIGHT, buff=0.25)
        r.move_to([-4.0, -1.0, 0])
        self.play(Write(r))
        ex = texto("El resto siempre es 1: el 3 se repite para siempre", 26, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ex))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Redondear: quedarnos con menos cifras")
        n = tex_decimal("2,368", 72).move_to([0, 2.0, 0])
        self.play(Write(n))
        redondear(self, "2,368", "c", "", 0.5, x=-4.5, notas=notas)
        redondear(self, "2,368", "d", "", -1.0, x=-4.5, notas=notas)
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejemplo: 10 € entre 3 personas")
        e = MathTex(r"10 : 3 = 3{,}333\ldots", r"\approx 3{,}33 \text{ €}", font_size=60).move_to([0, 1.4, 0])
        e[1].set_color(ACENTO)
        self.play(Write(e[0]))
        self.play(Write(e[1]))
        c = texto("Redondeamos a los céntimos (centésimas)", 26, GREY_B).next_to(e, DOWN, buff=0.3)
        self.play(FadeIn(c))
        comp = MathTex(r"3 \cdot 3{,}33 = 9{,}99 \text{ €}", font_size=52).move_to([0, -0.7, 0])
        self.play(Write(comp))
        sobra = texto("Sobra 1 céntimo", 30, ROSA).next_to(comp, DOWN, buff=0.3)
        self.play(FadeIn(sobra))
        self.wait(3)


# ===========================================================================
COLOR_PERIODO = "#FF79C6"
COLOR_ANTE = "#5DADE2"


def periodico(ent, ante, per, size=60, arco=True):
    """Decimal periódico con el periodo en rosa y un arco encima: 0,1⌒6. Devuelve VGroup(numero, arco)."""
    partes = [ent + "{,}" + ante, per] if ante else [ent + "{,}", per]
    t = MathTex(*partes, font_size=size)
    t[1].set_color(COLOR_PERIODO)
    if ante:
        # colorea el anteperiodo (las cifras después de la coma)
        t[0][len(ent) + 1:].set_color(COLOR_ANTE)
    g = VGroup(t)
    if arco:
        k = size / 60
        a = ArcBetweenPoints(t[1].get_corner(UL) + UP * 0.1 * k + LEFT * 0.02,
                             t[1].get_corner(UR) + UP * 0.1 * k + RIGHT * 0.02, angle=-PI / 2.2,
                             color=COLOR_PERIODO, stroke_width=4 * k)
        g.add(a)
    return g


class DecimalesPeriodicos(Scene):
    def construct(self):
        cab = titulo(self, "Decimales periódicos", "Cifras que se repiten para siempre")

        # 1/3: el periodo y el arco
        r = VGroup(fraccion(1, 3, 64), MathTex(r"= 0{,}3333\ldots", font_size=60)).arrange(RIGHT, buff=0.25)
        r.move_to([0, 1.6, 0])
        self.play(Write(r))
        exp = texto("La cifra que se repite se llama PERIODO", 30, COLOR_PERIODO).move_to([0, 0.3, 0])
        self.play(FadeIn(exp))
        p = periodico("0", "", "3", 80).move_to([0, -1.2, 0])
        igual = VGroup(fraccion(1, 3, 64), MathTex("=", font_size=70)).arrange(RIGHT, buff=0.25).next_to(p, LEFT, buff=0.3)
        self.play(FadeIn(igual), Write(p[0]))
        self.play(Create(p[1]))
        arco_t = texto("se escribe con un arco encima", 24, GREY_B).next_to(p, RIGHT, buff=0.5)
        self.play(FadeIn(arco_t))
        self.wait(2.5)
        limpiar(self, cab)

        # 2/11: periódico puro, el resto se repite
        subtitulo(self, cab, "Periódico puro")
        f = VGroup(fraccion(2, 11, 64), MathTex("= 2 : 11", font_size=56)).arrange(RIGHT, buff=0.3).move_to([-4.3, 1.6, 0])
        self.play(Write(f))
        division_larga(self, "2", 11, -0.6, 1.7, size=52, max_dec=4, lateral=True, rt=0.45)
        rep = texto("El resto 2 vuelve a salir:\nla división se repite igual", 26, ACENTO).move_to([-4.3, -0.4, 0])
        self.play(FadeIn(rep))
        self.wait(1)
        res = VGroup(fraccion(2, 11, 56), MathTex(r"= 0{,}1818\ldots =", font_size=52),
                     periodico("0", "", "18", 60)).arrange(RIGHT, buff=0.25).move_to([0, -2.4, 0])
        self.play(Write(res))
        puro = texto("El periodo empieza justo después de la coma", 26, COLOR_PERIODO).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(puro))
        self.wait(2.5)
        limpiar(self, cab)

        # 1/6: periódico mixto
        subtitulo(self, cab, "Periódico mixto")
        f = VGroup(fraccion(1, 6, 64), MathTex("= 1 : 6", font_size=56)).arrange(RIGHT, buff=0.3).move_to([-4.3, 1.6, 0])
        self.play(Write(f))
        division_larga(self, "1", 6, -0.6, 1.7, size=52, max_dec=4, lateral=True, rt=0.45)
        res = VGroup(fraccion(1, 6, 56), MathTex(r"= 0{,}1666\ldots =", font_size=52),
                     periodico("0", "1", "6", 60)).arrange(RIGHT, buff=0.25).move_to([0, -2.1, 0])
        self.play(Write(res))
        num = res[2][0]
        ante = Brace(num[0][2:], DOWN, buff=0.1, color=COLOR_ANTE)
        ante_t = texto("anteperiodo", 22, COLOR_ANTE).next_to(ante, DOWN, buff=0.05)
        ante_t.shift(LEFT * (ante_t.width / 2 + 0.05))
        per = Brace(num[1], DOWN, buff=0.1, color=COLOR_PERIODO)
        per_t = texto("periodo", 22, COLOR_PERIODO).next_to(per, DOWN, buff=0.05)
        per_t.shift(RIGHT * (per_t.width / 2 + 0.05))
        self.play(GrowFromCenter(ante), FadeIn(ante_t), GrowFromCenter(per), FadeIn(per_t))
        self.wait(2.5)
        limpiar(self, cab)

        # Resumen: los tres tipos
        subtitulo(self, cab, "Tres tipos de decimales")
        tipos = [
            ("Exacto", VGroup(MathTex(r"0{,}75", font_size=60)), "La división termina", OK),
            ("Periódico puro", periodico("0", "", "18", 60), "Se repite desde la coma", COLOR_PERIODO),
            ("Periódico mixto", periodico("0", "1", "6", 60), "Hay cifras antes del periodo", COLOR_ANTE),
        ]
        cajas = VGroup()
        for nombre, num, desc, col in tipos:
            c = VGroup(texto(nombre, 30, col), num, texto(desc, 22, GREY_B)).arrange(DOWN, buff=0.35)
            marco = SurroundingRectangle(c, color=col, buff=0.3, corner_radius=0.15)
            cajas.add(VGroup(marco, c))
        cajas.arrange(RIGHT, buff=0.4).move_to([0, -0.2, 0])
        for c in cajas:
            self.play(FadeIn(c, shift=UP * 0.2))
            self.wait(0.6)
        self.wait(2)
        limpiar(self, cab)

        # ¿Cómo saber si será exacto? Mirar el denominador
        subtitulo(self, cab, "¿Exacto o periódico?")
        cond = texto("Fracción simplificada: si el denominador solo tiene los factores 2 y 5,\n"
                     "el decimal es exacto. Si tiene otro factor (3, 7, 11...), es periódico.", 26)
        cond.next_to(cab, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(cond))
        casos = [((3, 4), [2, 2], True, "0,75"), ((7, 20), [2, 2, 5], True, "0,35"),
                 ((5, 6), [2, 3], False, "0,8333..."), ((4, 15), [3, 5], False, "0,2666...")]
        fila_y = [0.6, -0.5, -1.6, -2.7]
        for ((n, d), fact, exacto, dec), y in zip(casos, fila_y):
            fr = fraccion(n, d, 40).move_to([-5.6, y, 0])
            den = MathTex(f"{d} =", font_size=40).move_to([-4.2, y, 0])
            piezas = VGroup(*[pieza(pp, 0.27) for pp in fact]).arrange(RIGHT, buff=0.15).next_to(den, RIGHT, buff=0.25)
            self.play(FadeIn(fr), FadeIn(den), LaggedStart(*[GrowFromCenter(pz) for pz in piezas], lag_ratio=0.2),
                      run_time=0.9)
            veredicto = texto("solo 2 y 5 → exacto" if exacto else "tiene un 3 → periódico", 26,
                              OK if exacto else COLOR_PERIODO).move_to([0.9, y, 0], aligned_edge=LEFT)
            veredicto.align_to([-1.0, 0, 0], LEFT)
            valor = MathTex(tx(dec), font_size=40, color=OK if exacto else COLOR_PERIODO)
            valor.move_to([4.6, y, 0], aligned_edge=LEFT)
            self.play(FadeIn(veredicto, shift=RIGHT * 0.2))
            self.play(Write(valor), run_time=0.7)
            self.wait(0.6)
        por_que = texto("¿Por qué? Porque contamos de 10 en 10, y 10 = 2 · 5", 24, ACENTO).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(por_que))
        self.wait(3)
        limpiar(self, cab)

        # Truncar o redondear
        subtitulo(self, cab, "Truncar o redondear")
        n = periodico("0", "", "6", 70).move_to([0, 1.8, 0])
        igual = VGroup(fraccion(2, 3, 56), MathTex(r"= 0{,}6666\ldots =", font_size=56)).arrange(RIGHT, buff=0.25)
        igual.next_to(n, LEFT, buff=0.25)
        VGroup(igual, n).move_to([0, 1.8, 0])
        self.play(Write(igual), Write(n))
        t1 = VGroup(texto("Truncar a las centésimas:", 28, COLOR_ANTE),
                    MathTex(r"0{,}66", r"\,|\,66\ldots", font_size=56)).arrange(RIGHT, buff=0.4)
        t1[1][1].set_color(GREY_D)
        t1.move_to([0, 0.3, 0])
        self.play(FadeIn(t1[0]), Write(t1[1]))
        tij = texto("cortamos y tiramos el resto", 22, GREY_B).next_to(t1, DOWN, buff=0.15)
        self.play(FadeIn(tij))
        t2 = VGroup(texto("Redondear a las centésimas:", 28, ACENTO),
                    MathTex(r"0{,}6", r"6", r"6\ldots", r"\approx 0{,}67", font_size=56)).arrange(RIGHT, buff=0.4)
        t2.move_to([0, -1.4, 0])
        self.play(FadeIn(t2[0]), Write(t2[1][:3]))
        self.play(Indicate(t2[1][2], color=ACENTO, scale_factor=1.5))
        self.play(Write(t2[1][3]))
        cerca = texto("6 ≥ 5: subimos 1. 0,67 está más cerca de 0,666... que 0,66", 24, GREY_B)
        cerca.next_to(t2, DOWN, buff=0.15)
        self.play(FadeIn(cerca))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
SUMA_RESTA = [("4,25", "+", "3,6"), ("12,07", "+", "0,95"), ("9,4", "-", "2,75"), ("15", "-", "3,08")]
SUMA_RESTA_E = ("0,6", "0,45", "0,3")  # e) 0,6 + 0,45 − 0,3
POR_UNIDAD = [("2,58", "x", 10), ("0,037", "x", 100), ("4,1", "x", 1000), ("63,5", ":", 10), ("2,4", ":", 100),
              ("7", ":", 1000)]
MULTIPLICA = [("3,2", "4"), ("1,5", "2,6"), ("0,35", "1,2"), ("0,05", "0,3")]
DIVIDE = [("9,6", "4"), ("13,5", "5"), ("6", "8"), ("2,4", "0,3"), ("7,5", "0,25"), ("1,44", "1,2")]
FRAC_DEC = [(3, 5), (7, 8), (2, 3)]
REDONDEA = [("3,1416", "c"), ("12,857", "d"), ("0,995", "c")]
PROBLEMAS = [
    "a) Compras 3 cuadernos de 1,25 € y un bolígrafo de 2,40 €. Pagas con 10 €.\n"
    "     ¿Cuánto te devuelven?",
    "b) Echamos 35 litros de gasolina a 1,62 € el litro. ¿Cuánto pagamos?",
    "c) ¿Cuántos trozos de 0,75 m salen de una cuerda de 7,5 m?",
    "d) Una cena cuesta 47,40 € y pagan 4 amigos a partes iguales.\n"
    "     ¿Cuánto paga cada uno?",
]
SIMB = {"+": "+", "-": MENOS, "x": "·", ":": ":"}


def op_txt(a, op, b):
    return f"{a} {SIMB[op]} {b}"


def pagina_enunciados(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 27, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.25)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def enunciados_1():
    sr = [f"{l}) {op_txt(*o)}" for l, o in zip("abcd", SUMA_RESTA)]
    sr.append(f"e) {SUMA_RESTA_E[0]} + {SUMA_RESTA_E[1]} {MENOS} {SUMA_RESTA_E[2]}")
    pu = [f"{l}) {op_txt(*o)}" for l, o in zip("abcdef", POR_UNIDAD)]
    return [
        ("1. Suma o resta:", "     ".join(sr[:3]) + "\n" + "     ".join(sr[3:])),
        ("2. Calcula:", "     ".join(pu[:3]) + "\n" + "     ".join(pu[3:])),
        ("3. Multiplica:", "     ".join(f"{l}) {a} · {b}" for l, (a, b) in zip("abcd", MULTIPLICA))),
        ("4. Divide:", "     ".join(f"{l}) {a} : {b}" for l, (a, b) in zip("abcdef", DIVIDE))),
    ]


def enunciados_2():
    return [
        ("5. Fracciones y redondeo:",
         "a) Escribe como decimal:   " + "     ".join(f"{n}/{d}" for n, d in FRAC_DEC) +
         "\n     (si no termina, redondea a las centésimas)\n"
         "b) Redondea:   " + "     ".join(f"{s} a las {NOMBRE_POS[p]}" for s, p in REDONDEA[:2]) +
         "\n     " + "     ".join(f"{s} a las {NOMBRE_POS[p]}" for s, p in REDONDEA[2:])),
        ("6. Problemas:", "\n".join(PROBLEMAS)),
    ]


def resolver_division(scene, a, b, letra, x0, y, notas=None, lateral=False, cabecera=None, max_dec=3, size=46,
                      resultado_fmt=None):
    """letra) a : b [= a' : b'] = cociente, con la división larga debajo."""
    if "," in b:
        a2, b2, f = con_divisor_natural(a, b)
        partes = [rf"{tx(a)} : {tx(b)}", rf"= {tx(a2)} : {b2}"]
    else:
        a2, b2, f = a, int(b), 1
        partes = [cabecera or rf"{tx(a)} : {tx(b)}"]
    head = MathTex(*partes, font_size=44)
    lab = texto(f"{letra})", 28) if letra else VGroup()
    hg = VGroup(lab, head).arrange(RIGHT, buff=0.3).move_to([0, y, 0]).align_to([x0 - 0.5, 0, 0], LEFT)
    scene.play(FadeIn(lab), Write(head[0]), run_time=0.8)
    if len(partes) > 1:
        if notas:
            notas(f"El divisor tiene coma: multiplicamos los dos por {f}")
        scene.play(Write(head[1]), run_time=0.8)
        if notas:
            scene.wait(1)
    q = division_larga(scene, a2, b2, x0, y - 1.05, size=size, max_dec=max_dec, notas=notas, lateral=lateral)
    qs = resultado_fmt(q) if resultado_fmt else rf"= {tx(q)}"
    r = MathTex(qs, font_size=44, color=ACENTO).next_to(head, RIGHT, buff=0.25)
    scene.play(Write(r))
    scene.play(Circumscribe(r, color=ACENTO), run_time=0.7)
    if notas:
        notas.fin()
    return q


def resolver_por_unidad(scene, items, letras):
    rows = []
    for (s, op, n), l in zip(items, letras):
        res = D(s) * n if op == "x" else D(s) / n
        k = len(str(n)) - 1
        simb = r"\cdot" if op == "x" else ":"
        m = MathTex(rf"\text{{{l})}}\;\; {tx(s)} {simb} {n} = ", tx(norm(res)), font_size=48)
        m[1].set_color(ACENTO)
        nota = f"{k} lugar{'es' if k > 1 else ''} a la " + ("izquierda" if op == "x" else "derecha")
        rows.append((m, nota))
    filas(scene, rows, y0=2.0, dy=0.95, x0=-5.8, size_nota=24)


def problema_compra(scene, notas=None):
    e = texto(PROBLEMAS[0][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    c = D("1.25") * 3
    s = c + D("2.40")
    d = D(10) - s
    rows = [
        (MathTex(rf"3 \cdot 1{{,}}25 = {tx(fmt(c, 2))}", font_size=50), "los 3 cuadernos"),
        (MathTex(rf"{tx(fmt(c, 2))} + 2{{,}}40 = {tx(fmt(s, 2))}", font_size=50), "más el bolígrafo: lo que gastamos"),
        (MathTex(rf"10 - {tx(fmt(s, 2))} = {tx(fmt(d, 2))}", font_size=50, color=ACENTO), "lo que nos devuelven"),
    ]
    filas(scene, rows, y0=1.0, dy=1.05, x0=-5.0, size_nota=26, espera=1)
    sol = texto(f"Nos devuelven {fmt(d, 2)} €", 32, OK).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_gasolina(scene):
    e = texto(PROBLEMAS[1][3:], 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    mult_fila(scene, "35", "1,62", "", 0.6, x=-5.0, size=52)
    sol = texto(f"Pagamos {fmt(D(35) * D('1.62'), 2)} €", 32, OK).to_edge(DOWN, buff=0.8)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_cuerda(scene):
    e = texto(PROBLEMAS[2][3:], 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    q = resolver_division(scene, "7,5", "0,75", "", -1.5, 1.3, lateral=True)
    sol = texto(f"Salen {q} trozos", 32, OK).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_cena(scene):
    e = texto(PROBLEMAS[3][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    q = resolver_division(scene, "47,40", "4", "", -2.0, 1.3, lateral=True)
    sol = texto(f"Cada uno paga {q} €", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def frac_cabecera(n, d):
    return rf"\frac{{{n}}}{{{d}}} = {n} : {d}"


def frac_resultado(q):
    dec = q.partition(",")[2]
    if len(dec) >= 3 and len(set(dec)) == 1:
        red = fmt(D(q.replace(",", ".")), 2)
        return rf"= {tx(q)}\ldots \approx {tx(red)}"
    return rf"= {tx(q)}"


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Operaciones con decimales")
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2(), size=22)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))
        notas = Notas(self)

        subtitulo(self, cab, "Ejercicio 1 a)")
        operar_columnas(self, "4,25", "3,6", "+", (0, 0.3), w=1.0, h=0.85, notas=notas)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2 a)")
        cols = ["C", "D", "U", ",", "d", "c", "m"]
        tabla, centros = tabla_posiciones(cols, filas=1, centro=np.array([0, 0.1, 0]), w=1.05, h=1.0)
        self.play(FadeIn(tabla))
        mover_en_tabla(self, "2,58", "x", 10, centros, notas=notas)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3 a)")
        mult_fila(self, *MULTIPLICA[0], "a", 0.6, x=-5.6, size=56, notas=notas)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 4 a)")
        resolver_division(self, *DIVIDE[0], "a", -2.0, 1.9, notas=notas, lateral=True, size=56)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 a)")
        n, d = FRAC_DEC[0]
        resolver_division(self, str(n), str(d), "a", -2.0, 1.9, notas=notas, lateral=True, size=56,
                          cabecera=frac_cabecera(n, d), resultado_fmt=frac_resultado)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 b)")
        redondear(self, *REDONDEA[0], "a", 0.6, x=-5.6, size=72, notas=notas)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 6 a)")
        problema_compra(self)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Operaciones con decimales")

        subtitulo(self, cab, "Ejercicio 1 b) y c)")
        for (a, op, b), l, x in zip(SUMA_RESTA[1:3], "bc", (-3.6, 3.4)):
            lab = texto(f"{l})", 30).move_to([x - 2.6, 1.6, 0])
            self.play(FadeIn(lab))
            operar_columnas(self, a, b, op, (x, -0.2), w=0.8, h=0.8, size=48, nombres=False)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 1 d) y e)")
        a, op, b = SUMA_RESTA[3]
        self.play(FadeIn(texto("d)", 30).move_to([-6.2, 1.6, 0])))
        operar_columnas(self, a, b, op, (-4.0, -0.2), w=0.75, h=0.8, size=46, nombres=False)
        x, y, z = SUMA_RESTA_E
        self.play(FadeIn(texto(f"e)  {x} + {y} {MENOS} {z}", 26).move_to([2.8, 2.3, 0])))
        r1, _ = operar_columnas(self, x, y, "+", (0.9, -0.2), w=0.7, h=0.8, size=44, nombres=False)
        operar_columnas(self, r1, z, "-", (4.9, -0.2), w=0.7, h=0.8, size=44, nombres=False)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2: b) a f)")
        resolver_por_unidad(self, POR_UNIDAD[1:], "bcdef")
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        for (a, b), l, y in zip(MULTIPLICA[1:], "bcd", (1.6, 0.0, -1.6)):
            mult_fila(self, a, b, l, y, size=44)
        self.wait(2)
        limpiar(self, cab)

        for sub, items, letras in (("Ejercicio 4 b) y c)", DIVIDE[1:3], "bc"), ("Ejercicio 4 d) y e)", DIVIDE[3:5], "de"),
                                   ("Ejercicio 4 f)", DIVIDE[5:], "f")):
            subtitulo(self, cab, sub)
            for (a, b), l, x in zip(items, letras, (-4.6, 2.0)):
                resolver_division(self, a, b, l, x, 2.0)
            self.wait(1.5)
            limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 a): b) y c)")
        for (n, d), l, x in zip(FRAC_DEC[1:], "bc", (-4.6, 2.2)):
            resolver_division(self, str(n), str(d), l, x, 2.0, cabecera=frac_cabecera(n, d),
                              resultado_fmt=frac_resultado)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 b): b) y c)")
        for (s, p), l, y in zip(REDONDEA[1:], "bc", (1.0, -1.0)):
            redondear(self, s, p, l, y, x=-5.6, size=64)
        nota = texto("0,995 → 0,99 + 0,01 = 1,00 (las centésimas se quedan: 1,00)", 24, GREY_B).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(nota))
        self.wait(2)
        limpiar(self, cab)

        for sub, f in (("Ejercicio 6 b)", problema_gasolina), ("Ejercicio 6 c)", problema_cuerda),
                       ("Ejercicio 6 d)", problema_cena)):
            subtitulo(self, cab, sub)
            f(self)
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes operar con decimales.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
