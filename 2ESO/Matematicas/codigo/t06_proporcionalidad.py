"""Tema 6 · Proporcionalidad numérica (2º ESO)

Sigue el índice del libro: proporcionalidad directa e inversa · problemas · proporcionalidad compuesta ·
porcentajes · aumentos y disminuciones porcentuales.

Escenas:
    RazonProporcion           – limonada: vasos con la misma razón tienen el mismo color; proporción,
                                productos cruzados y cuarto proporcional
    ProporcionalidadDirecta   – tabla con ×2 / ×3, constante k, gráfica: recta que pasa por el origen;
                                el taxi (no proporcional)
    ProporcionalidadInversa   – rectángulos de área 12 (el vértice dibuja la curva); pintores y días con
                                bloques que se reordenan; directa frente a inversa
    ReglaDeTres               – esquema con flechas (mismo sentido / sentido contrario), regla de tres y
                                reducción a la unidad
    ProporcionalidadCompuesta – obreros × días en cuadrícula; cadena de factores; un caso con inversa
    Porcentajes               – cuadrícula de 100; % de una cantidad, el total, qué % es (barras)
    AumentosDisminuciones     – barras que crecen y se recortan; índice de variación; hacia atrás; encadenados
    EjerciciosEjemplo / EjerciciosResueltos1 / EjerciciosResueltos2

Colores: 1.ª magnitud cian, 2.ª naranja, 3.ª rosa; la incógnita x en amarillo; los porcentajes en verde.

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t06_proporcionalidad.py Porcentajes
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t06_proporcionalidad.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COMUN = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from t09_potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t03_lenguaje_algebraico import X, cuenta, lista, pagina_enunciados, tarjeta, ROSA, LETRA  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 6 · Proporcionalidad numérica"
TITULOS = {
    "RazonProporcion": "Razón y proporción",
    "ProporcionalidadDirecta": "Proporcionalidad directa",
    "ProporcionalidadInversa": "Proporcionalidad inversa",
    "ReglaDeTres": "Problemas: regla de tres y reducción a la unidad",
    "ProporcionalidadCompuesta": "Proporcionalidad compuesta",
    "Porcentajes": "Porcentajes",
    "AumentosDisminuciones": "Aumentos y disminuciones porcentuales",
    "InteresSimple": "Aprende +: interés simple",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 6)",
    "EjerciciosResueltos2": "Ejercicios resueltos (7 a 9)",
}
EXTRAS = {"InteresSimple": "E2"}
INTERACTIVOS = [("E1", "Pruébalo tú: ¿directa, inversa o ninguna?", "interactivos/directa_inversa.html",
                 "ProporcionalidadInversa"),
                ("E3", "Pruébalo tú: ¿qué oferta compensa?", "interactivos/ofertas.html", "InteresSimple")]

M1, M2, M3 = "#4FC3F7", "#FF9F43", ROSA     # magnitudes: cian, naranja, rosa
PCT = "#7BD88F"                            # porcentajes
LIMON, AGUA = "#F4D03F", "#5DADE2"
TRAB = "#C39BD3"                           # bloques de trabajo


class Sub:
    """Subtítulo que sustituye al anterior."""

    def __init__(self, scene, cab):
        self.scene, self.cab, self.t = scene, cab, None

    def __call__(self, txt):
        if self.t is not None and self.t in self.scene.mobjects:
            self.scene.play(FadeOut(self.t), run_time=0.4)
        self.t = subtitulo(self.scene, self.cab, txt)

    def olvidar(self):
        self.t = None


def T(s, size=44, color=WHITE):
    return MathTex(s, font_size=size, color=color)


def celda(v, size, col):
    if v == "x":
        return MathTex("x", font_size=size, color=LETRA)
    if v == "?":
        return MathTex("?", font_size=size, color=GREY_B)
    return MathTex(v, font_size=size, color=col)


def tabla_h(nombres, filas, cx, cy, cols=(M1, M2), w=1.1, h=0.72, wn=2.2, size=40):
    """Tabla horizontal: nombre de la magnitud a la izquierda y los valores en fila."""
    n, nf = len(filas[0]), len(filas)
    W, H = wn + n * w, nf * h
    x0, ytop = cx - W / 2, cy + h / 2
    marco = VGroup(Rectangle(width=W, height=H, stroke_color=GREY_B, stroke_width=2).move_to([cx, ytop - H / 2, 0]))
    for r in range(1, nf):
        marco.add(Line([x0, ytop - r * h, 0], [x0 + W, ytop - r * h, 0], stroke_color=GREY_B, stroke_width=2))
    for k in range(n):
        marco.add(Line([x0 + wn + k * w, ytop, 0], [x0 + wn + k * w, ytop - H, 0], stroke_color=GREY_B, stroke_width=2))
    labs = VGroup(*[texto(nm, 24, cols[r]).move_to([x0 + wn / 2, cy - r * h, 0]) for r, nm in enumerate(nombres)])
    celdas = [[celda(v, size, cols[r]).move_to([x0 + wn + (k + 0.5) * w, cy - r * h, 0]) for k, v in enumerate(fila)]
              for r, fila in enumerate(filas)]
    return marco, labs, celdas, (ytop, ytop - H)


def tabla_v(cabs, filas, cx, cy, cols, w=1.9, h=0.68, size=40, tam=26):
    """Tabla con las cabeceras arriba."""
    n, nf = len(cabs), len(filas)
    W, H = n * w, (nf + 1) * h
    x0, ytop = cx - W / 2, cy + h / 2
    marco = VGroup(Rectangle(width=W, height=H, stroke_color=GREY_B, stroke_width=2).move_to([cx, ytop - H / 2, 0]),
                   Line([x0, ytop - h, 0], [x0 + W, ytop - h, 0], stroke_color=GREY_B, stroke_width=2))
    for k in range(1, n):
        marco.add(Line([x0 + k * w, ytop, 0], [x0 + k * w, ytop - H, 0], stroke_color=GREY_B, stroke_width=2))
    cab = VGroup(*[texto(c, tam, cols[k]).move_to([x0 + (k + 0.5) * w, cy, 0]) for k, c in enumerate(cabs)])
    celdas = [[celda(v, size, cols[k]).move_to([x0 + (k + 0.5) * w, cy - (r + 1) * h, 0]) for k, v in enumerate(fila)]
              for r, fila in enumerate(filas)]
    return marco, cab, celdas


def flecha_arco(xa, xb, y, etiqueta, arriba=True, color=ACENTO):
    ang = -PI / 2 if arriba else PI / 2
    arc = CurvedArrow([xa, y, 0], [xb, y, 0], angle=ang, color=color, stroke_width=3, tip_length=0.16)
    lab = MathTex(etiqueta, font_size=30, color=color).next_to(arc, UP if arriba else DOWN, buff=0.06)
    return VGroup(arc, lab)


def esquema(n1, n2, f1, f2, cx, cy, inversa=False, size=44, dx=1.25, dy=0.75):
    """Esquema de regla de tres con las flechas. Devuelve (cabeceras, filas, flechas, tipo)."""
    cabs = VGroup(texto(n1, 26, M1).move_to([cx - dx, cy, 0]), texto(n2, 26, M2).move_to([cx + dx, cy, 0]))
    filas = VGroup()
    for k, (a, b) in enumerate((f1, f2)):
        y = cy - 0.75 - k * dy
        filas.add(VGroup(celda(a, size, M1).move_to([cx - dx, y, 0]), celda(b, size, M2).move_to([cx + dx, y, 0])))
    y1, y2 = cy - 0.55, cy - 0.75 - dy - 0.2
    fl1 = Arrow([cx - dx - 0.9, y1, 0], [cx - dx - 0.9, y2, 0], buff=0, color=M1, stroke_width=5,
                max_tip_length_to_length_ratio=0.25)
    a, b = ([y1, y2] if not inversa else [y2, y1])
    fl2 = Arrow([cx + dx + 0.9, a, 0], [cx + dx + 0.9, b, 0], buff=0, color=M2, stroke_width=5,
                max_tip_length_to_length_ratio=0.25)
    tipo = texto("INVERSA" if inversa else "DIRECTA", 26, ROSA if inversa else OK).move_to([cx, y2 - 0.45, 0])
    return cabs, filas, VGroup(fl1, fl2), tipo


def encadenar(inicio, pasos, size=48):
    """inicio → (factor) → valor → ...   pasos = [(factor_tex, valor)]."""
    partes = [inicio]
    for f, v in pasos:
        partes += [f"\\xrightarrow{{\\qquad {f}\\qquad}}", v]
    m = MathTex(*partes, font_size=size)
    for i in range(1, len(partes), 2):
        m[i].set_color(ACENTO)
    return m


def rejilla_pos(filas, cols, centro, s=0.46):
    cx, cy = centro[0], centro[1]
    return [np.array([cx + (c - (cols - 1) / 2) * s, cy + ((filas - 1) / 2 - r) * s, 0])
            for r in range(filas) for c in range(cols)]


def llaves(filas, cols, centro, s, t_f, t_c, col_f=M1, col_c=M2):
    pos = rejilla_pos(filas, cols, centro, s)
    fantasmas = VGroup(*[Square(s * 0.85).move_to(p) for p in pos])
    izq = Brace(fantasmas, LEFT, buff=0.12, color=col_f)
    aba = Brace(fantasmas, DOWN, buff=0.12, color=col_c)
    li = texto(t_f, 24, col_f).next_to(izq, LEFT, buff=0.12)
    la = texto(t_c, 24, col_c).next_to(aba, DOWN, buff=0.1)
    return VGroup(izq, li, aba, la)


def barra(x0, y, ancho, alto=0.6, color=GREY_B, opacidad=0.35):
    return Rectangle(width=ancho, height=alto, stroke_color=WHITE, stroke_width=2, fill_color=color,
                     fill_opacity=opacidad).move_to([x0 + ancho / 2, y, 0])


# ---------------------------------------------------------------------------
def vaso(cx, y0, l, a, u=0.2, w=1.3, H=2.3):
    borde = VMobject(color=WHITE, stroke_width=4)
    borde.set_points_as_corners([[cx - w / 2, y0 + H, 0], [cx - w / 2, y0, 0], [cx + w / 2, y0, 0], [cx + w / 2, y0 + H, 0]])
    col = interpolate_color(ManimColor(AGUA), ManimColor(LIMON), l / (l + a))
    liq = Rectangle(width=w - 0.12, height=(l + a) * u, stroke_width=0, fill_color=col, fill_opacity=0.9)
    liq.move_to([cx, y0 + 0.05 + (l + a) * u / 2, 0])
    return borde, liq


def cubitos(l, a, cx, y, s=0.26):
    fl = VGroup(*[Square(s, stroke_width=1.5, stroke_color=WHITE, fill_color=LIMON, fill_opacity=0.95) for _ in range(l)])
    fa = VGroup(*[Square(s, stroke_width=1.5, stroke_color=WHITE, fill_color=AGUA, fill_opacity=0.95) for _ in range(a)])
    fl.arrange(RIGHT, buff=0.05)
    fa.arrange(RIGHT, buff=0.05)
    return VGroup(fl, fa).arrange(DOWN, buff=0.1).move_to([cx, y, 0])


def razon_tex(n, d, size=52):
    t = MathTex(f"\\dfrac{{{n}}}{{{d}}}", font_size=size)
    k = len(str(n))
    t[0][:k].set_color(LIMON)
    t[0][k + 1:].set_color(AGUA)
    return t


class RazonProporcion(Scene):
    def construct(self):
        cab = titulo(self, "Razón y proporción")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Razón")
        ley = VGroup(Square(0.26, fill_color=LIMON, fill_opacity=0.95, stroke_width=1.5), texto("limón", 24, LIMON),
                     Square(0.26, fill_color=AGUA, fill_opacity=0.95, stroke_width=1.5), texto("agua", 24, AGUA))
        ley.arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.45)
        self.play(FadeIn(ley))
        notas("Hacemos limonada mezclando vasos de zumo de limón y vasos de agua")
        self.wait(1)
        datos = [(-4.5, 2, 3, "Vaso A: 2 de limón y 3 de agua"),
                 (0.0, 4, 6, "Vaso B: el doble de todo, 4 de limón y 6 de agua"),
                 (4.5, 3, 3, "Vaso C: 3 de limón y 3 de agua")]
        etiquetas, liquidos = [], []
        for cx, l, a, txt in datos:
            notas(txt)
            cb = cubitos(l, a, cx, 1.95)
            borde, liq = vaso(cx, -1.25, l, a)
            self.play(Create(borde), LaggedStart(*[FadeIn(c, scale=0.5) for c in [*cb[0], *cb[1]]], lag_ratio=0.08))
            self.play(ReplacementTransform(cb, liq), run_time=1.2)
            r = razon_tex(l, a).move_to([cx, -1.95, 0])
            self.play(Write(r))
            etiquetas.append(r)
            liquidos.append(liq)
            if cx < -1:
                notas("La RAZÓN compara las dos cantidades dividiendo: 2 de limón por cada 3 de agua")
                self.wait(2.5)
        eq = MathTex("=\\dfrac{2}{3}", font_size=44, color=GREY_B).next_to(etiquetas[1], RIGHT, buff=0.15)
        self.play(Write(eq))
        s1 = MathTex("=", font_size=60, color=OK).move_to([-2.25, -1.95, 0])
        self.play(FadeIn(s1, scale=1.5), Indicate(liquidos[0], color=WHITE), Indicate(liquidos[1], color=WHITE))
        notas("¡Mismo color, mismo sabor! 4/6 = 2/3: las dos razones son iguales", color=OK)
        self.wait(3)
        eq2 = MathTex("=1", font_size=44, color=GREY_B).next_to(etiquetas[2], RIGHT, buff=0.15)
        s2 = MathTex("\\neq", font_size=60, color=MAL).move_to([2.25, -1.95, 0])
        self.play(Write(eq2), FadeIn(s2, scale=1.5))
        notas("3/3 = 1 no es 2/3: un vaso de limón por cada uno de agua. Sabe más a limón", color=MAL)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Proporción")
        p = MathTex("\\dfrac{2}{3}", "=", "\\dfrac{4}{6}", font_size=96).move_to([0, 1.1, 0])
        notas("Dos razones iguales forman una PROPORCIÓN")
        self.play(Write(p))
        self.wait(1.5)
        a_, b_, c_, d_ = p[0][0], p[0][2], p[2][0], p[2][2]
        l1 = Line(a_.get_center(), d_.get_center(), buff=0.38, color=M2, stroke_width=5)
        l2 = Line(b_.get_center(), c_.get_center(), buff=0.38, color=M1, stroke_width=5)
        notas("Multiplicamos en cruz...")
        self.play(Create(l1), a_.animate.set_color(M2), d_.animate.set_color(M2))
        pr1 = MathTex("2\\cdot 6=12", font_size=50, color=M2).move_to([-2.6, -1.0, 0])
        self.play(Write(pr1))
        self.play(Create(l2), b_.animate.set_color(M1), c_.animate.set_color(M1))
        pr2 = MathTex("3\\cdot 4=12", font_size=50, color=M1).move_to([2.6, -1.0, 0])
        self.play(Write(pr2))
        notas("...¡y los dos productos son iguales! Así se comprueba si es una proporción", color=OK)
        self.wait(2.5)
        regla = MathTex("\\dfrac{a}{b}=\\dfrac{c}{d}", "\\ \\Longleftrightarrow\\ ", "a\\cdot d=b\\cdot c", font_size=46)
        card = tarjeta(regla).move_to([0, -2.3, 0])
        self.play(Create(card[0]), Write(regla))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Un término desconocido")
        enun = texto("Con 10 vasos de limón, ¿cuánta agua necesito para que sepa igual que el vaso A?", 28)
        enun.move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        notas("Llamamos x a los vasos de agua: la razón tiene que seguir siendo 2/3")
        e = X("\\dfrac{2}{3}=\\dfrac{10}{x}", 56)
        pasos = [("2\\cdot x=3\\cdot 10", "Productos cruzados"), ("2x=30", None), ("x=\\dfrac{30}{2}=15", None)]
        cuenta(self, e, pasos, -2.0, 1.0, notas, None, True, 52, dy=1.0)
        notas("15 vasos de agua. Comprobamos: 10/15 = 2/3 ✓", color=OK)
        self.wait(3)
        notas.fin()


# ---------------------------------------------------------------------------
class ProporcionalidadDirecta(Scene):
    def construct(self):
        cab = titulo(self, "Proporcionalidad directa")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Las naranjas")
        enun = texto("En la frutería, 1 kg de naranjas cuesta 2 €", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        marco, labs, cel, (ytop, ybot) = tabla_h(["Peso (kg)", "Precio (€)"],
                                                 [["1", "2", "3", "4", "5"], ["2", "4", "6", "8", "10"]], 0, 0.9)
        self.play(Create(marco), FadeIn(labs))
        for k in range(5):
            self.play(FadeIn(cel[0][k]), FadeIn(cel[1][k]), run_time=0.45)
        notas("Si el peso se multiplica por 2...")
        xs = [c.get_center()[0] for c in cel[0]]
        a1 = flecha_arco(xs[0], xs[1], ytop + 0.05, "\\times 2", True)
        self.play(Create(a1[0]), FadeIn(a1[1]))
        notas("...el precio también se multiplica por 2")
        a2 = flecha_arco(xs[0], xs[1], ybot - 0.05, "\\times 2", False)
        self.play(Create(a2[0]), FadeIn(a2[1]))
        self.wait(1.5)
        self.play(FadeOut(a1), FadeOut(a2))
        a1 = flecha_arco(xs[1], xs[3], ytop + 0.05, "\\times 2", True)
        a2 = flecha_arco(xs[1], xs[3], ybot - 0.05, "\\times 2", False)
        self.play(Create(a1[0]), FadeIn(a1[1]), Create(a2[0]), FadeIn(a2[1]))
        self.wait(1)
        self.play(FadeOut(a1), FadeOut(a2))
        a1 = flecha_arco(xs[0], xs[2], ytop + 0.05, "\\times 3", True)
        a2 = flecha_arco(xs[0], xs[2], ybot - 0.05, "\\times 3", False)
        notas("Y si se multiplica por 3, también por 3: magnitudes DIRECTAMENTE proporcionales", color=OK)
        self.play(Create(a1[0]), FadeIn(a1[1]), Create(a2[0]), FadeIn(a2[1]))
        self.wait(3)
        self.play(FadeOut(a1), FadeOut(a2))

        sub("Constante de proporcionalidad")
        notas("Dividimos cada precio entre su peso...")
        q = MathTex("\\dfrac{2}{1}", "=", "\\dfrac{4}{2}", "=", "\\dfrac{6}{3}", "=", "\\dfrac{8}{4}", "=",
                    "\\dfrac{10}{5}", "=", "2", font_size=48).move_to([0, -1.2, 0])
        for i in range(0, 9, 2):
            q[i][0:-2].set_color(M2) if i == 8 else q[i][0].set_color(M2)
            q[i][-1].set_color(M1)
        self.play(Write(q[:9]), run_time=2)
        self.play(Write(q[9:]), q[10].animate.set_color(ACENTO))
        notas("...¡siempre sale 2! Es la constante de proporcionalidad: k = 2 (el precio de 1 kg)", color=ACENTO)
        self.wait(2.5)
        f = MathTex("\\text{precio}", "=", "2", "\\cdot", "\\text{peso}", font_size=48).move_to([0, -2.4, 0])
        f[0].set_color(M2)
        f[2].set_color(ACENTO)
        f[4].set_color(M1)
        self.play(Write(f))
        self.wait(2.5)
        notas.fin()

        sub("La gráfica")
        tabla = VGroup(marco, labs, *cel[0], *cel[1])
        self.play(FadeOut(VGroup(enun, q, f)), tabla.animate.scale(0.62).move_to([-3.6, 1.6, 0]))
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 12, 2], x_length=5.4, y_length=4.9, tips=False,
                  axis_config={"include_numbers": True, "font_size": 22, "color": GREY_B}).move_to([3.4, -0.35, 0])
        lx = texto("kg", 22, M1).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        ly = texto("€", 24, M2).next_to(ax.y_axis.get_end(), RIGHT, buff=0.22)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly))
        notas("Cada columna de la tabla es un punto: (peso, precio)")
        puntos = VGroup()
        for k in range(5):
            d = Dot(ax.c2p(k + 1, 2 * (k + 1)), color=ACENTO, radius=0.09)
            self.play(TransformFromCopy(VGroup(cel[0][k], cel[1][k]), d), run_time=0.7)
            puntos.add(d)
        rec = Line(ax.c2p(0, 0), ax.c2p(6, 12), color=M2, stroke_width=4)
        self.play(Create(rec))
        self.bring_to_front(puntos)
        o = Dot(ax.c2p(0, 0), color=OK, radius=0.11)
        notas("Los puntos están en una RECTA... ¡que pasa por el (0, 0)! 0 kg cuestan 0 €", color=OK)
        self.play(FadeIn(o, scale=2), Flash(o, color=OK))
        self.wait(3)
        notas.fin()

        sub("¿Y si no es proporcional?")
        self.play(FadeOut(VGroup(tabla, puntos, rec, o)))
        enun = texto("Un taxi cobra 3 € al subir\ny 1 € por cada km", 28).move_to([-3.5, 2.2, 0])
        self.play(FadeIn(enun))
        marco, labs, cel, _ = tabla_h(["km", "Precio (€)"], [["1", "2", "3", "4"], ["4", "5", "6", "7"]],
                                      -3.5, 1.2, w=0.9, wn=1.9, size=36)
        self.play(Create(marco), FadeIn(labs), *[FadeIn(c) for c in cel[0] + cel[1]])
        q = MathTex("\\dfrac{4}{1}=4", ",\\quad", "\\dfrac{5}{2}=2{,}5", ",\\quad", "\\dfrac{6}{3}=2",
                    font_size=40).move_to([-3.5, -0.6, 0])
        notas("Dividimos: 4, 2,5, 2... ¡no sale siempre lo mismo!")
        self.play(Write(q))
        self.wait(1.5)
        mal = texto("2 km no cuestan el doble que 1 km", 26, MAL).move_to([-3.5, -1.6, 0])
        self.play(FadeIn(mal))
        pts = VGroup(*[Dot(ax.c2p(k, 3 + k), color=MAL, radius=0.09) for k in range(1, 5)])
        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in pts], lag_ratio=0.2))
        r2 = Line(ax.c2p(0, 3), ax.c2p(6, 9), color=MAL, stroke_width=4)
        self.play(Create(r2))
        self.bring_to_front(pts)
        notas("Es una recta, pero NO pasa por el (0, 0): no es proporcional", color=MAL)
        self.wait(3.5)
        notas.fin()


# ---------------------------------------------------------------------------
class ProporcionalidadInversa(Scene):
    def construct(self):
        cab = titulo(self, "Proporcionalidad inversa")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Rectángulos de área 12")
        ax = Axes(x_range=[0, 13, 1], y_range=[0, 13, 1], x_length=5.4, y_length=5.0, tips=False,
                  axis_config={"include_numbers": True, "font_size": 20, "color": GREY_B,
                               "numbers_to_include": [2, 4, 6, 8, 10, 12]}).move_to([3.5, -0.35, 0])
        lx = texto("base", 22, M1).next_to(ax.x_axis.get_end(), DOWN, buff=0.3)
        ly = texto("altura", 22, M2).next_to(ax.y_axis.get_end(), RIGHT, buff=0.22)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly))
        cabs = VGroup(texto("base", 24, M1).move_to([-6.1, 1.95, 0]), texto("altura", 24, M2).move_to([-4.85, 1.95, 0]),
                      texto("base · altura", 24).move_to([-2.75, 1.95, 0]))
        raya = Line([-6.7, 1.68, 0], [-1.85, 1.68, 0], color=GREY_B, stroke_width=2)
        self.play(FadeIn(cabs), Create(raya))
        b = ValueTracker(1)
        rect = always_redraw(lambda: Polygon(
            ax.c2p(0, 0), ax.c2p(b.get_value(), 0), ax.c2p(b.get_value(), 12 / b.get_value()),
            ax.c2p(0, 12 / b.get_value()), stroke_color=M1, stroke_width=3, fill_color=M1, fill_opacity=0.25))
        punto = always_redraw(lambda: Dot(ax.c2p(b.get_value(), 12 / b.get_value()), color=ACENTO, radius=0.09))
        notas("Todos estos rectángulos tienen área 12. Empezamos con base 1 y altura 12")
        self.play(FadeIn(rect), FadeIn(punto))
        rastro = TracedPath(punto.get_center, stroke_color=ACENTO, stroke_width=4)
        self.add(rastro)
        filas = VGroup()

        def fila(base, k):
            alt = 12 // base
            y = 1.3 - k * 0.55
            f = VGroup(MathTex(str(base), font_size=36, color=M1).move_to([-6.1, y, 0]),
                       MathTex(str(alt), font_size=36, color=M2).move_to([-4.85, y, 0]),
                       MathTex(f"{base}\\cdot {alt}=12", font_size=34).move_to([-2.75, y, 0]))
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.6)
            filas.add(f)

        fila(1, 0)
        notas("Si la base crece, la altura tiene que bajar para que el área siga siendo 12")
        for k, base in enumerate([2, 3, 4, 6, 12], start=1):
            self.play(b.animate.set_value(base), run_time=1.6)
            fila(base, k)
        self.wait(1)
        fx = [f[0].get_center() for f in filas]
        fa = [f[1].get_center() for f in filas]
        g1 = CurvedArrow(fx[0] + LEFT * 0.35, fx[1] + LEFT * 0.35, angle=PI / 2, color=ACENTO, stroke_width=3,
                         tip_length=0.14)
        t1 = MathTex("\\times 2", font_size=28, color=ACENTO).next_to(g1, LEFT, buff=0.05)
        g2 = CurvedArrow(fa[0] + RIGHT * 0.4, fa[1] + RIGHT * 0.4, angle=-PI / 2, color=ACENTO, stroke_width=3,
                         tip_length=0.14)
        t2 = MathTex(":2", font_size=28, color=ACENTO).next_to(g2, RIGHT, buff=0.05)
        notas("Si la base se multiplica por 2, la altura se DIVIDE entre 2: proporcionalidad INVERSA", color=OK)
        self.play(Create(g1), FadeIn(t1))
        self.play(Create(g2), FadeIn(t2))
        self.wait(2.5)
        self.play(b.animate.set_value(3), run_time=1.5)
        notas("El producto siempre es el mismo (12). Y los puntos no forman una recta: forman una CURVA", color=ACENTO)
        self.play(Indicate(VGroup(*[f[2] for f in filas]), color=ACENTO))
        self.wait(3.5)
        notas.fin()
        rastro.clear_updaters()
        rect.clear_updaters()
        punto.clear_updaters()
        limpiar(self, cab)
        sub.olvidar()

        sub("Pintores y días")
        enun = texto("2 pintores tardan 6 días en pintar una casa", 28).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        centro, s = (2.6, 0.1, 0), 0.46
        pos = rejilla_pos(2, 6, centro, s)
        bloques = VGroup(*[Square(s * 0.85, stroke_width=1.5, stroke_color=WHITE, fill_color=TRAB, fill_opacity=0.75)
                           .move_to(p) for p in pos])
        ll = llaves(2, 6, centro, s, "2 pintores", "6 días")
        notas("Cada cuadrado es el trabajo de un pintor en un día: en total, 2 · 6 = 12")
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in bloques], lag_ratio=0.05))
        self.play(FadeIn(ll))
        cab_t = VGroup(texto("pintores", 24, M1).move_to([-5.9, 1.4, 0]), texto("días", 24, M2).move_to([-4.6, 1.4, 0]))
        raya = Line([-6.6, 1.13, 0], [-2.4, 1.13, 0], color=GREY_B, stroke_width=2)
        self.play(FadeIn(cab_t), Create(raya))
        tfilas = VGroup()

        def fila_p(p, d, k):
            y = 0.75 - k * 0.55
            f = VGroup(MathTex(str(p), font_size=36, color=M1).move_to([-5.9, y, 0]),
                       MathTex(str(d), font_size=36, color=M2).move_to([-4.6, y, 0]),
                       MathTex(f"{p}\\cdot {d}=12", font_size=32, color=GREY_B).move_to([-3.2, y, 0]))
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.6)
            tfilas.add(f)

        fila_p(2, 6, 0)
        for k, (p, d, txt) in enumerate([(4, 3, "Con el doble de pintores, la mitad de días"),
                                         (3, 4, "Con 3 pintores, 4 días"),
                                         (1, 12, "Un pintor solo tarda 12 días")], start=1):
            notas(txt)
            pos = rejilla_pos(p, d, centro, s)
            nl = llaves(p, d, centro, s, f"{p} pintor" + ("es" if p > 1 else ""), f"{d} días")
            self.play(*[q.animate.move_to(pp) for q, pp in zip(bloques, pos)], Transform(ll, nl), run_time=1.4)
            fila_p(p, d, k)
            self.wait(1)
        notas("El trabajo total no cambia: pintores · días = 12 siempre", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Directa frente a inversa")
        cd = VGroup(texto("DIRECTA", 30, OK), texto("Una × 2  →  la otra × 2", 26), MathTex("\\dfrac{y}{x}=k", font_size=44),
                    texto("Recta que pasa por (0, 0)", 26)).arrange(DOWN, buff=0.35)
        ci = VGroup(texto("INVERSA", 30, ROSA), texto("Una × 2  →  la otra : 2", 26), MathTex("x\\cdot y=k", font_size=44),
                    texto("Curva", 26)).arrange(DOWN, buff=0.35)
        t1 = tarjeta(cd, color=OK, buff=0.4).move_to([-3.3, 0.1, 0])
        t2 = tarjeta(ci, color=ROSA, buff=0.4).move_to([3.3, 0.1, 0])
        t2[0].stretch_to_fit_height(t1[0].height).move_to([3.3, 0.1, 0])
        self.play(Create(t1[0]), Create(t2[0]))
        for a, c in zip(cd, ci):
            self.play(FadeIn(a, shift=UP * 0.15), FadeIn(c, shift=UP * 0.15), run_time=0.7)
            self.wait(0.8)
        notas("En la directa se mantiene el COCIENTE; en la inversa, el PRODUCTO")
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
class ReglaDeTres(Scene):
    def construct(self):
        cab = titulo(self, "Regla de tres", "Problemas de proporcionalidad")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Directa")
        enun = texto("3 kg de manzanas cuestan 4,50 €. ¿Cuánto cuestan 5 kg?", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        cabs, filas, fl, tipo = esquema("kg", "€", ("3", "4{,}50"), ("5", "x"), -4.2, 1.4)
        self.play(FadeIn(cabs), FadeIn(filas[0]))
        self.play(FadeIn(filas[1]))
        notas("¿Más kilos → más euros? Sí: las dos flechas van en el MISMO sentido")
        self.play(GrowArrow(fl[0]))
        self.play(GrowArrow(fl[1]))
        self.play(FadeIn(tipo, scale=1.3))
        self.wait(1.5)
        e = X("\\dfrac{3}{5}=\\dfrac{4{,}50}{x}", 50)
        pasos = [("3\\cdot x=5\\cdot 4{,}50", "Productos cruzados"), ("3x=22{,}5", None), ("x=\\dfrac{22{,}5}{3}=7{,}50", None)]
        notas("Escribimos la proporción tal como está en el esquema")
        g = cuenta(self, e, pasos, 0.0, 1.2, notas, None, True, 46, dy=0.95)
        notas("5 kg cuestan 7,50 €", color=OK)
        self.wait(2.5)
        self.play(FadeOut(g))
        notas("Otra forma: REDUCCIÓN A LA UNIDAD (¿cuánto cuesta 1 kg?)")
        u = VGroup(texto("1 kg  →  4,50 : 3 = 1,50 €", 32), texto("5 kg  →  1,50 · 5 = 7,50 €", 32))
        u.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.3, 0.6, 0])
        self.play(FadeIn(u[0], shift=RIGHT * 0.2))
        self.wait(1.5)
        self.play(FadeIn(u[1], shift=RIGHT * 0.2))
        self.play(Circumscribe(u[1], color=ACENTO))
        notas("¡El mismo resultado! Usa el método que te resulte más cómodo", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Inversa")
        enun = texto("4 grifos llenan un depósito en 6 horas. ¿Cuánto tardan 3 grifos?", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        cabs, filas, fl, tipo = esquema("grifos", "horas", ("4", "6"), ("3", "x"), -4.2, 1.4, inversa=True)
        self.play(FadeIn(cabs), FadeIn(filas[0]))
        self.play(FadeIn(filas[1]))
        notas("Menos grifos → ¿menos horas? ¡No! MÁS horas: flechas en sentido CONTRARIO")
        self.play(GrowArrow(fl[0]))
        self.play(GrowArrow(fl[1]))
        self.play(FadeIn(tipo, scale=1.3))
        self.wait(1.5)
        e = X("4\\cdot 6=3\\cdot x", 50)
        pasos = [("24=3x", None), ("x=\\dfrac{24}{3}=8", None)]
        notas("En la inversa se mantiene el PRODUCTO: grifos · horas")
        g = cuenta(self, e, pasos, 0.0, 1.2, notas, None, True, 48, dy=0.95)
        notas("3 grifos tardan 8 horas", color=OK)
        self.wait(2.5)
        self.play(FadeOut(g))
        notas("Reducción a la unidad: ¿cuánto tardaría 1 grifo solo?")
        u = VGroup(texto("1 grifo  →  6 · 4 = 24 horas", 32), texto("3 grifos  →  24 : 3 = 8 horas", 32))
        u.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.3, 0.6, 0])
        self.play(FadeIn(u[0], shift=RIGHT * 0.2))
        notas("Un grifo solo tarda 4 veces más: 24 horas")
        self.wait(1.5)
        self.play(FadeIn(u[1], shift=RIGHT * 0.2))
        self.play(Circumscribe(u[1], color=ACENTO))
        notas("Con 3 grifos, la tercera parte: 8 horas", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("¿Directa o inversa?")
        pasos_t = VGroup(texto("Pregúntate: si una magnitud AUMENTA, ¿qué hace la otra?", 30),
                         texto("Aumenta también  →  DIRECTA  (flechas en el mismo sentido)", 28, OK),
                         texto("Disminuye  →  INVERSA  (flechas en sentido contrario)", 28, ROSA),
                         texto("¡Cuidado! No todo es proporcional: la edad y la altura de una persona", 28, MAL))
        pasos_t.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        card = tarjeta(pasos_t, buff=0.4).move_to([0, 0.2, 0])
        self.play(Create(card[0]))
        for m in pasos_t:
            self.play(FadeIn(m, shift=RIGHT * 0.2))
            self.wait(1.4)
        self.wait(3)


# ---------------------------------------------------------------------------
class ProporcionalidadCompuesta(Scene):
    def construct(self):
        cab = titulo(self, "Proporcionalidad compuesta", "Tres magnitudes a la vez")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Obreros, días y metros")
        enun = texto("5 obreros construyen 100 m de muro en 4 días.\n¿Cuántos metros construirán 3 obreros en 6 días?", 28)
        enun.move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        centro, s = (3.3, -0.4, 0), 0.5
        pos = rejilla_pos(5, 4, centro, s)
        bloques = VGroup(*[Square(s * 0.85, stroke_width=1.5, stroke_color=WHITE, fill_color=M3, fill_opacity=0.6)
                           .move_to(p) for p in pos])
        ll = llaves(5, 4, centro, s, "5 obreros", "4 días")
        notas("Cada cuadrado: un obrero trabajando un día")
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in bloques], lag_ratio=0.04), FadeIn(ll))
        lin = [texto("5 · 4 = 20 cuadrados  →  100 m", 30),
               texto("1 cuadrado  →  100 : 20 = 5 m", 30),
               texto("3 · 6 = 18 cuadrados", 30),
               texto("18 · 5 = 90 m", 34, ACENTO)]
        for k, m in enumerate(lin):
            m.move_to([-6.4, 0.9 - k * 0.75, 0], aligned_edge=LEFT)
        self.play(FadeIn(lin[0]))
        self.wait(1)
        notas("Entre los 20 hacen 100 m: cada cuadrado son 5 m")
        self.play(FadeIn(lin[1]))
        self.wait(2)
        notas("Ahora: 3 obreros durante 6 días")
        pos2 = rejilla_pos(3, 6, centro, s)
        nl = llaves(3, 6, centro, s, "3 obreros", "6 días")
        self.play(*[q.animate.move_to(p) for q, p in zip(bloques[:18], pos2)],
                  *[FadeOut(q, scale=0.3) for q in bloques[18:]], Transform(ll, nl), run_time=1.6)
        self.play(FadeIn(lin[2]))
        self.wait(1)
        self.play(FadeIn(lin[3]), Create(SurroundingRectangle(lin[3], color=ACENTO, buff=0.12)))
        notas("Construirán 90 m de muro", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Con la tabla")
        marco, cabs, cel = tabla_v(["obreros", "días", "metros"], [["5", "4", "100"], ["3", "6", "x"]], -3.7, 1.9,
                                   (M1, M2, M3), w=1.8)
        self.play(Create(marco), FadeIn(cabs), *[FadeIn(c) for c in cel[0] + cel[1]])
        notas("Comparamos cada magnitud con la que buscamos (metros)")
        tipos = VGroup(texto("menos obreros → menos metros: DIRECTA", 24, OK),
                       texto("más días → más metros: DIRECTA", 24, OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        tipos.move_to([3.5, 1.4, 0])
        self.play(FadeIn(tipos[0]))
        self.play(FadeIn(tipos[1]))
        self.wait(1.5)
        c = encadenar("100", [("\\cdot\\dfrac{3}{5}", "60"), ("\\cdot\\dfrac{6}{4}", "90")], 54).move_to([0, -0.7, 0])
        notas("Primero cambiamos los obreros (5 → 3) y luego los días (4 → 6)")
        self.play(Write(c[0]))
        self.play(Write(c[1]), Write(c[2]))
        e1 = texto("obreros: 5 → 3", 22, M1).next_to(c[1], DOWN, buff=0.25)
        self.play(FadeIn(e1))
        self.wait(1)
        self.play(Write(c[3]), Write(c[4]))
        e2 = texto("días: 4 → 6", 22, M2).next_to(c[3], DOWN, buff=0.25)
        self.play(FadeIn(e2))
        self.play(Circumscribe(c[4], color=ACENTO))
        notas("90 m: lo mismo que con los cuadrados", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Con una inversa")
        enun = texto("4 máquinas fabrican 600 piezas en 6 horas.\n¿Cuántas horas tardarán 8 máquinas en fabricar 1000 piezas?", 28)
        enun.move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        marco, cabs, cel = tabla_v(["máquinas", "piezas", "horas"], [["4", "600", "6"], ["8", "1000", "x"]], -3.7, 1.0,
                                   (M1, M3, M2), w=1.8)
        self.play(Create(marco), FadeIn(cabs), *[FadeIn(c) for c in cel[0] + cel[1]])
        tipos = VGroup(texto("más máquinas → menos horas: INVERSA", 24, ROSA),
                       texto("más piezas → más horas: DIRECTA", 24, OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        tipos.move_to([3.5, 0.5, 0])
        notas("Ahora una de las dos es INVERSA")
        self.play(FadeIn(tipos[0]))
        self.play(FadeIn(tipos[1]))
        self.wait(1.5)
        c = encadenar("6", [("\\cdot\\dfrac{4}{8}", "3"), ("\\cdot\\dfrac{1000}{600}", "5")], 54).move_to([0, -1.4, 0])
        notas("Inversa: la fracción va DADA LA VUELTA (4/8): el doble de máquinas, la mitad de horas")
        self.play(Write(c[0]))
        self.play(Write(c[1]), Write(c[2]))
        e1 = texto("máquinas: 4 → 8", 22, M1).next_to(c[1], DOWN, buff=0.25)
        self.play(FadeIn(e1))
        self.wait(2)
        notas("Directa: más piezas, más horas (1000/600)")
        self.play(Write(c[3]), Write(c[4]))
        e2 = texto("piezas: 600 → 1000", 22, M3).next_to(c[3], DOWN, buff=0.25)
        self.play(FadeIn(e2))
        self.play(Circumscribe(c[4], color=ACENTO))
        notas("Tardarán 5 horas", color=OK)
        self.wait(3)
        notas.fin()


# ---------------------------------------------------------------------------
def cuadricula100(centro, s=0.3, g=0.05):
    cs = VGroup(*[Square(s, stroke_width=1, stroke_color=GREY_B, fill_color=VACIO, fill_opacity=1) for _ in range(100)])
    return cs.arrange_in_grid(rows=10, cols=10, buff=g).move_to(centro)


class Porcentajes(Scene):
    def construct(self):
        cab = titulo(self, "Porcentajes")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("¿Qué es un porcentaje?")
        cg = cuadricula100([-3.4, -0.2, 0])
        self.play(LaggedStart(*[FadeIn(q) for q in cg], lag_ratio=0.01))
        notas("Una cuadrícula de 100 cuadraditos. Pintamos 35...")
        self.play(LaggedStart(*[cg[k].animate.set_fill(PCT) for k in range(35)], lag_ratio=0.03))
        r = VGroup(MathTex("35\\,\\%", font_size=80, color=PCT), texto("35 de cada 100", 28),
                   MathTex("=\\dfrac{35}{100}", font_size=56), MathTex("=0{,}35", font_size=56))
        r.arrange(DOWN, buff=0.35).move_to([2.8, -0.1, 0])
        for m in r:
            self.play(FadeIn(m, shift=LEFT * 0.2))
            self.wait(0.6)
        notas("Un porcentaje es una fracción de denominador 100: también se escribe como decimal")
        self.wait(3)
        casos = [(lambda k: k % 10 < 5, "50\\,\\%=\\dfrac{1}{2}", "la mitad"),
                 (lambda k: k % 10 < 5 and k // 10 < 5, "25\\,\\%=\\dfrac{1}{4}", "la cuarta parte"),
                 (lambda k: k % 10 == 0, "10\\,\\%=\\dfrac{1}{10}", "la décima parte")]
        self.play(FadeOut(r))
        prev = None
        for cond, tex, txt in casos:
            m = VGroup(MathTex(tex, font_size=60, color=PCT), texto(txt, 30)).arrange(DOWN, buff=0.3).move_to([2.8, 0, 0])
            anims = [cg[k].animate.set_fill(PCT if cond(k) else VACIO) for k in range(100)]
            self.play(*anims, *([FadeOut(prev)] if prev else []), run_time=0.9)
            self.play(FadeIn(m))
            self.wait(2)
            prev = m
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("El % de una cantidad")
        enun = texto("Calcula el 35 % de 240", 32).move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        x0, y, W = -4.5, 0.7, 9.0
        total = barra(x0, y, W)
        parte = barra(x0, y, W * 0.35, color=PCT, opacidad=0.85)
        t100 = MathTex("100\\,\\%", font_size=32, color=GREY_B).next_to(total, DOWN, buff=0.15).align_to(total, RIGHT)
        tt = MathTex("240", font_size=40).next_to(total, UP, buff=0.15).align_to(total, RIGHT)
        self.play(Create(total), FadeIn(t100), FadeIn(tt))
        notas("La barra entera (100 %) son 240")
        self.wait(1)
        t35 = MathTex("35\\,\\%", font_size=32, color=PCT).next_to(parte, DOWN, buff=0.15)
        tx = MathTex("?", font_size=40, color=LETRA).next_to(parte, UP, buff=0.15)
        self.play(GrowFromEdge(parte, LEFT), FadeIn(t35), FadeIn(tx))
        e = MathTex("35\\,\\%\\ \\text{de}\\ 240", "=", "0{,}35\\cdot 240", "=", "84", font_size=50).move_to([0, -1.2, 0])
        e[0][:3].set_color(PCT)
        notas("Pasamos el porcentaje a decimal (35 % = 0,35) y multiplicamos")
        self.play(Write(e[:3]))
        self.wait(1)
        self.play(Write(e[3:]))
        t84 = MathTex("84", font_size=40, color=LETRA).move_to(tx)
        self.play(Transform(tx, t84), Circumscribe(e[4], color=ACENTO))
        notas("El 35 % de 240 es 84", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Calcular el total")
        enun = texto("El 20 % de un número es 30. ¿Cuál es el número?", 32).move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        x0, y, W = -4.5, 0.7, 9.0
        trozos = VGroup(*[barra(x0 + k * W / 5, y, W / 5) for k in range(5)])
        self.play(Create(trozos))
        notas("Partimos la barra en 5 trozos: cada trozo es el 20 %")
        self.play(trozos[0].animate.set_fill(PCT, 0.85))
        ets = VGroup(*[MathTex("20\\,\\%", font_size=28, color=PCT if k == 0 else GREY_B).next_to(trozos[k], DOWN, buff=0.12)
                       for k in range(5)])
        vs = VGroup(*[MathTex("30", font_size=36, color=PCT if k == 0 else WHITE).next_to(trozos[k], UP, buff=0.12)
                      for k in range(5)])
        self.play(FadeIn(ets[0]), FadeIn(vs[0]))
        self.wait(1)
        notas("Si un trozo son 30, los 5 trozos son...")
        self.play(LaggedStart(*[FadeIn(v) for v in vs[1:]], *[FadeIn(t) for t in ets[1:]], lag_ratio=0.2))
        tot = MathTex("5\\cdot 30=150", font_size=50, color=ACENTO).move_to([0, -0.6, 0])
        self.play(Write(tot))
        self.wait(1.5)
        e = X("0{,}20\\cdot x=30\\ \\ \\Rightarrow\\ \\ x=\\dfrac{30}{0{,}20}=150", 46).move_to([0, -1.9, 0])
        notas("Con una ecuación: el 20 % de x es 30")
        self.play(Write(e))
        notas("El número es 150. Comprobamos: 0,20 · 150 = 30 ✓", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("¿Qué porcentaje es?")
        enun = texto("En una clase de 24 alumnos aprueban 18. ¿Qué porcentaje aprueba?", 30).move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        x0, y, W = -4.8, 0.7, 9.6
        cel = VGroup(*[barra(x0 + k * W / 24, y, W / 24) for k in range(24)])
        self.play(Create(cel), run_time=1.2)
        notas("24 alumnos: 18 aprueban")
        self.play(LaggedStart(*[cel[k].animate.set_fill(PCT, 0.85) for k in range(18)], lag_ratio=0.05))
        marcas = VGroup(*[MathTex(f"{p}\\,\\%", font_size=26, color=GREY_B).move_to([x0 + W * p / 100, y - 0.6, 0])
                          for p in (0, 25, 50, 75, 100)])
        rayas = VGroup(*[Line([x0 + W * p / 100, y - 0.38, 0], [x0 + W * p / 100, y + 0.38, 0], color=WHITE, stroke_width=3)
                         for p in (25, 50, 75)])
        self.play(FadeIn(marcas), Create(rayas))
        notas("Se ve que son 3 de cada 4... calculémoslo")
        e = MathTex("\\dfrac{18}{24}", "=", "0{,}75", "=", "75\\,\\%", font_size=56).move_to([0, -1.2, 0])
        e[4].set_color(PCT)
        self.play(Write(e[:3]))
        notas("Dividimos la parte entre el total y lo pasamos a porcentaje (× 100)")
        self.wait(1.5)
        self.play(Write(e[3:]))
        self.play(Indicate(marcas[3], color=PCT), Circumscribe(e[4], color=ACENTO))
        notas("Aprueba el 75 % de la clase", color=OK)
        self.wait(3)
        notas.fin()


# ---------------------------------------------------------------------------
class AumentosDisminuciones(Scene):
    def construct(self):
        cab = titulo(self, "Aumentos y disminuciones", "Porcentajes")
        notas = Notas(self)
        sub = Sub(self, cab)
        U = 0.065                          # ancho por euro

        sub("Aumentos")
        enun = texto("Un abrigo de 80 € sube un 15 %. ¿Cuánto cuesta ahora?", 30).move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        x0, y = -5.2, 0.45
        b = barra(x0, y, 80 * U, alto=0.7)
        tb = texto("80 €", 26).move_to(b)
        t100 = MathTex("100\\,\\%", font_size=30, color=GREY_B).next_to(b, DOWN, buff=0.15)
        self.play(Create(b), FadeIn(tb), FadeIn(t100))
        ex = barra(x0 + 80 * U, y, 12 * U, alto=0.7, color=PCT, opacidad=0.85)
        t15 = MathTex("+15\\,\\%", font_size=30, color=PCT).next_to(ex, DOWN, buff=0.15)
        notas("Al precio (el 100 %) le añadimos un 15 % más")
        self.play(GrowFromEdge(ex, LEFT), FadeIn(t15))
        br = Brace(VGroup(b, ex), UP, buff=0.1, color=ACENTO)
        t115 = MathTex("115\\,\\%=1{,}15", font_size=34, color=ACENTO).next_to(br, UP, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(t115))
        notas("El precio nuevo es el 115 % del antiguo: multiplicamos por 1,15")
        self.wait(2)
        e = MathTex("80\\cdot 1{,}15", "=", "92", font_size=56).move_to([0, -0.8, 0])
        self.play(Write(e))
        iv = texto("Índice de variación:  1 + 0,15 = 1,15", 28, ACENTO).move_to([0, -1.9, 0])
        self.play(FadeIn(iv))
        notas("Ahora cuesta 92 €", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Disminuciones")
        enun = texto("Unas zapatillas de 60 € tienen un 25 % de descuento. ¿Cuánto pago?", 30).move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        x0, W = -4.5, 8.0
        queda = barra(x0, y, W * 0.75, alto=0.7, color=PCT, opacidad=0.6)
        quita = barra(x0 + W * 0.75, y, W * 0.25, alto=0.7, color=PCT, opacidad=0.6)
        entera = barra(x0, y, W, alto=0.7, color=PCT, opacidad=0.6)
        tt = texto("60 €", 26).move_to(entera)
        t100 = MathTex("100\\,\\%", font_size=30, color=GREY_B).next_to(entera, DOWN, buff=0.15)
        self.play(Create(entera), FadeIn(tt), FadeIn(t100))
        notas("El precio entero es el 100 %. Nos quitan el 25 %...")
        self.wait(1)
        self.remove(entera)
        self.add(queda, quita)
        self.bring_to_front(tt)
        self.play(quita.animate.set_fill(MAL, 0.8))
        t25 = MathTex("-25\\,\\%", font_size=30, color=MAL).next_to(quita, UP, buff=0.15)
        self.play(FadeIn(t25))
        self.play(FadeOut(VGroup(quita, t25), shift=RIGHT * 1.5), FadeOut(t100), FadeOut(tt))
        t75 = MathTex("75\\,\\%=0{,}75", font_size=34, color=PCT).next_to(queda, DOWN, buff=0.15)
        self.play(FadeIn(t75))
        notas("...y pagamos el 75 % que queda: multiplicamos por 0,75")
        self.wait(2)
        e = MathTex("60\\cdot 0{,}75", "=", "45", font_size=56).move_to([0, -0.8, 0])
        self.play(Write(e))
        iv = texto("Índice de variación:  1 − 0,25 = 0,75", 28, ACENTO).move_to([0, -1.9, 0])
        self.play(FadeIn(iv))
        notas("Pago 45 €", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Hacia atrás")
        enun = texto("Tras subir un 20 %, un juego cuesta 54 €. ¿Cuánto costaba antes?", 30).move_to([0, 2.3, 0])
        self.play(FadeIn(enun))
        x0, W = -4.8, 7.5
        b100 = barra(x0, y, W, alto=0.7)
        b20 = barra(x0 + W, y, W * 0.2, alto=0.7, color=PCT, opacidad=0.85)
        br = Brace(VGroup(b100, b20), UP, buff=0.1, color=ACENTO)
        t54 = texto("54 € = 120 %", 26, ACENTO).next_to(br, UP, buff=0.1)
        tq = MathTex("x", "\\ (100\\,\\%)", font_size=36).move_to(b100)
        tq[0].set_color(LETRA)
        self.play(Create(b100), Create(b20), GrowFromCenter(br), FadeIn(t54), FadeIn(tq))
        notas("Los 54 € ya son el 120 % del precio de antes")
        self.wait(2)
        e = X("x\\cdot 1{,}20=54\\ \\ \\Rightarrow\\ \\ x=\\dfrac{54}{1{,}20}=45", 50).move_to([0, -0.7, 0])
        self.play(Write(e))
        notas("Antes costaba 45 €. Comprobamos: 45 · 1,20 = 54 ✓", color=OK)
        self.wait(2.5)
        mal = VGroup(texto("¡Error típico! Quitar el 20 % a 54:", 26, MAL), MathTex("54\\cdot 0{,}80=43{,}20", font_size=40, color=MAL),
                     MathTex("\\times", font_size=50, color=MAL)).arrange(RIGHT, buff=0.3).move_to([0, -2.0, 0])
        self.play(FadeIn(mal))
        notas("El 20 % se calculó sobre el precio de ANTES, no sobre 54", color=MAL)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Uno detrás de otro")
        enun = texto("Una bici de 200 €: ¿sube un 20 % y baja un 20 %, o al revés?", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        U = 0.02
        cols = [(-6.4, "Sube 20 % y baja 20 %", [(200, None, "200 €"), (240, "\\cdot 1{,}20", "240 €"),
                                                 (192, "\\cdot 0{,}80", "192 €")], "1{,}20\\cdot 0{,}80=0{,}96"),
                (0.6, "Baja 20 % y sube 20 %", [(200, None, "200 €"), (160, "\\cdot 0{,}80", "160 €"),
                                                (192, "\\cdot 1{,}20", "192 €")], "0{,}80\\cdot 1{,}20=0{,}96")]
        notas_c = ["Primero sube: 200 · 1,20 = 240. Luego baja el 20 % de 240...",
                   "Ahora al revés: primero baja a 160 y luego sube el 20 % de 160..."]
        finales, cuentas = [], []
        for c, (x0, tit, datos, tex) in enumerate(cols):
            notas(notas_c[c])
            ti = texto(tit, 26, ACENTO).move_to([x0, 1.65, 0], aligned_edge=LEFT)
            self.play(FadeIn(ti))
            prev = None
            for k, (v, f, t) in enumerate(datos):
                yy = 0.95 - k * 0.85
                col = GREY_B if k == 0 else (PCT if v >= (prev_v if prev else 0) else MAL)
                bb = barra(x0, yy, v * U, alto=0.55, color=col, opacidad=0.6)
                tt = texto(t, 24).move_to(bb)
                if f:
                    ff = MathTex(f, font_size=32, color=ACENTO).next_to(bb, RIGHT, buff=0.2)
                    self.play(TransformFromCopy(prev, bb), FadeIn(tt), FadeIn(ff))
                else:
                    self.play(Create(bb), FadeIn(tt))
                prev, prev_v = bb, v
                self.wait(0.6)
            finales.append(VGroup(bb, tt))
            m = MathTex(tex, font_size=38).move_to([x0 + 2.4, -1.75, 0])
            self.play(Write(m))
            cuentas.append(m)
            self.wait(1)
        self.play(*[Circumscribe(f, color=ACENTO) for f in finales])
        notas("¡Los dos acaban en 192 €! No vuelve a 200: subir y bajar un 20 % hace perder un 4 %", color=ACENTO)
        self.wait(3.5)
        notas("Y el orden da igual: los índices se MULTIPLICAN, y 1,20 · 0,80 = 0,80 · 1,20 = 0,96", color=OK)
        self.wait(4)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Volver al precio de antes")
        enun = texto("¿Por cuánto multiplico para volver a 200 €?", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        U = 0.02
        casos = [(-6.4, [(200, None, "200 €"), (240, "\\cdot 1{,}20", "240 €"), (200, "\\cdot\\dfrac{5}{6}", "200 €")],
                  "1{,}20=\\dfrac{6}{5}", "\\dfrac{6}{5}\\cdot\\dfrac{5}{6}=1",
                  "Subir un 20 % es multiplicar por 1,20 = 6/5. Para deshacerlo, la fracción dada la vuelta: 5/6"),
                 (0.6, [(200, None, "200 €"), (160, "\\cdot 0{,}80", "160 €"), (200, "\\cdot\\dfrac{5}{4}", "200 €")],
                  "0{,}80=\\dfrac{4}{5}", "\\dfrac{4}{5}\\cdot\\dfrac{5}{4}=1",
                  "Bajar un 20 % es multiplicar por 0,80 = 4/5. Para deshacerlo: por 5/4")]
        for x0, datos, frac_tex, prod_tex, nota in casos:
            prev = None
            for k, (v, f, t) in enumerate(datos):
                yy = 1.45 - k * 0.95
                col = GREY_B if k == 0 else (PCT if v >= prev_v else MAL)
                bb = barra(x0, yy, v * U, alto=0.55, color=col, opacidad=0.6)
                tt = texto(t, 24).move_to(bb)
                if f:
                    ff = MathTex(f, font_size=34, color=ACENTO).next_to(bb, RIGHT, buff=0.2)
                    if k == 2:
                        fr = MathTex(frac_tex, font_size=36).move_to([x0 + 2.4, -1.35, 0])
                        notas(nota)
                        self.play(Write(fr))
                        self.wait(1.5)
                    self.play(TransformFromCopy(prev, bb), FadeIn(tt), FadeIn(ff))
                else:
                    self.play(Create(bb), FadeIn(tt))
                prev, prev_v = bb, v
                self.wait(0.6)
            p = MathTex(prod_tex, font_size=36, color=OK).move_to([x0 + 2.4, -2.35, 0])
            self.play(Write(p))
            self.wait(2)
        notas("¡Ojo! Deshacer una subida del 20 % es BAJAR un 16,7 % (5/6 = 0,833...)", color=ACENTO)
        self.wait(3.5)
        notas("Y deshacer una bajada del 20 % es SUBIR un 25 % (5/4 = 1,25)", color=ACENTO)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Resumen")
        r = VGroup(MathTex("\\text{Aumento del } r\\,\\%", "\\ \\rightarrow\\ ", "\\cdot\\left(1+\\dfrac{r}{100}\\right)", font_size=44),
                   MathTex("\\text{Disminuci\\'on del } r\\,\\%", "\\ \\rightarrow\\ ", "\\cdot\\left(1-\\dfrac{r}{100}\\right)", font_size=44),
                   MathTex("\\text{Encadenados}", "\\ \\rightarrow\\ ", "\\text{se multiplican los \\'{\\i}ndices}", font_size=44))
        r[0][2].set_color(PCT)
        r[1][2].set_color(MAL)
        r[2][2].set_color(ACENTO)
        r.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        card = tarjeta(r, buff=0.4).move_to([0, 0.2, 0])
        self.play(Create(card[0]))
        for m in r:
            self.play(FadeIn(m, shift=RIGHT * 0.2))
            self.wait(1.3)
        self.wait(3)


# ---------------------------------------------------------------------------
class InteresSimple(Scene):
    def construct(self):
        cab = titulo(self, "Interés simple", "Aprende +")
        notas = Notas(self)
        sub = Sub(self, cab)

        sub("Una cuenta de ahorro")
        enun = texto("Dejo 1000 € en el banco al 3 % anual. ¿Cuánto gano en 4 años?", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        cap = Rectangle(width=1.6, height=2.6, stroke_color=WHITE, stroke_width=2, fill_color=M1, fill_opacity=0.35)
        cap.move_to([-5.3, -0.3, 0])
        tcap = VGroup(texto("1000 €", 28), texto("capital", 22, M1)).arrange(DOWN, buff=0.15).move_to(cap)
        self.play(Create(cap), FadeIn(tcap))
        notas("Cada año el banco me paga el 3 % de 1000 €: 0,03 · 1000 = 30 €")
        self.wait(2)
        suelo = -1.6
        xs = [-2.9 + k * 1.75 for k in range(4)]
        anos = VGroup(*[texto(f"año {k + 1}", 24, M2).move_to([xs[k], suelo - 0.35, 0]) for k in range(4)])
        base = Line([xs[0] - 0.8, suelo, 0], [xs[-1] + 0.8, suelo, 0], color=GREY_B, stroke_width=2)
        self.play(Create(base), FadeIn(anos))
        totales = VGroup()
        for k in range(4):
            nuevos = VGroup()
            for j in range(k + 1):
                b = Rectangle(width=1.0, height=0.5, stroke_color=WHITE, stroke_width=1.5, fill_color=PCT, fill_opacity=0.8)
                b.move_to([xs[k], suelo + 0.25 + j * 0.55, 0])
                t = texto("30 €", 20).move_to(b)
                nuevos.add(VGroup(b, t))
            # los de años anteriores se copian; el nuevo sale del capital
            if k > 0:
                self.play(*[TransformFromCopy(totales[k - 1][1][j], nuevos[j]) for j in range(k)], run_time=0.7)
            self.play(TransformFromCopy(VGroup(cap.copy().scale(0.2)), nuevos[k]), run_time=0.8)
            tot = MathTex(f"{30 * (k + 1)}", font_size=36, color=ACENTO).next_to(nuevos, UP, buff=0.15)
            self.play(FadeIn(tot))
            totales.add(VGroup(tot, nuevos))
            if k == 0:
                notas("El capital NO cambia: cada año me dan otros 30 €, siempre los mismos")
            self.wait(0.6)
        notas("En 4 años: 30 · 4 = 120 €. Es INTERÉS SIMPLE: siempre sobre el capital inicial", color=OK)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("La fórmula")
        f = MathTex("I", "=", "C", "\\cdot", "r", "\\cdot", "t", font_size=96).move_to([0, 1.75, 0])
        f[0].set_color(PCT)
        f[2].set_color(M1)
        f[4].set_color(ACENTO)
        f[6].set_color(M2)
        self.play(Write(f))
        leyenda = VGroup(texto("I = interés (lo que gano)", 28, PCT), texto("C = capital (lo que dejo)", 28, M1),
                         texto("r = tanto por uno (3 % → 0,03)", 28, ACENTO), texto("t = tiempo (en años)", 28, M2))
        leyenda.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -0.25, 0])
        for m in leyenda:
            self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.5)
        ej = MathTex("I=1000\\cdot 0{,}03\\cdot 4=120", font_size=50, color=ACENTO).move_to([0, -2.35, 0])
        self.play(Write(ej))
        notas("Es lo mismo que hemos hecho con las monedas: 30 € por año, durante 4 años", color=OK)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Hacia atrás")
        enun = texto("Con 1500 € al 2 %, ¿cuántos años tardo en ganar 90 €?", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        notas("Ahora lo que no sabemos es el tiempo t")
        def TT(*partes):
            m = MathTex(*partes, font_size=52)
            for p_ in m:
                if p_.get_tex_string() == "t":
                    p_.set_color(LETRA)
            return m

        e = TT("90=1500\\cdot 0{,}02\\cdot", "t")
        pasos = [(TT("90=30\\cdot", "t"), "Cada año gano 1500 · 0,02 = 30 €"), (TT("t", "=\\dfrac{90}{30}=3"), None)]
        cuenta(self, e, pasos, -2.6, 1.2, notas, None, True, 52, dy=1.0)
        notas("3 años: 30 € el primero, 30 € el segundo y 30 € el tercero", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Simple frente a compuesto")
        enun = texto("1000 € al 10 % durante 5 años", 30).move_to([0, 2.4, 0])
        self.play(FadeIn(enun))
        U = 0.0021
        suelo = -2.0
        simple = [1000 + 100 * k for k in range(6)]
        comp = [round(1000 * 1.1 ** k, 2) for k in range(6)]
        ley = VGroup(Square(0.25, fill_color=PCT, fill_opacity=0.8, stroke_width=1), texto("simple", 24, PCT),
                     Square(0.25, fill_color=M1, fill_opacity=0.8, stroke_width=1), texto("compuesto", 24, M1))
        ley.arrange(RIGHT, buff=0.15).move_to([-4.3, 1.7, 0])
        self.play(FadeIn(ley))
        notas("Simple: cada año +100 € (el 10 % de 1000)")
        bs, bc = VGroup(), VGroup()
        for k in range(6):
            x = -5.6 + k * 1.75
            b = Rectangle(width=0.55, height=simple[k] * U, stroke_width=1.5, stroke_color=WHITE, fill_color=PCT,
                          fill_opacity=0.75)
            b.move_to([x - 0.3, suelo + simple[k] * U / 2, 0])
            bs.add(VGroup(b, MathTex(str(k), font_size=30, color=M2).move_to([x, suelo - 0.3, 0])))
        self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in bs], lag_ratio=0.15),
                  *[FadeIn(g[1]) for g in bs])
        ts = MathTex("1500", font_size=34, color=PCT).move_to([4.6, bs[-1][0].get_top()[1] - 0.15, 0])
        self.play(FadeIn(ts))
        notas("Compuesto: cada año el 10 % de lo que YA tengo (los intereses también dan intereses)")
        for k in range(6):
            x = -5.6 + k * 1.75
            b = Rectangle(width=0.55, height=comp[k] * U, stroke_width=1.5, stroke_color=WHITE, fill_color=M1,
                          fill_opacity=0.75)
            b.move_to([x + 0.3, suelo + comp[k] * U / 2, 0])
            bc.add(b)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bc], lag_ratio=0.15))
        tc = MathTex("1610{,}51", font_size=34, color=M1).move_to([4.75, bc[-1].get_top()[1] + 0.15, 0])
        self.play(FadeIn(tc))
        anos = texto("años", 22, M2).move_to([3.5, suelo - 0.75, 0])
        self.play(FadeIn(anos))
        notas("Con el compuesto se gana más, y cada vez más deprisa. Lo verás en 3.º de ESO", color=ACENTO)
        self.wait(4)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios
def enunciados_1():
    return [
        ("1. ¿Forman proporción?", lista(["3/4 y 9/12", "2/5 y 6/14", "1,5/2 y 6/8"], 3)),
        ("2. Calcula x:", lista(["4/6 = 10/x", "x/8 = 15/24", "3/x = 12/20"], 3)),
        ("3. ¿Directa o inversa? Completa la tabla:",
         "a)  2, 4, 6, ?   →   6, 12, ?, 30            b)  1, 2, 3, ?   →   24, 12, ?, 4"),
    ]


def enunciados_2():
    return [
        ("4. 6 cuadernos cuestan 9 €. ¿Cuánto cuestan 10 cuadernos?", ""),
        ("5. 3 camiones tardan 8 días en transportar una carga. ¿Cuánto tardan 4 camiones?", ""),
        ("6. 6 personas gastan 180 € en comida en 5 días. ¿Cuánto gastarán 4 personas en 9 días?", ""),
    ]


def enunciados_3():
    return [
        ("7. Calcula:", lista(["30 % de 150", "8 % de 250", "120 % de 45"], 3)),
        ("8. Problemas de porcentajes:",
         "a) El 15 % de un número es 36. ¿Cuál es el número?\nb) ¿Qué porcentaje es 27 de 90?"),
        ("9. Aumentos y descuentos:",
         "a) Un móvil de 250 € sube un 12 %. ¿Cuánto cuesta ahora?\n"
         "b) Unos pantalones de 40 € tienen un 30 % de descuento. ¿Cuánto pago?\n"
         "c) Tras un descuento del 25 % he pagado 60 €. ¿Cuál era el precio?"),
    ]


PROP = [("\\dfrac{3}{4}\\ \\ \\mathrm{y}\\ \\ \\dfrac{9}{12}", "3\\cdot 12=36,\\quad 4\\cdot 9=36", True, "Sí: 36 = 36"),
        ("\\dfrac{2}{5}\\ \\ \\mathrm{y}\\ \\ \\dfrac{6}{14}", "2\\cdot 14=28,\\quad 5\\cdot 6=30", False, "No: 28 ≠ 30"),
        ("\\dfrac{1{,}5}{2}\\ \\ \\mathrm{y}\\ \\ \\dfrac{6}{8}", "1{,}5\\cdot 8=12,\\quad 2\\cdot 6=12", True, "Sí: 12 = 12")]
CUARTO = [("\\dfrac{4}{6}=\\dfrac{10}{x}", [("4x=60", "Productos cruzados: 4 · x = 6 · 10"), ("x=\\dfrac{60}{4}=15", None)]),
          ("\\dfrac{x}{8}=\\dfrac{15}{24}", [("24x=120", None), ("x=\\dfrac{120}{24}=5", None)]),
          ("\\dfrac{3}{x}=\\dfrac{12}{20}", [("12x=60", None), ("x=\\dfrac{60}{12}=5", None)])]
TABLAS = [
    ([["2", "4", "6", "?"], ["6", "12", "?", "30"]], False, "\\dfrac{6}{2}=\\dfrac{12}{4}=3",
     "Cocientes iguales: DIRECTA con k = 3", [(1, 2, "18", "6\\cdot 3=18"), (0, 3, "10", "30:3=10")]),
    ([["1", "2", "3", "?"], ["24", "12", "?", "4"]], True, "1\\cdot 24=2\\cdot 12=24",
     "Productos iguales: INVERSA (el producto es 24)", [(1, 2, "8", "24:3=8"), (0, 3, "6", "24:4=6")]),
]
REGLA = {
    4: ("6 cuadernos cuestan 9 €. ¿Cuánto cuestan 10 cuadernos?", ("cuadernos", "€"), ("6", "9"), ("10", "x"), False,
        [("\\dfrac{6}{10}=\\dfrac{9}{x}", "Más cuadernos → más dinero: DIRECTA"), ("6x=90", "Productos cruzados"),
         ("x=\\dfrac{90}{6}=15", None)],
        "10 cuadernos cuestan 15 €  (1 cuaderno: 9 : 6 = 1,50 €;  1,50 · 10 = 15 €)"),
    5: ("3 camiones tardan 8 días en transportar una carga. ¿Cuánto tardan 4 camiones?", ("camiones", "días"),
        ("3", "8"), ("4", "x"), True,
        [("3\\cdot 8=4\\cdot x", "Más camiones → menos días: INVERSA. El producto no cambia"), ("24=4x", None),
         ("x=\\dfrac{24}{4}=6", None)],
        "4 camiones tardan 6 días  (1 camión solo: 3 · 8 = 24 días;  24 : 4 = 6)"),
}
PCT_EJ = {
    "7a": ("30\\,\\%\\ \\mathrm{de}\\ 150", [("0{,}30\\cdot 150=45", "30 % = 0,30")], None),
    "7b": ("8\\,\\%\\ \\mathrm{de}\\ 250", [("0{,}08\\cdot 250=20", "¡Ojo! 8 % = 0,08 (no 0,8)")], None),
    "7c": ("120\\,\\%\\ \\mathrm{de}\\ 45", [("1{,}20\\cdot 45=54", "Más del 100 %: sale más que 45")], None),
    "8a": ("0{,}15\\cdot x=36", [("x=\\dfrac{36}{0{,}15}=240", None)], "El 15 % de un número es 36"),
    "8b": ("\\dfrac{27}{90}=0{,}30", [("0{,}30=30\\,\\%", None)], "¿Qué porcentaje es 27 de 90?"),
    "9a": ("250\\cdot 1{,}12=280", [], "Sube un 12 %: índice 1 + 0,12 = 1,12"),
    "9b": ("40\\cdot 0{,}70=28", [], "30 % de descuento: índice 0,70"),
    "9c": ("x\\cdot 0{,}75=60", [("x=\\dfrac{60}{0{,}75}=80", None)], "25 % de descuento: pagué el 75 %"),
}


def ej_prop(scene, i, x, y, notas, ejemplo=False):
    enun, prod, ok, ver = PROP[i]
    g = cuenta(scene, X(enun, 44), [(prod, "Multiplicamos en cruz" if ejemplo else None)], x, y, notas,
               f"{'abc'[i]})", ejemplo, 40, dy=1.0)
    v = texto(ver, 28, OK if ok else MAL).next_to(g[-1], DOWN, buff=0.3).align_to(g[-1], LEFT)
    scene.play(FadeIn(v))
    scene.wait(1.2 if ejemplo else 0.6)
    return VGroup(g, v)


def ej_cuarto(scene, i, x, y, notas, ejemplo=False):
    enun, pasos = CUARTO[i]
    if not ejemplo:
        pasos = [(p, None) for p, _ in pasos]
    return cuenta(scene, X(enun, 48), pasos, x, y, notas, f"{'abc'[i]})", ejemplo, 46, dy=1.0)


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


def ej_regla(scene, n, notas, ejemplo=False):
    enun, (n1, n2), f1, f2, inv, pasos, fin = REGLA[n]
    t = texto(enun, 28).move_to([0, 2.4, 0])
    if t.width > 13:
        t.scale_to_fit_width(13)
    scene.play(FadeIn(t))
    cabs, filas, fl, tipo = esquema(n1, n2, f1, f2, -4.3, 1.4, inversa=inv)
    scene.play(FadeIn(cabs), FadeIn(filas))
    scene.play(GrowArrow(fl[0]), GrowArrow(fl[1]))
    scene.play(FadeIn(tipo, scale=1.3))
    e, n0 = pasos[0]
    if n0:
        notas(n0)
    rest = pasos[1:] if ejemplo else [(p, None) for p, _ in pasos[1:]]
    cuenta(scene, X(e, 48), rest, -0.2, 1.2, notas, None, ejemplo, 46, dy=0.95)
    notas(fin, color=OK)
    scene.wait(3)
    notas.fin()


def ej_compuesta(scene, notas):
    t = texto("6 personas gastan 180 € en comida en 5 días.\n¿Cuánto gastarán 4 personas en 9 días?", 28)
    t.move_to([0, 2.35, 0])
    scene.play(FadeIn(t))
    marco, cabs, cel = tabla_v(["personas", "días", "€"], [["6", "5", "180"], ["4", "9", "x"]], -3.0, 1.3,
                               (M1, M2, M3), w=1.7)
    scene.play(Create(marco), FadeIn(cabs), *[FadeIn(c) for c in cel[0] + cel[1]])
    tipos = VGroup(texto("menos personas → menos €: DIRECTA", 24, OK),
                   texto("más días → más €: DIRECTA", 24, OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    tipos.move_to([3.4, 0.9, 0])
    scene.play(FadeIn(tipos))
    c = encadenar("180", [("\\cdot\\dfrac{4}{6}", "120"), ("\\cdot\\dfrac{9}{5}", "216")], 52).move_to([0, -1.0, 0])
    scene.play(Write(c[:3]))
    scene.play(FadeIn(texto("personas: 6 → 4", 22, M1).next_to(c[1], DOWN, buff=0.25)))
    scene.play(Write(c[3:]))
    scene.play(FadeIn(texto("días: 5 → 9", 22, M2).next_to(c[3], DOWN, buff=0.25)))
    scene.play(Circumscribe(c[4], color=ACENTO))
    notas("Gastarán 216 €  (1 persona 1 día: 180 : 30 = 6 €;  4 · 9 · 6 = 216 €)", color=OK)
    scene.wait(3.5)
    notas.fin()


def ej_pct(scene, clave, x, y, notas, ejemplo=False, size=46):
    enun, pasos, frase = PCT_EJ[clave]
    et = f"{clave[1]})"
    g = VGroup()
    if frase:
        f = texto(frase, 26, GREY_B).move_to([x, y + 0.75, 0], aligned_edge=LEFT)
        scene.play(FadeIn(f))
        g.add(f)
    if not ejemplo:
        pasos = [(p, None) for p, _ in pasos]
    g.add(cuenta(scene, X(enun, size), pasos, x, y, notas, et, ejemplo, size, dy=1.0))
    scene.wait(0.8)
    return g


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Proporcionalidad numérica")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos un apartado de cada tipo", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        ej_prop(self, 0, -2.4, 1.2, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        ej_cuarto(self, 0, -2.4, 1.5, notas, ejemplo=True)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        ej_tabla(self, 0, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4")
        ej_regla(self, 4, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        ej_pct(self, "7a", -2.6, 1.0, notas, ejemplo=True, size=52)
        notas("El 30 % de 150 es 45", color=OK)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9 a)")
        ej_pct(self, "9a", -2.6, 1.0, notas, ejemplo=True, size=52)
        notas("Ahora cuesta 280 €", color=OK)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 6")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1: b) y c)")
        ej_prop(self, 1, -5.8, 1.2, notas)
        ej_prop(self, 2, 0.9, 1.2, notas)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2: b) y c)")
        ej_cuarto(self, 1, -5.8, 1.5, notas)
        ej_cuarto(self, 2, 0.9, 1.5, notas)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 b)")
        ej_tabla(self, 1, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5")
        ej_regla(self, 5, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6")
        ej_compuesta(self, notas)
        limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 7 a 9.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 7 a 9")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 7: b) y c)")
        ej_pct(self, "7b", -5.8, 1.2, notas, size=42)
        ej_pct(self, "7c", 0.9, 1.2, notas, size=42)
        notas("b) 20      c) 54", color=OK)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 8")
        ej_pct(self, "8a", -5.8, 1.2, notas, size=42)
        ej_pct(self, "8b", 0.9, 1.2, notas, size=42)
        notas("a) El número es 240      b) 27 es el 30 % de 90", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9: b) y c)")
        ej_pct(self, "9b", -5.8, 1.2, notas, size=42)
        ej_pct(self, "9c", 0.9, 1.2, notas, size=42)
        notas("b) Pago 28 €      c) El precio era 80 €  (80 · 0,75 = 60 ✓)", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
