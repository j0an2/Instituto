"""Tema 6 · Números decimales: representación y ordenación (1º ESO)

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
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

CD, CC, CM = COLOR_POS["d"], COLOR_POS["c"], COLOR_POS["m"]


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
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
        limpiar(self, cab)

        # Dinero: 2,45 €
        sub = subtitulo(self, cab, "Lo usamos cada día: el dinero")
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
        limpiar(self, cab)

        # Descomposición
        sub = subtitulo(self, cab, "Cada cifra vale según su posición")
        n = tex_decimal("34,072", 72).move_to([0, 1.7, 0])
        self.play(Write(n))
        partes = [("3", "D", "30"), ("4", "U", "4"), ("0", "d", "0"), ("7", "c", "0,07"), ("2", "m", "0,002")]
        filas = VGroup()
        for cif, pos, val in partes:
            f = VGroup(MathTex(cif, font_size=44, color=COLOR_POS[pos]),
                       Text(f"{NOMBRE_POS[pos]}", font_size=24, color=COLOR_POS[pos]),
                       MathTex(r"\rightarrow", font_size=40), MathTex(val.replace(",", "{,}"), font_size=44,
                                                                       color=COLOR_POS[pos])).arrange(RIGHT, buff=0.3)
            filas.add(f)
        filas.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.2, -1.0, 0])
        for f in filas:
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
        subtitulo(self, cab, f"¿Qué es mayor, {a} o {b}?")
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
        limpiar(self, cab)

    def trampa(self, cab):
        subtitulo(self, cab, "¡Cuidado! ¿Qué es mayor, 0,5 o 0,45?")
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
        limpiar(self, cab)

    def cuadricula(self, n):
        celdas = VGroup(*[Square(0.4, stroke_color=WHITE, stroke_width=1, fill_color=VACIO, fill_opacity=1)
                          for _ in range(100)]).arrange_in_grid(rows=10, cols=10, buff=0)
        for k in range(n):
            c, r = divmod(k, 10)
            celdas[r * 10 + c].set_fill(CC, 1)
        return celdas

    def ceros(self, cab):
        subtitulo(self, cab, "Los ceros a la derecha no cambian el valor")
        ancho = 9.0
        filas = [(10, 5, "0,5", (5, 10)), (100, 50, "0,50", (50, 100)), (1000, 500, "0,500", (500, 1000))]
        grupo = VGroup()
        for i, (partes, tomadas, s, (n, d)) in enumerate(filas):
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
        nota = texto("¡Como las fracciones equivalentes del tema 5!", 24, GREY_B).to_edge(DOWN, buff=0.35)
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


def D(s):
    return Decimal(s.replace(",", "."))


def ndec(s):
    return len(s.partition(",")[2])


def fmt(v, k):
    return f"{v:.{k}f}".replace(".", ",") if k else str(int(v))


def pad(s, k):
    ent, _, dec = s.partition(",")
    return ent if k == 0 else ent + "," + dec + "0" * (k - len(dec))


def tex_pad(s, k, size=52):
    """Decimal con ceros añadidos hasta k decimales (los ceros nuevos en gris)."""
    t = tex_decimal(pad(s, k), size)
    extra = k - ndec(s)
    if extra:
        for p in t[-extra:]:
            p.set_color(GREY_B)
    return t


def filas(scene, rows, y0=1.9, dy=1.0, x0=-6.2, size_nota=22):
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
        s = fmt(Decimal(n) / Decimal(d), k)
        m = con_letra(l, VGroup(fraccion(n, d, size=44), MathTex("=", font_size=48), tex_decimal(s, 52))
                      .arrange(RIGHT, buff=0.25))
        nota = f"denominador {d}  →  {k} cifra{'s' if k > 1 else ''} decimal{'es' if k > 1 else ''}"
        if len(str(n)) < k:
            nota += " (con un 0)"
        rows.append((m, nota))
    filas(scene, rows, y0=1.8 if len(rows) > 1 else 0.6, dy=1.3)
    if ejemplo:
        regla = texto("Denominador 10 → 1 cifra decimal · 100 → 2 cifras · 1000 → 3 cifras", 26, ACENTO)
        scene.play(FadeIn(regla.to_edge(DOWN, buff=0.5)))
        scene.wait(2)


# --- 1b. Decimal → fracción
def resolver_dec_frac(scene, items, letras, ejemplo=False):
    rows = []
    for s, l in zip(items, letras):
        k = ndec(s)
        d = 10 ** k
        n = int(s.replace(",", ""))
        m = con_letra(l, VGroup(tex_decimal(s, 52), MathTex("=", font_size=48), fraccion(n, d, size=44))
                      .arrange(RIGHT, buff=0.25))
        rows.append((m, f"{k} cifra{'s' if k > 1 else ''} decimal{'es' if k > 1 else ''}  →  denominador {d}"))
    filas(scene, rows, y0=1.8 if len(rows) > 1 else 0.6, dy=1.3)
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
    filas(scene, rows, y0=1.9 if len(rows) > 1 else 0.6, dy=1.1)
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
    filas(scene, rows, y0=1.9 if len(rows) > 1 else 0.6, dy=1.1)
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
        s = str(a) if i == 0 else str(b) if i == 10 else fmt(v, 1)
        etiquetas.add(Text(s, font_size=18, color=CD if 0 < i < 10 else WHITE).next_to(r.n2p(float(v)), DOWN, buff=0.18))
    scene.play(FadeIn(lab), Create(r), FadeIn(etiquetas))
    for s in vals:
        v = float(D(s))
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
        if ndec(s) == 2:
            abajo = fmt(D(s).quantize(Decimal("0.1"), rounding="ROUND_FLOOR"), 1)
            arriba = fmt(D(abajo.replace(",", ".")) + Decimal("0.1"), 1) if False else fmt(D(abajo) + Decimal("0.1"), 1)
            nota = texto(f"{s} está justo a mitad de camino entre {abajo} y {arriba}", 24, GREY_B).move_to([0, -1.8, 0])
            scene.play(FadeIn(nota))
    scene.wait(2.5)


# --- 4. Comparar
def colocar(s, k, fila, centros, size=60):
    t = tex_pad(s, k, size)
    for p, pos in zip(t, t.posiciones):
        p.move_to(centros[(fila, pos)])
    return t


def resolver_compara(scene, a, b, letra, ejemplo=False):
    k = max(ndec(a), ndec(b))
    ne = max(len(a.partition(",")[0]), len(b.partition(",")[0]))
    cols = ["C", "D", "U"][3 - ne:] + [","] + ["d", "c", "m"][:k]
    lab = texto(f"{letra})", 34).move_to([-6.3, 0.3, 0])
    tabla, centros = tabla_posiciones(cols, filas=2, centro=np.array([-2.6, 0.2, 0]))
    scene.play(FadeIn(lab), FadeIn(tabla))
    ta = colocar(a, k, 0, centros)
    tb = colocar(b, k, 1, centros)
    scene.play(FadeIn(ta), FadeIn(tb))
    if k > min(ndec(a), ndec(b)):
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
    sig = ">" if D(a) > D(b) else "<" if D(a) < D(b) else "="
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
    k = max(ndec(s) for s in items)
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
    orden = sorted(range(len(items)), key=lambda i: D(items[i]), reverse=not creciente)
    if nombres:
        cad = f"  {signo}  ".join(f"{nombres[i]} ({pad(items[i], k)}{unidad})" for i in orden)
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
    k = max(ndec(a), ndec(b)) + 1
    t1 = texto(f"{letra}) Entre {a} y {b}", 30).move_to([0, 2.2, 0])
    scene.play(FadeIn(t1))
    t2 = VGroup(texto("Añadimos una cifra decimal más:", 26, GREY_B), tex_pad(a, k, 44), texto("y", 26, GREY_B),
                tex_pad(b, k, 44)).arrange(RIGHT, buff=0.25).move_to([0, 1.3, 0])
    scene.play(FadeIn(t2))
    va, vb = D(a), D(b)
    r = NumberLine(x_range=[0, 10, 1], length=11, include_tip=False, stroke_width=3, tick_size=0.1).move_to([0, -0.4, 0])
    ext = VGroup(tex_decimal(pad(a, k), 32).next_to(r.n2p(0), DOWN, buff=0.2),
                 tex_decimal(pad(b, k), 32).next_to(r.n2p(10), DOWN, buff=0.2))
    nota_z = texto("hacemos zoom: el trozo se divide en 10 partes", 22, GREY_B).next_to(r, UP, buff=0.35)
    scene.play(Create(r), FadeIn(ext), FadeIn(nota_z))
    m = (va + vb) / 2
    sm = fmt(m, k)
    p = Dot(r.n2p(5), radius=0.12, color=ACENTO)
    lp = tex_decimal(sm, 40).next_to(p, UP, buff=0.3)
    scene.play(FadeOut(nota_z), FadeIn(p, scale=2), Write(lp))
    res = VGroup(tex_decimal(a, 56), MathTex("<", font_size=56), tex_decimal(sm, 56), MathTex("<", font_size=56),
                 tex_decimal(b, 56)).arrange(RIGHT, buff=0.25).move_to([0, -1.9, 0])
    scene.play(Write(res))
    if ejemplo:
        otras = [fmt(va + (vb - va) * j / 10, k) for j in (1, 2, 8, 9)]
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


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Números decimales")
        pagina_enunciados(self, cab, ENUN_1)
        pagina_enunciados(self, cab, ENUN_2, size=22)
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
            subtitulo(self, cab, sub)
            f()
            limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
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
            subtitulo(self, cab, sub)
            f()
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes leer, comparar y ordenar decimales.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
