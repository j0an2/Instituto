"""Estilo común para todas las animaciones de Matemáticas 1º ESO."""
import os

from manim import *

# Paleta
FONDO = "#1e1e2e"
TEXTO = WHITE
ACENTO = YELLOW
OK = GREEN
MAL = RED

# Números enteros (temas 3 y 4): positivos cálidos, negativos fríos
POSITIVO = "#FF9F43"
NEGATIVO = "#4FC3F7"
MENOS = "−"  # signo menos tipográfico para Text()


def color_entero(n):
    return POSITIVO if n > 0 else NEGATIVO if n < 0 else WHITE


def fmt_entero(n, mas=True):
    """'+3', '−3', '0' (para Text)."""
    if n == 0:
        return "0"
    return (f"+{n}" if mas else str(n)) if n > 0 else f"{MENOS}{abs(n)}"


def s_ent(n, mas=True):
    """Cadena LaTeX de un entero con el signo pegado: '{+3}', '{-3}', '{0}'."""
    s = "0" if n == 0 else (f"+{n}" if mas else str(n)) if n > 0 else str(n)
    return "{" + s + "}"


def par_ent(n):
    """Entero entre paréntesis para LaTeX: '(+3)', '(-3)'."""
    return "(" + ("0" if n == 0 else f"+{n}" if n > 0 else str(n)) + ")"


def tex_entero(n, mas=True, size=40):
    return MathTex(s_ent(n, mas), font_size=size, color=color_entero(n))


def expr_enteros(*items, size=52, parentesis=True):
    """MathTex a partir de enteros (coloreados, entre paréntesis) y operadores (str)."""
    partes, colores = [], []
    for it in items:
        if isinstance(it, int):
            partes.append(par_ent(it) if parentesis else s_ent(it))
            colores.append(color_entero(it))
        else:
            partes.append(it)
            colores.append(None)
    t = MathTex(*partes, font_size=size)
    for i, c in enumerate(colores):
        if c:
            t[i].set_color(c)
    return t


def recta_enteros(a=-6, b=6, largo=12.0, y=0.0, size=32):
    """NumberLine con etiquetas coloreadas. Devuelve (VGroup(linea, etiquetas), linea)."""
    linea = NumberLine(x_range=[a, b, 1], length=largo, include_tip=False, stroke_width=3,
                       tick_size=0.1).move_to([0, y, 0])
    etiquetas = VGroup(*[tex_entero(n, mas=False, size=size).next_to(linea.n2p(n), DOWN, buff=0.22)
                         for n in range(a, b + 1)])
    return VGroup(linea, etiquetas), linea


def salto(scene, punto, linea, desde, hasta, color, paso=1, rt=0.35, alto=0.25):
    """Mueve 'punto' por la recta de 'desde' a 'hasta' en saltos de 'paso', dejando rastro."""
    traza = VGroup()
    d = paso if hasta > desde else -paso
    k = desde
    while k != hasta:
        a, b = linea.n2p(k) + UP * alto, linea.n2p(k + d) + UP * alto
        arco = ArcBetweenPoints(a, b, angle=-PI / 1.5 * (1 if d > 0 else -1))
        t = DashedVMobject(arco.copy().set_stroke(color, 3))
        scene.play(MoveAlongPath(punto, arco), Create(t), run_time=rt * (1 + 0.3 * (paso - 1)), rate_func=linear)
        traza.add(t)
        k += d
    return traza


def ficha_entero(signo, r=0.3):
    """Ficha + (naranja) o − (azul)."""
    col = POSITIVO if signo > 0 else NEGATIVO
    c = Circle(radius=r, fill_color=col, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    t = Text("+" if signo > 0 else MENOS, font_size=int(r * 120), color=WHITE, weight=BOLD).move_to(c)
    g = VGroup(c, t)
    g.signo = signo
    return g


# Fracciones (tema 5 en adelante): numerador verde, denominador lila, parte tomada amarilla
NUMERADOR = "#7BD88F"
DENOMINADOR = "#C39BD3"
VACIO = "#3a3a4a"


def fraccion(n, d, size=48, colores=True, color=None):
    """Fracción dibujada a mano: VGroup(numerador, raya, denominador)."""
    k = size / 48
    cn = color or (NUMERADOR if colores else WHITE)
    cd = color or (DENOMINADOR if colores else WHITE)
    num = MathTex(str(n), font_size=size, color=cn)
    den = MathTex(str(d), font_size=size, color=cd)
    w = max(num.width, den.width) + 0.18 * k
    raya = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3 * k, color=color or WHITE)
    num.next_to(raya, UP, buff=0.1 * k)
    den.next_to(raya, DOWN, buff=0.1 * k)
    g = VGroup(num, raya, den)
    g.n, g.d = n, d
    return g


def cadena(*items, size=48, buff=0.3):
    """Fila de fracciones (tuplas (n, d) o mobjects) y símbolos (str)."""
    partes = []
    for it in items:
        if isinstance(it, tuple):
            partes.append(fraccion(*it, size=size))
        elif isinstance(it, str):
            partes.append(MathTex(it, font_size=size))
        else:
            partes.append(it)
    return VGroup(*partes).arrange(RIGHT, buff=buff)


def barra(partes, tomadas, ancho=6.0, alto=0.9, color=ACENTO):
    """Barra dividida en 'partes' iguales con 'tomadas' coloreadas."""
    w = ancho / partes
    g = VGroup(*[Rectangle(width=w, height=alto, stroke_color=WHITE, stroke_width=2,
                           fill_color=color if i < tomadas else VACIO, fill_opacity=1)
                 for i in range(partes)]).arrange(RIGHT, buff=0)
    return g


def pizza(partes, tomadas, r=1.3, color=ACENTO):
    """Círculo dividido en 'partes' sectores iguales (en sentido horario desde arriba)."""
    a = TAU / partes
    return VGroup(*[AnnularSector(inner_radius=0, outer_radius=r, angle=a, start_angle=PI / 2 - (i + 1) * a,
                                  stroke_color=WHITE, stroke_width=2,
                                  fill_color=color if i < tomadas else VACIO, fill_opacity=1)
                    for i in range(partes)])


# Decimales (tema 6 en adelante): un color fijo por posición
COLOR_POS = {"M": "#C9B6E4", "C": "#8E9AAF", "D": "#B8C0CC", "U": WHITE,
             "d": "#5DADE2", "c": "#58D68D", "m": "#EB984E", "x": "#F4D03F"}
NOMBRE_POS = {"M": "millares", "C": "centenas", "D": "decenas", "U": "unidades",
              "d": "décimas", "c": "centésimas", "m": "milésimas", "x": "diezmilésimas"}


def dec_txt(x, n):
    """Número con n decimales y coma: dec_txt(0.37, 2) -> '0,37'."""
    return f"{x:.{n}f}".replace(".", ",")


def tex_decimal(s, size=48, colores=True):
    """MathTex de un decimal escrito con coma ('34,072'), un trozo por cifra, coloreado por posición."""
    ent, coma, dec = s.partition(",")
    partes, cols = [], []
    for i, ch in enumerate(ent):
        partes.append(ch)
        cols.append(COLOR_POS["UDCM"[len(ent) - 1 - i]])
    if coma:
        partes.append("{,}")
        cols.append(WHITE)
    for i, ch in enumerate(dec):
        partes.append(ch)
        cols.append(COLOR_POS["dcmx"[i]])
    t = MathTex(*partes, font_size=size)
    if colores:
        for p, c in zip(t, cols):
            p.set_color(c)
    t.posiciones = [("UDCM"[len(ent) - 1 - i]) for i in range(len(ent))] + ([","] if coma else []) + \
        ["dcmx"[i] for i in range(len(dec))]
    return t


def tabla_posiciones(cols, filas=1, centro=ORIGIN, w=1.15, h=0.85, nombres=True):
    """Tabla de valor posicional. cols p.ej. ['C','D','U',',','d','c','m'].
    Devuelve (VGroup dibujable, dict {(fila, col): centro de la casilla})."""
    anchos = [0.45 if c == "," else w for c in cols]
    total = sum(anchos)
    x = -total / 2
    grupo, centros = VGroup(), {}
    for c, a in zip(cols, anchos):
        cx = x + a / 2
        if c != ",":
            cab = Rectangle(width=a, height=0.6, stroke_color=GREY_B, stroke_width=2,
                            fill_color=COLOR_POS[c], fill_opacity=0.25).move_to([cx, h * filas / 2 + 0.3, 0])
            letra = MathTex(c, font_size=36, color=COLOR_POS[c]).move_to(cab)
            grupo.add(cab, letra)
            if nombres:
                grupo.add(Text(NOMBRE_POS[c], font_size=15, color=COLOR_POS[c]).next_to(cab, UP, buff=0.08))
        for f in range(filas):
            cy = h * filas / 2 - h * (f + 0.5)
            if c != ",":
                grupo.add(Rectangle(width=a, height=h, stroke_color=GREY_B, stroke_width=2).move_to([cx, cy, 0]))
            centros[(f, c)] = np.array([cx, cy, 0])
        x += a
    grupo.shift(centro)
    centros = {k: v + np.array(centro) for k, v in centros.items()}
    return grupo, centros


# Colores por número primo (criba, factorización...)
COLOR_PRIMO = {2: BLUE, 3: GREEN, 5: ORANGE, 7: PURPLE}

config.background_color = FONDO


def titulo(scene, texto, subtitulo=None):
    """Muestra un título centrado, lo sube a la esquina y lo devuelve."""
    t = Text(texto, font_size=56, weight=BOLD)
    grupo = VGroup(t)
    if subtitulo:
        s = Text(subtitulo, font_size=30, color=GREY_B).next_to(t, DOWN)
        grupo.add(s)
    scene.play(Write(t))
    if subtitulo:
        scene.play(FadeIn(grupo[1], shift=UP * 0.3))
    scene.wait(1)
    pequeno = Text(texto, font_size=32, weight=BOLD).to_corner(UL)
    scene.play(ReplacementTransform(t, pequeno), *[FadeOut(m) for m in grupo[1:]])
    return pequeno


def texto(cadena, size=34, color=TEXTO, **kw):
    return Text(cadena, font_size=size, color=color, **kw)


def es_primo(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def pieza(p, r=0.32):
    """Ficha circular de un primo con su color fijo (los «ladrillos»)."""
    circ = Circle(radius=r, fill_color=COLOR_PRIMO.get(p, GREY), fill_opacity=1,
                  stroke_color=WHITE, stroke_width=2)
    num = Text(str(p), font_size=int(r * 85), color=WHITE, weight=BOLD).move_to(circ)
    g = VGroup(circ, num)
    g.valor = p
    return g


# ---------------------------------------------------------------------------
# Xola, la mascota: aparece en una esquina, cambia de expresión y habla con bocadillo.
# Expresiones (1ESO/mascota/xola/*.png): saluda, celebra, duda, idea, ok, pensando,
# senala, sorpresa, triste.
# ---------------------------------------------------------------------------
DIR_XOLA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "mascota", "xola"))


class Xola:
    def __init__(self, scene, alto=2.0, esquina=DR, buff=0.25):
        self.scene, self.alto, self.esquina, self.buff = scene, alto, esquina, buff
        self.img = None
        self.globo = None

    def _imagen(self, expr):
        im = ImageMobject(os.path.join(DIR_XOLA, expr + ".png")).set_height(self.alto)
        return im.to_corner(self.esquina, buff=self.buff)

    def _bocadillo(self, frase, size=24):
        t = Text(frase, font_size=size, color="#1e1e2e", line_spacing=0.9)
        caja = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.4, corner_radius=0.2,
                                fill_color=WHITE, fill_opacity=1, stroke_color=WHITE)
        lado = 1 if self.esquina[0] > 0 else -1          # globo encima de la Xola, pegado al borde de la pantalla
        caja.next_to(self.img, UP, buff=0.3).align_to(self.img, lado * RIGHT)
        t.move_to(caja)
        base = caja.get_edge_center(DOWN) * [0, 1, 0] + self.img.get_center() * [1, 0, 0]
        pico = Polygon(base + LEFT * 0.18, base + RIGHT * 0.18, base + DOWN * 0.3,
                       fill_color=WHITE, fill_opacity=1, stroke_width=0)
        return VGroup(pico, caja, t).set_z_index(5)

    def _quitar_globo(self):
        if self.globo is None:
            return []
        g, self.globo = self.globo, None
        return [FadeOut(g)]

    def entra(self, expr="saluda", frase=None, espera=1.5):
        self.img = self._imagen(expr).set_z_index(4)
        self.scene.play(FadeIn(self.img, shift=UP * 0.4), run_time=0.6)
        if frase:
            self.dice(frase, espera)

    def dice(self, frase, espera=1.5):
        anims = self._quitar_globo()
        self.globo = self._bocadillo(frase)
        self.scene.play(*anims, FadeIn(self.globo, scale=0.8), run_time=0.4)
        if espera:
            self.scene.wait(espera)

    def cambia(self, expr, frase=None, espera=1.5):
        if self.img is None:
            return self.entra(expr, frase, espera)
        nueva = self._imagen(expr).set_z_index(4)
        anims = [FadeOut(self.img), FadeIn(nueva)] + self._quitar_globo()
        self.scene.play(*anims, run_time=0.4)
        self.img = nueva
        if expr == "celebra":
            self.scene.play(self.img.animate.shift(UP * 0.3), rate_func=there_and_back, run_time=0.4)
        if frase:
            self.dice(frase, espera)

    def calla(self):
        anims = self._quitar_globo()
        if anims:
            self.scene.play(*anims, run_time=0.3)

    def sale(self):
        if self.img is None:
            return
        self.scene.play(FadeOut(self.img, shift=DOWN * 0.4), *self._quitar_globo(), run_time=0.5)
        self.img = None
