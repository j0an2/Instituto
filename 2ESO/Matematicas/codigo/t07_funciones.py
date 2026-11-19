"""Tema 7 · Funciones y gráficas (2º ESO)

Sigue el índice del libro: coordenadas cartesianas · concepto de función · gráficas de funciones ·
dominio y recorrido, puntos de corte · continuidad, crecimiento · interpretación de gráficas.

Escenas:
    Coordenadas             – hundir la flota → ejes; un punto se coloca andando primero en x y luego en y;
                              el orden importa; leer un punto; cuadrantes y puntos sobre los ejes
    ConceptoFuncion         – la máquina «× 2 + 1» que llena una tabla; una sola salida (diagramas de flechas);
                              variables; las cuatro formas: enunciado, tabla, fórmula y gráfica
    GraficaFuncion          – temperatura: tabla → puntos → curva; cine: puntos que no se unen;
                              prueba de la recta vertical (curva sí, circunferencia no)
    DominioRecorrido        – «sombra» de la gráfica sobre los ejes; puntos de corte
    ContinuidadCrecimiento  – lápiz que no se levanta / aparcamiento con saltos; un punto que recorre la
                              gráfica coloreando subidas y bajadas; máximo y mínimo
    InterpretacionGraficas  – la excursión (caminante sincronizado con la gráfica); llenar dos vasos
    EjerciciosEjemplo / EjerciciosResueltos1 / EjerciciosResueltos2

Colores: x amarillo, y cian (como en el tema 5); crece verde, decrece rojo, constante gris.

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t07_funciones.py Coordenadas
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t07_funciones.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COMUN = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from t09_potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t03_lenguaje_algebraico import lista, pagina_enunciados, tarjeta, ROSA, LETRA  # noqa: E402
from t05_sistemas import XY, Y_COL, Sub  # noqa: E402
from t06_proporcionalidad import tabla_h  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 7 · Funciones y gráficas"
TITULOS = {
    "Coordenadas": "Coordenadas cartesianas",
    "ConceptoFuncion": "¿Qué es una función?",
    "GraficaFuncion": "La gráfica de una función",
    "DominioRecorrido": "Dominio, recorrido y puntos de corte",
    "ContinuidadCrecimiento": "Continuidad, crecimiento, máximos y mínimos",
    "InterpretacionGraficas": "Interpretar gráficas",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 3)",
    "EjerciciosResueltos2": "Ejercicios resueltos (4 a 6)",
}

CRECE, DECRECE, CONST = OK, MAL, "#B8C0CC"
NAR = "#FF9F43"


def num(v):
    s = ("%g" % v)
    return s.replace(".", "{,}")


def par(nombre, x, y, size=34):
    sep = ";\\ " if (x != int(x) or y != int(y)) else ",\\,"
    m = MathTex(f"{nombre}(", num(x), sep, num(y), ")", font_size=size)
    m[1].set_color(LETRA)
    m[3].set_color(Y_COL)
    return m


def plano(xr, yr, u, centro, num_size=20, nums=True, tips=False):
    """Ejes con la misma escala u en x e y. Devuelve (ax, grupo con las letras x, y)."""
    ax = Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1], x_length=(xr[1] - xr[0]) * u,
              y_length=(yr[1] - yr[0]) * u, tips=tips,
              axis_config={"include_numbers": nums, "font_size": num_size, "color": GREY_B})
    ax.move_to([centro[0], centro[1], 0])
    lx = MathTex("x", font_size=30, color=LETRA).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
    ly = MathTex("y", font_size=30, color=Y_COL).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2)
    return ax, VGroup(ax, lx, ly)


def ejes_xy(xr, yr, xl, yl, centro, step=(1, 1), nx="x", ny="y", num_size=20):
    ax = Axes(x_range=[xr[0], xr[1], step[0]], y_range=[yr[0], yr[1], step[1]], x_length=xl, y_length=yl, tips=False,
              axis_config={"include_numbers": True, "font_size": num_size, "color": GREY_B})
    ax.move_to([centro[0], centro[1], 0])
    lx = texto(nx, 22, LETRA).next_to(ax.x_axis.get_end(), DL, buff=0.3).shift(DOWN * 0.3)
    ly = texto(ny, 22, Y_COL).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2)
    return ax, VGroup(ax, lx, ly)


def poligonal(ax, pts, color=WHITE, sw=5):
    m = VMobject(color=color, stroke_width=sw)
    m.set_points_as_corners([ax.c2p(*p) for p in pts])
    return m


def proy(ax, x, y, col=GREY_B):
    p = ax.c2p(x, y)
    g = VGroup()
    if y != 0:
        g.add(DashedLine(p, ax.c2p(x, 0), color=col, stroke_width=2))
    if x != 0:
        g.add(DashedLine(p, ax.c2p(0, y), color=col, stroke_width=2))
    return g


def etiq_dir(x, y):
    return (UR if x >= 0 else UL) if y >= 0 else (DR if x >= 0 else DL)


# ---------------------------------------------------------------------------
class Coordenadas(Scene):
    def construct(self):
        cab = titulo(self, "Coordenadas cartesianas")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Hundir la flota")
        s, x0, y0 = 0.72, -1.45, -1.75
        celdas = VGroup(*[Square(s, stroke_color=GREY_B, stroke_width=2).move_to([x0 + i * s, y0 + j * s, 0])
                          for i in range(5) for j in range(5)])
        letras = VGroup(*[texto(l, 26, LETRA).move_to([x0 + i * s, y0 - s, 0]) for i, l in enumerate("ABCDE")])
        nums = VGroup(*[texto(str(j + 1), 26, Y_COL).move_to([x0 - s, y0 + j * s, 0]) for j in range(5)])
        self.play(Create(celdas), FadeIn(letras), FadeIn(nums))
        barco = celdas[2 * 5 + 3].copy().set_fill(ROSA, 0.8)
        notas("¿Dónde está el barco? Hay que dar DOS datos: la columna y la fila")
        self.play(FadeIn(barco, scale=0.5))
        l1 = DashedLine(letras[2].get_top(), barco.get_bottom(), color=LETRA)
        l2 = DashedLine(nums[3].get_right(), barco.get_left(), color=Y_COL)
        self.play(Create(l1))
        self.play(Create(l2))
        c4 = texto("C4", 44, ROSA).move_to([3.4, 0.2, 0])
        self.play(Write(c4))
        notas("En matemáticas hacemos lo mismo, pero con números en las dos direcciones")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Los ejes")
        ax = Axes(x_range=[-6, 6, 1], y_range=[-4, 4, 1], x_length=8.4, y_length=5.6, tips=True,
                  axis_config={"include_numbers": True, "font_size": 20, "color": GREY_B}).move_to([0, -0.3, 0])
        self.play(Create(ax.x_axis))
        tx = texto("eje X (de abscisas)", 22, LETRA).next_to(ax.x_axis.get_end(), UP, buff=0.2).shift(LEFT * 1.1)
        self.play(FadeIn(tx))
        self.play(Create(ax.y_axis))
        ty = texto("eje Y (de ordenadas)", 22, Y_COL).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2)
        self.play(FadeIn(ty))
        o = texto("O", 24).next_to(ax.c2p(0, 0), DL, buff=0.08)
        notas("Se cortan en el ORIGEN, el punto (0, 0)")
        self.play(FadeIn(o), Flash(ax.c2p(0, 0), color=ACENTO))
        self.wait(1.5)

        sub("Colocar un punto")
        guardados = VGroup()

        def poner(nombre, x, y, col=ACENTO, txt=None, espera=1.0):
            d = Dot(ax.c2p(0, 0), color=col, radius=0.1)
            self.add(d)
            fl = VGroup()
            if txt:
                notas(txt[0])
            if x != 0:
                a = Arrow(ax.c2p(0, 0), ax.c2p(x, 0), buff=0, color=LETRA, stroke_width=6,
                          max_tip_length_to_length_ratio=0.18)
                self.play(GrowArrow(a), d.animate.move_to(ax.c2p(x, 0)))
                fl.add(a)
            if txt and len(txt) > 1:
                notas(txt[1])
            if y != 0:
                b = Arrow(ax.c2p(x, 0), ax.c2p(x, y), buff=0, color=Y_COL, stroke_width=6,
                          max_tip_length_to_length_ratio=0.18)
                self.play(GrowArrow(b), d.animate.move_to(ax.c2p(x, y)))
                fl.add(b)
            lab = par(nombre, x, y).next_to(d, etiq_dir(x, y), buff=0.1)
            self.play(Write(lab))
            self.wait(espera)
            self.play(FadeOut(fl))
            guardados.add(d, lab)
            return d, lab

        poner("A", 3, 2, txt=("Para llegar a A(3, 2), primero nos movemos en horizontal: x = 3",
                              "Después en vertical: y = 2. Siempre primero la x y después la y"), espera=2)
        poner("B", -4, 1, txt=("Si x es negativa, vamos hacia la IZQUIERDA",))
        poner("C", -2, -3, txt=("Si y es negativa, hacia ABAJO",))
        poner("D", 4, -2)
        notas("¡Cuidado con el orden! (2, 3) no es lo mismo que (3, 2)", color=MAL)
        e = Dot(ax.c2p(2, 3), color=ROSA, radius=0.1)
        le = par("E", 2, 3).next_to(e, UR, buff=0.1)
        self.play(FadeIn(e, scale=2), Write(le))
        self.play(Indicate(guardados[1]), Indicate(le))
        self.wait(2.5)
        self.play(FadeOut(guardados), FadeOut(VGroup(e, le)))

        sub("Leer un punto")
        g = Dot(ax.c2p(-5, 3), color=ACENTO, radius=0.1)
        self.play(FadeIn(g, scale=2))
        notas("Para leer un punto bajamos (o subimos) hasta los ejes")
        pr = proy(ax, -5, 3, col=WHITE)
        self.play(Create(pr[0]))
        self.play(Indicate(ax.x_axis.numbers[1], color=LETRA, scale_factor=1.6))
        self.play(Create(pr[1]))
        self.play(Indicate(ax.y_axis.numbers[6], color=Y_COL, scale_factor=1.6))
        lg = par("F", -5, 3).next_to(g, UR, buff=0.1)
        self.play(Write(lg))
        self.wait(2)
        self.play(FadeOut(VGroup(g, pr, lg)))
        notas.fin()

        sub("Cuadrantes")
        c = [("1.º", "(+,\\,+)", (3, 2), OK), ("2.º", "(-,\\,+)", (-3, 2), Y_COL),
             ("3.º", "(-,\\,-)", (-3, -2), ROSA), ("4.º", "(+,\\,-)", (3, -2), NAR)]
        rects = VGroup()
        for k, (nom, sig, (cx, cy), col) in enumerate(c):
            r = Rectangle(width=6 * 0.7, height=4 * 0.7, stroke_width=0, fill_color=col, fill_opacity=0.15)
            r.move_to(ax.c2p(cx, cy))
            t = VGroup(texto(nom + " cuadrante", 24, col), MathTex(sig, font_size=40, color=col)).arrange(DOWN, buff=0.1)
            t.move_to(ax.c2p(cx, cy))
            self.play(FadeIn(r), FadeIn(t), run_time=0.8)
            rects.add(VGroup(r, t))
        notas("Los ejes dividen el plano en 4 cuadrantes. Los signos dicen en cuál está el punto")
        self.wait(3)
        self.play(*[g[1].animate.set_opacity(0.35) for g in rects])
        notas("¿Y si una coordenada es 0? Entonces el punto está SOBRE un eje")
        p1 = Dot(ax.c2p(3, 0), color=ACENTO, radius=0.1)
        l1 = par("G", 3, 0).next_to(p1, UP, buff=0.12)
        p2 = Dot(ax.c2p(0, -3), color=ACENTO, radius=0.1)
        l2 = par("H", 0, -3).next_to(p2, RIGHT, buff=0.12)
        self.play(FadeIn(p1, scale=2), Write(l1))
        self.play(FadeIn(p2, scale=2), Write(l2))
        notas("y = 0: está en el eje X.  x = 0: está en el eje Y", color=ACENTO)
        self.wait(3.5)
        notas.fin()


# ---------------------------------------------------------------------------
def diagrama(xs, ys, flechas, cx, cy, col_f=WHITE):
    """Diagrama de flechas: dos óvalos con los elementos. flechas = [(i, j)]."""
    ox = Ellipse(width=1.3, height=0.75 * max(len(xs), len(ys)) + 0.8, color=LETRA).move_to([cx - 1.3, cy, 0])
    oy = Ellipse(width=1.3, height=0.75 * max(len(xs), len(ys)) + 0.8, color=Y_COL).move_to([cx + 1.3, cy, 0])
    ex = VGroup(*[MathTex(v, font_size=36, color=LETRA) for v in xs]).arrange(DOWN, buff=0.4).move_to(ox)
    ey = VGroup(*[MathTex(v, font_size=36, color=Y_COL) for v in ys]).arrange(DOWN, buff=0.4).move_to(oy)
    fl = VGroup(*[Arrow(ex[i].get_right(), ey[j].get_left(), buff=0.12, color=col_f, stroke_width=3,
                        max_tip_length_to_length_ratio=0.15) for i, j in flechas])
    return VGroup(ox, oy, ex, ey), fl


class ConceptoFuncion(Scene):
    def construct(self):
        cab = titulo(self, "¿Qué es una función?")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Una máquina")
        caja = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.2, color=ACENTO, fill_color=ACENTO,
                                fill_opacity=0.12).move_to([-1.6, 0.6, 0])
        regla = MathTex("\\times 2\\ \\ +1", font_size=46, color=ACENTO).move_to(caja)
        ent = Arrow([-5.2, 0.6, 0], caja.get_left(), buff=0.1, color=LETRA)
        sal = Arrow(caja.get_right(), [2.0, 0.6, 0], buff=0.1, color=Y_COL)
        self.play(Create(caja), Write(regla), GrowArrow(ent), GrowArrow(sal))
        cabx = MathTex("x", font_size=40, color=LETRA).move_to([3.8, 1.9, 0])
        caby = MathTex("y", font_size=40, color=Y_COL).move_to([5.3, 1.9, 0])
        raya = Line([3.2, 1.6, 0], [5.9, 1.6, 0], color=GREY_B, stroke_width=2)
        self.play(FadeIn(cabx), FadeIn(caby), Create(raya))
        notas("Entra un número x... la máquina lo multiplica por 2 y le suma 1... y sale y")
        for k, v in enumerate([1, 2, 3, 5]):
            a = MathTex(str(v), font_size=48, color=LETRA).move_to([-5.6, 0.6, 0])
            self.play(FadeIn(a), run_time=0.3)
            self.play(a.animate.move_to(caja).scale(0.4).set_opacity(0), run_time=0.6)
            b = MathTex(str(2 * v + 1), font_size=48, color=Y_COL).move_to(caja).scale(0.4)
            self.play(b.animate.scale(2.5).move_to([2.5, 0.6, 0]), run_time=0.6)
            y = 1.15 - k * 0.5
            cx_ = MathTex(str(v), font_size=36, color=LETRA).move_to([3.8, y, 0])
            cy_ = MathTex(str(2 * v + 1), font_size=36, color=Y_COL).move_to([5.3, y, 0])
            self.play(FadeIn(cx_), Transform(b, cy_), run_time=0.5)
        f = XY("y=2x+1", 54).move_to([-1.6, -1.2, 0])
        self.play(Write(f))
        notas("Esta máquina es una FUNCIÓN: a cada x le hace corresponder una y", color=OK)
        self.wait(3)
        var = VGroup(texto("x: variable INDEPENDIENTE (la elegimos nosotros)", 26, LETRA),
                     texto("y: variable DEPENDIENTE (depende de x)", 26, Y_COL)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        var.move_to([-1.2, -2.35, 0])
        notas.fin()
        self.play(FadeIn(var, shift=UP * 0.2))
        self.wait(3.5)
        limpiar(self, cab)
        sub.olvidar()

        sub("Una sola salida")
        d = texto("Una FUNCIÓN relaciona cada valor de x con UN ÚNICO valor de y", 30, ACENTO).move_to([0, 2.5, 0])
        self.play(FadeIn(d))
        g1, f1 = diagrama(["1", "2", "3"], ["3", "5", "7"], [(0, 0), (1, 1), (2, 2)], -3.5, -0.45, OK)
        t1 = texto("y = 2x + 1", 26).next_to(g1, UP, buff=0.2)
        self.play(FadeIn(g1), FadeIn(t1))
        self.play(LaggedStart(*[GrowArrow(a) for a in f1], lag_ratio=0.3))
        v1 = texto("Sí es función", 28, OK).next_to(g1, DOWN, buff=0.15)
        notas("Cada x tiene UNA flecha: es una función")
        self.play(FadeIn(v1))
        self.wait(1.5)
        g2, f2 = diagrama(["4", "9"], ["2", "-2", "3", "-3"], [(0, 0), (0, 1), (1, 2), (1, 3)], 3.5, -0.45, MAL)
        t2 = texto("x → número cuyo cuadrado es x", 24).next_to(g2, UP, buff=0.2)
        self.play(FadeIn(g2), FadeIn(t2))
        self.play(LaggedStart(*[GrowArrow(a) for a in f2], lag_ratio=0.3))
        notas("Pero 4 tiene DOS salidas: 2 · 2 = 4 y (−2) · (−2) = 4", color=MAL)
        v2 = texto("No es función", 28, MAL).next_to(g2, DOWN, buff=0.15)
        self.play(FadeIn(v2), Indicate(g2[2][0], color=MAL))
        self.wait(3)
        self.play(FadeOut(VGroup(g2, f2, t2, v2)))
        g3, f3 = diagrama(["-2", "2", "3"], ["4", "9"], [(0, 0), (1, 0), (2, 1)], 3.5, -0.45, OK)
        t3 = XY("y=x^{2}", 34).next_to(g3, UP, buff=0.2)
        self.play(FadeIn(g3), FadeIn(t3))
        self.play(LaggedStart(*[GrowArrow(a) for a in f3], lag_ratio=0.3))
        v3 = texto("Sí es función", 28, OK).next_to(g3, DOWN, buff=0.15)
        notas("En cambio, que DOS x vayan a la misma y no es problema: cada x sigue teniendo una sola salida", color=OK)
        self.play(FadeIn(v3))
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Cuatro formas de dar una función")
        notas("El mismo ejemplo de cuatro maneras: 1 kg de tomates cuesta 2 €")
        pos = [(-3.45, 1.15), (3.45, 1.15), (-3.45, -1.75), (3.45, -1.75)]
        marcos = VGroup(*[RoundedRectangle(width=6.5, height=2.6, corner_radius=0.15, color=GREY_B).move_to([x, y, 0])
                          for x, y in pos])
        tits = ["1. Con palabras", "2. Con una tabla", "3. Con una fórmula", "4. Con una gráfica"]
        tt = VGroup(*[texto(t, 24, ACENTO).next_to(m.get_corner(UL), DR, buff=0.15) for t, m in zip(tits, marcos)])
        self.play(Create(marcos), FadeIn(tt))
        c1 = texto("«Cada kilo de tomates\ncuesta 2 €»", 30).move_to(marcos[0]).shift(DOWN * 0.15)
        self.play(FadeIn(c1))
        self.wait(1)
        marco, labs, cel, _ = tabla_h(["kg", "€"], [["1", "2", "3", "4"], ["2", "4", "6", "8"]], 3.45, 1.25,
                                      cols=(LETRA, Y_COL), w=0.8, wn=1.0, size=32)
        self.play(Create(marco), FadeIn(labs), *[FadeIn(c) for c in cel[0] + cel[1]])
        self.wait(1)
        c3 = XY("y=2x", 60).move_to(marcos[2]).shift(DOWN * 0.15)
        self.play(Write(c3))
        self.wait(1)
        ax = Axes(x_range=[0, 4.5, 1], y_range=[0, 9, 2], x_length=3.4, y_length=1.75, tips=False,
                  axis_config={"include_numbers": True, "font_size": 16, "color": GREY_B}).move_to([3.7, -1.95, 0])
        pts = VGroup(*[Dot(ax.c2p(k, 2 * k), color=ACENTO, radius=0.06) for k in range(1, 5)])
        self.play(Create(ax), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.2))
        self.play(Create(Line(ax.c2p(0, 0), ax.c2p(4.5, 9), color=Y_COL, stroke_width=3)))
        notas("Las cuatro dicen lo mismo. Pasaremos de una a otra según lo que necesitemos", color=OK)
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
class GraficaFuncion(Scene):
    def construct(self):
        cab = titulo(self, "La gráfica de una función")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("De la tabla a la gráfica")
        horas = [0, 4, 8, 12, 16, 20, 24]
        temps = [8, 6, 10, 18, 20, 14, 9]
        marco, labs, cel, _ = tabla_h(["hora", "°C"], [[str(h) for h in horas], [str(t) for t in temps]], 0, 2.25,
                                      cols=(LETRA, Y_COL), w=0.85, wn=1.2, size=30)
        notas("La temperatura de un día de primavera, cada 4 horas")
        self.play(Create(marco), FadeIn(labs), *[FadeIn(c) for c in cel[0] + cel[1]])
        ax, g = ejes_xy((0, 25), (0, 25), 9.0, 3.3, (0.2, -1.2), step=(4, 5), nx="hora", ny="°C")
        self.play(Create(g))
        notas("Cada columna de la tabla es un punto (hora, temperatura)")
        dots = VGroup()
        for k, (h, t) in enumerate(zip(horas, temps)):
            d = Dot(ax.c2p(h, t), color=ACENTO, radius=0.08)
            self.play(TransformFromCopy(VGroup(cel[0][k], cel[1][k]), d), run_time=0.55)
            dots.add(d)
        curva = VMobject(color=Y_COL, stroke_width=4).set_points_smoothly([ax.c2p(h, t) for h, t in zip(horas, temps)])
        notas("La temperatura no da saltos: pasa por todos los valores intermedios. Unimos los puntos")
        self.play(Create(curva), run_time=2)
        self.bring_to_front(dots)
        self.wait(1)
        p = Dot(ax.c2p(10, 14), color=ROSA, radius=0.09)
        notas("Y así podemos leer valores que no estaban en la tabla: a las 10, unos 14 °C", color=OK)
        self.play(Create(proy(ax, 10, 14, col=ROSA)), FadeIn(p, scale=2))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("¿Unimos los puntos?")
        enun = texto("Entradas de cine:\n6 € cada una", 30).move_to([-4.3, 1.5, 0])
        self.play(FadeIn(enun))
        ax, g = ejes_xy((0, 6.6), (0, 36), 5.9, 4.2, (2.9, -0.5), step=(1, 6), nx="entradas", ny="€")
        self.play(Create(g))
        pts = VGroup(*[Dot(ax.c2p(k, 6 * k), color=ACENTO, radius=0.09) for k in range(1, 6)])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in pts], lag_ratio=0.2))
        lin = DashedLine(ax.c2p(1, 6), ax.c2p(5, 30), color=GREY_B)
        notas("¿Los unimos? ¿Qué sería el punto del medio, 2,5 entradas?")
        self.play(Create(lin))
        q = Dot(ax.c2p(2.5, 15), color=MAL, radius=0.09)
        cr = Cross(q, stroke_color=MAL, scale_factor=2.5)
        self.play(FadeIn(q), Create(cr))
        no = texto("¡No existe media entrada!", 28, MAL).move_to([-4.3, 0.0, 0])
        self.play(FadeIn(no))
        self.wait(1.5)
        self.play(FadeOut(VGroup(lin, q, cr)))
        regla = texto("Solo unimos los puntos si\nla x puede tomar cualquier\nvalor (tiempo, peso...)", 26, ACENTO)
        regla.move_to([-4.3, -1.5, 0])
        self.play(FadeIn(regla))
        notas("Aquí la gráfica son puntos sueltos", color=OK)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("¿Es una función?")
        notas("La prueba de la RECTA VERTICAL: la pasamos por toda la gráfica")
        ax1, g1 = plano((-3, 3), (-3, 3), 0.72, (-3.5, -0.35), num_size=16)
        ax2, g2 = plano((-3, 3), (-3, 3), 0.72, (3.5, -0.35), num_size=16)
        f = lambda x: 0.25 * x ** 3 - x
        c1 = ax1.plot(f, x_range=[-2.75, 2.75], color=Y_COL, stroke_width=4)
        c2 = Circle(radius=2 * 0.72, color=ROSA, stroke_width=4).move_to(ax2.c2p(0, 0))
        self.play(Create(g1), Create(g2), Create(c1), Create(c2))
        t = ValueTracker(-2.9)
        v1 = always_redraw(lambda: DashedLine(ax1.c2p(t.get_value(), -3), ax1.c2p(t.get_value(), 3), color=ACENTO))
        d1 = always_redraw(lambda: Dot(ax1.c2p(t.get_value(), f(t.get_value())), color=OK, radius=0.09)
                           if abs(t.get_value()) <= 2.75 else VectorizedPoint())
        self.add(v1, d1)
        self.play(t.animate.set_value(2.9), run_time=3, rate_func=linear)
        r1 = texto("Siempre UN punto: sí es función", 26, OK).next_to(g1, UP, buff=0.1)
        self.play(FadeIn(r1))
        u = ValueTracker(-2.9)

        def dos():
            x = u.get_value()
            if abs(x) >= 2:
                return VGroup()
            h = np.sqrt(4 - x * x)
            return VGroup(Dot(ax2.c2p(x, h), color=MAL, radius=0.09), Dot(ax2.c2p(x, -h), color=MAL, radius=0.09))
        v2 = always_redraw(lambda: DashedLine(ax2.c2p(u.get_value(), -3), ax2.c2p(u.get_value(), 3), color=ACENTO))
        d2 = always_redraw(dos)
        self.add(v2, d2)
        self.play(u.animate.set_value(0.8), run_time=2, rate_func=linear)
        notas("Aquí la recta corta DOS veces: a esa x le tocan dos y", color=MAL)
        self.wait(2)
        self.play(u.animate.set_value(2.9), run_time=1.5, rate_func=linear)
        r2 = texto("Dos puntos: no es función", 26, MAL).next_to(g2, UP, buff=0.1)
        self.play(FadeIn(r2))
        notas("Si alguna recta vertical corta la gráfica en dos puntos, NO es una función", color=ACENTO)
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
class DominioRecorrido(Scene):
    def construct(self):
        cab = titulo(self, "Dominio y recorrido", "y puntos de corte")
        notas = Notas(self)
        sub = Sub(self, cab)
        f = lambda x: -0.5 * (x + 1) * (x - 3)
        ax, g = plano((-3, 5), (-3, 3), 0.75, (2.9, -0.4))
        curva = ax.plot(f, x_range=[-2, 4], color=WHITE, stroke_width=5)
        ext = VGroup(Dot(ax.c2p(-2, f(-2)), radius=0.08), Dot(ax.c2p(4, f(4)), radius=0.08))
        self.play(Create(g))
        self.play(Create(curva), FadeIn(ext))
        notas("Esta función solo está dibujada entre x = −2 y x = 4")
        self.wait(1.5)

        sub("Dominio")
        xs = np.linspace(-2, 4, 31)
        lv = VGroup(*[Line(ax.c2p(x, f(x)), ax.c2p(x, 0), color=LETRA, stroke_width=2, stroke_opacity=0.6) for x in xs])
        notas("Como si una luz desde arriba proyectara la sombra de la gráfica sobre el eje X")
        self.play(LaggedStart(*[Create(l) for l in lv], lag_ratio=0.04), run_time=2)
        dom = Line(ax.c2p(-2, 0), ax.c2p(4, 0), color=LETRA, stroke_width=10)
        dd = VGroup(Dot(ax.c2p(-2, 0), color=LETRA, radius=0.1), Dot(ax.c2p(4, 0), color=LETRA, radius=0.1))
        self.play(Create(dom), FadeIn(dd), FadeOut(lv))
        t1 = VGroup(texto("DOMINIO: los valores de x", 28, LETRA), texto("que tienen imagen", 28, LETRA),
                    MathTex("\\mathrm{Dom}\\,f=[-2,\\,4]", font_size=46, color=LETRA))
        t1.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.2, 1.5, 0])
        self.play(FadeIn(t1[:2]))
        self.play(Write(t1[2]))
        notas("[−2, 4] quiere decir: todos los números desde −2 hasta 4", color=ACENTO)
        self.wait(3)

        sub("Recorrido")
        lh = VGroup(*[Line(ax.c2p(x, f(x)), ax.c2p(0, f(x)), color=Y_COL, stroke_width=2, stroke_opacity=0.6) for x in xs])
        notas("Ahora la sombra sobre el eje Y: ¿qué alturas alcanza la gráfica?")
        self.play(LaggedStart(*[Create(l) for l in lh], lag_ratio=0.04), run_time=2)
        rec = Line(ax.c2p(0, -2.5), ax.c2p(0, 2), color=Y_COL, stroke_width=10)
        rd = VGroup(Dot(ax.c2p(0, -2.5), color=Y_COL, radius=0.1), Dot(ax.c2p(0, 2), color=Y_COL, radius=0.1))
        self.play(Create(rec), FadeIn(rd), FadeOut(lh))
        t2 = VGroup(texto("RECORRIDO: los valores", 28, Y_COL), texto("que toma y", 28, Y_COL),
                    MathTex("\\mathrm{Rec}\\,f=[-2{,}5;\\ 2]", font_size=46, color=Y_COL))
        t2.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.2, -0.6, 0])
        self.play(FadeIn(t2[:2]))
        self.play(Write(t2[2]))
        notas("La gráfica baja hasta −2,5 y sube hasta 2", color=ACENTO)
        self.wait(3)
        notas.fin()
        self.play(FadeOut(VGroup(t1, t2, dom, dd, rec, rd)))

        sub("Puntos de corte")
        notas("¿Dónde cruza la gráfica los ejes?")
        cx = VGroup(Dot(ax.c2p(-1, 0), color=ROSA, radius=0.11), Dot(ax.c2p(3, 0), color=ROSA, radius=0.11))
        cy = Dot(ax.c2p(0, 1.5), color=OK, radius=0.11)
        tx = VGroup(texto("Con el eje X (y = 0):", 28, ROSA),
                    VGroup(par("", -1, 0, 40), par("", 3, 0, 40)).arrange(RIGHT, buff=0.4))
        tx.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.2, 1.3, 0])
        self.play(FadeIn(cx, scale=2), *[Flash(d, color=ROSA) for d in cx])
        self.play(FadeIn(tx))
        self.wait(1.5)
        ty = VGroup(texto("Con el eje Y (x = 0):", 28, OK), par("", 0, 1.5, 40))
        ty.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.2, -0.6, 0])
        self.play(FadeIn(cy, scale=2), Flash(cy, color=OK))
        self.play(FadeIn(ty))
        notas("Con el eje Y como mucho hay un corte (si no, no sería función); con el eje X puede haber varios",
              color=ACENTO)
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
def lapiz():
    p = Polygon([0, 0, 0], [0.12, 0.35, 0], [-0.12, 0.35, 0], color=ACENTO, fill_color=ACENTO, fill_opacity=1)
    cuerpo = Rectangle(width=0.24, height=0.7, color=ACENTO, fill_color="#E8C547", fill_opacity=1).next_to(p, UP, buff=0)
    return VGroup(p, cuerpo).rotate(-0.5, about_point=ORIGIN)


def lapiz_en(pt):
    lp = lapiz()
    lp.shift(np.array(pt) - lp[0].get_vertices()[0])
    return lp


PERFIL = [(-5, -1), (-3, 3), (-1, 0), (1, 2), (3, 2), (5, -2)]


def color_tramo(a, b):
    return CRECE if b[1] > a[1] else (DECRECE if b[1] < a[1] else CONST)


class ContinuidadCrecimiento(Scene):
    def construct(self):
        cab = titulo(self, "Continuidad y crecimiento")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Continua o discontinua")
        ax1, g1 = ejes_xy((0, 4), (0, 4), 4.6, 3.6, (-3.5, -0.2), nx="", ny="")
        ax2, g2 = ejes_xy((0, 3.5), (0, 5), 4.6, 3.6, (3.5, -0.2), nx="horas", ny="€")
        t1 = texto("Altura de una planta", 26, OK).next_to(g1, UP, buff=0.25)
        t2 = texto("Precio del aparcamiento", 26, NAR).next_to(g2, UP, buff=0.25)
        self.play(Create(g1), FadeIn(t1))
        c = ax1.plot(lambda x: 0.4 + 3 / (1 + np.exp(-2 * (x - 2))), x_range=[0, 4], color=OK, stroke_width=5)
        lp = lapiz_en(c.get_start())
        camino = c.copy().shift(lp.get_center() - c.get_start())
        notas("Esta gráfica se dibuja SIN levantar el lápiz: es CONTINUA")
        self.play(FadeIn(lp))
        self.play(Create(c), MoveAlongPath(lp, camino), run_time=2.5, rate_func=linear)
        self.play(FadeOut(lp))
        self.play(Create(g2), FadeIn(t2))
        notas("Aparcamiento: 2 € la primera hora, 3 € hasta 2 h y 4 € hasta 3 h")
        tramos = VGroup()
        for k, v in enumerate([2, 3, 4]):
            seg = Line(ax2.c2p(k, v), ax2.c2p(k + 1, v), color=NAR, stroke_width=5)
            abierto = Circle(radius=0.08, color=NAR, stroke_width=3, fill_color=FONDO, fill_opacity=1).move_to(ax2.c2p(k, v))
            cerrado = Dot(ax2.c2p(k + 1, v), color=NAR, radius=0.08)
            lp = lapiz_en(seg.get_start())
            self.play(FadeIn(lp), run_time=0.3)
            self.play(Create(seg), lp.animate.shift(seg.get_end() - seg.get_start()), run_time=1)
            self.play(FadeIn(abierto), FadeIn(cerrado), lp.animate.shift(UP * 0.5).set_opacity(0.4), run_time=0.6)
            self.remove(lp)
            tramos.add(seg, abierto, cerrado)
        notas("Aquí hay que LEVANTAR el lápiz: hay saltos. Es DISCONTINUA", color=MAL)
        self.wait(2)
        notas("El punto lleno es el que vale: a las 2 h justas pagas 3 € (el hueco es «aún no»)", color=ACENTO)
        self.wait(4)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Crece, decrece o es constante")
        ax, g = plano((-6, 6), (-3, 4), 0.58, (-1.9, -0.35), num_size=18)
        self.play(Create(g))
        notas("Recorremos la gráfica de IZQUIERDA a DERECHA, como si fuéramos en bici")
        bici = Dot(ax.c2p(*PERFIL[0]), color=WHITE, radius=0.12)
        self.add(bici)
        textos = {CRECE: "Sube: la función CRECE", DECRECE: "Baja: la función DECRECE",
                  CONST: "Llano: la función es CONSTANTE"}
        segs = VGroup()
        for a, b in zip(PERFIL[:-1], PERFIL[1:]):
            col = color_tramo(a, b)
            s = Line(ax.c2p(*a), ax.c2p(*b), color=col, stroke_width=6)
            notas(textos[col], color=col)
            self.play(Create(s), bici.animate.move_to(ax.c2p(*b)), run_time=1.3, rate_func=linear)
            segs.add(s)
            self.bring_to_front(bici)
        self.play(FadeOut(bici))
        notas.fin()
        info = [("Crece en", "(-5,\\,-3)\\ \\text{y}\\ (-1,\\,1)", CRECE, [(-5, -3), (-1, 1)]),
                ("Decrece en", "(-3,\\,-1)\\ \\text{y}\\ (3,\\,5)", DECRECE, [(-3, -1), (3, 5)]),
                ("Constante en", "(1,\\,3)", CONST, [(1, 3)])]
        filas = VGroup()
        for k, (t, tex, col, ints) in enumerate(info):
            f_ = VGroup(texto(t, 26, col), MathTex(tex, font_size=34, color=col)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            f_.move_to([5.0, 1.9 - k * 1.2, 0])
            marcas = VGroup(*[Line(ax.c2p(i0, 0), ax.c2p(i1, 0), color=col, stroke_width=10) for i0, i1 in ints])
            self.play(FadeIn(f_), Create(marcas))
            self.wait(1)
            self.play(FadeOut(marcas))
            filas.add(f_)
        notas("Los intervalos se dan con los valores de x (dónde), no con los de y", color=ACENTO)
        self.wait(3.5)
        notas.fin()

        sub("Máximos y mínimos")
        self.play(FadeOut(filas))
        palo = Line(ax.c2p(-3, 3), ax.c2p(-3, 3) + UP * 0.8, color=WHITE, stroke_width=3)
        band = Polygon(palo.get_end(), palo.get_end() + DOWN * 0.3 + RIGHT * 0.45, palo.get_end() + DOWN * 0.3,
                       color=ROSA, fill_color=ROSA, fill_opacity=1)
        notas("En (−3, 3) pasa de subir a bajar: es la cima, un MÁXIMO", color=ROSA)
        self.play(Create(palo), FadeIn(band))
        tm = VGroup(texto("Máximo", 28, ROSA), par("", -3, 3, 38)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tm.move_to([5.0, 1.6, 0])
        self.play(FadeIn(tm))
        self.wait(2)
        valle = Dot(ax.c2p(-1, 0), color=Y_COL, radius=0.13)
        notas("En (−1, 0) pasa de bajar a subir: es un valle, un MÍNIMO", color=Y_COL)
        self.play(FadeIn(valle, scale=2), Flash(valle, color=Y_COL))
        tn = VGroup(texto("Mínimo", 28, Y_COL), par("", -1, 0, 38)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tn.move_to([5.0, 0.0, 0])
        self.play(FadeIn(tn))
        self.wait(2)
        notas("Máximo: de crecer a decrecer.  Mínimo: de decrecer a crecer", color=ACENTO)
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
def casa(p, s=0.5):
    base = Square(s, color=WHITE, fill_color="#8E9AAF", fill_opacity=1).move_to(p)
    techo = Polygon(base.get_corner(UL), base.get_corner(UR), base.get_top() + UP * s * 0.6,
                    color=WHITE, fill_color=MAL, fill_opacity=1)
    return VGroup(base, techo)


def monte(p, s=0.9):
    return Polygon(p + LEFT * s * 0.6, p + RIGHT * s * 0.6, p + UP * s, color=WHITE, fill_color=OK, fill_opacity=0.8)


def dist_exc(t):
    if t <= 2:
        return 3 * t
    if t <= 3:
        return 6
    if t <= 4.5:
        return 6 - 4 * (t - 3)
    return 0


class InterpretacionGraficas(Scene):
    def construct(self):
        cab = titulo(self, "Interpretar gráficas")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("La excursión")
        ax, g = ejes_xy((0, 5.5), (0, 7), 6.0, 4.2, (3.5, -0.6), nx="tiempo (h)", ny="distancia a casa (km)")
        x0, x1, yc = -6.2, -1.2, 1.3
        camino = Line([x0, yc, 0], [x1, yc, 0], color=GREY_B, stroke_width=4)
        ca = casa(np.array([x0, yc + 0.25, 0]))
        mo = monte(np.array([x1, yc, 0]))
        kms = VGroup(*[VGroup(Line([x0 + k * (x1 - x0) / 6, yc - 0.08, 0], [x0 + k * (x1 - x0) / 6, yc + 0.08, 0],
                                   color=GREY_B),
                              texto(str(k), 18, GREY_B).move_to([x0 + k * (x1 - x0) / 6, yc - 0.3, 0])) for k in range(7)])
        tk = texto("km", 20, GREY_B).move_to([x1 + 0.5, yc - 0.3, 0])
        self.play(Create(g), Create(camino), FadeIn(ca), FadeIn(mo), FadeIn(kms), FadeIn(tk))
        t = ValueTracker(0)
        persona = always_redraw(lambda: Dot([x0 + dist_exc(t.get_value()) * (x1 - x0) / 6, yc + 0.22, 0],
                                            color=ACENTO, radius=0.13))
        traza = always_redraw(lambda: ax.plot(dist_exc, x_range=[0, max(t.get_value(), 0.03), 0.01],
                                              color=Y_COL, stroke_width=5, use_smoothing=False))
        punto = always_redraw(lambda: Dot(ax.c2p(t.get_value(), dist_exc(t.get_value())), color=ACENTO, radius=0.09))
        self.add(traza, persona, punto)
        tramos = [(2, "Sale de casa hacia el mirador: la distancia AUMENTA y la gráfica SUBE", CRECE),
                  (3, "Descansa en el mirador: la distancia no cambia, la gráfica es HORIZONTAL", CONST),
                  (4.5, "Vuelve a casa: la distancia DISMINUYE y la gráfica BAJA hasta 0", DECRECE),
                  (5, "Ya está en casa: distancia 0", ACENTO)]
        for fin, txt, col in tramos:
            notas(txt, color=col)
            self.play(t.animate.set_value(fin), run_time=2.2 if fin != 5 else 1, rate_func=linear)
            self.wait(1.2)
        notas.fin()
        preg = VGroup(
            texto("¿A qué distancia está el mirador?  6 km", 22),
            texto("¿Cuánto tiempo descansa?  De 2 h a 3 h: 1 hora", 22),
            texto("Ida: 6 km en 2 h = 3 km/h", 22, CRECE),
            texto("Vuelta: 6 km en 1,5 h = 4 km/h", 22, DECRECE))
        preg.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-6.8, -1.0, 0], aligned_edge=LEFT)
        for p_ in preg[:2]:
            self.play(FadeIn(p_, shift=RIGHT * 0.2))
            self.wait(1.5)
        self.play(FadeIn(preg[2], shift=RIGHT * 0.2))
        self.play(FadeIn(preg[3], shift=RIGHT * 0.2))
        ida = Line(ax.c2p(0, 0), ax.c2p(2, 6), color=CRECE, stroke_width=8)
        vu = Line(ax.c2p(3, 6), ax.c2p(4.5, 0), color=DECRECE, stroke_width=8)
        self.play(Create(ida), Create(vu))
        notas("La vuelta es más rápida: su tramo está MÁS INCLINADO", color=ACENTO)
        self.wait(4)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Llenar dos vasos")
        H, Vmax, T = 2.4, 2.88, 9.0
        base_y = -2.2
        notas("Llenamos dos vasos con el mismo grifo. ¿Cómo sube el agua en cada uno?")
        v1x, v2x = -5.4, -2.7
        w1 = 1.2
        vaso1 = VMobject(color=WHITE, stroke_width=4).set_points_as_corners(
            [[v1x - w1 / 2, base_y + H + 0.2, 0], [v1x - w1 / 2, base_y, 0], [v1x + w1 / 2, base_y, 0],
             [v1x + w1 / 2, base_y + H + 0.2, 0]])
        w0, k = 0.6, 0.5

        def ancho2(h):
            return w0 + k * h
        vaso2 = VMobject(color=WHITE, stroke_width=4).set_points_as_corners(
            [[v2x - ancho2(H + 0.2) / 2, base_y + H + 0.2, 0], [v2x - w0 / 2, base_y, 0], [v2x + w0 / 2, base_y, 0],
             [v2x + ancho2(H + 0.2) / 2, base_y + H + 0.2, 0]])
        ax, g = ejes_xy((0, 10.9), (0, 3), 6.2, 3.9, (3.5, -0.45), step=(2, 1), nx="tiempo", ny="altura del agua")
        self.play(Create(vaso1), Create(vaso2), Create(g))
        tt = ValueTracker(0.12)

        def h1(t):
            return min(H, Vmax * t / T / w1)

        def h2(t):
            V = min(Vmax, Vmax * t / T)
            return (-w0 + np.sqrt(w0 * w0 + 2 * k * V)) / k

        agua1 = always_redraw(lambda: Rectangle(width=w1 - 0.08, height=max(h1(tt.get_value()), 0.001), stroke_width=0,
                                                fill_color=Y_COL, fill_opacity=0.7)
                              .move_to([v1x, base_y + h1(tt.get_value()) / 2, 0]))

        def poli2():
            h = max(h2(tt.get_value()), 0.001)
            return Polygon([v2x - w0 / 2 + 0.04, base_y, 0], [v2x + w0 / 2 - 0.04, base_y, 0],
                           [v2x + ancho2(h) / 2 - 0.04, base_y + h, 0], [v2x - ancho2(h) / 2 + 0.04, base_y + h, 0],
                           stroke_width=0, fill_color=NAR, fill_opacity=0.7)
        agua2 = always_redraw(poli2)
        c1 = always_redraw(lambda: ax.plot(h1, x_range=[0, tt.get_value(), 0.05], color=Y_COL, stroke_width=4))
        c2 = always_redraw(lambda: ax.plot(h2, x_range=[0, tt.get_value(), 0.05], color=NAR, stroke_width=4))
        self.add(agua1, agua2, c1, c2)
        self.play(tt.animate.set_value(T), run_time=6, rate_func=linear)
        notas("El vaso recto sube SIEMPRE IGUAL: su gráfica es una recta", color=Y_COL)
        self.wait(3)
        notas("El vaso que se ensancha sube rápido al principio y cada vez más despacio: la gráfica se curva",
              color=NAR)
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios
def enunciados_1():
    return [
        ("1. Coordenadas:", "a) Escribe las coordenadas de los puntos A, B, C y D de la gráfica.\n"
                            "b) ¿En qué cuadrante está cada punto?   (−3, 5)    (4, −1)    (−2, −6)    (0, 2)"),
        ("2. ¿Es función? (prueba de la recta vertical)", "a) Una curva que sube y baja    b) Una «C» tumbada    c) Una «V»"),
        ("3. Con la función y = 3x − 2:", "a) Completa la tabla para x = −1, 0, 1, 2.\n"
                                          "b) ¿Pasa la gráfica por el punto (2, 4)? ¿Y por (1, 2)?"),
    ]


def enunciados_2():
    return [
        ("4. Observa la gráfica (dibujada de x = −2 a x = 4):", "a) Dominio y recorrido.      b) Puntos de corte con los ejes."),
        ("5. En la gráfica de tramos rectos:", "a) ¿Dónde crece, decrece y es constante?      b) Máximo y mínimo."),
        ("6. Ana va en bici a casa de su abuela (gráfica distancia–tiempo):",
         "a) ¿A qué distancia vive la abuela?\nb) ¿Cuánto tiempo se para y dónde?\nc) ¿En qué tramo va más rápido?"),
    ]


P1 = [("A", 2, 3), ("B", -3, 1), ("C", -1, -2), ("D", 4, 0)]
CUADR = [("(-3,\\,5)", "2.º cuadrante", Y_COL), ("(4,\\,-1)", "4.º cuadrante", NAR),
         ("(-2,\\,-6)", "3.º cuadrante", ROSA), ("(0,\\,2)", "sobre el eje Y", ACENTO)]
F4 = lambda x: 0.5 * (x - 1) ** 2 - 2
P5 = [(-5, 0), (-3, -2), (-1, 1), (1, 1), (3, 4), (5, 0)]
P6 = [(0, 0), (60, 12), (90, 12), (120, 20)]


def ej1a(scene, notas, ejemplo=False):
    ax, g = plano((-5, 5), (-3, 4), 0.62, (1.8, -0.35), num_size=18)
    scene.play(Create(g))
    dots = VGroup(*[Dot(ax.c2p(x, y), color=ACENTO, radius=0.09) for _, x, y in P1])
    nombres = VGroup(*[texto(n, 24, ACENTO).next_to(d, etiq_dir(x, y), buff=0.08) for d, (n, x, y) in zip(dots, P1)])
    scene.play(FadeIn(dots), FadeIn(nombres))
    res = VGroup()
    lista_p = P1[:1] if ejemplo else P1[1:]
    for k, (n, x, y) in enumerate(lista_p):
        i = [p[0] for p in P1].index(n)
        pr = proy(ax, x, y, col=WHITE)
        if ejemplo:
            notas("Bajamos al eje X y vamos al eje Y")
        scene.play(Create(pr), Indicate(dots[i]))
        m = par(n, x, y, 40).move_to([-5.2, 1.6 - k * 0.8, 0])
        scene.play(TransformFromCopy(nombres[i], m))
        scene.play(FadeOut(pr), run_time=0.4)
        res.add(m)
    if not ejemplo:
        notas("D está sobre el eje X: su y es 0", color=ACENTO)
    scene.wait(2)
    notas.fin()


def ej1b(scene, notas):
    filas = VGroup()
    for k, (tex, txt, col) in enumerate(CUADR):
        f = VGroup(MathTex(tex, font_size=44), MathTex("\\rightarrow", font_size=40), texto(txt, 30, col))
        f.arrange(RIGHT, buff=0.4).move_to([-0.5, 1.6 - k * 1.0, 0], aligned_edge=LEFT).shift(LEFT * 2.5)
        scene.play(FadeIn(f[0]))
        scene.play(FadeIn(f[1:], shift=RIGHT * 0.2))
        filas.add(f)
    notas("Signos: (+,+) 1.º · (−,+) 2.º · (−,−) 3.º · (+,−) 4.º. Si una coordenada es 0, está en un eje", color=ACENTO)
    scene.wait(3)
    notas.fin()


def ej2(scene, cual, notas, ejemplo=False):
    ax, g = plano((-3, 3), (-3, 3), 0.75, (0, -0.35), num_size=16)
    scene.play(Create(g))
    if cual == 0:
        f = lambda x: 0.3 * x ** 3 - 1.2 * x + 0.5
        c = ax.plot(f, x_range=[-2.7, 2.7], color=Y_COL, stroke_width=4)
        cortes = lambda x: [f(x)] if abs(x) <= 2.7 else []
        txt, ok = "Siempre un punto: SÍ es función", True
    elif cual == 1:
        c = ax.plot_parametric_curve(lambda s: np.array([s * s / 2 - 2, s, 0]), t_range=[-2.8, 2.8], color=Y_COL,
                                     stroke_width=4)
        cortes = lambda x: [np.sqrt(2 * (x + 2)), -np.sqrt(2 * (x + 2))] if -2 < x <= 1.92 else ([0] if abs(x + 2) < 0.02 else [])
        txt, ok = "Corta dos veces: NO es función", False
    else:
        f = lambda x: abs(x) - 1
        c = ax.plot(f, x_range=[-3, 3], color=Y_COL, stroke_width=4, use_smoothing=False)
        cortes = lambda x: [f(x)]
        txt, ok = "Siempre un punto (aunque tenga un pico): SÍ es función", True
    scene.play(Create(c))
    t = ValueTracker(-2.95)
    v = always_redraw(lambda: DashedLine(ax.c2p(t.get_value(), -3), ax.c2p(t.get_value(), 3), color=ACENTO))
    d = always_redraw(lambda: VGroup(*[Dot(ax.c2p(t.get_value(), y), color=OK if ok else MAL, radius=0.09)
                                       for y in cortes(t.get_value()) if -3 <= y <= 3]))
    scene.add(v, d)
    if ejemplo:
        notas("Pasamos una recta vertical por toda la gráfica")
    scene.play(t.animate.set_value(2.95), run_time=3, rate_func=linear)
    scene.remove(v, d)
    notas(txt, color=OK if ok else MAL)
    scene.wait(2.5)
    notas.fin()


def ej3a(scene, notas, ejemplo=False):
    f = XY("y=3x-2", 50).move_to([0, 2.2, 0])
    scene.play(Write(f))
    marco, labs, cel, _ = tabla_h(["x", "y"], [["-1", "0", "1", "2"], ["?", "?", "?", "?"]], 0, 1.0,
                                  cols=(LETRA, Y_COL), w=1.3, wn=1.0, size=40)
    scene.play(Create(marco), FadeIn(labs), *[FadeIn(c) for c in cel[0] + cel[1]])
    cuentas = ["3\\cdot(-1)-2=-5", "3\\cdot 0-2=-2", "3\\cdot 1-2=1", "3\\cdot 2-2=4"]
    vals = ["-5", "-2", "1", "4"]
    if ejemplo:
        notas("Sustituimos cada x en la fórmula")
    for k, (cu, v) in enumerate(zip(cuentas, vals)):
        m = MathTex(cu, font_size=38).move_to([-2.7 if k % 2 == 0 else 2.7, -0.7 - (k // 2) * 0.85, 0])
        scene.play(Write(m), run_time=0.8)
        nv = MathTex(v, font_size=40, color=Y_COL).move_to(cel[1][k])
        scene.play(Transform(cel[1][k], nv))
    scene.wait(2)
    notas.fin()


def ej3b(scene, notas):
    f = XY("y=3x-2", 50).move_to([0, 2.2, 0])
    scene.play(Write(f))
    for k, (pt, cu, ok, txt) in enumerate([("(2,\\,4)", "3\\cdot 2-2=4", True, "Sale 4: SÍ pasa por (2, 4)"),
                                           ("(1,\\,2)", "3\\cdot 1-2=1\\neq 2", False, "Sale 1, no 2: NO pasa por (1, 2)")]):
        y = 0.9 - k * 1.9
        p = MathTex(pt, font_size=46, color=ACENTO).move_to([-4.6, y, 0])
        c = MathTex(cu, font_size=46).next_to(p, RIGHT, buff=0.8)
        v = texto(txt, 28, OK if ok else MAL).next_to(c, DOWN, buff=0.25).align_to(c, LEFT)
        scene.play(FadeIn(p))
        notas("Sustituimos la x del punto y miramos si sale su y")
        scene.play(Write(c))
        scene.play(FadeIn(v))
        scene.wait(1.5)
    notas.fin()


def grafica4(scene):
    ax, g = plano((-3, 5), (-3, 3), 0.72, (3.0, -0.4), num_size=18)
    c = ax.plot(F4, x_range=[-2, 4], color=WHITE, stroke_width=5)
    ext = VGroup(Dot(ax.c2p(-2, F4(-2)), radius=0.08), Dot(ax.c2p(4, F4(4)), radius=0.08))
    scene.play(Create(g), Create(c), FadeIn(ext))
    return ax


def ej4a(scene, notas, ejemplo=False):
    ax = grafica4(scene)
    if ejemplo:
        notas("La sombra sobre el eje X da el dominio")
    dom = Line(ax.c2p(-2, 0), ax.c2p(4, 0), color=LETRA, stroke_width=10)
    scene.play(Create(dom))
    t1 = MathTex("\\mathrm{Dom}\\,f=[-2,\\,4]", font_size=46, color=LETRA).move_to([-4.0, 1.2, 0])
    scene.play(Write(t1))
    if ejemplo:
        notas("La sombra sobre el eje Y da el recorrido: de −2 (el valle) a 2,5 (los extremos)")
    rec = Line(ax.c2p(0, -2), ax.c2p(0, 2.5), color=Y_COL, stroke_width=10)
    scene.play(Create(rec))
    t2 = MathTex("\\mathrm{Rec}\\,f=[-2,\\,2{,}5]", font_size=46, color=Y_COL).move_to([-4.0, 0.0, 0])
    scene.play(Write(t2))
    scene.wait(2.5)
    notas.fin()


def ej4b(scene, notas):
    ax = grafica4(scene)
    cx = VGroup(Dot(ax.c2p(-1, 0), color=ROSA, radius=0.11), Dot(ax.c2p(3, 0), color=ROSA, radius=0.11))
    cy = Dot(ax.c2p(0, -1.5), color=OK, radius=0.11)
    tx = VGroup(texto("Eje X:", 28, ROSA), VGroup(par("", -1, 0, 40), par("", 3, 0, 40)).arrange(RIGHT, buff=0.4))
    tx.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.0, 1.2, 0])
    ty = VGroup(texto("Eje Y:", 28, OK), par("", 0, -1.5, 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    ty.move_to([-4.0, -0.5, 0])
    scene.play(FadeIn(cx, scale=2), FadeIn(tx))
    scene.play(FadeIn(cy, scale=2), FadeIn(ty))
    notas("Corta al eje X en x = −1 y x = 3, y al eje Y en y = −1,5", color=ACENTO)
    scene.wait(3)
    notas.fin()


def grafica5(scene):
    ax, g = plano((-6, 6), (-3, 5), 0.56, (-1.9, -0.45), num_size=16)
    p = poligonal(ax, P5, color=WHITE)
    scene.play(Create(g), Create(p))
    return ax


def ej5a(scene, notas, ejemplo=False):
    ax = grafica5(scene)
    if ejemplo:
        notas("De izquierda a derecha, tramo a tramo")
    segs = VGroup()
    for a, b in zip(P5[:-1], P5[1:]):
        s = Line(ax.c2p(*a), ax.c2p(*b), color=color_tramo(a, b), stroke_width=7)
        scene.play(Create(s), run_time=0.7)
        segs.add(s)
    info = [("Crece en", "(-3,\\,-1)\\ \\text{y}\\ (1,\\,3)", CRECE), ("Decrece en", "(-5,\\,-3)\\ \\text{y}\\ (3,\\,5)", DECRECE),
            ("Constante en", "(-1,\\,1)", CONST)]
    for k, (t, tex, col) in enumerate(info):
        f_ = VGroup(texto(t, 26, col), MathTex(tex, font_size=34, color=col)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        f_.move_to([5.0, 1.8 - k * 1.2, 0])
        scene.play(FadeIn(f_))
        scene.wait(0.8)
    scene.wait(2)
    notas.fin()


def ej5b(scene, notas):
    ax = grafica5(scene)
    mx = Dot(ax.c2p(3, 4), color=ROSA, radius=0.13)
    mn = Dot(ax.c2p(-3, -2), color=Y_COL, radius=0.13)
    scene.play(FadeIn(mx, scale=2), Flash(mx, color=ROSA))
    t1 = VGroup(texto("Máximo", 28, ROSA), par("", 3, 4, 38)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.0, 1.4, 0])
    scene.play(FadeIn(t1))
    notas("En (3, 4) pasa de crecer a decrecer", color=ROSA)
    scene.wait(1.5)
    scene.play(FadeIn(mn, scale=2), Flash(mn, color=Y_COL))
    t2 = VGroup(texto("Mínimo", 28, Y_COL), par("", -3, -2, 38)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.0, -0.2, 0])
    scene.play(FadeIn(t2))
    notas("En (−3, −2) pasa de decrecer a crecer", color=Y_COL)
    scene.wait(2.5)
    notas.fin()


def grafica6(scene):
    ax, g = ejes_xy((0, 138), (0, 22), 5.4, 4.2, (3.4, -0.5), step=(30, 4), nx="tiempo (min)", ny="distancia (km)",
                    num_size=18)
    p = poligonal(ax, P6, color=Y_COL)
    scene.play(Create(g), Create(p))
    return ax


def ej6(scene, partes, notas, ejemplo=False):
    ax = grafica6(scene)
    y = 1.6
    if "a" in partes:
        if ejemplo:
            notas("El final de la gráfica: cuando llega, está a 20 km")
        d = Dot(ax.c2p(120, 20), color=ACENTO, radius=0.1)
        scene.play(FadeIn(d, scale=2), Create(proy(ax, 120, 20)))
        t = texto("a) La abuela vive a 20 km", 28, ACENTO).move_to([-6.6, y, 0], aligned_edge=LEFT)
        scene.play(FadeIn(t))
        y -= 1.0
        scene.wait(1.5)
    if "b" in partes:
        s = Line(ax.c2p(60, 12), ax.c2p(90, 12), color=CONST, stroke_width=9)
        scene.play(Create(s))
        t = texto("b) Tramo horizontal: de 60 a 90 min.\n    Se para media hora a 12 km", 26, CONST).move_to([-6.6, y, 0], aligned_edge=LEFT)
        scene.play(FadeIn(t))
        y -= 1.3
        scene.wait(1.5)
    if "c" in partes:
        s1 = Line(ax.c2p(0, 0), ax.c2p(60, 12), color=CRECE, stroke_width=8)
        s2 = Line(ax.c2p(90, 12), ax.c2p(120, 20), color=ROSA, stroke_width=8)
        scene.play(Create(s1))
        t1 = texto("1.er tramo: 12 km en 60 min = 12 km/h", 24, CRECE).move_to([-6.6, y, 0], aligned_edge=LEFT)
        scene.play(FadeIn(t1))
        scene.play(Create(s2))
        t2 = texto("Último: 8 km en 30 min = 16 km/h", 24, ROSA).move_to([-6.6, y - 0.55, 0], aligned_edge=LEFT)
        scene.play(FadeIn(t2))
        notas("c) Va más rápido en el último tramo: es el más inclinado", color=ACENTO)
        scene.wait(2.5)
    notas.fin()


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Funciones y gráficas")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))
        pasos = [("Ejercicio 1 a)", lambda: ej1a(self, notas, True)), ("Ejercicio 2 a)", lambda: ej2(self, 0, notas, True)),
                 ("Ejercicio 3 a)", lambda: ej3a(self, notas, True)), ("Ejercicio 4 a)", lambda: ej4a(self, notas, True)),
                 ("Ejercicio 5 a)", lambda: ej5a(self, notas, True)), ("Ejercicio 6 a)", lambda: ej6(self, "a", notas, True))]
        for t, fn in pasos:
            subtitulo(self, cab, t)
            fn()
            limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 3")
        notas = Notas(self, size=24)
        pasos = [("Ejercicio 1 a): B, C y D", lambda: ej1a(self, notas)), ("Ejercicio 1 b)", lambda: ej1b(self, notas)),
                 ("Ejercicio 2 b)", lambda: ej2(self, 1, notas)), ("Ejercicio 2 c)", lambda: ej2(self, 2, notas)),
                 ("Ejercicio 3 b)", lambda: ej3b(self, notas))]
        for t, fn in pasos:
            subtitulo(self, cab, t)
            fn()
            limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 4 a 6.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 4 a 6")
        notas = Notas(self, size=24)
        pasos = [("Ejercicio 4 b)", lambda: ej4b(self, notas)), ("Ejercicio 5 b)", lambda: ej5b(self, notas)),
                 ("Ejercicio 6 b) y c)", lambda: ej6(self, "bc", notas))]
        for t, fn in pasos:
            subtitulo(self, cab, t)
            fn()
            limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
