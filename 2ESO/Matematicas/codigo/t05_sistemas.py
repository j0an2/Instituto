"""Tema 5 · Sistemas de ecuaciones (2º ESO)

Sigue el índice del libro: sistemas lineales · método gráfico · sustitución · reducción · igualación.

Escenas:
    QueEsSistema      – una ecuación con dos incógnitas tiene infinitas soluciones (tabla → puntos → recta);
                        un sistema pide las dos a la vez: la pareja común es el punto de corte
    MetodoGrafico     – dos puntos por recta, punto de corte y comprobación; cuando no se lee exacto
    Sustitucion       – despejar y «trasladar» la expresión a la otra ecuación
    Reduccion         – dos balanzas que se juntan; suma en columnas; multiplicar antes de sumar
    Igualacion        – despejar la misma incógnita en las dos e igualar
    TresMetodos       – (extra E1) el mismo sistema por los tres métodos
    TiposSistemas     – se cortan (1 solución), paralelas (ninguna, 0 = 3), coinciden (infinitas, 0 = 0)
    NumeroSoluciones  – (extra E2, Aprende +) cuántas soluciones sin resolver: a1/a2, b1/b2, c1/c2; productos en cruz si hay un 0
                        (detrás: página interactiva E3, interactivos/dos_rectas.html)
    Problemas         – gallinas y conejos (con dibujo de patas) y entradas de cine
    EjerciciosEjemplo / EjerciciosResueltos1 / EjerciciosResueltos2

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t05_sistemas.py Reduccion
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t05_sistemas.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COMUN = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t03_lenguaje_algebraico import cuenta, lista, pagina_enunciados, tarjeta, ROSA, LETRA  # noqa: E402
from t04_ecuaciones import balanza  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 5 · Sistemas de ecuaciones"
TITULOS = {
    "QueEsSistema": "¿Qué es un sistema de ecuaciones?",
    "MetodoGrafico": "Método gráfico",
    "Sustitucion": "Método de sustitución",
    "Reduccion": "Método de reducción",
    "Igualacion": "Método de igualación",
    "TresMetodos": "El mismo sistema por los tres métodos",
    "TiposSistemas": "Tipos de sistemas: una, ninguna o infinitas soluciones",
    "NumeroSoluciones": "Aprende +: ¿cuántas soluciones? (sin resolver)",
    "Problemas": "Problemas con sistemas",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 3)",
    "EjerciciosResueltos2": "Ejercicios resueltos (4 a 9)",
}
EXTRAS = {"TresMetodos": "E1", "NumeroSoluciones": "E2"}
INTERACTIVOS = [("E3", "Pruébalo tú: dos rectas", "interactivos/dos_rectas.html", "NumeroSoluciones")]

Y_COL = "#4FC3F7"                 # la y, en cian (la x sigue en amarillo)
E1C, E2C = "#FF9F43", ROSA        # ecuación (1) naranja, ecuación (2) rosa


def XY(s, size=48, color=None, col=None):
    """MathTex con la x amarilla y la y cian; color = color del resto; col = {trozo: color}."""
    col = col or {}
    t = MathTex(s, font_size=size, substrings_to_isolate=list(col) + ["x", "y"])
    if color:
        t.set_color(color)
    t.set_color_by_tex("x", LETRA)
    t.set_color_by_tex("y", Y_COL)
    for k, c in col.items():
        t.set_color_by_tex(k, c)
    return t


def sistema(e1, e2, size=44, numeros=True):
    """Llave con las dos ecuaciones (la 1 en naranja y la 2 en rosa). g[1][0] y g[1][1] son las ecuaciones."""
    f1, f2 = XY(e1, size, E1C), XY(e2, size, E2C)
    filas = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    llave = Brace(filas, LEFT, buff=0.12)
    g = VGroup(llave, filas)
    if numeros:
        g.add(MathTex("(1)", font_size=size - 14, color=E1C).next_to(f1, RIGHT, buff=0.35),
              MathTex("(2)", font_size=size - 14, color=E2C).next_to(f2, RIGHT, buff=0.35))
    return g


def C(scene, enun, pasos, x, y, notas=None, etiqueta=None, ejemplo=False, size=48, dy=None):
    """cuenta() con x e y coloreadas."""
    e = enun if isinstance(enun, Mobject) else XY(enun, size)
    ps = [(p if isinstance(p, Mobject) else XY(p, size), n) for p, n in pasos]
    return cuenta(scene, e, ps, x, y, notas, etiqueta, ejemplo, size, dy)


def ejes(xr=(-1, 6), yr=(-1, 6), xl=5.4, yl=5.0, centro=(3.4, -0.3, 0), num=22):
    ax = Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1], x_length=xl, y_length=yl, tips=False,
              axis_config={"include_numbers": True, "font_size": num, "color": GREY_B})
    ax.move_to(centro)
    lx = MathTex("x", font_size=32, color=LETRA).next_to(ax.x_axis.get_right(), UR, buff=0.08)
    ly = MathTex("y", font_size=32, color=Y_COL).next_to(ax.y_axis.get_end(), RIGHT, buff=0.22)
    return ax, VGroup(ax, lx, ly)


def recta(ax, a, b, c, color, sw=5):
    """La recta ax + by = c, recortada a los ejes."""
    x0, x1 = ax.x_range[0], ax.x_range[1]
    y0, y1 = ax.y_range[0], ax.y_range[1]
    if b == 0:
        return Line(ax.c2p(c / a, y0), ax.c2p(c / a, y1), color=color, stroke_width=sw)
    f = lambda x: (c - a * x) / b
    lo, hi = x0, x1
    if a != 0:
        xa, xb = (c - b * y0) / a, (c - b * y1) / a
        lo, hi = max(lo, min(xa, xb)), min(hi, max(xa, xb))
    return Line(ax.c2p(lo, f(lo)), ax.c2p(hi, f(hi)), color=color, stroke_width=sw)


def proyecciones(ax, x, y):
    p = ax.c2p(x, y)
    return VGroup(DashedLine(p, ax.c2p(x, 0), color=GREY_B, stroke_width=2),
                  DashedLine(p, ax.c2p(0, y), color=GREY_B, stroke_width=2))


def tabla(pares, x0, y0, color, size=34):
    """Tabla x | y. Devuelve (VGroup cabecera+raya, lista de filas)."""
    hx = MathTex("x", font_size=size, color=LETRA).move_to([x0, y0, 0])
    hy = MathTex("y", font_size=size, color=Y_COL).move_to([x0 + 1.0, y0, 0])
    raya = Line([x0 - 0.4, y0 - 0.25, 0], [x0 + 1.4, y0 - 0.25, 0], color=GREY_B, stroke_width=2)
    filas = []
    for k, (u, v) in enumerate(pares):
        y = y0 - 0.5 - k * 0.45
        filas.append(VGroup(MathTex(str(u), font_size=size - 2, color=color).move_to([x0, y, 0]),
                            MathTex(str(v), font_size=size - 2, color=color).move_to([x0 + 1.0, y, 0])))
    return VGroup(hx, hy, raya), filas


def pasos_card(scene, textos):
    p = VGroup(*[texto(t, 30) for t in textos]).arrange(DOWN, aligned_edge=LEFT, buff=0.33)
    card = tarjeta(p).move_to([0, 0.2, 0])
    scene.play(Create(card[0]))
    for m in p:
        scene.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.55)
    scene.wait(2.5)


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


# ---------------------------------------------------------------------------
class QueEsSistema(Scene):
    def construct(self):
        cab = titulo(self, "¿Qué es un sistema?", "Dos ecuaciones a la vez")
        notas = Notas(self)
        sub = Sub(self, cab)
        sub("Una ecuación con dos incógnitas")
        ax, g_ax = ejes()
        e1 = XY("x+y=5", 44, E1C).move_to([-5.5, 2.25, 0])
        self.play(Write(e1))
        notas("Dos incógnitas, x e y. ¿Qué parejas de números suman 5?")
        self.play(Create(g_ax))
        cabe1, filas1 = tabla([(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)], -6.0, 1.6, E1C)
        self.play(FadeIn(cabe1))
        puntos1 = VGroup()
        for (u, v), f in zip([(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)], filas1):
            d = Dot(ax.c2p(u, v), color=E1C, radius=0.08)
            self.play(FadeIn(f), FadeIn(d, scale=1.6), run_time=0.45)
            puntos1.add(d)
        notas("¡Todos los puntos están en línea recta!", color=E1C)
        r1 = recta(ax, 1, 1, 5, E1C)
        self.play(Create(r1), run_time=1.2)
        notas("Y también los de en medio, como x = 2,5 e y = 2,5: tiene INFINITAS soluciones")
        d = Dot(ax.c2p(2.5, 2.5), color=WHITE, radius=0.08)
        self.play(FadeIn(d, scale=2), Flash(d, color=E1C))
        self.wait(2)
        self.play(FadeOut(d))

        e2 = XY("x-y=1", 44, E2C).move_to([-2.9, 2.25, 0])
        self.play(Write(e2))
        notas("Otra ecuación: ¿qué parejas de números se restan y dan 1?")
        pares2 = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
        cabe2, filas2 = tabla(pares2, -3.4, 1.6, E2C)
        self.play(FadeIn(cabe2))
        puntos2 = VGroup()
        for (u, v), f in zip(pares2, filas2):
            d = Dot(ax.c2p(u, v), color=E2C, radius=0.08)
            self.play(FadeIn(f), FadeIn(d, scale=1.6), run_time=0.45)
            puntos2.add(d)
        r2 = recta(ax, 1, -1, 1, E2C)
        self.play(Create(r2), run_time=1.2)
        self.wait(1)

        sub("El sistema")
        notas("Un SISTEMA pide que se cumplan las DOS a la vez: ¿hay una pareja en las dos tablas?", color=ACENTO)
        self.wait(2)
        c1 = SurroundingRectangle(filas1[3], color=ACENTO, buff=0.08)
        c2 = SurroundingRectangle(filas2[2], color=ACENTO, buff=0.08)
        self.play(Create(c1), Create(c2))
        sol = Dot(ax.c2p(3, 2), color=ACENTO, radius=0.12)
        self.play(FadeIn(sol, scale=2), Flash(sol, color=ACENTO), Create(proyecciones(ax, 3, 2)))
        notas("¡x = 3, y = 2! Y en el dibujo es justo el punto donde se CORTAN las dos rectas", color=ACENTO)
        self.wait(3)
        self.play(FadeOut(VGroup(cabe1, cabe2, *filas1, *filas2, c1, c2, e1, e2)))
        s = sistema("x+y=5", "x-y=1", 44).move_to([-4.2, 1.6, 0])
        self.play(Write(s))
        r = XY("x=3,\\quad y=2", 46).move_to([-4.2, 0.1, 0])
        caja = SurroundingRectangle(r, color=ACENTO, buff=0.2, corner_radius=0.1)
        self.play(Write(r), Create(caja))
        notas("Así se escribe un sistema. Su solución es la pareja (3, 2). Comprobamos:")
        comp = VGroup(MathTex("3+2=5", "\\ \\checkmark", font_size=40, color=E1C),
                      MathTex("3-2=1", "\\ \\checkmark", font_size=40, color=E2C)).arrange(DOWN, buff=0.3)
        comp.move_to([-4.2, -1.5, 0])
        for m in comp:
            m[1].set_color(OK)
            self.play(Write(m))
        self.wait(3)
        notas.fin()


class MetodoGrafico(Scene):
    def construct(self):
        cab = titulo(self, "Método gráfico")
        notas = Notas(self)
        sub = Sub(self, cab)
        sub("Los pasos")
        pasos_card(self, ["1. Para cada ecuación, una tabla con dos puntos",
                          "2. Dibujamos las dos rectas",
                          "3. La solución es el punto de corte",
                          "4. Comprobamos en las dos ecuaciones"])
        limpiar(self, cab)
        sub.olvidar()

        sub("Ejemplo")
        s = sistema("2x+y=7", "x-y=-1", 42).move_to([-4.4, 2.0, 0])
        self.play(Write(s))
        ax, g_ax = ejes(yr=(-1, 8), yl=5.2, centro=(3.4, -0.4, 0))
        self.play(Create(g_ax))
        notas("Para dibujar una recta bastan DOS puntos. Damos valores a x y calculamos y")
        cab1, f1 = tabla([(0, 7), (3, 1)], -6.0, 0.7, E1C)
        cab2, f2 = tabla([(0, 1), (3, 4)], -3.4, 0.7, E2C)
        exp = VGroup(XY("x=0\\Rightarrow y=7", 28, E1C), XY("x=3\\Rightarrow y=1", 28, E1C)).arrange(DOWN, buff=0.15)
        exp.move_to([-5.5, -1.1, 0])
        exp2 = VGroup(XY("x=0\\Rightarrow y=1", 28, E2C), XY("x=3\\Rightarrow y=4", 28, E2C)).arrange(DOWN, buff=0.15)
        exp2.move_to([-2.9, -1.1, 0])
        self.play(FadeIn(cab1))
        for f, (u, v), m in zip(f1, [(0, 7), (3, 1)], exp):
            self.play(FadeIn(m), FadeIn(f), FadeIn(Dot(ax.c2p(u, v), color=E1C, radius=0.08), scale=1.6), run_time=0.8)
        self.play(Create(recta(ax, 2, 1, 7, E1C)))
        self.play(FadeIn(cab2))
        for f, (u, v), m in zip(f2, [(0, 1), (3, 4)], exp2):
            self.play(FadeIn(m), FadeIn(f), FadeIn(Dot(ax.c2p(u, v), color=E2C, radius=0.08), scale=1.6), run_time=0.8)
        self.play(Create(recta(ax, 1, -1, -1, E2C)))
        notas("Las rectas se cortan en un punto: lo leemos en los ejes", color=ACENTO)
        sol = Dot(ax.c2p(2, 3), color=ACENTO, radius=0.12)
        self.play(FadeIn(sol, scale=2), Flash(sol, color=ACENTO), Create(proyecciones(ax, 2, 3)))
        et = MathTex("(2,\\,3)", font_size=36, color=ACENTO).next_to(sol, RIGHT, buff=0.15)
        self.play(Write(et))
        self.wait(1.5)
        self.play(FadeOut(VGroup(cab1, cab2, *f1, *f2, exp, exp2)))
        r = XY("x=2,\\quad y=3", 44).move_to([-4.4, 0.3, 0])
        self.play(Write(r))
        comp = VGroup(MathTex("2\\cdot 2+3=7", "\\ \\checkmark", font_size=38, color=E1C),
                      MathTex("2-3=-1", "\\ \\checkmark", font_size=38, color=E2C)).arrange(DOWN, buff=0.3)
        comp.move_to([-4.4, -1.3, 0])
        notas("Comprobamos en las DOS ecuaciones")
        for m in comp:
            m[1].set_color(OK)
            self.play(Write(m))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("Un inconveniente")
        s = sistema("x+y=4", "3x-y=1", 42).move_to([-4.4, 2.0, 0])
        self.play(Write(s))
        ax, g_ax = ejes(centro=(3.4, -0.3, 0))
        self.play(Create(g_ax))
        self.play(Create(recta(ax, 1, 1, 4, E1C)), Create(recta(ax, 3, -1, 1, E2C)))
        sol = Dot(ax.c2p(1.25, 2.75), color=ACENTO, radius=0.12)
        self.play(FadeIn(sol, scale=2), Create(proyecciones(ax, 1.25, 2.75)))
        q = texto("¿x = 1? ¿y = 3?\nA ojo no se puede leer exacto", 30, ACENTO).move_to([-4.2, 0.0, 0])
        self.play(FadeIn(q))
        notas("La solución es x = 1,25 e y = 2,75: con el dibujo solo sabemos «más o menos»")
        self.wait(2.5)
        notas("Por eso hay métodos algebraicos, que dan la solución exacta. ¡Vamos con ellos!", color=ACENTO)
        self.wait(3)
        notas.fin()


class Sustitucion(Scene):
    def construct(self):
        cab = titulo(self, "Método de sustitución")
        notas = Notas(self)
        sub = Sub(self, cab)
        sub("Los pasos")
        pasos_card(self, ["1. Despejamos una incógnita (mejor si no tiene número delante)",
                          "2. La sustituimos en la OTRA ecuación",
                          "3. Resolvemos: queda una ecuación con una sola incógnita",
                          "4. Volvemos a lo despejado para calcular la otra",
                          "5. Comprobamos"])
        limpiar(self, cab)
        sub.olvidar()

        sub("Ejemplo")
        s = sistema("x+2y=7", "3x-y=7", 44).move_to([-4.6, 2.0, 0])
        self.play(Write(s))
        notas("En la (1), la x no tiene número delante: la despejamos")
        self.play(Indicate(s[1][0], color=E1C))
        d = VGroup(XY("x=", 48), XY("7-2y", 48)).arrange(RIGHT, buff=0.12).move_to([-6.0, 0.6, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(s[1][0], d))
        caja = SurroundingRectangle(d[1], color=ACENTO, buff=0.1, corner_radius=0.08)
        self.play(Create(caja))
        notas("Ahora ya sabemos lo que vale x: «7 − 2y». Lo llevamos a la (2)")
        self.wait(1.5)
        # La (2) por trozos para quitar la x y meter el paréntesis
        e2 = VGroup(XY("3", 48, E2C), XY("x", 48), XY("-y=7", 48, E2C)).arrange(RIGHT, buff=0.06)
        e2.move_to([0.8, 1.6, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(s[1][1], e2))
        self.play(Indicate(e2[1], color=ACENTO, scale_factor=1.5))
        nuevo = VGroup(XY("3", 48, E2C), XY("(7-2y)", 48), XY("-y=7", 48, E2C)).arrange(RIGHT, buff=0.06)
        nuevo.move_to(e2, aligned_edge=LEFT)
        self.play(FadeOut(e2[1], shift=UP * 0.4),
                  TransformFromCopy(d[1], nuevo[1], path_arc=-PI / 3),
                  Transform(e2[0], nuevo[0]), Transform(e2[2], nuevo[2]), run_time=1.8)
        notas("¡Donde había una x ponemos (7 − 2y)! Ahora solo queda la y", color=ACENTO)
        self.wait(2)
        pasos = [("21-6y-y=7", "Quitamos el paréntesis: 3 · 7 = 21  y  3 · (−2y) = −6y"),
                 ("-7y=7-21", "Transponemos"),
                 ("-7y=-14", None),
                 ("y=2", "El −7 pasa dividiendo")]
        g = VGroup()
        prev = nuevo
        for tex, nota in pasos:
            if nota:
                notas(nota)
            m = XY(tex, 46).next_to(prev, DOWN, buff=0.32).align_to(nuevo, LEFT).shift(RIGHT * 0.3)
            self.play(Write(m))
            self.wait(0.6)
            g.add(m)
            prev = m
        self.play(Circumscribe(g[-1], color=ACENTO))
        notas("Volvemos a lo que habíamos despejado, con y = 2")
        v = XY("x=7-2\\cdot 2=3", 48).move_to([-6.0, -0.4, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(d, v))
        r = XY("x=3,\\quad y=2", 48).move_to([-4.4, -1.8, 0])
        cr = SurroundingRectangle(r, color=ACENTO, buff=0.2, corner_radius=0.1)
        self.play(Write(r), Create(cr))
        notas("Comprobamos:  3 + 2 · 2 = 7 ✓   y   3 · 3 − 2 = 7 ✓", color=OK)
        self.wait(3.5)
        notas.fin()


def fila_cols(textos, y, color, xs, size=50):
    """Términos colocados en columnas (x, y, =, número). None deja el hueco."""
    return [XY(t, size, color).move_to([cx, y, 0]) if t else None for t, cx in zip(textos, xs)]


class Reduccion(Scene):
    def construct(self):
        cab = titulo(self, "Método de reducción")
        notas = Notas(self)
        sub = Sub(self, cab)

        # --- La idea: sumar dos balanzas
        sub("La idea: sumar ecuaciones")
        s = sistema("x+y=5", "x-y=1", 44).move_to([0, 2.1, 0])
        self.play(Write(s))
        notas("Cada ecuación es una balanza en equilibrio")
        b1, m1, _ = balanza(cx=-3.6, y=-1.0, L=1.7, pw=0.85)
        b2, m2, _ = balanza(cx=3.6, y=-1.0, L=1.7, pw=0.85)
        def plato(m, lado):
            return m[1][lado][1]
        t1 = [XY("x+y", 40, E1C).next_to(plato(m1, 0), UP, buff=0.1), XY("5", 40, E1C).next_to(plato(m1, 1), UP, buff=0.1)]
        t2 = [XY("x-y", 40, E2C).next_to(plato(m2, 0), UP, buff=0.1), XY("1", 40, E2C).next_to(plato(m2, 1), UP, buff=0.1)]
        self.play(FadeIn(VGroup(b1, m1, b2, m2)), *[FadeIn(t) for t in t1 + t2])
        self.wait(1.5)
        notas("Si juntamos lo de la izquierda de las dos, y lo de la derecha de las dos, ¡sigue en equilibrio!")
        b3, m3, _ = balanza(cx=0, y=-1.0, L=3.0, pw=1.5)
        t3 = [XY("x+y+x-y", 40).next_to(plato(m3, 0), UP, buff=0.1), XY("5+1", 40).next_to(plato(m3, 1), UP, buff=0.1)]
        self.play(ReplacementTransform(VGroup(b1, b2), b3), ReplacementTransform(VGroup(m1, m2), m3),
                  ReplacementTransform(VGroup(t1[0], t2[0]), t3[0]), ReplacementTransform(VGroup(t1[1], t2[1]), t3[1]),
                  run_time=1.8)
        self.wait(1)
        notas("Y aquí está la magia: +y y −y se anulan", color=ACENTO)
        t4 = [XY("2x", 44).move_to(t3[0]), XY("6", 44).move_to(t3[1])]
        self.play(Indicate(t3[0], color=ACENTO))
        self.play(ReplacementTransform(t3[0], t4[0]), ReplacementTransform(t3[1], t4[1]))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        # --- En columnas
        sub("Sumamos en columnas")
        xs = [-2.6, -0.9, 0.5, 1.9]
        a = fila_cols(["x", "+y", "=", "5"], 1.6, E1C, xs)
        b = fila_cols(["x", "-y", "=", "1"], 0.6, E2C, xs)
        n1 = MathTex("(1)", font_size=32, color=E1C).move_to([3.4, 1.6, 0])
        n2 = MathTex("(2)", font_size=32, color=E2C).move_to([3.4, 0.6, 0])
        mas = MathTex("+", font_size=50).move_to([-3.7, 0.6, 0])
        raya = Line([-4.0, 0.05, 0], [2.6, 0.05, 0], stroke_width=3)
        self.play(*[Write(m) for m in a], FadeIn(n1))
        self.play(*[Write(m) for m in b], FadeIn(n2), Write(mas))
        self.play(Create(raya))
        notas("Columna a columna: x + x = 2x")
        r = fila_cols(["2x", None, "=", "6"], -0.5, WHITE, xs)
        self.play(Indicate(VGroup(a[0], b[0]), color=LETRA), FadeIn(r[0], shift=DOWN * 0.2))
        notas("+y − y = 0: ¡se anulan! Por eso se llama reducción", color=ACENTO)
        self.play(Indicate(VGroup(a[1], b[1]), color=Y_COL, scale_factor=1.3))
        cero = MathTex("0", font_size=44, color=GREY_B).move_to([xs[1], -0.5, 0])
        self.play(FadeIn(cero))
        self.play(FadeOut(cero))
        self.play(FadeIn(r[2]), Indicate(VGroup(a[3], b[3])), FadeIn(r[3], shift=DOWN * 0.2))
        self.wait(1)
        pas = VGroup(XY("x=3", 48), XY("3+y=5\\ \\Rightarrow\\ y=2", 48)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        pas.move_to([-2.6, -1.9, 0], aligned_edge=LEFT)
        notas("2x = 6, así que x = 3. Y lo llevamos a la (1) para sacar la y")
        self.play(Write(pas[0]))
        self.play(Write(pas[1]))
        self.play(Circumscribe(pas, color=ACENTO))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        # --- Multiplicar antes
        sub("Si no se anula: multiplicamos")
        s = sistema("3x+2y=12", "x-y=-1", 44).move_to([-4.4, 2.1, 0])
        self.play(Write(s))
        notas("Aquí hay +2y y −y: si sumamos no se anulan")
        self.wait(1.5)
        notas("Multiplicamos TODA la (2) por 2: así tendremos −2y", color=ACENTO)
        xs = [-2.0, -0.2, 1.2, 2.6]
        a = fila_cols(["3x", "+2y", "=", "12"], 0.9, E1C, xs, 48)
        b0 = fila_cols(["x", "-y", "=", "-1"], -0.1, E2C, xs, 48)
        b = fila_cols(["2x", "-2y", "=", "-2"], -0.1, E2C, xs, 48)
        self.play(*[Write(m) for m in a])
        self.play(*[Write(m) for m in b0])
        por2 = MathTex("\\cdot 2", font_size=40, color=ACENTO).move_to([4.0, -0.1, 0])
        self.play(FadeIn(por2, shift=LEFT * 0.3))
        self.play(*[ReplacementTransform(u, v) for u, v in zip(b0, b)])
        self.play(Indicate(VGroup(a[1], b[1]), color=Y_COL, scale_factor=1.3))
        mas = MathTex("+", font_size=48).move_to([-3.2, -0.1, 0])
        raya = Line([-3.5, -0.6, 0], [3.2, -0.6, 0], stroke_width=3)
        self.play(Write(mas), Create(raya))
        r = fila_cols(["5x", None, "=", "10"], -1.15, WHITE, xs, 48)
        self.play(*[FadeIn(m, shift=DOWN * 0.2) for m in r if m])
        notas("Ahora sí: +2y − 2y = 0. Queda 5x = 10, x = 2")
        fin = XY("x=2\\ \\Rightarrow\\ 2-y=-1\\ \\Rightarrow\\ y=3", 44).move_to([0, -2.2, 0])
        self.play(Write(fin))
        self.play(Circumscribe(fin, color=ACENTO))
        notas("Comprobamos: 3 · 2 + 2 · 3 = 12 ✓   y   2 − 3 = −1 ✓", color=OK)
        self.wait(3.5)
        notas.fin()


class Igualacion(Scene):
    def construct(self):
        cab = titulo(self, "Método de igualación")
        notas = Notas(self)
        sub = Sub(self, cab)
        sub("Los pasos")
        pasos_card(self, ["1. Despejamos la MISMA incógnita en las dos ecuaciones",
                          "2. Igualamos lo que hemos obtenido",
                          "3. Resolvemos la ecuación que queda",
                          "4. Sustituimos para calcular la otra incógnita"])
        limpiar(self, cab)
        sub.olvidar()

        sub("Ejemplo")
        s = sistema("x+y=5", "2x-y=1", 44).move_to([-4.6, 2.1, 0])
        self.play(Write(s))
        notas("Despejamos la y en las dos")
        d1 = VGroup(XY("y=", 50), XY("5-x", 50, E1C)).arrange(RIGHT, buff=0.12).move_to([-6.0, 0.6, 0], aligned_edge=LEFT)
        d2 = VGroup(XY("y=", 50), XY("2x-1", 50, E2C)).arrange(RIGHT, buff=0.12).move_to([-6.0, -0.4, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(s[1][0], d1))
        self.play(TransformFromCopy(s[1][1], d2))
        k1 = SurroundingRectangle(d1[1], color=E1C, buff=0.1)
        k2 = SurroundingRectangle(d2[1], color=E2C, buff=0.1)
        self.play(Create(k1), Create(k2))
        notas("Si y vale «5 − x» y también vale «2x − 1», esas dos cosas tienen que ser iguales", color=ACENTO)
        self.wait(2)
        igual = MathTex("=", font_size=56).move_to([2.2, 1.3, 0])
        a = d1[1].copy()
        b = d2[1].copy()
        self.play(a.animate.next_to(igual, LEFT, buff=0.25), b.animate.next_to(igual, RIGHT, buff=0.25),
                  FadeIn(igual), run_time=1.6)
        pasos = [("-x-2x=-1-5", "Transponemos: x a un lado, números al otro"), ("-3x=-6", None), ("x=2", None)]
        prev = VGroup(a, igual, b)
        g = VGroup()
        for tex, nota in pasos:
            if nota:
                notas(nota)
            m = XY(tex, 48).next_to(prev, DOWN, buff=0.35).align_to(a, LEFT)
            self.play(Write(m))
            self.wait(0.5)
            g.add(m)
            prev = m
        notas("Sustituimos x = 2 en cualquiera de las despejadas")
        v = XY("y=5-2=3", 50).move_to([-6.0, -1.5, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(d1, v))
        r = XY("x=2,\\quad y=3", 48).move_to([2.6, -1.9, 0])
        cr = SurroundingRectangle(r, color=ACENTO, buff=0.2, corner_radius=0.1)
        self.play(Write(r), Create(cr))
        notas("Comprobamos:  2 + 3 = 5 ✓   y   2 · 2 − 3 = 1 ✓", color=OK)
        self.wait(3.5)
        notas.fin()


class TresMetodos(Scene):
    def construct(self):
        cab = titulo(self, "Tres métodos, la misma solución")
        notas = Notas(self)
        s = sistema("x+y=5", "2x-y=1", 40).move_to([0, 2.2, 0])
        self.play(Write(s))
        notas("Resolvemos el mismo sistema de las tres formas")
        cols = [("Sustitución", ["y=5-x", "2x-(5-x)=1", "3x-5=1", "x=2", "y=5-2=3"]),
                ("Igualación", ["y=5-x", "y=2x-1", "5-x=2x-1", "-3x=-6", "x=2,\\ y=3"]),
                ("Reducción", ["(1)+(2):", "3x=6", "x=2", "2+y=5", "y=3"])]
        grupos = VGroup()
        for k, (nom, lineas) in enumerate(cols):
            cx = -4.6 + k * 4.6
            t = texto(nom, 30, ACENTO).move_to([cx, 1.15, 0])
            self.play(FadeIn(t))
            g = VGroup(t)
            for i, tex in enumerate(lineas):
                m = XY(tex, 36).move_to([cx, 0.5 - i * 0.62, 0])
                self.play(Write(m), run_time=0.7)
                g.add(m)
            self.play(Circumscribe(g[-1], color=OK), run_time=0.6)
            grupos.add(g)
            self.wait(0.5)
        notas("¡Los tres dan x = 2, y = 3! El método no cambia la solución, solo el camino", color=OK)
        self.wait(3)
        self.play(FadeOut(grupos), FadeOut(s))
        notas.fin()
        self.wait(0.5)


class TiposSistemas(Scene):
    def construct(self):
        cab = titulo(self, "Tipos de sistemas")
        notas = Notas(self)
        sub = Sub(self, cab)
        ax, g_ax = ejes(xr=(-1, 6), yr=(-1, 6), centro=(3.4, -0.3, 0))
        casos = [
            ("Se cortan", ("x+y=4", "x-y=2"), (1, 1, 4), (1, -1, 2), (3, 1),
             ["2x=6\\ \\Rightarrow\\ x=3,\\ y=1"], "UNA solución", "Compatible determinado", OK,
             "Dos rectas que se cortan: un único punto común"),
            ("Paralelas", ("x+y=4", "x+y=1"), (1, 1, 4), (1, 1, 1), None,
             ["(1)-(2):\\quad 0=3"], "NINGUNA solución", "Incompatible", MAL,
             "Al restar desaparecen x e y y queda 0 = 3: ¡imposible! Las rectas nunca se cortan"),
            ("Coinciden", ("x+y=4", "2x+2y=8"), (1, 1, 4), (2, 2, 8), None,
             ["(2)-2\\cdot(1):\\quad 0=0"], "INFINITAS soluciones", "Compatible indeterminado", ACENTO,
             "La (2) es la (1) multiplicada por 2: es la MISMA recta. Queda 0 = 0, siempre cierto"),
        ]
        self.play(Create(g_ax))
        for nombre, (e1, e2), r1, r2, pt, cuentas, tsol, ttipo, col, nota in casos:
            sub(nombre)
            s = sistema(e1, e2, 42).move_to([-4.4, 2.0, 0])
            self.play(Write(s))
            l1 = recta(ax, *r1, E1C)
            l2 = recta(ax, *r2, E2C)
            if nombre == "Coinciden":
                l2 = DashedVMobject(l2, num_dashes=30)
            self.play(Create(l1))
            self.play(Create(l2))
            extra = VGroup()
            if pt:
                d = Dot(ax.c2p(*pt), color=ACENTO, radius=0.12)
                self.play(FadeIn(d, scale=2), Flash(d, color=ACENTO))
                extra.add(d)
            c = VGroup(*[XY(t, 40) for t in cuentas]).arrange(DOWN, aligned_edge=LEFT).move_to([-4.4, 0.4, 0])
            self.play(Write(c))
            t1 = texto(tsol, 34, col).move_to([-4.4, -0.7, 0])
            t2 = texto(ttipo, 26, GREY_B).next_to(t1, DOWN, buff=0.2)
            self.play(FadeIn(t1, shift=UP * 0.2))
            self.play(FadeIn(t2))
            notas(nota, color=col)
            self.wait(4)
            notas.fin()
            self.play(FadeOut(VGroup(s, l1, l2, extra, c, t1, t2)))
        self.play(FadeOut(g_ax))

        sub("Resumen")
        resumen = VGroup()
        for k, (tit, col, segs, t) in enumerate([
                ("Se cortan", OK, [((-0.8, -0.6), (0.8, 0.6)), ((-0.8, 0.6), (0.8, -0.6))], "1 solución"),
                ("Paralelas", MAL, [((-0.8, -0.2), (0.8, 0.5)), ((-0.8, -0.7), (0.8, 0.0))], "ninguna"),
                ("Coinciden", ACENTO, [((-0.8, -0.5), (0.8, 0.5))], "infinitas")]):
            caja = RoundedRectangle(width=3.4, height=3.0, corner_radius=0.2, color=col).move_to([-4.2 + k * 4.2, 0.2, 0])
            lineas = VGroup(*[Line(caja.get_center() + [u[0], u[1], 0], caja.get_center() + [v[0], v[1], 0],
                                   color=(E1C if i == 0 else E2C), stroke_width=5) for i, (u, v) in enumerate(segs)])
            if tit == "Coinciden":
                lineas.add(DashedLine(caja.get_center() + [-0.8, -0.5, 0], caja.get_center() + [0.8, 0.5, 0],
                                      color=E2C, stroke_width=5))
            lineas.shift(UP * 0.3)
            ti = texto(tit, 28, col).next_to(caja.get_top(), DOWN, buff=0.2)
            tt = texto(t, 28).next_to(caja.get_bottom(), UP, buff=0.25)
            g = VGroup(caja, lineas, ti, tt)
            self.play(FadeIn(g, shift=UP * 0.2))
            resumen.add(g)
        notas("Con métodos algebraicos: si sale 0 = número, no hay solución; si sale 0 = 0, hay infinitas")
        self.wait(4)
        notas.fin()


class NumeroSoluciones(Scene):
    def construct(self):
        cab = titulo(self, "¿Cuántas soluciones?", "Aprende +: sin resolver el sistema")
        notas = Notas(self)
        sub = Sub(self, cab)

        # --- 1. La idea: comparar columna a columna
        sub("Comparamos los coeficientes")

        def fila(i, col):
            t = MathTex(f"a_{{{i}}}", "x", "+", f"b_{{{i}}}", "y", "=", f"c_{{{i}}}", font_size=60, color=col)
            t[1].set_color(LETRA)
            t[4].set_color(Y_COL)
            return t

        f1, f2 = fila(1, E1C), fila(2, E2C)
        g = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 1.2, 0])
        llave = Brace(g, LEFT, buff=0.15)
        self.play(GrowFromCenter(llave), Write(f1), Write(f2))
        notas("Un sistema cualquiera: a, b y c son los números de cada ecuación")
        self.wait(2)
        fracs, cajas = VGroup(), VGroup()
        for j, colr, nom in [(0, LETRA, "a"), (3, Y_COL, "b"), (6, WHITE, "c")]:
            cajas.add(SurroundingRectangle(VGroup(f1[j], f2[j]), color=colr, buff=0.12, corner_radius=0.08))
            fracs.add(MathTex(f"\\dfrac{{{nom}_1}}{{{nom}_2}}", font_size=60, color=colr))
        fracs.arrange(RIGHT, buff=1.6).move_to([0, -1.3, 0])
        textos = ["Dividimos los números de la x...", "...los de la y...", "...y los números sueltos"]
        for k, j in enumerate((0, 3, 6)):
            notas(textos[k])
            self.play(Create(cajas[k]))
            self.play(TransformFromCopy(VGroup(f1[j], f2[j]), fracs[k]))
            self.wait(0.6)
        notas("¿Salen iguales o distintas? ¡Eso decide cuántas soluciones hay!", color=ACENTO)
        self.wait(3)
        notas.fin()
        self.play(FadeOut(VGroup(llave, f1, f2, cajas, fracs)))

        # --- 2. Tres casos: primero las fracciones, después las rectas lo confirman
        ax, g_ax = ejes(xr=(-1, 6), yr=(-1, 6), centro=(3.6, -0.3, 0))
        casos = [
            ("Proporciones distintas", ("x+2y=8", "3x-y=3"), (3, -1, 3), (2, 3),
             ["\\dfrac{1}{3}", "\\neq", "\\dfrac{2}{-1}"], [None, "-2"],
             "UNA solución", "Las rectas se cortan", OK, None,
             "Ya son distintas: no hace falta mirar los números sueltos",
             "Proporciones distintas → las rectas van inclinadas distinto → se cortan en un punto"),
            ("x e y iguales, el número no", ("x+2y=8", "2x+4y=6"), (2, 4, 6), None,
             ["\\dfrac{1}{2}", "=", "\\dfrac{2}{4}", "\\neq", "\\dfrac{8}{6}"], [None, "\\tfrac{1}{2}", "\\tfrac{4}{3}"],
             "NINGUNA solución", "Rectas paralelas", MAL, "(1)\\cdot 2:\\ \\ 2x+4y=16",
             "La x y la y van en la misma proporción (1/2), pero los números sueltos no (4/3)",
             "La (1) por 2 da 2x + 4y = 16, pero la (2) dice 6: misma inclinación, rectas distintas"),
            ("Todo en la misma proporción", ("x+2y=8", "3x+6y=24"), (3, 6, 24), None,
             ["\\dfrac{1}{3}", "=", "\\dfrac{2}{6}", "=", "\\dfrac{8}{24}"], [None, "\\tfrac{1}{3}", "\\tfrac{1}{3}"],
             "INFINITAS soluciones", "Es la misma recta", ACENTO, "(1)\\cdot 3:\\ \\ 3x+6y=24",
             "Las tres fracciones valen 1/3",
             "La (2) es la (1) multiplicada por 3: la MISMA recta → infinitas soluciones"),
        ]
        self.play(Create(g_ax))
        for nombre, (e1, e2), r2, pt, fila_f, simp, tsol, tdet, col, extra_tex, n1, n2 in casos:
            sub(nombre)
            s = sistema(e1, e2, 42).move_to([-3.9, 2.15, 0])
            self.play(Write(s))
            row = MathTex(*fila_f, font_size=50).move_to([-3.9, 0.55, 0])
            colores = [LETRA, ACENTO, Y_COL, ACENTO, WHITE]
            for i, m in enumerate(row):
                m.set_color(colores[i])
            simps = VGroup()
            for i, v in zip((0, 2, 4), simp):
                if v is not None:
                    simps.add(MathTex("=" + v, font_size=30, color=GREY_B).next_to(row[i], DOWN, buff=0.15))
            self.play(Write(row[0]))
            self.play(Write(row[2]))
            for m in simps[:1]:
                self.play(FadeIn(m), run_time=0.5)
            self.play(FadeIn(row[1], scale=1.6))
            if len(row) > 3:
                self.play(Write(row[4]))
                self.play(FadeIn(simps[1]), run_time=0.5)
                self.play(FadeIn(row[3], scale=1.6))
            notas(n1)
            self.wait(2.5)
            t1 = texto(tsol, 34, col).move_to([-3.9, -0.95, 0])
            t2 = texto(tdet, 26, GREY_B).next_to(t1, DOWN, buff=0.18)
            self.play(FadeIn(t1, shift=UP * 0.2), FadeIn(t2))
            extra = VGroup()
            if extra_tex:
                extra.add(XY(extra_tex, 36, E1C).move_to([-3.9, -2.2, 0]))
                self.play(Write(extra[0]))
            l1 = recta(ax, 1, 2, 8, E1C)
            l2 = recta(ax, *r2, E2C)
            if pt is None and r2[2] == 24:
                l2 = DashedVMobject(l2, num_dashes=30)
            self.play(Create(l1))
            self.play(Create(l2))
            if pt:
                d = Dot(ax.c2p(*pt), color=ACENTO, radius=0.12)
                self.play(FadeIn(d, scale=2), Flash(d, color=ACENTO))
                extra.add(d)
            notas(n2, color=col)
            self.wait(4)
            notas.fin()
            self.play(FadeOut(VGroup(s, row, simps, t1, t2, extra, l1, l2)))
        self.play(FadeOut(g_ax))

        # --- 3. Resumen
        sub("Resumen")
        reglas = [("\\dfrac{a_1}{a_2}\\neq\\dfrac{b_1}{b_2}", "→ UNA solución (se cortan)", OK),
                  ("\\dfrac{a_1}{a_2}=\\dfrac{b_1}{b_2}\\neq\\dfrac{c_1}{c_2}", "→ NINGUNA (paralelas)", MAL),
                  ("\\dfrac{a_1}{a_2}=\\dfrac{b_1}{b_2}=\\dfrac{c_1}{c_2}", "→ INFINITAS (coinciden)", ACENTO)]
        filas = VGroup()
        for k, (tex, txt, col) in enumerate(reglas):
            y = 1.5 - k * 1.55
            m = MathTex(tex, font_size=48).move_to([-5.0, y, 0], aligned_edge=LEFT)
            t = texto(txt, 32, col).move_to([-0.4, y, 0], aligned_edge=LEFT)
            filas.add(VGroup(m, t))
        card = tarjeta(filas, buff=0.4)
        self.play(Create(card[0]))
        for f in filas:
            self.play(Write(f[0]))
            self.play(FadeIn(f[1], shift=RIGHT * 0.2))
            self.wait(1.2)
        notas("Sin resolver ni dibujar, ya sabemos cuántas soluciones tiene")
        self.wait(3.5)
        notas.fin()
        self.play(FadeOut(VGroup(card, filas)))

        # --- 4. ¿Y si hay un 0?
        sub("¿Y si hay un 0?")
        s = sistema("x+y=5", "2y=4", 44).move_to([-4.0, 1.9, 0])
        self.play(Write(s))
        notas("En la (2) no hay x: su número es 0, y no se puede dividir entre 0")
        fr = MathTex("\\dfrac{a_1}{a_2}=\\dfrac{1}{0}", font_size=50).move_to([-4.0, 0.2, 0])
        fr[0][0:5].set_color(LETRA)
        self.play(Write(fr))
        cruz = Cross(fr, stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        self.wait(2)
        notas("Truco: en vez de dividir, multiplicamos en cruz", color=ACENTO)
        eq = MathTex("\\dfrac{a_1}{a_2}=\\dfrac{b_1}{b_2}", "\\ \\Longleftrightarrow\\ ", "a_1\\cdot b_2=a_2\\cdot b_1",
                     font_size=38).move_to([3.3, 1.7, 0])
        self.play(Write(eq))
        self.wait(2)
        m1 = MathTex("a_1\\cdot b_2=1\\cdot 2=2", font_size=40).move_to([3.3, 0.6, 0])
        m2 = MathTex("a_2\\cdot b_1=0\\cdot 1=0", font_size=40).move_to([3.3, -0.2, 0])
        m3 = MathTex("2\\neq 0", font_size=46, color=OK).move_to([3.3, -1.1, 0])
        t = texto("Distintos → UNA solución: x = 3, y = 2", 28, OK).move_to([3.3, -1.9, 0])
        self.play(Write(m1))
        self.play(Write(m2))
        self.play(FadeIn(m3, scale=1.4))
        self.play(FadeIn(t, shift=UP * 0.2))
        notas("Productos en cruz distintos: se cortan. Iguales: paralelas o la misma recta", color=OK)
        self.wait(4.5)
        notas.fin()


def animal(cx, y, patas=2):
    cuerpo = Circle(0.3, color=WHITE, fill_color="#E8D9B5", fill_opacity=0.9).move_to([cx, y, 0])
    pt = VGroup(*[Line([cx + dx, y - 0.28, 0], [cx + dx, y - 0.62, 0], stroke_width=4, color="#E8D9B5")
                  for dx in ((-0.1, 0.1) if patas == 2 else (-0.21, -0.07, 0.07, 0.21))])
    return VGroup(cuerpo, pt)


class Problemas(Scene):
    def construct(self):
        cab = titulo(self, "Problemas con sistemas")
        notas = Notas(self)
        sub = Sub(self, cab)
        sub("Gallinas y conejos")
        enun = texto("En una granja hay gallinas y conejos: 10 cabezas y 32 patas.\n¿Cuántos hay de cada?", 28)
        enun.move_to([0, 2.2, 0])
        self.play(FadeIn(enun))
        notas("Antes de las ecuaciones, pensémoslo con un dibujo: imaginamos que TODOS son gallinas")
        anim = [animal(-5.4 + k * 1.2, 0.6) for k in range(10)]
        self.play(LaggedStart(*[FadeIn(a) for a in anim], lag_ratio=0.1))
        cont = MathTex("20", "\\text{ patas}", font_size=44).move_to([0, -0.8, 0])
        self.play(Write(cont))
        notas("10 gallinas tienen 20 patas. ¡Faltan 12! Cada conejo tiene 2 patas más que una gallina")
        self.wait(2)
        total = 20
        for k in range(6):
            a = anim[9 - k]
            cx = a[0].get_center()[0]
            nuevo = animal(cx, 0.6, 4)
            nuevo[0].set_fill(Y_COL, 0.8)
            orejas = VGroup(*[Ellipse(width=0.12, height=0.34, color=Y_COL, fill_color=Y_COL, fill_opacity=0.8)
                              .move_to([cx + dx, 1.0, 0]) for dx in (-0.1, 0.1)])
            total += 2
            nc = MathTex(str(total), "\\text{ patas}", font_size=44).move_to(cont)
            self.play(Transform(a, VGroup(nuevo, orejas)), Transform(cont, nc), run_time=0.6)
        notas("Con 6 conejos llegamos a 32: 6 conejos y 4 gallinas", color=OK)
        self.wait(2.5)
        self.play(FadeOut(VGroup(*anim, cont)))
        notas("Ahora con un sistema: x = gallinas, y = conejos")
        s = sistema("x+y=10", "2x+4y=32", 42).move_to([-4.4, 0.9, 0])
        ex = VGroup(texto("cabezas", 24, E1C).next_to(s[1][0], RIGHT, buff=1.0),
                    texto("patas", 24, E2C).next_to(s[1][1], RIGHT, buff=1.0))
        self.play(Write(s), FadeIn(ex))
        pas = [("2x+2y=20", "Reducción: multiplicamos la (1) por 2"),
               ("2y=12", "Restamos a la (2): (2x + 4y) − (2x + 2y) = 2y  y  32 − 20 = 12"),
               ("y=6,\\quad x=10-6=4", None)]
        C(self, XY("x+y=10", 42, E1C), pas, 0.6, 0.9, notas, None, False, 42, dy=0.9)
        notas("4 gallinas y 6 conejos: ¡lo mismo que con el dibujo!", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)
        sub.olvidar()

        sub("En el cine")
        enun = texto("2 entradas de adulto y 3 de niño cuestan 31 €;\n1 de adulto y 2 de niño cuestan 18 €. ¿Cuánto vale cada una?", 28)
        enun.move_to([0, 2.2, 0])
        self.play(FadeIn(enun))
        notas("x = precio de adulto, y = precio de niño")
        s = sistema("2x+3y=31", "x+2y=18", 42).move_to([-4.4, 0.6, 0])
        self.play(Write(s))
        pas = [("2(18-2y)+3y=31", "Sustitución: en la (2), x = 18 − 2y. Lo llevamos a la (1)"),
               ("36-4y+3y=31", None), ("-y=-5\\ \\Rightarrow\\ y=5", None),
               ("x=18-2\\cdot 5=8", "Volvemos a x = 18 − 2y")]
        C(self, XY("x=18-2y", 44), pas, 0.4, 1.0, notas, None, False, 44, dy=0.85)
        notas("Adulto 8 €, niño 5 €.  Comprobamos: 16 + 15 = 31 ✓  y  8 + 10 = 18 ✓", color=OK)
        self.wait(3.5)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios
def s_txt(e1, e2):
    return f"{{ {e1} ;  {e2} }}"


def enunciados_1():
    return [
        ("1. Comprueba si x = 2, y = 1 es solución del sistema:",
         lista([s_txt("x + y = 3", "x − y = 1"), s_txt("2x + y = 5", "x + 3y = 6"), s_txt("3x − y = 5", "x + 2y = 4")], 3)),
        ("2. Resuelve gráficamente:", lista([s_txt("x + y = 6", "x − y = 2"), s_txt("y = 2x", "x + y = 3")], 2)),
        ("3. Resuelve por sustitución:",
         lista([s_txt("x + y = 7", "2x − y = 5"), s_txt("x − 2y = 1", "3x + y = 10"), s_txt("2x + 3y = 12", "x + y = 5")], 3)),
    ]


def enunciados_2():
    return [
        ("4. Resuelve por reducción:",
         lista([s_txt("x + y = 8", "x − y = 2"), s_txt("2x + y = 9", "3x − y = 11"), s_txt("3x + 2y = 7", "x + y = 3")], 3)),
        ("5. Resuelve por igualación:", lista([s_txt("y = x + 1", "y = 3x − 3"), s_txt("x + y = 6", "x − y = 4")], 2)),
        ("6. Sin dibujar, ¿cuántas soluciones tiene?",
         lista([s_txt("x + y = 3", "2x + 2y = 6"), s_txt("x − y = 1", "x − y = 4"), s_txt("x + y = 5", "x − y = 3")], 3)),
    ]


def enunciados_3():
    return [
        ("7. Dos números suman 25 y su diferencia es 7. ¿Cuáles son?", ""),
        ("8. En una granja hay 15 animales entre gallinas y cerdos, y 44 patas. ¿Cuántos hay de cada?", ""),
        ("9. 3 cuadernos y 2 bolígrafos cuestan 8 €; 1 cuaderno y 4 bolígrafos, 6 €. ¿Cuánto vale cada cosa?", ""),
    ]


COMPRUEBA = [
    (("x+y=3", "x-y=1"), ["2+1=3", "2-1=1"], [True, True]),
    (("2x+y=5", "x+3y=6"), ["2\\cdot 2+1=5", "2+3\\cdot 1=5\\neq 6"], [True, False]),
    (("3x-y=5", "x+2y=4"), ["3\\cdot 2-1=5", "2+2\\cdot 1=4"], [True, True]),
]
GRAFICO = [
    (("x+y=6", "x-y=2"), (1, 1, 6), (1, -1, 2), (4, 2), [(0, 6), (6, 0)], [(2, 0), (6, 4)]),
    (("y=2x", "x+y=3"), (-2, 1, 0), (1, 1, 3), (1, 2), [(0, 0), (3, 6)], [(0, 3), (3, 0)]),
]
SUSTIT = [
    (("x+y=7", "2x-y=5"), [("x=7-y", "Despejamos x en la (1)"), ("2(7-y)-y=5", "Sustituimos en la (2)"),
                            ("14-3y=5", None), ("y=3", None), ("x=7-3=4", "Volvemos a lo despejado")]),
    (("x-2y=1", "3x+y=10"), [("x=1+2y", "Despejamos x en la (1)"), ("3(1+2y)+y=10", None), ("3+7y=10", None),
                             ("y=1", None), ("x=1+2=3", None)]),
    (("2x+3y=12", "x+y=5"), [("x=5-y", "Despejamos x en la (2): no tiene número delante"), ("2(5-y)+3y=12", None),
                             ("10+y=12", None), ("y=2", None), ("x=5-2=3", None)]),
]
REDUC = [
    (("x+y=8", "x-y=2"), [("2x=10", "Sumamos: +y y −y se anulan"), ("x=5", None),
                          ("5+y=8\\ \\Rightarrow\\ y=3", "Sustituimos en la (1)")]),
    (("2x+y=9", "3x-y=11"), [("5x=20", "Sumamos"), ("x=4", None), ("8+y=9\\ \\Rightarrow\\ y=1", None)]),
    (("3x+2y=7", "x+y=3"), [("-2x-2y=-6", "Multiplicamos la (2) por −2"),
                            ("x=1", "Sumamos con la (1): 3x − 2x = x  y  7 − 6 = 1"),
                            ("1+y=3\\ \\Rightarrow\\ y=2", None)]),
]
IGUAL = [
    (("y=x+1", "y=3x-3"), [("x+1=3x-3", "Las dos ya tienen la y despejada: igualamos"), ("-2x=-4", None),
                           ("x=2", None), ("y=2+1=3", None)]),
    (("x+y=6", "x-y=4"), [("y=6-x,\\quad y=x-4", "Despejamos y en las dos"), ("6-x=x-4", "Igualamos"),
                          ("-2x=-10", None), ("x=5,\\quad y=1", None)]),
]
TIPOS = [
    (("x+y=3", "2x+2y=6"), "(2)-2\\cdot(1):\\quad 0=0", "Infinitas soluciones", ACENTO,
     "La (2) es la (1) multiplicada por 2: la misma recta"),
    (("x-y=1", "x-y=4"), "(1)-(2):\\quad 0=-3", "Ninguna solución", MAL, "0 = −3 es imposible: rectas paralelas"),
    (("x+y=5", "x-y=3"), "2x=8\\ \\Rightarrow\\ x=4,\\ y=1", "Una solución", OK, "Sumando sale x = 4 e y = 1: se cortan"),
]
PROBLEMAS_EJ = {
    7: ("Dos números suman 25 y su diferencia es 7. ¿Cuáles son?", ("x+y=25", "x-y=7"),
        [("2x=32", "Reducción: sumamos"), ("x=16", None), ("y=25-16=9", None)],
        "x = el mayor, y = el menor", "Los números son 16 y 9.  Comprobamos: 16 + 9 = 25 ✓  16 − 9 = 7 ✓"),
    8: ("En una granja hay 15 animales entre gallinas y cerdos, y 44 patas.", ("x+y=15", "2x+4y=44"),
        [("2x+2y=30", "Multiplicamos la (1) por 2"), ("2y=14", "Restamos a la (2)"), ("y=7,\\quad x=15-7=8", None)],
        "x = gallinas (2 patas), y = cerdos (4 patas)", "8 gallinas y 7 cerdos.  Comprobamos: 16 + 28 = 44 ✓"),
    9: ("3 cuadernos y 2 bolígrafos cuestan 8 €; 1 cuaderno y 4 bolígrafos, 6 €.", ("3x+2y=8", "x+4y=6"),
        [("x=6-4y", "Sustitución: despejamos x en la (2)"), ("3(6-4y)+2y=8", None), ("18-10y=8", None),
         ("y=1,\\quad x=6-4=2", None)],
        "x = cuaderno, y = bolígrafo", "Cuaderno 2 €, bolígrafo 1 €.  Comprobamos: 6 + 2 = 8 ✓  2 + 4 = 6 ✓"),
}


def ej_comprueba(scene, i, x, y, notas, ejemplo=False):
    (e1, e2), filas, oks = COMPRUEBA[i]
    et = texto(f"{'abc'[i]})", 28)
    s = sistema(e1, e2, 40, numeros=False).move_to([x, y, 0], aligned_edge=LEFT)
    et.next_to(s, LEFT, buff=0.25)
    scene.play(FadeIn(et), Write(s))
    if ejemplo:
        notas("Sustituimos x = 2 e y = 1 en las DOS ecuaciones")
    g = VGroup(et, s)
    prev = s
    for tex, ok, colr in zip(filas, oks, (E1C, E2C)):
        m = MathTex(tex, "\\ \\checkmark" if ok else "\\ \\times", font_size=38, color=colr)
        m[1].set_color(OK if ok else MAL)
        m.next_to(prev, DOWN, buff=0.3).align_to(s, LEFT).shift(RIGHT * 0.3)
        scene.play(Write(m))
        g.add(m)
        prev = m
    v = texto("Sí es solución" if all(oks) else "No es solución (falla la segunda)", 28, OK if all(oks) else MAL)
    v.next_to(prev, DOWN, buff=0.3).align_to(s, LEFT)
    scene.play(FadeIn(v))
    scene.wait(1.5 if ejemplo else 0.8)
    g.add(v)
    return g


def ej_grafico(scene, i, notas, ejemplo=False):
    (e1, e2), r1, r2, pt, p1, p2 = GRAFICO[i]
    s = sistema(e1, e2, 42).move_to([-4.6, 2.0, 0])
    scene.play(Write(s))
    ax, g_ax = ejes(xr=(-1, 7), yr=(-1, 7), xl=5.6, yl=5.2, centro=(3.3, -0.4, 0))
    scene.play(Create(g_ax))
    if ejemplo:
        notas("Dos puntos de cada recta (damos valores a x)")
    t = VGroup(texto("(1): " + ", ".join(f"({u}, {v})" for u, v in p1), 26, E1C),
               texto("(2): " + ", ".join(f"({u}, {v})" for u, v in p2), 26, E2C)).arrange(DOWN, aligned_edge=LEFT)
    t.move_to([-4.6, 0.4, 0])
    scene.play(FadeIn(t[0]), *[FadeIn(Dot(ax.c2p(u, v), color=E1C, radius=0.07)) for u, v in p1])
    scene.play(Create(recta(ax, *r1, E1C)))
    scene.play(FadeIn(t[1]), *[FadeIn(Dot(ax.c2p(u, v), color=E2C, radius=0.07)) for u, v in p2])
    scene.play(Create(recta(ax, *r2, E2C)))
    d = Dot(ax.c2p(*pt), color=ACENTO, radius=0.12)
    scene.play(FadeIn(d, scale=2), Flash(d, color=ACENTO), Create(proyecciones(ax, *pt)))
    r = XY(f"x={pt[0]},\\quad y={pt[1]}", 44).move_to([-4.6, -1.0, 0])
    scene.play(Write(r), Create(SurroundingRectangle(r, color=ACENTO, buff=0.15)))
    notas(f"Se cortan en ({pt[0]}, {pt[1]})")
    scene.wait(2)
    notas.fin()


def ej_metodo(scene, datos, i, x, y, notas, ejemplo=False, size=44, dy=0.85):
    (e1, e2), pasos = datos[i]
    s = sistema(e1, e2, size)
    return C(scene, s, pasos, x, y, notas, f"{'abc'[i]})", ejemplo, size, dy)


def ej_tipos(scene, idx, notas, ejemplo=False):
    if ejemplo:
        notas("Intentamos reducir: si desaparecen x e y, miramos lo que queda")
    for k, i in enumerate(idx):
        (e1, e2), cuentas, tsol, col, nota = TIPOS[i]
        y = 1.5 - k * 1.85
        et = texto(f"{'abc'[i]})", 28).move_to([-6.4, y, 0])
        s = sistema(e1, e2, 38, numeros=False).next_to(et, RIGHT, buff=0.3)
        c = XY(cuentas, 36).move_to([0.6, y, 0])
        t = texto(tsol, 28, col).move_to([4.7, y, 0])
        scene.play(FadeIn(et), Write(s))
        scene.play(Write(c))
        scene.play(FadeIn(t, shift=LEFT * 0.2))
        notas(nota, color=col)
        scene.wait(1.6 if ejemplo else 1.0)
    notas.fin()


def ej_problema(scene, n, notas, ejemplo=False):
    enun, (e1, e2), pasos, inc, fin = PROBLEMAS_EJ[n]
    t = texto(enun, 28).move_to([0, 2.2, 0])
    if t.width > 13:
        t.scale_to_fit_width(13)
    scene.play(FadeIn(t))
    notas(inc)
    scene.wait(1.2)
    s = sistema(e1, e2, 44)
    C(scene, s, pasos, -4.0, 0.9, notas, None, ejemplo, 44, dy=0.85)
    notas(fin, color=OK)
    scene.wait(3)
    notas.fin()


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Sistemas de ecuaciones")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        ej_comprueba(self, 0, -2.0, 1.4, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        ej_grafico(self, 0, notas, ejemplo=True)
        limpiar(self, cab)
        for n, datos in ((3, SUSTIT), (4, REDUC), (5, IGUAL)):
            subtitulo(self, cab, f"Ejercicio {n} a)")
            ej_metodo(self, datos, 0, -3.4, 2.0, notas, ejemplo=True, size=44, dy=0.82)
            self.wait(1)
            notas.fin()
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        ej_tipos(self, [0], notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7")
        ej_problema(self, 7, notas, ejemplo=True)
        limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 3")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1: b) y c)")
        ej_comprueba(self, 1, -5.6, 1.4, notas)
        ej_comprueba(self, 2, 1.2, 1.4, notas)
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 b)")
        ej_grafico(self, 1, notas)
        limpiar(self, cab)
        for i in (1, 2):
            subtitulo(self, cab, f"Ejercicio 3 {'abc'[i]})")
            ej_metodo(self, SUSTIT, i, -3.4, 2.0, notas, size=44, dy=0.82)
            self.wait(1)
            notas.fin()
            limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 4 a 9.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 4 a 9")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 4: b) y c)")
        ej_metodo(self, REDUC, 1, -6.2, 1.7, notas, size=40, dy=0.85)
        ej_metodo(self, REDUC, 2, 0.6, 1.7, notas, size=40, dy=0.85)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 b)")
        ej_metodo(self, IGUAL, 1, -3.4, 1.7, notas, size=46, dy=0.9)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6: b) y c)")
        ej_tipos(self, [1, 2], notas)
        limpiar(self, cab)
        for n in (8, 9):
            subtitulo(self, cab, f"Ejercicio {n}")
            ej_problema(self, n, notas)
            limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
