r"""Tema 9 · Magnitudes y medida (1º ESO) — unidad 8 del libro

Escenas:
    Magnitudes              – qué se puede medir; medir es comparar (palmos, clips, el metro)
    SistemaMetrico          – múltiplos y submúltiplos: kilo, hecto, deca, deci, centi, mili
    Longitud                – la escalera km … mm: bajar ×10, subir :10
    MasaCapacidad           – la misma escalera con g y con L; la tonelada; 1 L de agua pesa 1 kg
    Superficie              – 1 m² = 100 dm² (cuadrícula); escalera de 100 en 100; ha, a, ca
    Volumen                 – 1 dm³ = 1000 cm³ (cubitos); de 1000 en 1000; 1 dm³ = 1 L; la pecera
    Tiempo                  – sistema sexagesimal: de 60 en 60; h, min, s; 1,5 h ≠ 1 h 50 min
    Monedas                 – el euro: monedas y billetes, 1 € = 100 céntimos, 3,5 € ≠ 3 € 5 c, cambio de moneda
    ComplejasIncomplejas    – 3 km 25 m 4 dm ↔ 3025,4 m con la tabla; también tiempo y dinero
    Operaciones             – sumar/restar en la misma unidad; sumar y restar tiempos (desagrupando); × y :
    EjerciciosEjemplo / EjerciciosResueltos1 / EjerciciosResueltos2  (10 ejercicios)
Orden del libro (unidad 8): magnitudes · SMD (longitud, masa, capacidad) · superficie y volumen · sexagesimal ·
monetarias · forma compleja e incompleja · operaciones.

Ilustraciones (ComfyUI, img/t09/*_card.png): palmos, balanza, camion, botella, campo, piscina, pecera, crono.

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\venvs\manim\Scripts\python.exe -m manim -pql t09_medida.py Longitud
    ~\venvs\manim\Scripts\python.exe publicar.py t09_medida.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COD_2ESO = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "2ESO", "Matematicas", "codigo"))
sys.path.append(COD_2ESO)          # al final: los nombres de 1.º tienen prioridad
from estilo import *  # noqa: E402,F403
from potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t03_lenguaje_algebraico import lista, pagina_enunciados, tarjeta  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 9 · Magnitudes y medida"
TITULOS = {
    "Magnitudes": "Magnitudes: ¿qué se puede medir?",
    "SistemaMetrico": "El Sistema Métrico Decimal",
    "Longitud": "Unidades de longitud: la escalera",
    "MasaCapacidad": "Unidades de masa y de capacidad",
    "Superficie": "Unidades de superficie",
    "Volumen": "Unidades de volumen",
    "Tiempo": "El sistema sexagesimal: horas, minutos y segundos",
    "Monedas": "Unidades monetarias: el euro",
    "ComplejasIncomplejas": "Forma compleja e incompleja",
    "Operaciones": "Operaciones con medidas",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 4)",
    "EjerciciosResueltos2": "Ejercicios resueltos (5 a 10)",
}

IMG = os.path.join(AQUI, "img", "t09")
LONG, MASA, CAPA = "#5DADE2", "#FF9F43", "#7BD88F"
SUPE, VOLU, TIEM = "#C39BD3", "#FF79C6", "#F7DC6F"
MADERA = "#B9770E"

U_LONG = ["km", "hm", "dam", "m", "dm", "cm", "mm"]
U_MASA = ["kg", "hg", "dag", "g", "dg", "cg", "mg"]
U_CAPA = ["kL", "hL", "daL", "L", "dL", "cL", "mL"]
U_SUPE = ["km²", "hm²", "dam²", "m²", "dm²", "cm²", "mm²"]
U_VOLU = ["km³", "hm³", "dam³", "m³", "dm³", "cm³", "mm³"]


def ilustracion(nombre, alto=2.0):
    return ImageMobject(os.path.join(IMG, f"{nombre}_card.png")).set_height(alto)


def ajusta(m, ancho=None):
    ancho = ancho or config.frame_width - 1.0
    if m.width > ancho:
        m.scale_to_fit_width(ancho)
    return m


# ---------------------------------------------------------------------------
# La escalera de unidades
def escalera(unidades, color, x0=-5.8, y0=2.2, dx=1.45, dy=0.63, w=1.25, size=30, base=3):
    g = VGroup()
    for i, u in enumerate(unidades):
        c = RoundedRectangle(corner_radius=0.08, width=w, height=0.52, stroke_color=color,
                             fill_color=color, fill_opacity=0.45 if i == base else 0.15)
        c.move_to([x0 + i * dx, y0 - i * dy, 0])
        g.add(VGroup(c, Text(u, font_size=size, weight=BOLD if i == base else NORMAL).move_to(c)))
    return g


def flecha_escalon(esc, i, j, etiqueta, color):
    if j > i:                               # bajar: hacia la derecha y abajo
        a = esc[i].get_right() + RIGHT * 0.04
        b = esc[j].get_top() + UP * 0.04
        f = CurvedArrow(a, b, angle=-PI / 2, color=color, stroke_width=4, tip_length=0.15)
        lab = Text(etiqueta, font_size=26, color=color).move_to((a + b) / 2 + np.array([0.42, 0.2, 0]))
    else:                                   # subir: hacia la izquierda y arriba
        a = esc[i].get_left() + LEFT * 0.04
        b = esc[j].get_bottom() + DOWN * 0.04
        f = CurvedArrow(a, b, angle=-PI / 2, color=color, stroke_width=4, tip_length=0.15)
        lab = Text(etiqueta, font_size=26, color=color).move_to((a + b) / 2 + np.array([-0.42, -0.2, 0]))
    return VGroup(f, lab)


def regla_escalera(esc, factor):
    """Cartel con la regla: bajar un escalón ×factor, subir :factor."""
    r = VGroup(
        VGroup(Arrow(UP * 0.3 + LEFT * 0.3, DOWN * 0.3 + RIGHT * 0.3, color=OK, buff=0, stroke_width=5),
               texto(f"Bajar un escalón: × {factor}", 26, OK)).arrange(RIGHT, buff=0.25),
        VGroup(Arrow(DOWN * 0.3 + RIGHT * 0.3, UP * 0.3 + LEFT * 0.3, color=NEGATIVO, buff=0, stroke_width=5),
               texto(f"Subir un escalón: : {factor}", 26, NEGATIVO)).arrange(RIGHT, buff=0.25),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    return tarjeta(r, GREY_B, 0.25)


def convertir(scene, esc, i, j, factor, tex, nota, notas, y=-2.45, size=46, espera=2.0):
    """Flechas escalón a escalón de i a j y la cuenta abajo a la izquierda. Devuelve lo que hay que borrar."""
    paso = 1 if j > i else -1
    color = OK if j > i else NEGATIVO
    signo = "×" if j > i else ":"
    scene.play(Indicate(esc[i], color=ACENTO, scale_factor=1.15))
    fl = VGroup()
    for k in range(i, j, paso):
        f = flecha_escalon(esc, k, k + paso, f"{signo}{factor}", color)
        scene.play(Create(f[0]), FadeIn(f[1]), run_time=0.6)
        fl.add(f)
    scene.play(Indicate(esc[j], color=ACENTO, scale_factor=1.15))
    if nota:
        notas(nota)
    cuenta = tex if isinstance(tex, Mobject) else MathTex(tex, font_size=size)
    cuenta = ajusta(cuenta).move_to([0, y, 0]).to_edge(LEFT, buff=0.6)
    scene.play(Write(cuenta))
    scene.wait(espera)
    return VGroup(fl, cuenta)


# ---------------------------------------------------------------------------
# Tabla de unidades (forma compleja / incompleja)
def tabla_unidades(unidades, color, centro=ORIGIN, w=1.6, h=1.05):
    cab, celdas = VGroup(), VGroup()
    x0 = -w * (len(unidades) - 1) / 2
    for k, u in enumerate(unidades):
        c = Rectangle(width=w, height=0.65, stroke_color=GREY_B, stroke_width=2,
                      fill_color=color, fill_opacity=0.4 if k == 3 else 0.15).move_to([x0 + k * w, h / 2 + 0.325, 0])
        cab.add(VGroup(c, Text(u, font_size=32).move_to(c)))
        celdas.add(Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=2).move_to([x0 + k * w, 0, 0]))
    g = VGroup(cab, celdas).move_to(centro)
    return g


def digito(d, celda, color=WHITE):
    return Text(str(d), font_size=56, color=color).move_to(celda)


# ---------------------------------------------------------------------------
# Bloques en perspectiva (volumen)
def bloque_iso(nx, ny, nz, s=0.3, color=VOLU, origen=ORIGIN):
    c, sn = np.cos(PI / 6) * s, np.sin(PI / 6) * s

    def P(x, y, z):
        return np.array([(x - y) * c, (x + y) * sn + z * s, 0]) + origen

    cubos = [(x, y, z) for x in range(nx) for y in range(ny) for z in range(nz)]
    cubos.sort(key=lambda t: (-(t[0] + t[1]), t[2]))
    g = VGroup()
    for x, y, z in cubos:
        top = Polygon(P(x, y, z + 1), P(x + 1, y, z + 1), P(x + 1, y + 1, z + 1), P(x, y + 1, z + 1))
        izq = Polygon(P(x, y, z), P(x, y + 1, z), P(x, y + 1, z + 1), P(x, y, z + 1))
        der = Polygon(P(x, y, z), P(x + 1, y, z), P(x + 1, y, z + 1), P(x, y, z + 1))
        g.add(VGroup(top.set_fill(interpolate_color(ManimColor(color), WHITE, 0.35), 1),
                     izq.set_fill(interpolate_color(ManimColor(color), BLACK, 0.35), 1),
                     der.set_fill(color, 1)).set_stroke(WHITE, 1))
    return g


def cubo_rejilla(n=10, L=3.0, color=VOLU, origen=ORIGIN, op=0.35):
    """Cubo grande de lado L con las caras visibles divididas en n x n (sin dibujar cada cubito)."""
    c, sn = np.cos(PI / 6) * L, np.sin(PI / 6) * L

    def P(x, y, z):          # x, y, z en [0, 1]
        return np.array([(x - y) * c, (x + y) * sn + z * L, 0]) + origen

    caras = VGroup(
        Polygon(P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), P(0, 1, 1)).set_fill(interpolate_color(ManimColor(color), WHITE, 0.3), op),
        Polygon(P(0, 0, 0), P(0, 1, 0), P(0, 1, 1), P(0, 0, 1)).set_fill(interpolate_color(ManimColor(color), BLACK, 0.3), op),
        Polygon(P(0, 0, 0), P(1, 0, 0), P(1, 0, 1), P(0, 0, 1)).set_fill(color, op),
    ).set_stroke(WHITE, 2.5)
    rej = VGroup()
    for k in range(1, n):
        t = k / n
        rej.add(Line(P(t, 0, 1), P(t, 1, 1)), Line(P(0, t, 1), P(1, t, 1)),       # arriba
                Line(P(0, t, 0), P(0, t, 1)), Line(P(0, 0, t), P(0, 1, t)),       # izquierda
                Line(P(t, 0, 0), P(t, 0, 1)), Line(P(0, 0, t), P(1, 0, t)))       # derecha
    rej.set_stroke(WHITE, 1, opacity=0.6)
    return VGroup(caras, rej), P


# ---------------------------------------------------------------------------
# Recipientes de vidrio cúbicos y una botella de 1 L para «verter» agua
AGUA = "#3FA9F5"


def _iso(L, origen):
    c, sn = np.cos(PI / 6) * L, np.sin(PI / 6) * L
    return lambda x, y, z: np.array([(x - y) * c, (x + y) * sn + z * L, 0]) + origen


def recipiente(L, origen):
    """Cubo de vidrio abierto: (caras de detrás, caras de delante)."""
    P = _iso(L, origen)
    vid = dict(fill_color=GREY_A, stroke_color=WHITE)
    atras = VGroup(
        Polygon(P(0, 0, 0), P(1, 0, 0), P(1, 1, 0), P(0, 1, 0)),
        Polygon(P(1, 0, 0), P(1, 1, 0), P(1, 1, 1), P(1, 0, 1)),
        Polygon(P(0, 1, 0), P(1, 1, 0), P(1, 1, 1), P(0, 1, 1)),
    ).set_style(fill_opacity=0.06, stroke_width=1.5, stroke_opacity=0.5, **vid)
    delante = VGroup(
        Polygon(P(0, 0, 0), P(0, 1, 0), P(0, 1, 1), P(0, 0, 1)),
        Polygon(P(0, 0, 0), P(1, 0, 0), P(1, 0, 1), P(0, 0, 1)),
    ).set_style(fill_opacity=0.1, stroke_width=3, **vid)
    return atras, delante


def agua_prisma(L, origen, h):
    """Agua dentro del cubo hasta la altura h (fracción de 0 a 1)."""
    P = _iso(L, origen)
    if h < 0.003:            # vacío: no se dibuja nada
        return VGroup()
    return VGroup(
        Polygon(P(0, 0, 0), P(0, 1, 0), P(0, 1, h), P(0, 0, h)).set_fill(interpolate_color(ManimColor(AGUA), BLACK, 0.3), 0.85),
        Polygon(P(0, 0, 0), P(1, 0, 0), P(1, 0, h), P(0, 0, h)).set_fill(AGUA, 0.85),
        Polygon(P(0, 0, h), P(1, 0, h), P(1, 1, h), P(0, 1, h)).set_fill(interpolate_color(ManimColor(AGUA), WHITE, 0.3), 0.9),
    ).set_stroke(width=0)


def botella_1L(alto=1.5):
    """Botella sencilla con agua. El último elemento marca la boca."""
    w = alto * 0.48
    cuerpo = RoundedRectangle(corner_radius=w * 0.25, width=w, height=alto * 0.72, stroke_color=WHITE, stroke_width=3)
    agua = RoundedRectangle(corner_radius=w * 0.22, width=w * 0.9, height=alto * 0.62, stroke_width=0,
                            fill_color=AGUA, fill_opacity=0.85).align_to(cuerpo, DOWN).shift(UP * 0.04)
    cuello = Rectangle(width=w * 0.38, height=alto * 0.2, stroke_color=WHITE, stroke_width=3).next_to(cuerpo, UP, buff=0)
    tapon = Rectangle(width=w * 0.46, height=alto * 0.08, stroke_width=0, fill_color=OK, fill_opacity=1).next_to(cuello, UP, buff=0)
    etiqueta = Text("1 L", font_size=int(alto * 20), weight=BOLD).move_to(cuerpo)
    boca = VectorizedPoint(tapon.get_top())
    return VGroup(agua, cuerpo, cuello, tapon, etiqueta, boca)


# ===========================================================================
class Magnitudes(Scene):
    def construct(self):
        cab = titulo(self, "Magnitudes y medida", "¿Qué se puede medir?")
        notas = Notas(self)

        subtitulo(self, cab, "¿Qué es una magnitud?")
        datos = [("palmos", "Longitud", "metro (m)", LONG), ("balanza", "Masa", "gramo (g)", MASA),
                 ("botella", "Capacidad", "litro (L)", CAPA), ("crono", "Tiempo", "segundo (s)", TIEM)]
        fichas = Group()
        for img, mag, uni, col in datos:
            fichas.add(Group(ilustracion(img, 1.9),
                             VGroup(texto(mag, 30, col), texto(uni, 24, GREY_B)).arrange(DOWN, buff=0.12)
                             ).arrange(DOWN, buff=0.25))
        fichas.arrange(RIGHT, buff=0.45).move_to([0, 0.35, 0])
        ajusta(fichas)
        notas("Una magnitud es algo que se puede medir: se expresa con un número y una unidad")
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fichas], lag_ratio=0.25))
        self.wait(5)
        limpiar(self, cab)

        subtitulo(self, cab, "¿Se puede medir?")
        casos = [("La altura de una puerta", True), ("Lo divertida que es una película", False),
                 ("La masa de una mochila", True), ("La alegría de una persona", False),
                 ("El tiempo que dura un partido", True)]
        filas = VGroup()
        for t, si in casos:
            marca = texto("✓  Sí: es una magnitud", 26, OK) if si else texto("✗  No: no se puede medir con un número", 26, MAL)
            filas.add(VGroup(texto(t, 30), marca).arrange(RIGHT, buff=0.5))
        filas.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.1, 0])
        for f in filas:
            ajusta(f)
        filas.to_edge(LEFT, buff=0.8)
        notas("Una magnitud es algo que se puede medir: se expresa con un número y una unidad")
        for f in filas:
            self.play(FadeIn(f[0]), run_time=0.6)
            self.wait(0.6)
            self.play(FadeIn(f[1], shift=LEFT * 0.2), run_time=0.6)
        # La segunda frase va encima de la definición: así se ven las dos
        extra = texto("Gustos y sentimientos no son magnitudes: no hay una unidad para medirlos", 26, MAL)
        ajusta(extra).next_to(notas.actual, UP, buff=0.25)
        self.play(FadeIn(extra, shift=UP * 0.15), run_time=0.6)
        self.wait(4)
        limpiar(self, cab)

        # --- Medir es comparar
        subtitulo(self, cab, "Medir es comparar")
        mesa = Rectangle(width=7.2, height=0.3, fill_color=MADERA, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        mesa.move_to([0, 1.5, 0])
        patas = VGroup(*[Rectangle(width=0.22, height=1.0, fill_color=MADERA, fill_opacity=1, stroke_width=0)
                         .next_to(mesa, DOWN, buff=0).align_to(mesa, s) for s in (LEFT, RIGHT)])
        self.play(FadeIn(mesa), FadeIn(patas))
        notas("Queremos saber cuánto mide la mesa de largo")
        self.wait(1)
        palmo = 7.2 / 5
        palmos = VGroup(*[RoundedRectangle(corner_radius=0.1, width=palmo - 0.05, height=0.35, fill_color=MASA,
                                           fill_opacity=0.6, stroke_color=WHITE, stroke_width=1.5)
                          .move_to([mesa.get_left()[0] + palmo * (k + 0.5), 2.0, 0]) for k in range(5)])
        cuenta = VGroup()
        notas("Medir es ver cuántas veces cabe una unidad: por ejemplo, un palmo")
        for k, p in enumerate(palmos):
            n = texto(str(k + 1), 22).move_to(p)
            cuenta.add(n)
            self.play(FadeIn(p, shift=DOWN * 0.2), FadeIn(n), run_time=0.45)
        r1 = texto("La mesa mide 5 palmos", 30, MASA).move_to([0, -0.3, 0])
        self.play(Write(r1))
        self.wait(1)
        clip = 7.2 / 16
        clips = VGroup(*[RoundedRectangle(corner_radius=0.06, width=clip - 0.04, height=0.2, fill_color=GREY_B,
                                          fill_opacity=0.7, stroke_width=1)
                         .move_to([mesa.get_left()[0] + clip * (k + 0.5), 1.0, 0]) for k in range(16)])
        notas("Con clips sale otro número: la medida depende de la unidad")
        self.play(LaggedStart(*[FadeIn(c) for c in clips], lag_ratio=0.08))
        r2 = texto("La mesa mide 16 clips", 30, GREY_B).next_to(r1, DOWN, buff=0.3)
        self.play(Write(r2))
        self.wait(1.5)
        notas("Y si mide los palmos otra persona, con la mano más grande, saldrá otro número…", color=MAL)
        self.wait(2.5)
        self.play(FadeOut(palmos), FadeOut(cuenta), FadeOut(clips), FadeOut(r1), FadeOut(r2))

        metro = 7.2 / 1.2
        regla = VGroup(Rectangle(width=metro, height=0.35, fill_color=LONG, fill_opacity=0.6, stroke_color=WHITE,
                                 stroke_width=1.5),
                       *[Line(UP * 0.17, DOWN * 0.0).shift(RIGHT * (-metro / 2 + metro * k / 10))
                         for k in range(1, 10)])
        regla.move_to([mesa.get_left()[0] + metro / 2, 2.0, 0])
        regla[1:].set_stroke(WHITE, 1.5).align_to(regla[0], UP)
        lm = texto("1 metro", 24).move_to(regla[0])
        notas("Por eso usamos una unidad que es igual en todo el mundo: el metro")
        self.play(FadeIn(regla), FadeIn(lm))
        resto = Brace(Line(regla.get_right(), [mesa.get_right()[0], 2.0, 0]), UP, buff=0.25, color=ACENTO)
        self.play(GrowFromCenter(resto), FadeIn(texto("20 cm", 22, ACENTO).next_to(resto, UP, buff=0.08)))
        res = VGroup(MathTex("1{,}2", font_size=80, color=ACENTO), MathTex("\\text{m}", font_size=80, color=LONG)
                     ).arrange(RIGHT, buff=0.7).move_to([0, -0.4, 0])
        bn = Brace(res[0], DOWN, color=ACENTO)
        bu = Brace(res[1], DOWN, color=LONG)
        self.play(Write(res))
        self.play(GrowFromCenter(bn), GrowFromCenter(bu),
                  FadeIn(texto("número", 26, ACENTO).next_to(bn, DOWN, buff=0.1).align_to(bn, RIGHT)),
                  FadeIn(texto("unidad", 26, LONG).next_to(bu, DOWN, buff=0.1).align_to(bu, LEFT)))
        notas("Una medida siempre lleva un número y una unidad: «1,2» solo no dice nada")
        self.wait(3)
        notas.fin()


class SistemaMetrico(Scene):
    def construct(self):
        cab = titulo(self, "El Sistema Métrico Decimal", "Múltiplos y submúltiplos")
        notas = Notas(self)
        subtitulo(self, cab, "Múltiplos y submúltiplos")
        notas("Para no usar números enormes ni diminutos, la unidad tiene «hermanas» mayores y menores")
        pref = [("kilo", "k", "1000"), ("hecto", "h", "100"), ("deca", "da", "10"), ("unidad", "", "1"),
                ("deci", "d", "0{,}1"), ("centi", "c", "0{,}01"), ("mili", "m", "0{,}001")]
        # Escalera dibujada: cada peldaño es una unidad
        dx, dy, x0, y0 = 1.95, 0.6, -6.82, 1.45
        linea = VGroup()
        peld = VGroup()
        for k, (p, s, v) in enumerate(pref):
            col = POSITIVO if k < 3 else (ACENTO if k == 3 else NEGATIVO)
            xl, y = x0 + k * dx, y0 - k * dy
            tramo = VGroup(Line([xl, y, 0], [xl + dx, y, 0], color=WHITE, stroke_width=5))
            if k < 6:
                tramo.add(Line([xl + dx, y, 0], [xl + dx, y - dy, 0], color=WHITE, stroke_width=5))
            linea.add(tramo)
            nom = texto(p + (f" ({s})" if s else ""), 26, col)
            val = MathTex(v, font_size=30)
            et = VGroup(nom, val).arrange(DOWN, buff=0.08)
            et.move_to([xl + 0.8, y + 0.1 + et.height / 2, 0])
            peld.add(et)
        self.play(Create(linea[3]), FadeIn(peld[3]))
        notas("En el centro, la unidad: el metro, el gramo o el litro")
        self.wait(1.5)
        self.play(LaggedStart(*[AnimationGroup(Create(linea[k]), FadeIn(peld[k])) for k in (2, 1, 0)], lag_ratio=0.4))
        t1 = texto("múltiplos: más grandes", 28, POSITIVO).move_to([-4.2, -1.3, 0])
        self.play(FadeIn(t1))
        notas("Los múltiplos son más grandes: kilo = mil veces la unidad")
        self.wait(1.5)
        self.play(LaggedStart(*[AnimationGroup(Create(linea[k]), FadeIn(peld[k])) for k in (4, 5, 6)], lag_ratio=0.4))
        t2 = texto("submúltiplos: más pequeños", 28, NEGATIVO).move_to([3.9, 1.9, 0])
        self.play(FadeIn(t2))
        notas("Los submúltiplos son más pequeños: mili = la milésima parte")
        self.wait(2)

        # Regla de la escalera: bajar ×10, subir ÷10
        baja, sube = VGroup(), VGroup()
        for k in range(6):
            xr, y, y2 = x0 + (k + 1) * dx, y0 - k * dy, y0 - (k + 1) * dy
            f = CurvedArrow([xr - 0.6, y - 0.12, 0], [xr + 0.45, y2 - 0.12, 0], angle=PI / 2,
                            color=OK, stroke_width=4, tip_length=0.14)
            baja.add(VGroup(f, texto("×10", 22, OK).next_to(f, DOWN, buff=0.04)))
            g = CurvedArrow([xr + 1.5, y2 + 0.85, 0], [xr - 0.45, y + 0.82, 0], angle=PI / 3,
                            color=NEGATIVO, stroke_width=4, tip_length=0.14)
            sube.add(VGroup(g, texto("÷10", 22, NEGATIVO).next_to(g, UP, buff=0.04)))
        notas("Es DECIMAL: para BAJAR un escalón multiplicamos por 10")
        self.play(LaggedStart(*[Create(f[0]) for f in baja], lag_ratio=0.2), FadeIn(VGroup(*[f[1] for f in baja])))
        self.wait(2)
        notas("Y para SUBIR un escalón dividimos entre 10")
        self.play(LaggedStart(*[Create(f[0]) for f in sube], lag_ratio=0.2), FadeIn(VGroup(*[f[1] for f in sube])))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "Leer las unidades")
        ej = [("kilómetro", "km", "1\\ \\text{km} = 1000\\ \\text{m}", POSITIVO),
              ("centímetro", "cm", "1\\ \\text{m} = 100\\ \\text{cm}", NEGATIVO),
              ("kilogramo", "kg", "1\\ \\text{kg} = 1000\\ \\text{g}", POSITIVO),
              ("mililitro", "mL", "1\\ \\text{L} = 1000\\ \\text{mL}", NEGATIVO)]
        filas = VGroup()
        for nom, sim, tex, col in ej:
            filas.add(VGroup(texto(nom, 32, col), texto(f"({sim})", 28, GREY_B), MathTex(tex, font_size=44)))
        for f in filas:
            f[1].next_to(f[0], RIGHT, buff=0.2)
        filas.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-1.0, 0.2, 0])
        for f in filas:
            f[2].move_to([2.6, f[0].get_y(), 0], aligned_edge=LEFT)
        notas("El prefijo nos dice cuánto vale: kilo-metro = mil metros")
        for k, f in enumerate(filas):
            self.play(FadeIn(f[:2]), run_time=0.6)
            self.play(Write(f[2]), run_time=0.9)
            self.wait(0.8)
            if k == 1:
                notas("centi-metro: el metro partido en 100 trozos")
        notas("Con estos prefijos funcionan la longitud, la masa y la capacidad")
        self.wait(3)
        notas.fin()


class Longitud(Scene):
    def construct(self):
        cab = titulo(self, "Unidades de longitud", "La escalera")
        notas = Notas(self)
        subtitulo(self, cab, "¿Cuánto miden las cosas?")
        refs = [("Una hormiga", "unos 5 mm"), ("Un lápiz", "unos 15 cm"), ("Una puerta", "unos 2 m"),
                ("Un campo de fútbol", "unos 100 m"), ("Entre dos ciudades cercanas", "unos 60 km")]
        filas = VGroup(*[VGroup(texto(a, 30), texto(b, 30, LONG)) for a, b in refs])
        filas.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-1.2, 0.2, 0])
        for f in filas:
            f[1].move_to([2.0, f[0].get_y(), 0], aligned_edge=LEFT)
        notas("Elegimos la unidad según lo que medimos")
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in filas], lag_ratio=0.35))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "La escalera de las unidades")
        esc = escalera(U_LONG, LONG)
        notas("Ordenamos las unidades de mayor a menor como los escalones de una escalera")
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.12))
        self.wait(1.5)
        f1 = flecha_escalon(esc, 3, 4, "×10", OK)
        notas("Bajar un escalón: multiplicamos por 10   (1 m = 10 dm)", color=OK)
        self.play(Create(f1[0]), FadeIn(f1[1]))
        self.wait(2)
        f2 = flecha_escalon(esc, 3, 2, ":10", NEGATIVO)
        notas("Subir un escalón: dividimos entre 10   (1 m = 0,1 dam)", color=NEGATIVO)
        self.play(Create(f2[0]), FadeIn(f2[1]))
        self.wait(2)
        regla = regla_escalera(esc, 10).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        self.play(FadeIn(regla), FadeOut(f1), FadeOut(f2))
        notas("Truco: a una unidad más pequeña le corresponde un número más grande")
        self.wait(2.5)

        b = convertir(self, esc, 0, 3, 10, "3{,}5\\ \\text{km} = 3{,}5 \\cdot 1000 = 3500\\ \\text{m}",
                      "De km a m bajamos 3 escalones: × 10 × 10 × 10 = × 1000", notas)
        self.play(FadeOut(b))
        b = convertir(self, esc, 5, 3, 10, "450\\ \\text{cm} = 450 : 100 = 4{,}5\\ \\text{m}",
                      "De cm a m subimos 2 escalones: : 100", notas)
        self.play(FadeOut(b))
        b = convertir(self, esc, 6, 5, 10, "27\\ \\text{mm} = 27 : 10 = 2{,}7\\ \\text{cm}",
                      "De mm a cm subimos 1 escalón: : 10", notas)
        self.play(FadeOut(b))
        notas("Multiplicar por 10, 100, 1000: la coma va a la derecha. Dividir: a la izquierda")
        coma = VGroup(MathTex("3{,}5 \\cdot 1000 = 3500", font_size=50),
                      MathTex("450 : 100 = 4{,}50", font_size=50)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        coma.move_to([0, -2.2, 0]).to_edge(LEFT, buff=0.6)
        self.play(Write(coma))
        self.wait(3.5)
        notas.fin()


class MasaCapacidad(Scene):
    def construct(self):
        cab = titulo(self, "Masa y capacidad", "La misma escalera")
        notas = Notas(self)

        subtitulo(self, cab, "Unidades de masa")
        img = ilustracion("balanza", 2.2).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        esc = escalera(U_MASA, MASA)
        notas("La masa se mide con la balanza. La unidad es el gramo (g)")
        self.play(FadeIn(img))
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.12))
        notas("Mismos prefijos que con el metro: la escalera funciona igual, de 10 en 10")
        self.wait(2)
        b = convertir(self, esc, 0, 3, 10, "2{,}4\\ \\text{kg} = 2{,}4 \\cdot 1000 = 2400\\ \\text{g}",
                      "De kg a g: 3 escalones hacia abajo, × 1000", notas)
        self.play(FadeOut(b))
        b = convertir(self, esc, 6, 3, 10, "500\\ \\text{mg} = 500 : 1000 = 0{,}5\\ \\text{g}",
                      "De mg a g: 3 escalones hacia arriba, : 1000", notas)
        self.play(FadeOut(b))

        # La tonelada
        cam = ilustracion("camion", 2.2).move_to(img)
        notas("Para masas muy grandes (un camión) usamos la tonelada: 1 t = 1000 kg")
        self.play(FadeOut(img), FadeIn(cam))
        t = MathTex("1\\ \\text{t} = 1000\\ \\text{kg}", font_size=52, color=ACENTO).next_to(cam, DOWN, buff=0.3).align_to(cam, RIGHT)
        self.play(Write(t))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "Unidades de capacidad")
        img = ilustracion("botella", 2.2).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        esc = escalera(U_CAPA, CAPA)
        notas("La capacidad es lo que cabe en un recipiente. La unidad es el litro (L)")
        self.play(FadeIn(img))
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.12))
        self.wait(1.5)
        b = convertir(self, esc, 3, 5, 10, "1{,}5\\ \\text{L} = 1{,}5 \\cdot 100 = 150\\ \\text{cL}",
                      "Una botella de 1,5 L: de L a cL bajamos 2 escalones, × 100", notas)
        self.play(FadeOut(b))
        b = convertir(self, esc, 6, 3, 10, "250\\ \\text{mL} = 250 : 1000 = 0{,}25\\ \\text{L}",
                      "Un vaso de 250 mL: de mL a L subimos 3 escalones, : 1000", notas)
        self.play(FadeOut(b))
        limpiar(self, cab)

        subtitulo(self, cab, "Masa y capacidad del agua")
        img = ilustracion("botella", 2.6).move_to([-3.2, 0.4, 0])
        bal = ilustracion("balanza", 2.6).move_to([3.2, 0.4, 0])
        igual = MathTex("\\rightarrow", font_size=80).move_to([0, 0.4, 0])
        self.play(FadeIn(img), FadeIn(bal), FadeIn(igual))
        r = tarjeta(VGroup(MathTex("1\\ \\text{L de agua pesa } 1\\ \\text{kg}", font_size=50)), ACENTO)
        r.move_to([0, -2.0, 0])
        notas("Un litro de agua tiene una masa de un kilogramo, casi exacto")
        self.play(FadeIn(r))
        self.wait(3.5)
        notas.fin()


class Superficie(Scene):
    def construct(self):
        cab = titulo(self, "Unidades de superficie", "De 100 en 100")
        notas = Notas(self)
        subtitulo(self, cab, "El metro cuadrado")
        lado = 3.8
        cuad = Square(lado, stroke_color=WHITE, stroke_width=3, fill_color=SUPE, fill_opacity=0.25).move_to([-2.8, 0.25, 0])
        notas("Una superficie se mide con cuadrados. 1 m² es un cuadrado de 1 m de lado")
        self.play(DrawBorderThenFill(cuad))
        bl = Brace(cuad, DOWN, color=LONG)
        tl = texto("1 m = 10 dm", 24, LONG).next_to(bl, DOWN, buff=0.1)
        self.play(GrowFromCenter(bl), FadeIn(tl))
        self.wait(1)
        rej = VGroup()
        for k in range(1, 10):
            t = -lado / 2 + lado * k / 10
            rej.add(Line([t, -lado / 2, 0], [t, lado / 2, 0]), Line([-lado / 2, t, 0], [lado / 2, t, 0]))
        rej.set_stroke(WHITE, 1.2, opacity=0.7).move_to(cuad)
        notas("Cada lado se parte en 10 dm: salen cuadraditos de 1 dm²")
        self.play(Create(rej), run_time=2)
        fila = Rectangle(width=lado, height=lado / 10, stroke_width=0, fill_color=ACENTO, fill_opacity=0.6)
        fila.align_to(cuad, UP).align_to(cuad, LEFT)
        self.play(FadeIn(fila))
        t1 = texto("Una fila: 10 dm²", 32, ACENTO).move_to([2.8, 1.4, 0])
        self.play(FadeIn(t1))
        self.wait(1)
        t2 = texto("10 filas: 10 · 10 = 100 dm²", 32, ACENTO).next_to(t1, DOWN, buff=0.4)
        self.play(fila.animate.stretch_to_fit_height(lado).align_to(cuad, UP).set_fill(opacity=0.35), FadeIn(t2))
        r = tarjeta(VGroup(MathTex("1\\ \\text{m}^{2} = 100\\ \\text{dm}^{2}", font_size=52)), ACENTO).next_to(t2, DOWN, buff=0.6)
        notas("¡No es 10! En superficie cada escalón vale 100")
        self.play(FadeIn(r))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "La escalera de superficie")
        esc = escalera(U_SUPE, SUPE)
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.12))
        regla = regla_escalera(esc, 100).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        notas("Misma escalera, pero de 100 en 100")
        self.play(FadeIn(regla))
        self.wait(2)
        b = convertir(self, esc, 3, 4, 100, "3\\ \\text{m}^{2} = 3 \\cdot 100 = 300\\ \\text{dm}^{2}",
                      "De m² a dm²: 1 escalón hacia abajo, × 100", notas)
        self.play(FadeOut(b))
        b = convertir(self, esc, 5, 3, 100, "45\\,000\\ \\text{cm}^{2} = 45\\,000 : 10\\,000 = 4{,}5\\ \\text{m}^{2}",
                      "De cm² a m²: 2 escalones hacia arriba, : 100 : 100 = : 10 000", notas)
        self.play(FadeOut(b))
        limpiar(self, cab)

        subtitulo(self, cab, "Unidades agrarias")
        img = ilustracion("campo", 2.3).move_to([4.5, 1.0, 0])
        notas("Para medir campos y terrenos se usan las unidades agrarias")
        filas = VGroup(*[VGroup(texto(a, 30, SUPE), MathTex(b, font_size=42)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
                         for a, b in [("1 hectárea (ha)", "= 1\\ \\text{hm}^{2} = 10\\,000\\ \\text{m}^{2}"),
                                      ("1 área (a)", "= 1\\ \\text{dam}^{2} = 100\\ \\text{m}^{2}"),
                                      ("1 centiárea (ca)", "= 1\\ \\text{m}^{2}")]])
        filas.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-2.6, 0.9, 0])
        ajusta(filas, 8.0)
        filas.to_edge(LEFT, buff=0.4)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in filas], lag_ratio=0.4))
        self.play(FadeIn(img))
        cf = texto("Un campo de fútbol:\nunos 7000 m², casi 1 ha", 28, ACENTO).next_to(img, DOWN, buff=0.2)
        self.play(FadeIn(cf))
        self.wait(1.5)
        e = MathTex("2{,}5\\ \\text{ha} = 2{,}5\\ \\text{hm}^{2} = 2{,}5 \\cdot 10\\,000 = 25\\,000\\ \\text{m}^{2}",
                    font_size=46).move_to([0, -2.2, 0])
        notas("Para calcular, cambiamos la hectárea por hm² y usamos la escalera")
        self.play(Write(e))
        self.wait(3.5)
        notas.fin()


class Volumen(Scene):
    def construct(self):
        cab = titulo(self, "Unidades de volumen", "De 1000 en 1000")
        notas = Notas(self)
        subtitulo(self, cab, "El decímetro cúbico")
        notas("El volumen es el espacio que ocupa un cuerpo. Se mide con cubos")
        s = 0.215
        fila = bloque_iso(10, 1, 1, s, origen=np.array([-3.6, -2.35, 0]))
        self.play(LaggedStart(*[FadeIn(c) for c in fila], lag_ratio=0.05))
        t1 = texto("Una fila: 10 cm³", 32, ACENTO).move_to([2.0, 1.6, 0])
        notas("Cada cubito es 1 cm³: un cubo de 1 cm de lado")
        self.play(FadeIn(t1))
        self.wait(1)
        capa = bloque_iso(10, 10, 1, s, origen=np.array([-3.6, -2.35, 0]))
        t2 = texto("Una capa: 10 · 10 = 100 cm³", 32, ACENTO).next_to(t1, DOWN, buff=0.35).align_to(t1, LEFT)
        self.play(FadeOut(fila), FadeIn(capa), FadeIn(t2))
        self.wait(1)
        cubo, P = cubo_rejilla(10, 10 * s, origen=np.array([-3.6, -2.35, 0]), op=1)
        t3 = texto("10 capas: 100 · 10 = 1000 cm³", 32, ACENTO).next_to(t2, DOWN, buff=0.35).align_to(t1, LEFT)
        notas("Apilamos 10 capas: el cubo de 1 dm de lado tiene 1000 cubitos")
        self.play(FadeOut(capa), FadeIn(cubo), FadeIn(t3))
        r = tarjeta(VGroup(MathTex("1\\ \\text{dm}^{3} = 1000\\ \\text{cm}^{3}", font_size=50)), ACENTO
                    ).next_to(t3, DOWN, buff=0.5).align_to(t1, LEFT)
        self.play(FadeIn(r))
        notas("En volumen cada escalón vale 1000")
        self.wait(3)

        # 1 dm³ = 1 L
        # El agua llena todo el volumen (caras izquierda, derecha y superficie) de abajo arriba
        nivel = ValueTracker(0.02)

        def agua_cubo():
            h = nivel.get_value()
            return VGroup(
                Polygon(P(0, 0, 0), P(0, 1, 0), P(0, 1, h), P(0, 0, h)).set_fill(interpolate_color(ManimColor(AGUA), BLACK, 0.3), 0.8),
                Polygon(P(0, 0, 0), P(1, 0, 0), P(1, 0, h), P(0, 0, h)).set_fill(AGUA, 0.8),
                Polygon(P(0, 0, h), P(1, 0, h), P(1, 1, h), P(0, 1, h)).set_fill(interpolate_color(ManimColor(AGUA), WHITE, 0.3), 0.85),
            ).set_stroke(width=0)
        agua = always_redraw(agua_cubo)
        notas("Si llenamos de agua el cubo de 1 dm³, cabe exactamente 1 litro")
        self.add(agua)
        self.play(nivel.animate.set_value(1), run_time=2.5)
        r2 = tarjeta(VGroup(MathTex("1\\ \\text{dm}^{3} = 1\\ \\text{L}", font_size=50)), BLUE
                     ).next_to(r, DOWN, buff=0.3).align_to(t1, LEFT)
        self.play(FadeIn(r2))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "La escalera de volumen")
        esc = escalera(U_VOLU, VOLU)
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.12))
        regla = regla_escalera(esc, 1000).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        self.play(FadeIn(regla))
        self.wait(1.5)
        b = convertir(self, esc, 3, 4, 1000, "2\\ \\text{m}^{3} = 2 \\cdot 1000 = 2000\\ \\text{dm}^{3}",
                      "De m³ a dm³: 1 escalón hacia abajo, × 1000", notas)
        self.play(FadeOut(b))
        b = convertir(self, esc, 5, 4, 1000, "3500\\ \\text{cm}^{3} = 3500 : 1000 = 3{,}5\\ \\text{dm}^{3}",
                      "De cm³ a dm³: 1 escalón hacia arriba, : 1000", notas)
        self.play(FadeOut(b))
        limpiar(self, cab)

        self.verter_litro(cab, notas)

        subtitulo(self, cab, "Volumen y capacidad")
        tabla = VGroup(*[MathTex(t, font_size=50) for t in
                         ["1\\ \\text{m}^{3} = 1000\\ \\text{L}", "1\\ \\text{dm}^{3} = 1\\ \\text{L}",
                          "1\\ \\text{cm}^{3} = 1\\ \\text{mL}"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        tabla.scale(1.2).move_to([-3.4, 0.6, 0])
        tabla[1].set_color(ACENTO)
        self.play(Write(tabla[1]))
        notas("A partir de 1 dm³ = 1 L salen las otras dos")
        self.play(Write(tabla[0]), Write(tabla[2]))
        self.wait(2)
        img = ilustracion("pecera", 2.7).move_to([3.4, 1.0, 0])
        self.play(FadeIn(img))
        medidas = texto("40 cm × 25 cm × 30 cm", 30, ACENTO).next_to(img, DOWN, buff=0.2)
        notas("Una pecera mide 40 cm de largo, 25 cm de ancho y 30 cm de alto. ¿Cuántos litros caben?")
        self.play(FadeIn(medidas))
        self.wait(2)
        c = VGroup(MathTex("V = 40 \\cdot 25 \\cdot 30 = 30\\,000\\ \\text{cm}^{3}", font_size=44),
                   MathTex("30\\,000\\ \\text{cm}^{3} = 30\\ \\text{dm}^{3} = 30\\ \\text{L}", font_size=44)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -2.0, 0])
        notas("Largo × ancho × alto: cuántos cubitos de 1 cm³ caben")
        self.play(Write(c[0]))
        self.wait(1.5)
        notas("Pasamos a dm³ (: 1000) y como 1 dm³ = 1 L… ¡caben 30 litros!", color=OK)
        self.play(Write(c[1]))
        self.wait(3.5)
        notas.fin()


    def verter_litro(self, cab, notas):
        """1 L de agua en tres cubos: 1 dm³ se llena, 1 m³ apenas se moja, 1 cm³ se desborda."""
        subtitulo(self, cab, "¿Dónde cabe 1 litro?")
        base = -1.75
        datos = {"m": (1.7, -1.6), "dm": (0.75, 2.35), "cm": (0.22, 5.2)}
        rec, agua, nivel = {}, {}, {}
        for k, (L, x) in datos.items():
            o = np.array([x, base, 0])
            rec[k] = recipiente(L, o)
            nivel[k] = ValueTracker(0)
            agua[k] = always_redraw(lambda L=L, o=o, t=nivel[k]: agua_prisma(L, o, t.get_value()))
        etq = {k: MathTex("1\\ \\text{" + k + "}^{3}", font_size=40).move_to([datos[k][1], base - 0.45, 0])
               for k in datos}
        bot = botella_1L(1.5).move_to([-5.6, base + 0.75, 0])
        etq_b = MathTex("1\\ \\text{L}", font_size=40).move_to([-5.6, base - 0.45, 0])
        aviso = texto("(los tamaños no están a escala)", 20, GREY_B).move_to([4.6, -2.8, 0])

        notas("Una botella de 1 litro y tres cubos vacíos de vidrio: 1 m³, 1 dm³ y 1 cm³")
        self.play(FadeIn(bot), FadeIn(etq_b))
        for k in ("m", "dm", "cm"):
            self.add(rec[k][0], agua[k], rec[k][1])
            self.play(FadeIn(rec[k][0]), FadeIn(rec[k][1]), FadeIn(etq[k]), run_time=0.7)
        self.play(FadeIn(aviso))
        self.wait(1.5)
        bot.save_state()
        pos_fin = {"m": 3.65, "dm": 1.95, "cm": 1.5}

        def verter(k, h, nota, final, col):
            L, x = datos[k]
            sup = np.array([x, base + 1.5 * L, 0])
            bot.generate_target()
            bot.target.rotate(-2.1)
            bot.target.shift(sup + np.array([0.15, 0.55, 0]) - bot.target[-1].get_center())
            notas(nota)
            self.play(MoveToTarget(bot), run_time=1.2)
            boca = bot[-1].get_center()
            chorro = Line(boca, np.array([x, base + 0.5 * L + min(h, 1) * L, 0]), color=AGUA, stroke_width=7)
            self.play(Create(chorro), run_time=0.4)
            self.play(nivel[k].animate.set_value(min(h, 1)), FadeOut(bot[0]), run_time=2.2)
            if h > 1:     # se desborda: charcos a los lados y gotas
                P = _iso(L, np.array([x, base, 0]))
                charcos = VGroup(Ellipse(width=1.3, height=0.3).move_to(P(0, 1, 0) + LEFT * 0.35),
                                 Ellipse(width=1.3, height=0.3).move_to(P(1, 0, 0) + RIGHT * 0.35)
                                 ).set_style(fill_color=AGUA, fill_opacity=0.75, stroke_width=0)
                gotas = VGroup(*[Line(P(0, 0.5 * i, 1), P(0, 0.5 * i, 0) + LEFT * 0.25, color=AGUA, stroke_width=5)
                                 for i in (0, 1)],
                               *[Line(P(0.5 * i, 0, 1), P(0.5 * i, 0, 0) + RIGHT * 0.25, color=AGUA, stroke_width=5)
                                 for i in (1, 2)])
                self.play(Create(gotas), GrowFromCenter(charcos[0]), GrowFromCenter(charcos[1]), run_time=1.2)
            self.play(FadeOut(chorro), run_time=0.3)
            fin = texto(final, 26, col).move_to([x, base + pos_fin[k], 0])
            self.play(FadeIn(fin), Restore(bot), run_time=1.0)
            self.wait(1.8)

        verter("dm", 1, "1 L en el cubo de 1 dm³ de lado…", "¡Justo lleno!", OK)
        notas("1 dm³ = 1 L: un litro llena exactamente un cubo de 1 dm de lado", color=OK)
        self.wait(2.5)
        verter("m", 0.04, "Ahora en el cubo de 1 m³…", "Apenas moja el fondo", NEGATIVO)
        notas("En 1 m³ caben 1000 L: un litro es solo la milésima parte")
        self.wait(2.5)
        verter("cm", 2, "Y en el cubito de 1 cm³…", "¡Se desborda!", MAL)
        notas("En 1 cm³ solo cabe 1 mL: el litro no cabe ni de lejos")
        self.wait(3)
        limpiar(self, cab)

class Tiempo(Scene):
    def construct(self):
        cab = titulo(self, "Medir el tiempo", "Horas, minutos y segundos")
        notas = Notas(self)
        subtitulo(self, cab, "El sistema sexagesimal")
        img = ilustracion("crono", 2.2).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        self.play(FadeIn(img))
        notas("El tiempo NO va de 10 en 10: va de 60 en 60. Es el sistema sexagesimal")
        esc = escalera(["h", "min", "s"], TIEM, x0=-4.6, y0=1.6, dx=2.2, dy=1.0, w=1.6, size=32, base=-1)
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.2))
        f = VGroup(flecha_escalon(esc, 0, 1, "×60", OK), flecha_escalon(esc, 1, 2, "×60", OK))
        self.play(*[Create(x[0]) for x in f], *[FadeIn(x[1]) for x in f])
        eq = VGroup(MathTex("1\\ \\text{h} = 60\\ \\text{min}", font_size=48),
                    MathTex("1\\ \\text{min} = 60\\ \\text{s}", font_size=48),
                    MathTex("1\\ \\text{h} = 60 \\cdot 60 = 3600\\ \\text{s}", font_size=48, color=ACENTO)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.2, -1.7, 0])
        notas("Bajar un escalón: × 60. Subir: : 60")
        self.play(Write(eq[0]))
        self.play(Write(eq[1]))
        self.wait(1)
        notas("Dos escalones: × 60 × 60")
        self.play(Write(eq[2]))
        self.wait(3)
        limpiar(self, cab)

        # --- Compleja a incompleja
        subtitulo(self, cab, "De horas y minutos a minutos")
        c = VGroup(MathTex("2\\ \\text{h}\\ \\ 15\\ \\text{min}", font_size=56),
                   MathTex("= 2 \\cdot 60 + 15", font_size=56),
                   MathTex("= 120 + 15 = 135\\ \\text{min}", font_size=56)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        c.move_to([0, 0.6, 0])
        self.play(Write(c[0]))
        notas("Las horas a minutos (× 60) y sumamos los minutos que ya teníamos")
        self.play(Write(c[1]))
        self.wait(1)
        self.play(Write(c[2]))
        self.play(Circumscribe(c[2], color=OK))
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Incompleja a compleja: división
        subtitulo(self, cab, "De minutos a horas y minutos")
        p = MathTex("200\\ \\text{min} = \\ ?\\ \\text{h}\\ \\ ?\\ \\text{min}", font_size=54).move_to([0, 2.0, 0])
        self.play(Write(p))
        notas("¿Cuántas horas enteras caben en 200 minutos? Dividimos entre 60")
        div = VGroup(MathTex("200", font_size=56), MathTex("60", font_size=56, color=TIEM))
        div[0].move_to([-2.4, 0.5, 0])
        div[1].next_to(div[0], RIGHT, buff=0.6)
        caja = VGroup(Line(div[1].get_corner(UL) + LEFT * 0.2 + UP * 0.1, div[1].get_corner(DL) + LEFT * 0.2 + DOWN * 0.15),
                      Line(div[1].get_corner(DL) + LEFT * 0.2 + DOWN * 0.15, div[1].get_corner(DR) + RIGHT * 0.3 + DOWN * 0.15))
        coc = MathTex("3", font_size=56, color=ACENTO).next_to(div[1], DOWN, buff=0.35)
        resto = MathTex("20", font_size=56, color=OK).next_to(div[0], DOWN, buff=0.35).align_to(div[0], RIGHT)
        self.play(Write(div), Create(caja))
        self.play(Write(coc))
        self.wait(0.6)
        self.play(Write(resto))
        lc = texto("horas", 24, ACENTO).next_to(coc, RIGHT, buff=0.2)
        lr = texto("minutos que sobran", 24, OK).next_to(resto, LEFT, buff=0.2)
        self.play(FadeIn(lc), FadeIn(lr))
        notas("El cociente son las horas; el resto, los minutos que sobran")
        self.wait(1.5)
        r = MathTex("200\\ \\text{min} = 3\\ \\text{h}\\ \\ 20\\ \\text{min}", font_size=54).move_to([0, -1.7, 0])
        self.play(Write(r))
        comp = texto("Comprobamos: 3 · 60 + 20 = 180 + 20 = 200 ✓", 26, OK).next_to(r, DOWN, buff=0.3)
        self.play(FadeIn(comp))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- El error típico
        subtitulo(self, cab, "¡Cuidado con los decimales!")
        mal = VGroup(MathTex("1{,}5\\ \\text{h}", font_size=60), MathTex("\\neq", font_size=60, color=MAL),
                     MathTex("1\\ \\text{h}\\ \\ 50\\ \\text{min}", font_size=60, color=MAL)).arrange(RIGHT, buff=0.4)
        mal.move_to([0, 1.6, 0])
        self.play(Write(mal))
        notas("Una hora no tiene 100 minutos: 0,5 h NO son 50 minutos", color=MAL)
        self.wait(2.5)
        bien = VGroup(MathTex("0{,}5\\ \\text{h} = 0{,}5 \\cdot 60 = 30\\ \\text{min}", font_size=52),
                      MathTex("1{,}5\\ \\text{h} = 1\\ \\text{h}\\ \\ 30\\ \\text{min}", font_size=56, color=OK)
                      ).arrange(DOWN, buff=0.45).move_to([0, -0.6, 0])
        notas("0,5 h es media hora: 0,5 · 60 = 30 minutos")
        self.play(Write(bien[0]))
        self.wait(1)
        self.play(Write(bien[1]))
        self.play(Circumscribe(bien[1], color=OK))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)


# ---------------------------------------------------------------------------
def moneda(valor, r, color):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    return VGroup(c, Text(valor, font_size=int(r * 40), color="#1e1e2e", weight=BOLD).move_to(c))


def billete(valor, color, w=1.7):
    b = RoundedRectangle(corner_radius=0.08, width=w, height=w * 0.52, fill_color=color, fill_opacity=0.9,
                         stroke_color=WHITE, stroke_width=2)
    return VGroup(b, Text(valor, font_size=30, color="#1e1e2e", weight=BOLD).move_to(b))


class Monedas(Scene):
    def construct(self):
        cab = titulo(self, "Unidades monetarias", "El euro y el céntimo")
        notas = Notas(self)
        subtitulo(self, cab, "Monedas y billetes")
        cobre, oro, plata = "#D35400", "#F4D03F", "#D5D8DC"
        mon = VGroup(*[moneda(v, r, c) for v, r, c in
                       [("1c", 0.32, cobre), ("2c", 0.36, cobre), ("5c", 0.4, cobre), ("10c", 0.38, oro),
                        ("20c", 0.42, oro), ("50c", 0.46, oro), ("1€", 0.44, plata), ("2€", 0.5, plata)]])
        mon.arrange(RIGHT, buff=0.3).scale(1.4).move_to([0, 1.6, 0])
        bil = VGroup(*[billete(v, c) for v, c in [("5 €", "#AAB7B8"), ("10 €", "#E59866"), ("20 €", "#85C1E9"),
                                                   ("50 €", "#F0B27A"), ("100 €", "#82E0AA"), ("200 €", "#F7DC6F")]])
        bil.arrange(RIGHT, buff=0.25).move_to([0, -0.1, 0])
        ajusta(bil)
        notas("En España (y en muchos países de Europa) usamos el euro: €")
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in mon], lag_ratio=0.12))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bil], lag_ratio=0.12))
        self.wait(1.5)
        r = tarjeta(texto("1 euro = 100 céntimos", 36), ACENTO).move_to([0, -1.9, 0])
        notas("Un euro se divide en 100 céntimos (cent)")
        self.play(FadeIn(r))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "Euros y céntimos")
        esc = escalera(["euros (€)", "céntimos"], ACENTO, x0=-4.2, y0=1.7, dx=3.0, dy=1.1, w=2.6, size=30, base=0)
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in esc], lag_ratio=0.3))
        notas("Es como un escalón de 100: bajar × 100, subir : 100")
        self.wait(1.5)
        b = convertir(self, esc, 0, 1, 100, texto("3,45 € = 3,45 · 100 = 345 céntimos", 38),
                      "De euros a céntimos: × 100", notas, y=-1.4)
        self.play(FadeOut(b))
        b = convertir(self, esc, 1, 0, 100, texto("80 céntimos = 80 : 100 = 0,80 €", 38),
                      "De céntimos a euros: : 100", notas, y=-1.4)
        self.play(FadeOut(b))
        cmp = VGroup(texto("3,45 €  =  3 € y 45 céntimos", 38),
                     texto("Las dos cifras decimales son los céntimos", 26, GREY_B)).arrange(DOWN, buff=0.25)
        cmp.move_to([0, -1.6, 0])
        notas("La parte entera son los euros y los decimales, los céntimos")
        self.play(FadeIn(cmp))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "¡Cuidado!")
        mal = VGroup(texto("3,5 €", 44), texto("≠", 50, MAL), texto("3 € y 5 céntimos", 44, MAL)).arrange(RIGHT, buff=0.4)
        mal.move_to([0, 1.4, 0])
        self.play(FadeIn(mal))
        notas("3,5 € es lo mismo que 3,50 €: ¡son 50 céntimos, no 5!", color=MAL)
        self.wait(2.5)
        bien = texto("3,5 € = 3,50 € = 3 € y 50 céntimos", 44, OK).move_to([0, -0.2, 0])
        self.play(Write(bien))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "Otras monedas: el cambio")
        otras = texto("Dólar ($) · Libra (£) · Yen (¥) · Franco suizo (CHF)…", 32).move_to([0, 2.0, 0])
        notas("En otros países se usan otras monedas")
        self.play(FadeIn(otras))
        cambio = tarjeta(texto("Supongamos que 1 € = 1,10 $", 34), ACENTO).move_to([0, 0.9, 0])
        notas("El cambio varía cada día: este es un ejemplo")
        self.play(FadeIn(cambio))
        self.wait(1.5)
        c = VGroup(texto("20 € = 20 · 1,10 = 22 $", 40), texto("33 $ = 33 : 1,10 = 30 €", 40)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -1.0, 0])
        notas("De euros a dólares, multiplicamos por 1,10")
        self.play(Write(c[0]))
        self.wait(2)
        notas("De dólares a euros, dividimos entre 1,10")
        self.play(Write(c[1]))
        self.wait(3.5)
        notas.fin()


class ComplejasIncomplejas(Scene):
    def construct(self):
        cab = titulo(self, "Forma compleja e incompleja")
        notas = Notas(self)
        subtitulo(self, cab, "Dos maneras de escribir una medida")
        dos = VGroup(
            VGroup(texto("Forma compleja", 30, POSITIVO), texto("con varias unidades", 24, GREY_B),
                   MathTex("3\\ \\text{km}\\ \\ 25\\ \\text{m}\\ \\ 4\\ \\text{dm}", font_size=50)).arrange(DOWN, buff=0.25),
            VGroup(texto("Forma incompleja", 30, NEGATIVO), texto("con una sola unidad", 24, GREY_B),
                   MathTex("3025{,}4\\ \\text{m}", font_size=50)).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=1.6).move_to([0, 0.6, 0]).scale(1.3)
        self.play(FadeIn(dos[0]))
        self.wait(1)
        self.play(FadeIn(dos[1]))
        notas("Son la misma longitud escrita de dos formas. ¿Cómo se pasa de una a otra?")
        self.wait(3)
        limpiar(self, cab)

        # --- De compleja a incompleja con la tabla
        subtitulo(self, cab, "De compleja a incompleja")
        med = MathTex("3\\ \\text{km}", "\\ \\ 25\\ \\text{m}", "\\ \\ 4\\ \\text{dm}", "\\ \\text{en metros}",
                      font_size=50).move_to([0, 2.1, 0])
        med[3].set_color(GREY_B)
        self.play(Write(med))
        tab = tabla_unidades(U_LONG[:5], LONG, centro=[0, 0.1, 0])
        self.play(FadeIn(tab))
        cel = tab[1]
        notas("Cada cifra va a su columna: la última cifra de cada número, en su unidad")
        d = VGroup(digito(3, cel[0], ACENTO))
        self.play(Indicate(med[0]), FadeIn(d[0], shift=DOWN * 0.3))
        d.add(digito(2, cel[2], ACENTO), digito(5, cel[3], ACENTO))
        self.play(Indicate(med[1]), FadeIn(d[1], shift=DOWN * 0.3), FadeIn(d[2], shift=DOWN * 0.3))
        d.add(digito(4, cel[4], ACENTO))
        self.play(Indicate(med[2]), FadeIn(d[3], shift=DOWN * 0.3))
        self.wait(1)
        cero = digito(0, cel[1], GREY_B)
        notas("Las columnas vacías se rellenan con 0")
        self.play(FadeIn(cero, scale=1.4))
        coma = Text(",", font_size=70, color=MAL).move_to(cel[3].get_corner(DR) + np.array([0, 0.3, 0]))
        notas("Queremos metros: la coma va justo después de la columna de los metros", color=MAL)
        self.play(FadeIn(coma, scale=2))
        self.wait(1)
        res = MathTex("3\\ \\text{km}\\ \\ 25\\ \\text{m}\\ \\ 4\\ \\text{dm} = 3025{,}4\\ \\text{m}",
                      font_size=52, color=WHITE).move_to([0, -1.6, 0])
        self.play(Write(res))
        self.wait(1)
        otra = MathTex("= 3000\\ \\text{m} + 25\\ \\text{m} + 0{,}4\\ \\text{m}", font_size=44, color=GREY_B
                       ).next_to(res, DOWN, buff=0.3)
        notas("Otra forma: pasar cada parte a metros y sumar")
        self.play(FadeIn(otra))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- De incompleja a compleja
        subtitulo(self, cab, "De incompleja a compleja")
        med = MathTex("4{,}537\\ \\text{kg}", font_size=56).move_to([0, 2.1, 0])
        self.play(Write(med))
        tab = tabla_unidades(U_MASA[:4], MASA, centro=[0, 0.1, 0])
        tab[0][3][0].set_fill(opacity=0.15)
        tab[0][0][0].set_fill(opacity=0.4)
        self.play(FadeIn(tab))
        cel = tab[1]
        notas("Las unidades (el 4) van en los kg; las cifras decimales, a su derecha")
        ds = VGroup(*[digito(c, cel[k], ACENTO) for k, c in enumerate("4537")])
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.3) for x in ds], lag_ratio=0.3))
        coma2 = Text(",", font_size=70, color=MAL).move_to(cel[0].get_corner(DR) + np.array([0, 0.3, 0]))
        self.play(FadeIn(coma2, scale=2))
        self.wait(1)
        lab = VGroup(*[texto(u, 26, MASA).next_to(cel[k], DOWN, buff=0.12) for k, u in enumerate(["4 kg", "5 hg", "3 dag", "7 g"])])
        notas("Leemos cada cifra con su unidad")
        self.play(FadeIn(lab))
        r1 = MathTex("4{,}537\\ \\text{kg} = 4\\ \\text{kg}\\ \\ 5\\ \\text{hg}\\ \\ 3\\ \\text{dag}\\ \\ 7\\ \\text{g}",
                     font_size=48).move_to([0, -2.0, 0])
        self.play(Write(r1))
        self.wait(1.5)
        r2 = MathTex("= 4\\ \\text{kg}\\ \\ 537\\ \\text{g}", font_size=48, color=ACENTO).next_to(r1, DOWN, buff=0.3)
        notas("En la práctica se suele juntar: 4 kg y 537 g")
        self.play(Write(r2))
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)

        subtitulo(self, cab, "También con el tiempo y el dinero")
        ej = VGroup(
            VGroup(texto("2 h 15 min", 40, POSITIVO), texto("=", 40), texto("135 min", 40, NEGATIVO)).arrange(RIGHT, buff=0.4),
            VGroup(texto("3 € 45 céntimos", 40, POSITIVO), texto("=", 40), texto("3,45 €", 40, NEGATIVO)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.7).move_to([0, 0.5, 0])
        leyenda = VGroup(texto("compleja", 26, POSITIVO), texto("incompleja", 26, NEGATIVO)).arrange(RIGHT, buff=2.0)
        leyenda.next_to(ej, DOWN, buff=0.6)
        self.play(FadeIn(ej[0]))
        self.wait(1)
        self.play(FadeIn(ej[1]))
        self.play(FadeIn(leyenda))
        notas("Las horas y los minutos, o los euros y los céntimos, también se escriben en forma compleja")
        self.wait(3.5)
        notas.fin()


def celda(tex, x, y, color=WHITE, size=52):
    return MathTex(tex, font_size=size, color=color).move_to([x, y, 0], aligned_edge=RIGHT)


class Operaciones(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones con medidas")
        notas = Notas(self)
        subtitulo(self, cab, "Sumar y restar: misma unidad")
        notas("Para sumar o restar medidas, primero las pasamos todas a la misma unidad")
        s1 = VGroup(MathTex("2{,}5\\ \\text{km} + 350\\ \\text{m} + 1200\\ \\text{dm}", font_size=50),
                    MathTex("= 2500\\ \\text{m} + 350\\ \\text{m} + 120\\ \\text{m}", font_size=50),
                    MathTex("= 2970\\ \\text{m}", font_size=50, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        s1.move_to([0, 1.1, 0])
        self.play(Write(s1[0]))
        self.wait(1)
        notas("Todo a metros: 2,5 km = 2500 m y 1200 dm = 120 m")
        self.play(Write(s1[1]))
        self.wait(1)
        self.play(Write(s1[2]))
        self.wait(1.5)
        s2 = MathTex("3\\ \\text{kg} - 450\\ \\text{g} = 3000\\ \\text{g} - 450\\ \\text{g} = 2550\\ \\text{g}",
                     font_size=50).next_to(s1, DOWN, buff=0.7).align_to(s1, LEFT)
        notas("Para restar, igual: 3 kg = 3000 g")
        self.play(Write(s2))
        self.wait(3)
        limpiar(self, cab)

        # --- Suma en forma compleja (tiempo)
        subtitulo(self, cab, "Sumar tiempos")
        X = {"h": -1.4, "min": 1.4, "s": 3.9}
        filas = [(1.9, ("2", "40", "50")), (1.1, ("1", "35", "25"))]
        g = VGroup()
        for y, vals in filas:
            for (u, x), v in zip(X.items(), vals):
                g.add(celda(f"{v}\\ \\text{{{u}}}", x, y))
        mas = MathTex("+", font_size=52).move_to([-3.4, 1.1, 0])
        raya = Line([-3.8, 0.65, 0], [4.2, 0.65, 0])
        notas("Sumamos cada unidad por separado: segundos con segundos, minutos con minutos…")
        self.play(Write(g), Write(mas), Create(raya))
        r1 = VGroup(*[celda(f"{v}\\ \\text{{{u}}}", x, 0.15) for (u, x), v in zip(X.items(), ("3", "75", "75"))])
        self.play(Write(r1))
        self.wait(1)
        notas("75 s es más de un minuto: 75 s = 1 min 15 s", color=MAL)
        self.play(Indicate(r1[2], color=MAL))
        r2 = VGroup(*[celda(f"{v}\\ \\text{{{u}}}", x, -0.75) for (u, x), v in zip(X.items(), ("3", "76", "15"))])
        f1 = MathTex("\\leftarrow 1\\ \\text{min}", font_size=36, color=ACENTO).next_to(r2[2], RIGHT, buff=0.2)
        self.play(TransformFromCopy(r1, r2), FadeIn(f1))
        self.wait(1.5)
        notas("76 min es más de una hora: 76 min = 1 h 16 min", color=MAL)
        self.play(Indicate(r2[1], color=MAL))
        r3 = VGroup(*[celda(f"{v}\\ \\text{{{u}}}", x, -1.65, OK) for (u, x), v in zip(X.items(), ("4", "16", "15"))])
        f2 = MathTex("\\leftarrow 1\\ \\text{h}", font_size=36, color=ACENTO).next_to(r3[1], RIGHT, buff=0.2)
        self.play(TransformFromCopy(r2, r3), FadeIn(f2))
        notas("Resultado: 4 h 16 min 15 s", color=OK)
        self.wait(3)
        limpiar(self, cab)

        # --- Resta en forma compleja: desagrupar
        subtitulo(self, cab, "Restar tiempos")
        X = {"h": -0.6, "min": 2.2}
        arr = VGroup(celda("5\\ \\text{h}", X["h"], 1.2), celda("20\\ \\text{min}", X["min"], 1.2))
        aba = VGroup(celda("2\\ \\text{h}", X["h"], 0.3), celda("45\\ \\text{min}", X["min"], 0.3))
        menos = MathTex("-", font_size=52).move_to([-2.6, 0.3, 0])
        raya = Line([-3.0, -0.15, 0], [2.6, -0.15, 0])
        self.play(Write(arr), Write(aba), Write(menos), Create(raya))
        notas("A 20 min no le podemos quitar 45 min")
        self.play(Indicate(arr[1], color=MAL), Indicate(aba[1], color=MAL))
        self.wait(1)
        notas("Desagrupamos: rompemos 1 hora en 60 minutos")
        t1 = Line(arr[0].get_corner(DL), arr[0].get_corner(UR), color=MAL, stroke_width=5)
        t2 = Line(arr[1].get_corner(DL), arr[1].get_corner(UR), color=MAL, stroke_width=5)
        n1 = celda("4\\ \\text{h}", X["h"], 2.0, ACENTO, 44)
        n2 = celda("80\\ \\text{min}", X["min"], 2.0, ACENTO, 44)
        self.play(Create(t1), FadeIn(n1, shift=DOWN * 0.2))
        self.play(Create(t2), FadeIn(n2, shift=DOWN * 0.2))
        expl = texto("60 + 20 = 80", 28, ACENTO).next_to(n2, RIGHT, buff=0.4)
        self.play(FadeIn(expl))
        self.wait(1.5)
        res = VGroup(celda("2\\ \\text{h}", X["h"], -0.65, OK), celda("35\\ \\text{min}", X["min"], -0.65, OK))
        notas("Ahora sí: 80 − 45 = 35 min y 4 − 2 = 2 h", color=OK)
        self.play(Write(res[1]))
        self.play(Write(res[0]))
        self.wait(3)
        limpiar(self, cab)

        # --- Multiplicar y dividir
        subtitulo(self, cab, "Multiplicar y dividir")
        m = VGroup(MathTex("3 \\cdot (1\\ \\text{h}\\ \\ 25\\ \\text{min}) = 3\\ \\text{h}\\ \\ 75\\ \\text{min}", font_size=48),
                   MathTex("= 4\\ \\text{h}\\ \\ 15\\ \\text{min}", font_size=48, color=OK)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.4, 0])
        notas("Para multiplicar, multiplicamos cada unidad y después ajustamos (75 min = 1 h 15 min)")
        self.play(Write(m[0]))
        self.wait(1.5)
        self.play(Write(m[1]))
        self.wait(2)
        d = VGroup(MathTex("(2\\ \\text{h}\\ \\ 30\\ \\text{min}) : 2 = 150\\ \\text{min} : 2", font_size=48),
                   MathTex("= 75\\ \\text{min} = 1\\ \\text{h}\\ \\ 15\\ \\text{min}", font_size=48, color=OK)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(m, DOWN, buff=0.7).align_to(m, LEFT)
        notas("Para dividir, es más fácil pasar primero a forma incompleja (todo a minutos)")
        self.play(Write(d[0]))
        self.wait(1.5)
        self.play(Write(d[1]))
        self.wait(3.5)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios
def enunciados_1():
    return [
        ("1. Pasa a metros:", lista(["3,5 km", "470 cm", "25 dam", "82 mm"])),
        ("2. Completa:", lista(["2,4 kg = … g", "350 cL = … L", "1500 mL = … L", "3 t = … kg"])),
        ("3. Pasa a forma incompleja (en la unidad indicada):",
         lista(["4 km 30 m 5 dm (en m)", "2 kg 75 g (en g)", "6 L 4 dL 8 cL (en cL)"], 3)),
        ("4. Pasa a forma compleja:", lista(["5,325 km", "3,08 kg", "2,75 L"], 3)),
    ]


def enunciados_2():
    return [
        ("5. Pasa a la unidad indicada:", lista(["3 m² a dm²", "45 000 cm² a m²", "2,5 ha a m²"], 3)),
        ("6. Pasa a la unidad indicada:", lista(["2 m³ a dm³", "3500 cm³ a dm³", "4,5 dm³ a L", "2 m³ a L"])),
        ("7. Una botella tiene 1,5 L de agua.", "¿Cuántos vasos de 250 mL se pueden llenar?"),
        ("8. Una piscina mide 10 m de largo, 5 m de ancho y 2 m de profundidad.", "¿Cuántos litros de agua caben?"),
    ]


def enunciados_3():
    return [
        ("9. Pasa a la unidad indicada:", lista(["2 h 35 min a min", "150 min a h y min", "1,25 h a h y min"], 3)),
        ("10. Compro 3 libretas de 2,35 € cada una y pago con un billete de 10 €.", "¿Cuánto me devuelven?"),
    ]


T = "\\ \\text{"
SOL = {
    1: [("3{,}5" + T + "km} = 3{,}5 \\cdot 1000 = 3500" + T + "m}", "De km a m: 3 escalones hacia abajo, × 1000"),
        ("470" + T + "cm} = 470 : 100 = 4{,}7" + T + "m}", "De cm a m: 2 escalones hacia arriba, : 100"),
        ("25" + T + "dam} = 25 \\cdot 10 = 250" + T + "m}", "De dam a m: 1 escalón hacia abajo, × 10"),
        ("82" + T + "mm} = 82 : 1000 = 0{,}082" + T + "m}", "De mm a m: 3 escalones hacia arriba, : 1000")],
    2: [("2{,}4" + T + "kg} = 2{,}4 \\cdot 1000 = 2400" + T + "g}", "De kg a g: 3 escalones hacia abajo, × 1000"),
        ("350" + T + "cL} = 350 : 100 = 3{,}5" + T + "L}", "De cL a L: 2 escalones hacia arriba, : 100"),
        ("1500" + T + "mL} = 1500 : 1000 = 1{,}5" + T + "L}", "De mL a L: 3 escalones hacia arriba, : 1000"),
        ("3" + T + "t} = 3 \\cdot 1000 = 3000" + T + "kg}", "1 t = 1000 kg")],
    3: [("4" + T + "km}\\ 30" + T + "m}\\ 5" + T + "dm} = 4000 + 30 + 0{,}5 = 4030{,}5" + T + "m}",
         "Cada parte a metros: 4 km = 4000 m, 5 dm = 0,5 m. Y sumamos"),
        ("2" + T + "kg}\\ 75" + T + "g} = 2000 + 75 = 2075" + T + "g}", "2 kg = 2000 g. Y sumamos"),
        ("6" + T + "L}\\ 4" + T + "dL}\\ 8" + T + "cL} = 600 + 40 + 8 = 648" + T + "cL}",
         "6 L = 600 cL, 4 dL = 40 cL. Y sumamos")],
    4: [("5{,}325" + T + "km} = 5" + T + "km}\\ 3" + T + "hm}\\ 2" + T + "dam}\\ 5" + T + "m} = 5" + T + "km}\\ 325" + T + "m}",
         "Cada cifra con su unidad: km, hm, dam, m"),
        ("3{,}08" + T + "kg} = 3" + T + "kg}\\ 0" + T + "hg}\\ 8" + T + "dag} = 3" + T + "kg}\\ 80" + T + "g}",
         "Cuidado con el 0: no hay hectogramos"),
        ("2{,}75" + T + "L} = 2" + T + "L}\\ 7" + T + "dL}\\ 5" + T + "cL}", "Cada cifra con su unidad: L, dL, cL")],
    5: [("3" + T + "m}^{2} = 3 \\cdot 100 = 300" + T + "dm}^{2}", "De m² a dm²: 1 escalón hacia abajo, × 100"),
        ("45\\,000" + T + "cm}^{2} = 45\\,000 : 10\\,000 = 4{,}5" + T + "m}^{2}",
         "De cm² a m²: 2 escalones hacia arriba, : 10 000"),
        ("2{,}5" + T + "ha} = 2{,}5" + T + "hm}^{2} = 2{,}5 \\cdot 10\\,000 = 25\\,000" + T + "m}^{2}",
         "1 ha = 1 hm². De hm² a m²: 2 escalones hacia abajo, × 10 000")],
    6: [("2" + T + "m}^{3} = 2 \\cdot 1000 = 2000" + T + "dm}^{3}", "De m³ a dm³: 1 escalón hacia abajo, × 1000"),
        ("3500" + T + "cm}^{3} = 3500 : 1000 = 3{,}5" + T + "dm}^{3}", "De cm³ a dm³: 1 escalón hacia arriba, : 1000"),
        ("4{,}5" + T + "dm}^{3} = 4{,}5" + T + "L}", "1 dm³ = 1 L"),
        ("2" + T + "m}^{3} = 2000" + T + "dm}^{3} = 2000" + T + "L}", "Primero a dm³ y luego 1 dm³ = 1 L")],
    9: [("2" + T + "h}\\ 35" + T + "min} = 2 \\cdot 60 + 35 = 155" + T + "min}", "Las horas a minutos (× 60) y sumamos los 35"),
        ("150" + T + "min} = 2" + T + "h}\\ 30" + T + "min}", "150 : 60 = 2 y sobran 30: 2 h y 30 min"),
        ("1{,}25" + T + "h} = 1" + T + "h} + 0{,}25 \\cdot 60" + T + "min} = 1" + T + "h}\\ 15" + T + "min}",
         "¡No son 25 minutos! 0,25 h es un cuarto de hora: 0,25 · 60 = 15 min")],
}


def resuelve(scene, n, i, y, notas, size=54, x=-6.2):
    tex, nota = SOL[n][i]
    et = texto("abcd"[i] + ")", 32, ACENTO).move_to([x, y, 0], aligned_edge=LEFT)
    f = MathTex(tex, font_size=size).next_to(et, RIGHT, buff=0.3)
    if f.get_right()[0] > config.frame_width / 2 - 0.3:
        f.scale_to_fit_width(config.frame_width / 2 - 0.3 - f.get_left()[0]).next_to(et, RIGHT, buff=0.3)
    scene.play(FadeIn(et))
    notas(nota)
    scene.play(Write(f), run_time=1.6)
    scene.wait(1.5)


def ej_varios(scene, cab, n, idx, notas, rotulo, y0=1.5, dy=1.55):
    subtitulo(scene, cab, rotulo)
    for k, i in enumerate(idx):
        resuelve(scene, n, i, y0 - k * dy, notas)
    notas.fin()
    scene.wait(1)
    limpiar(scene, cab)


def problema_7(scene, notas):
    enun = ajusta(texto("Una botella tiene 1,5 L de agua.\n¿Cuántos vasos de 250 mL se pueden llenar?", 30)).move_to([-1.2, 2.2, 0])
    img = ilustracion("botella", 1.8).move_to([5.0, 1.9, 0])
    scene.play(FadeIn(enun), FadeIn(img))
    notas("Primero, las dos cantidades en la misma unidad: mL")
    c = VGroup(MathTex("1{,}5\\ \\text{L} = 1{,}5 \\cdot 1000 = 1500\\ \\text{mL}", font_size=48),
               MathTex("1500 : 250 = 6", font_size=48)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-1.0, -0.3, 0])
    scene.play(Write(c[0]))
    scene.wait(1.5)
    notas("¿Cuántas veces cabe 250 en 1500? Dividimos")
    scene.play(Write(c[1]))
    scene.wait(1)
    notas("Se pueden llenar 6 vasos", color=OK)
    scene.play(Circumscribe(c[1], color=OK))
    scene.wait(3)
    notas.fin()


def problema_8(scene, notas):
    enun = ajusta(texto("Una piscina mide 10 m de largo, 5 m de ancho\ny 2 m de profundidad. ¿Cuántos litros caben?", 30)).move_to([-1.4, 2.2, 0])
    img = ilustracion("piscina", 1.8).move_to([4.9, 1.9, 0])
    scene.play(FadeIn(enun), FadeIn(img))
    notas("Volumen: largo × ancho × alto")
    c = VGroup(MathTex("V = 10 \\cdot 5 \\cdot 2 = 100\\ \\text{m}^{3}", font_size=48),
               MathTex("100\\ \\text{m}^{3} = 100 \\cdot 1000 = 100\\,000\\ \\text{dm}^{3}", font_size=48),
               MathTex("100\\,000\\ \\text{dm}^{3} = 100\\,000\\ \\text{L}", font_size=48)
               ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-0.8, -0.5, 0])
    scene.play(Write(c[0]))
    scene.wait(1.5)
    notas("Pasamos a dm³: 1 escalón hacia abajo, × 1000")
    scene.play(Write(c[1]))
    scene.wait(1.5)
    notas("Y como 1 dm³ = 1 L…")
    scene.play(Write(c[2]))
    notas("Caben 100 000 litros de agua", color=OK)
    scene.play(Circumscribe(c[2], color=OK))
    scene.wait(3)
    notas.fin()


def problema_10(scene, notas):
    enun = ajusta(texto("Compro 3 libretas de 2,35 € cada una y pago con\nun billete de 10 €. ¿Cuánto me devuelven?", 30)).move_to([0, 2.2, 0])
    scene.play(FadeIn(enun))
    notas("Primero, cuánto cuestan las 3 libretas")
    c = VGroup(texto("3 · 2,35 € = 7,05 €", 40), texto("10 € − 7,05 € = 2,95 €", 40)
               ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.0, 0])
    scene.play(Write(c[0]))
    scene.wait(1.5)
    notas("Lo que me devuelven: lo que pago menos lo que cuesta")
    scene.play(Write(c[1]))
    scene.wait(1)
    notas("Me devuelven 2,95 € (2 € y 95 céntimos)", color=OK)
    scene.play(Circumscribe(c[1], color=OK))
    scene.wait(3)
    notas.fin()


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Magnitudes y medida")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))
        for n in range(1, 7):
            subtitulo(self, cab, f"Ejercicio {n} a)")
            resuelve(self, n, 0, 0.6, notas, size=58)
            self.wait(1)
            notas.fin()
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7")
        problema_7(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9 a)")
        resuelve(self, 9, 0, 0.6, notas, size=58)
        self.wait(1)
        notas.fin()
        limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 4")
        notas = Notas(self, size=24)
        ej_varios(self, cab, 1, [1, 2, 3], notas, "Ejercicio 1: b), c) y d)")
        ej_varios(self, cab, 2, [1, 2, 3], notas, "Ejercicio 2: b), c) y d)")
        ej_varios(self, cab, 3, [1, 2], notas, "Ejercicio 3: b) y c)", y0=1.0, dy=2.0)
        ej_varios(self, cab, 4, [1, 2], notas, "Ejercicio 4: b) y c)", y0=1.0, dy=2.0)
        fin = texto("En el siguiente vídeo: ejercicios 5 a 10.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 5 a 10")
        notas = Notas(self, size=24)
        ej_varios(self, cab, 5, [1, 2], notas, "Ejercicio 5: b) y c)", y0=1.0, dy=2.0)
        ej_varios(self, cab, 6, [1, 2, 3], notas, "Ejercicio 6: b), c) y d)")
        subtitulo(self, cab, "Ejercicio 8")
        problema_8(self, notas)
        limpiar(self, cab)
        ej_varios(self, cab, 9, [1, 2], notas, "Ejercicio 9: b) y c)", y0=1.0, dy=2.0)
        subtitulo(self, cab, "Ejercicio 10")
        problema_10(self, notas)
        limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
