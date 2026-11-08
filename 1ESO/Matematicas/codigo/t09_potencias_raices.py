"""Tema 9 · Potencias y raíces cuadradas (1º ESO)

Escenas:
    QueEsUnaPotencia     – cadena de mensajes: 2·2·2·2·2 = 2⁵ = 32; base y exponente; error 2⁵ ≠ 2·5
    CuadradosYCubos      – 3² como cuadrado de fichas, 2³ como cubo de bloques; 4² y 3³
    PotenciasEnteros     – (−2)², (−2)³, (−2)⁴: exponente par positivo, impar negativo; (−3)² ≠ −3²
    CuadradosPerfectos   – 9 y 16 forman cuadrado, 12 no; tabla de cuadrados del 1 al 15
    RaizCuadrada         – la raíz es el lado del cuadrado: √49 = 7; operación inversa
    RaizAproximada       – √30: cuadrado de 5 y sobran 5; entre 5 y 6; ≈ 5,5
    EjerciciosEjemplo    – enunciados (2 páginas) + primer apartado de cada ejercicio
    EjerciciosResueltos  – el resto

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t09_potencias_raices.py QueEsUnaPotencia
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t09_potencias_raices.py
"""
import os
import sys
from math import isqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 9 · Potencias y raíces cuadradas"
TITULOS = {
    "QueEsUnaPotencia": "¿Qué es una potencia?",
    "CuadradosYCubos": "Al cuadrado y al cubo",
    "PotenciasEnteros": "Potencias de números negativos",
    "CuadradosPerfectos": "Cuadrados perfectos",
    "RaizCuadrada": "La raíz cuadrada",
    "RaizAproximada": "Raíces aproximadas",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

ROSA = "#FF79C6"
SOBRA = "#FF9F43"


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


def b_tex(b):
    """Base para LaTeX: los negativos van entre paréntesis."""
    return f"({b})" if b < 0 else str(b)


def pot(b, e, size=48, menos_fuera=False):
    """Potencia con la base azul y el exponente rosa. menos_fuera: −b^e (el signo no es de la base)."""
    partes = ([("-", WHITE)] if menos_fuera else []) + [(b_tex(b), BASE), ("^{" + str(e) + "}", EXPONENTE)]
    return M(*partes, size=size)


def producto(b, e):
    """'b·b·b' en LaTeX."""
    return r" \cdot ".join([b_tex(b)] * e)


def num(n):
    """Número con separador de miles para LaTeX: 100000 -> 100\\,000; negativos con −."""
    s = f"{abs(n):,}".replace(",", r"\,")
    return ("-" if n < 0 else "") + s


def fichas_cuadrado(n, lado=None, r=0.13, buff=0.1, color=ACENTO):
    """n fichas colocadas en filas de 'lado' (por defecto, en fila)."""
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    lado = lado or n
    filas = -(-n // lado)
    g.arrange_in_grid(rows=filas, cols=lado, buff=buff, flow_order="rd")
    return g


def cuadricula(n, s=0.4, color=ACENTO, op=0.85):
    """Cuadrado de n x n casillas."""
    g = VGroup(*[Square(s, stroke_color=WHITE, stroke_width=1.5, fill_color=color, fill_opacity=op)
                 for _ in range(n * n)])
    g.arrange_in_grid(rows=n, cols=n, buff=0)
    return g


def cubo_iso(n, s=0.45, color=BASE):
    """n x n x n bloques en perspectiva isométrica (2D). Devuelve VGroup de cubitos (de atrás hacia delante)."""
    c, sn = np.cos(PI / 6) * s, np.sin(PI / 6) * s

    def P(x, y, z):
        return np.array([(x - y) * c, (x + y) * sn + z * s, 0])

    cubos = []
    for x in range(n):
        for y in range(n):
            for z in range(n):
                cubos.append((x, y, z))
    cubos.sort(key=lambda t: (-(t[0] + t[1]), t[2]))
    g = VGroup()
    for x, y, z in cubos:
        top = Polygon(P(x, y, z + 1), P(x + 1, y, z + 1), P(x + 1, y + 1, z + 1), P(x, y + 1, z + 1))
        izq = Polygon(P(x, y, z), P(x, y + 1, z), P(x, y + 1, z + 1), P(x, y, z + 1))
        der = Polygon(P(x, y, z), P(x + 1, y, z), P(x + 1, y, z + 1), P(x, y, z + 1))
        cara = VGroup(
            top.set_fill(interpolate_color(ManimColor(color), WHITE, 0.35), 1),
            izq.set_fill(interpolate_color(ManimColor(color), BLACK, 0.35), 1),
            der.set_fill(color, 1),
        ).set_stroke(WHITE, 1.5)
        g.add(cara)
    return g


# ===========================================================================
class QueEsUnaPotencia(Scene):
    def construct(self):
        cab = titulo(self, "Potencias", "¿Qué es una potencia?")
        intro = texto("Mandas un mensaje a 2 amigos. Cada uno lo reenvía a 2 más...", 28)
        intro.next_to(cab, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(intro))

        # Árbol: ronda k tiene 2^k personas
        rondas = 5
        xs_min, xs_max = -6.3, 1.6
        ys = [1.9 - k * 0.85 for k in range(rondas + 1)]
        niveles = []
        for k in range(rondas + 1):
            n = 2 ** k
            if n == 1:
                xs = [(xs_min + xs_max) / 2]
            else:
                paso = (xs_max - xs_min) / (n - 1) if k == rondas else (xs_max - xs_min) / n
                xs = ([xs_min + i * paso for i in range(n)] if k == rondas
                      else [xs_min + paso / 2 + i * paso for i in range(n)])
            r = 0.16 if k < 3 else 0.12 if k < 5 else 0.09
            niveles.append(VGroup(*[Dot([x, ys[k], 0], radius=r, color=WHITE if k == 0 else ACENTO) for x in xs]))
        yo = texto("tú", 20, GREY_B).next_to(niveles[0], RIGHT, buff=0.15)
        self.play(GrowFromCenter(niveles[0]), FadeIn(yo))

        cuentas = VGroup()
        prev = None
        for k in range(1, rondas + 1):
            lineas = VGroup(*[Line(niveles[k - 1][i // 2].get_center(), d.get_center(), stroke_width=1.5,
                                   color=GREY_B) for i, d in enumerate(niveles[k])])
            if k == 1:
                tex = M("2", size=36)
            else:
                tex = M(producto(2, k), "=", str(2 ** k), size=34)
                tex[-1].set_color(ACENTO)
            etiqueta = VGroup(texto(f"Ronda {k}:", 22, GREY_B), tex).arrange(RIGHT, buff=0.2)
            etiqueta.move_to([4.6, ys[k], 0])
            self.play(Create(lineas), LaggedStart(*[GrowFromCenter(d) for d in niveles[k]], lag_ratio=0.03),
                      FadeIn(etiqueta), run_time=1.0 + 0.15 * k)
            cuentas.add(etiqueta)
            prev = tex
        self.wait(1)

        largo = texto("¡Escribir 2 · 2 · 2 · 2 · 2 es muy largo!", 26, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(largo))
        self.wait(1.5)
        limpiar(self, cab)

        # La potencia
        subtitulo(self, cab, "Multiplicar un número por sí mismo varias veces")
        larga = M(producto(2, 5), size=64).move_to([-2.2, 1.2, 0])
        llave = Brace(larga, DOWN, buff=0.1, color=EXPONENTE)
        veces = texto("5 veces", 26, EXPONENTE).next_to(llave, DOWN, buff=0.1)
        self.play(Write(larga))
        self.play(GrowFromCenter(llave), FadeIn(veces))
        p = pot(2, 5, 110).move_to([3.2, 1.0, 0])
        igual = MathTex("=", font_size=80).move_to([1.6, 1.2, 0])
        self.play(Write(igual), TransformFromCopy(larga[0][0], p[0]), TransformFromCopy(veces, p[1]))
        res = MathTex("= 32", font_size=80, color=ACENTO).next_to(p, RIGHT, buff=0.3).shift(DOWN * 0.15)
        self.play(Write(res))
        fb = Arrow(p[0].get_bottom() + DOWN * 0.9 + LEFT * 0.6, p[0].get_bottom() + DOWN * 0.05, buff=0,
                   color=BASE, stroke_width=4)
        tb = texto("base: el número\nque se multiplica", 22, BASE).next_to(fb.get_start(), DOWN, buff=0.1)
        fe = Arrow(p[1].get_right() + RIGHT * 1.2 + UP * 0.3, p[1].get_right() + RIGHT * 0.05, buff=0,
                   color=EXPONENTE, stroke_width=4)
        te = texto("exponente: cuántas\nveces se multiplica", 22, EXPONENTE).next_to(fe.get_start(), UP, buff=0.1)
        self.play(GrowArrow(fb), FadeIn(tb))
        self.play(GrowArrow(fe), FadeIn(te))
        lee = texto("Se lee «dos elevado a cinco»", 26, GREY_B).move_to([0, -2.6, 0])
        self.play(FadeIn(lee))
        self.wait(2.5)
        limpiar(self, cab)

        # Error típico
        subtitulo(self, cab, "¡Cuidado con este error!")
        mal = M(("2", BASE), ("^{5}", EXPONENTE), r"\neq", r"2 \cdot 5", size=72).move_to([0, 2.0, 0])
        self.play(Write(mal))
        cruz = Cross(mal[3], stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        f32 = fichas_cuadrado(32, 8, r=0.12, buff=0.12).move_to([-3.2, -0.3, 0])
        f10 = fichas_cuadrado(10, 5, r=0.12, buff=0.12, color=MAL).move_to([3.2, 0.0, 0])
        l32 = M(r"2^5 = 32", size=40).next_to(f32, DOWN, buff=0.35)
        l10 = M(r"2 \cdot 5 = 10", size=40, ).next_to(f10, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(f) for f in f32], lag_ratio=0.02), FadeIn(l32))
        self.play(LaggedStart(*[FadeIn(f) for f in f10], lag_ratio=0.05), FadeIn(l10))
        exp = texto("El exponente NO multiplica a la base: dice cuántas veces se repite", 26, MAL)
        exp.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(exp))
        self.wait(2.5)
        limpiar(self, cab)

        # Exponente 1
        subtitulo(self, cab, "Exponente 1")
        uno = VGroup(pot(7, 1, 90), MathTex("= 7", font_size=80)).arrange(RIGHT, buff=0.3).move_to([0, 0.6, 0])
        self.play(Write(uno))
        e1 = texto("Una sola vez: el número tal cual", 28, GREY_B).next_to(uno, DOWN, buff=0.5)
        self.play(FadeIn(e1))
        self.wait(2.5)


# ===========================================================================
class CuadradosYCubos(Scene):
    def construct(self):
        cab = titulo(self, "Al cuadrado y al cubo")

        # 3² como cuadrado
        q = cuadricula(3, 0.75).move_to([-3.6, -0.2, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in q], lag_ratio=0.08))
        lado1 = Brace(q, DOWN, buff=0.12, color=BASE)
        lado2 = Brace(q, LEFT, buff=0.12, color=BASE)
        self.play(GrowFromCenter(lado1), GrowFromCenter(lado2),
                  FadeIn(MathTex("3", font_size=40, color=BASE).next_to(lado1, DOWN, buff=0.1)),
                  FadeIn(MathTex("3", font_size=40, color=BASE).next_to(lado2, LEFT, buff=0.1)))
        e = VGroup(pot(3, 2, 80), M(r"= 3 \cdot 3 = 9", size=64)).arrange(RIGHT, buff=0.25).move_to([2.6, 0.8, 0])
        self.play(Write(e))
        lee = texto("«tres al cuadrado»", 30, ACENTO).next_to(e, DOWN, buff=0.45)
        porq = texto("porque forma un CUADRADO\nde 3 × 3 = 9 casillas", 24, GREY_B).next_to(lee, DOWN, buff=0.3)
        self.play(FadeIn(lee))
        self.play(FadeIn(porq))
        self.wait(2.5)
        limpiar(self, cab)

        # 2³ como cubo
        cubo = cubo_iso(2, 0.85).move_to([-3.4, -0.4, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cubo], lag_ratio=0.15))
        e = VGroup(pot(2, 3, 80), M(r"= 2 \cdot 2 \cdot 2 = 8", size=64)).arrange(RIGHT, buff=0.25)
        e.move_to([2.8, 0.8, 0])
        self.play(Write(e))
        lee = texto("«dos al cubo»", 30, ACENTO).next_to(e, DOWN, buff=0.45)
        porq = texto("porque forma un CUBO\nde 2 × 2 × 2 = 8 bloques", 24, GREY_B).next_to(lee, DOWN, buff=0.3)
        self.play(FadeIn(lee))
        self.play(FadeIn(porq))
        self.wait(2.5)
        limpiar(self, cab)

        # 4² y 3³
        subtitulo(self, cab, "Más ejemplos")
        q4 = cuadricula(4, 0.5).move_to([-3.6, 0.2, 0])
        c3 = cubo_iso(3, 0.5).move_to([3.4, 0.3, 0])
        l4 = M(("4", BASE), ("^{2}", EXPONENTE), r"= 4 \cdot 4 = 16", size=48).next_to(q4, DOWN, buff=0.5)
        l3 = M(("3", BASE), ("^{3}", EXPONENTE), r"= 3 \cdot 3 \cdot 3 = 27", size=48).next_to(c3, DOWN, buff=0.5)
        l3.align_to(l4, DOWN)
        self.play(LaggedStart(*[FadeIn(c) for c in q4], lag_ratio=0.04), Write(l4))
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in c3], lag_ratio=0.05), Write(l3), run_time=2)
        nota = texto("Exponente 2: «al cuadrado»   ·   Exponente 3: «al cubo»", 28, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(nota))
        self.wait(3)


# ===========================================================================
class PotenciasEnteros(Scene):
    def construct(self):
        cab = titulo(self, "Potencias de números negativos")
        notas = Notas(self)
        regla = texto("Regla de los signos (tema 4):   (+)·(+) = +     (−)·(−) = +     (+)·(−) = −", 24, GREY_B)
        if regla.width > config.frame_width - 1.2:
            regla.scale_to_fit_width(config.frame_width - 1.2)
        regla.next_to(cab, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(regla))

        filas = [(2, [r"(-2) \cdot (-2)"], 4), (3, [r"(-2) \cdot (-2) \cdot (-2)", r"(+4) \cdot (-2)"], -8),
                 (4, [r"(-2) \cdot (-2) \cdot (-2) \cdot (-2)", r"(+4) \cdot (+4)"], 16)]
        ys = [1.4, 0.0, -1.4]
        for (e, pasos, r), y in zip(filas, ys):
            partes = [pot(-2, e, 52)]
            for pz in pasos:
                partes.append(M("= " + pz, size=46))
            fin = M("= " + ("+" if r > 0 else "") + num(r), size=52)
            fin.set_color(color_entero(r))
            partes.append(fin)
            fila = VGroup(*partes).arrange(RIGHT, buff=0.25).move_to([0, y, 0]).to_edge(LEFT, buff=0.7)
            for pz in partes:
                self.play(Write(pz), run_time=0.8)
            par = "par" if e % 2 == 0 else "impar"
            et = texto(f"exponente {par}", 24, POSITIVO if e % 2 == 0 else NEGATIVO).next_to(fila, RIGHT, buff=0.4)
            if et.get_right()[0] > config.frame_width / 2 - 0.2:
                et.next_to(fila, DOWN, buff=0.08).align_to(fila, RIGHT)
            self.play(FadeIn(et))
            self.wait(0.6)
        notas("Base negativa: exponente PAR → resultado positivo · exponente IMPAR → negativo")
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # Trampa: el paréntesis
        subtitulo(self, cab, "¡El paréntesis lo cambia todo!")
        a = VGroup(pot(-3, 2, 64), M(r"= (-3) \cdot (-3) =", size=52), M("+9", size=60).set_color(POSITIVO))
        a.arrange(RIGHT, buff=0.25).move_to([0, 1.2, 0])
        b = VGroup(pot(3, 2, 64, menos_fuera=True), M(r"= -(3 \cdot 3) =", size=52), M("-9", size=60).set_color(NEGATIVO))
        b.arrange(RIGHT, buff=0.25).move_to([0, -0.6, 0])
        self.play(Write(a))
        ta = texto("la base es −3 (con su signo)", 24, GREY_B).next_to(a, DOWN, buff=0.15)
        self.play(FadeIn(ta))
        self.wait(1)
        self.play(Write(b))
        tb = texto("sin paréntesis, la base es solo el 3: el − se queda fuera", 24, GREY_B).next_to(b, DOWN, buff=0.15)
        self.play(FadeIn(tb))
        self.play(Circumscribe(a[0], color=ACENTO), Circumscribe(b[0], color=ACENTO))
        self.wait(3)


# ===========================================================================
class CuadradosPerfectos(Scene):
    def construct(self):
        cab = titulo(self, "Cuadrados perfectos")
        pregunta = texto("¿Con cuántas fichas se puede formar un cuadrado?", 30).next_to(cab, DOWN, buff=0.4)
        pregunta.to_edge(LEFT, buff=0.6)
        self.play(FadeIn(pregunta))

        xs = [-4.6, 0.0, 4.6]
        for n, x in zip((9, 16, 12), xs):
            f = fichas_cuadrado(n, r=0.11, buff=0.1).scale_to_fit_width(min(3.6, n * 0.32)).move_to([x, 1.1, 0])
            et = MathTex(str(n), font_size=44).next_to(f, UP, buff=0.2)
            self.play(LaggedStart(*[FadeIn(d) for d in f], lag_ratio=0.03), FadeIn(et), run_time=0.8)
            lado = isqrt(n)
            if lado * lado == n:
                destino = fichas_cuadrado(n, lado, r=0.15, buff=0.18).move_to([x, -0.6, 0])
                self.play(Transform(f, destino))
                ok = M(f"{n} = ", (str(lado), BASE), ("^{2}", EXPONENTE), size=44).next_to(f, DOWN, buff=0.35)
                ok.add(MathTex(r"\checkmark", font_size=44, color=OK).next_to(ok, RIGHT, buff=0.2))
                self.play(Write(ok))
            else:
                # intentamos un cuadrado de (lado+1) x (lado+1): faltan fichas
                k = lado + 1
                plantilla = fichas_cuadrado(k * k, k, r=0.15, buff=0.18).move_to([x, -0.6, 0])
                self.play(*[Transform(f[i], plantilla[i].copy()) for i in range(n)])
                huecos = VGroup(*[DashedVMobject(Circle(0.15, color=MAL)).move_to(plantilla[i])
                                  for i in range(n, k * k)])
                self.play(Create(huecos))
                ko = texto(f"{lado} × {lado} = {lado * lado}: sobran {n - lado * lado}\n"
                           f"{k} × {k} = {k * k}: faltan {k * k - n}", 22, MAL).next_to(plantilla, DOWN, buff=0.3)
                self.play(FadeIn(ko))
            self.wait(0.6)
        defi = texto("Cuadrado perfecto: un número que es el cuadrado de otro (9 = 3², 16 = 4²)", 26, ACENTO)
        defi.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(defi))
        self.wait(2.5)
        limpiar(self, cab)

        # Tabla de cuadrados del 1 al 15
        subtitulo(self, cab, "Los cuadrados del 1 al 15")
        w, h = 0.78, 0.7
        filas = VGroup()
        for fila, (lab, vals, col) in enumerate((("n", list(range(1, 16)), BASE),
                                                  ("n²", [k * k for k in range(1, 16)], ACENTO))):
            celdas = VGroup()
            cab_c = VGroup(Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.5,
                                     fill_color=VACIO, fill_opacity=1), texto(lab, 26, col))
            cab_c[1].move_to(cab_c[0])
            celdas.add(cab_c)
            for v in vals:
                c = VGroup(Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.5),
                           MathTex(str(v), font_size=30 if v < 100 else 26, color=col))
                c[1].move_to(c[0])
                celdas.add(c)
            celdas.arrange(RIGHT, buff=0)
            filas.add(celdas)
        filas.arrange(DOWN, buff=0).move_to([0, 0.2, 0])
        self.play(FadeIn(filas[0]), FadeIn(filas[1][0]), *[FadeIn(c[0]) for c in filas[1][1:]])
        self.play(LaggedStart(*[Write(c[1]) for c in filas[1][1:]], lag_ratio=0.15), run_time=3)
        trucos = texto("Apréndete los primeros: te ayudarán con las raíces", 26, GREY_B).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(trucos))
        self.wait(3)


# ===========================================================================
class RaizCuadrada(Scene):
    def construct(self):
        cab = titulo(self, "La raíz cuadrada")
        pregunta = texto("Tengo 49 fichas y quiero formar un cuadrado. ¿Cuánto mide el lado?", 28)
        pregunta.next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(pregunta))
        f = fichas_cuadrado(49, 7, r=0.14, buff=0.16).move_to([-3.4, -0.5, 0])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in f], lag_ratio=0.02), run_time=1.6)
        lado = Brace(f, DOWN, buff=0.15, color=BASE)
        lt = MathTex("7", font_size=48, color=BASE).next_to(lado, DOWN, buff=0.1)
        self.play(GrowFromCenter(lado), Write(lt))

        e = M(r"\sqrt{49}", "=", ("7", BASE), size=80).move_to([2.8, 1.0, 0])
        self.play(Write(e))
        porq = M(r"\text{porque }", ("7", BASE), ("^{2}", EXPONENTE), "= 49", size=48).next_to(e, DOWN, buff=0.4)
        self.play(Write(porq))
        defi = texto("La raíz cuadrada es el LADO del cuadrado", 28, ACENTO).next_to(porq, DOWN, buff=0.5)
        self.play(FadeIn(defi))
        self.wait(2.5)
        limpiar(self, cab)

        # Operación inversa
        subtitulo(self, cab, "Operaciones inversas")
        a = MathTex("7", font_size=96, color=BASE).move_to([-3, 0.3, 0])
        b = MathTex("49", font_size=96, color=ACENTO).move_to([3, 0.3, 0])
        ida = CurvedArrow(a.get_top() + UP * 0.2, b.get_top() + UP * 0.2, angle=-PI / 3, color=EXPONENTE)
        vuelta = CurvedArrow(b.get_bottom() + DOWN * 0.2, a.get_bottom() + DOWN * 0.2, angle=-PI / 3, color=OK)
        ti = texto("al cuadrado", 28, EXPONENTE).next_to(ida, UP, buff=0.1)
        tv = texto("raíz cuadrada", 28, OK).next_to(vuelta, DOWN, buff=0.1)
        self.play(FadeIn(a), FadeIn(b))
        self.play(Create(ida), FadeIn(ti))
        self.play(Create(vuelta), FadeIn(tv))
        self.wait(2.5)
        limpiar(self, cab)

        # Más raíces
        subtitulo(self, cab, "Más ejemplos")
        ejemplos = [(64, 8), (100, 10), (1, 1)]
        ys = [1.3, 0.0, -1.3]
        for (n, r), y in zip(ejemplos, ys):
            fila = VGroup(M(rf"\sqrt{{{n}}}", "=", (str(r), BASE), size=60),
                          M(r"\text{porque }", (str(r), BASE), ("^{2}", EXPONENTE), f"= {n}", size=40).set_color(GREY_B))
            fila[1][1].set_color(BASE)
            fila[1][2].set_color(EXPONENTE)
            fila.arrange(RIGHT, buff=0.8).move_to([0, y, 0])
            self.play(Write(fila[0]))
            self.play(FadeIn(fila[1], shift=LEFT * 0.2))
        nota = texto("Solo los cuadrados perfectos tienen raíz exacta", 26, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(nota))
        self.wait(3)


# ===========================================================================
class RaizAproximada(Scene):
    def construct(self):
        cab = titulo(self, "Raíces aproximadas", "¿Y si no es un cuadrado perfecto?")
        notas = Notas(self)
        pregunta = M(r"\sqrt{30} = \; ?", size=64).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        self.play(Write(pregunta))
        f = fichas_cuadrado(30, 6, r=0.14, buff=0.16).move_to([-3.2, -0.4, 0])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in f], lag_ratio=0.02), run_time=1.2)
        notas("Con 30 fichas, el cuadrado más grande que podemos hacer es de 5 × 5")
        cuad = fichas_cuadrado(25, 5, r=0.14, buff=0.16).move_to([-3.6, -0.3, 0])
        resto = VGroup(*[Dot(radius=0.14, color=SOBRA) for _ in range(5)]).arrange(DOWN, buff=0.16)
        resto.next_to(cuad, RIGHT, buff=0.45).align_to(cuad, UP)
        self.play(*[f[i].animate.move_to(cuad[i]) for i in range(25)],
                  *[f[25 + i].animate.move_to(resto[i]).set_color(SOBRA) for i in range(5)])
        self.wait(0.5)
        e = M(r"30 =", ("5", BASE), ("^{2}", EXPONENTE), "+", ("5", SOBRA), size=60).move_to([3.0, 1.0, 0])
        self.play(Write(e))
        l1 = VGroup(texto("raíz entera:", 26, BASE), MathTex("5", font_size=48, color=BASE)).arrange(RIGHT, buff=0.3)
        l2 = VGroup(texto("resto:", 26, SOBRA), MathTex("30 - 25 = 5", font_size=44, color=SOBRA)).arrange(RIGHT, buff=0.3)
        VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(e, DOWN, buff=0.5)
        self.play(FadeIn(l1))
        self.play(FadeIn(l2))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # Entre 5 y 6 en la recta
        subtitulo(self, cab, "Entre qué números está")
        e = M(("25", ACENTO), "<", "30", "<", ("36", ACENTO), size=64).move_to([0, 2.0, 0])
        self.play(Write(e))
        e2 = M(r"\sqrt{25}", "<", r"\sqrt{30}", "<", r"\sqrt{36}", size=60).next_to(e, DOWN, buff=0.4)
        e3 = M(("5", BASE), "<", r"\sqrt{30}", "<", ("6", BASE), size=60).next_to(e2, DOWN, buff=0.4)
        self.play(TransformFromCopy(e, e2))
        self.play(TransformFromCopy(e2, e3))
        recta = NumberLine(x_range=[4, 7, 1], length=9, include_numbers=True, font_size=36).move_to([0, -2.2, 0])
        punto = Dot(recta.n2p(30 ** 0.5), color=ROSA, radius=0.11)
        et = MathTex(r"\sqrt{30}", font_size=40, color=ROSA).next_to(punto, UP, buff=0.15)
        self.play(Create(recta))
        self.play(GrowFromCenter(punto), Write(et))
        self.wait(2)
        limpiar(self, cab)

        # Con decimales
        subtitulo(self, cab, "Afinamos con decimales")
        filas = [("5{,}4", "29{,}16", "<"), ("5{,}5", "30{,}25", ">")]
        g = VGroup()
        for b, c, s in filas:
            fila = M((b, BASE), ("^{2}", EXPONENTE), "=", c, s, "30", size=56)
            fila[3].set_color(OK if s == "<" else MAL)
            g.add(fila)
        g.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-2.5, 1.0, 0])
        for fila in g:
            self.play(Write(fila))
        entre = M(("5{,}4", BASE), "<", r"\sqrt{30}", "<", ("5{,}5", BASE), size=56).move_to([3.6, 1.0, 0])
        self.play(Write(entre))
        cerca = texto("De 29,16 a 30 hay 0,84, pero de 30 a 30,25 solo 0,25:\n30 está más cerca de 5,5²", 24, GREY_B)
        cerca.move_to([0, -1.0, 0])
        self.play(FadeIn(cerca))
        r = M(r"\sqrt{30} \approx", ("5{,}5", ACENTO), size=72).move_to([0, -2.6, 0])
        self.play(Write(r), Circumscribe(r, color=ACENTO))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
A_POTENCIA = [(3, 4), (5, 3), (10, 5), (-2, 3)]
CALCULA = [(2, 6), (4, 3), (7, 2), (1, 9), (10, 3), (0, 5)]
SIGNOS = [(-3, 2), (-3, 3), (-1, 7), (-1, 10), (-5, 2), (5, 2, "fuera")]
PERFECTOS = [36, 50, 81, 120, 144]
RAICES = [64, 121, 196, 400]
RAIZ_ENTERA = [20, 55, 90, 150]
PROBLEMAS = [
    "a) Con 169 baldosas cuadradas se forma un cuadrado. ¿Cuántas baldosas hay en cada lado?",
    "b) Un patio cuadrado tiene 225 m² de superficie. ¿Cuánto mide su lado? ¿Y su perímetro?",
    "c) Cadena de mensajes: cada persona lo reenvía a 3 amigos.\n"
    "     ¿Cuántos mensajes se envían en la 4.ª ronda?",
]
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def pot_txt(b, e, fuera=False):
    base = f"({MENOS}{abs(b)})" if b < 0 else str(b)
    return (MENOS if fuera else "") + base + str(e).translate(SUP)


def paso(scene, partes, nota, notas, ejemplo):
    """Escribe un trozo de la fila y cambia la nota."""
    anims = [Write(partes)]
    scene.play(*anims, run_time=1.0 if ejemplo else 0.8)
    if nota and notas:
        notas(nota)
        scene.wait(1.4 if ejemplo else 0.5)


def fila(scene, etiqueta, trozos, y, notas=None, ejemplo=False, x=-6.4, size=None, ancho_max=13.0):
    """trozos: lista de (mobject, nota). Se colocan en fila y se escriben de uno en uno."""
    size = size or (60 if ejemplo else 50)
    lab = texto(etiqueta, 30) if etiqueta else None
    mobs = [m for m, _ in trozos]
    g = VGroup(*([lab] if lab else []), *mobs).arrange(RIGHT, buff=0.3)
    if g.width > ancho_max:
        g.scale_to_fit_width(ancho_max)
    g.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    if lab:
        scene.play(FadeIn(lab), run_time=0.4)
    for m, nota in trozos:
        paso(scene, m, nota, notas, ejemplo)
    scene.play(Circumscribe(mobs[-1], color=ACENTO), run_time=0.7)
    return g


def t_a_potencia(b, e, s):
    r = b ** e
    return [(M(producto(b, e), size=s), None),
            (VGroup(MathTex("=", font_size=s), pot(b, e, s)).arrange(RIGHT, buff=0.2),
             f"{e} factores iguales: base {b}, exponente {e}"),
            (M("= " + num(r), size=s).set_color(ACENTO), None)]


def t_calcula(b, e, s):
    r = b ** e
    tr = [(pot(b, e, s), None)]
    if b in (0, 1):
        tr.append((M("= " + num(r), size=s).set_color(ACENTO),
                   f"{b} multiplicado por sí mismo siempre da {b}"))
    elif b == 10:
        tr.append((M("= " + producto(b, e), size=s), None))
        tr.append((M("= " + num(r), size=s).set_color(ACENTO), f"Un 1 seguido de {e} ceros"))
    else:
        tr.append((M("= " + producto(b, e), size=s), f"Multiplicamos el {b} por sí mismo {e} veces"))
        tr.append((M("= " + num(r), size=s).set_color(ACENTO), None))
    return tr


def t_signos(item, s):
    if len(item) == 3:
        b, e, _ = item
        r = -(b ** e)
        return [(pot(b, e, s, menos_fuera=True), None),
                (M(rf"= -({producto(b, e)})", size=s), "Sin paréntesis: la potencia es solo del " + str(b)),
                (M("= " + num(r), size=s).set_color(NEGATIVO), None)]
    b, e = item
    r = b ** e
    tr = [(pot(b, e, s), None)]
    if e <= 3:
        tr.append((M("= " + producto(b, e), size=s), None))
    par = e % 2 == 0
    tr.append((M("= " + ("+" if r > 0 else "") + num(r), size=s).set_color(color_entero(r)),
               f"Base negativa y exponente {'par → positivo' if par else 'impar → negativo'}"))
    return tr


def t_perfecto(n, s):
    r = isqrt(n)
    if r * r == n:
        return [(M(f"{n} =", (str(r), BASE), ("^{2}", EXPONENTE), size=s), f"{r} · {r} = {n}"),
                (texto("Sí", 32, OK), None)]
    return [(M(("{}".format(r), BASE), ("^{2}", EXPONENTE), f"= {r * r} <", str(n), "<", f"{(r + 1) ** 2} =",
               (str(r + 1), BASE), ("^{2}", EXPONENTE), size=s), f"Está entre {r}² y {r + 1}²: no es el cuadrado de nadie"),
            (texto("No", 32, MAL), None)]


def t_raiz(n, s):
    r = isqrt(n)
    return [(M(rf"\sqrt{{{n}}}", "=", (str(r), BASE), size=s), None),
            (M(r"\text{porque }", (str(r), BASE), ("^{2}", EXPONENTE), f"= {n}", size=int(s * 0.8)),
             f"Buscamos el número que al cuadrado da {n}")]


def t_raiz_entera(n, s):
    r = isqrt(n)
    return [(M(rf"\sqrt{{{n}}}:", size=s), None),
            (M(("{}".format(r), BASE), ("^{2}", EXPONENTE), f"= {r * r} \\le {n} <", f"{(r + 1) ** 2} =",
               (str(r + 1), BASE), ("^{2}", EXPONENTE), size=int(s * 0.85)),
             f"El cuadrado más grande que cabe en {n} es {r}² = {r * r}"),
            (M(r"\Rightarrow", r"\text{ raíz } ", (str(r), BASE), r",\ \text{resto } ", (str(n - r * r), SOBRA),
               size=int(s * 0.85)), f"Resto: {n} − {r * r} = {n - r * r}")]


def resolver(scene, func, items, letras, notas, ejemplo=False):
    ys = {1: [0.6], 2: [1.2, -0.9], 3: [1.7, 0.2, -1.3]}[len(items)]
    for it, l, y in zip(items, letras, ys):
        s = 60 if ejemplo else 50
        tr = func(*it, s) if isinstance(it, tuple) and func is not t_signos else func(it, s)
        fila(scene, f"{l})", tr, y, notas=notas, ejemplo=ejemplo)
    notas.fin()
    scene.wait(1.2)


def pagina_enunciados(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 28, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cab, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
    if grupo.width > config.frame_width - 1.0:
        grupo.scale_to_fit_width(config.frame_width - 1.0).to_edge(LEFT, buff=0.5)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def lista(items, por_linea=4):
    trozos = [f"{l}) {t}" for l, t in zip("abcdef", items)]
    return "\n".join("      ".join(trozos[i:i + por_linea]) for i in range(0, len(trozos), por_linea))


def enunciados_1():
    a_pot = [" · ".join([f"({MENOS}{abs(b)})" if b < 0 else str(b)] * e) for b, e in A_POTENCIA]
    return [
        ("1. Escribe como potencia y calcula:", lista(a_pot, 2)),
        ("2. Calcula:", lista([pot_txt(b, e) for b, e in CALCULA], 6)),
        ("3. ¡Cuidado con el signo! Calcula:",
         lista([pot_txt(*it[:2], fuera=len(it) == 3) for it in SIGNOS], 6)),
        ("4. ¿Son cuadrados perfectos?", lista([str(n) for n in PERFECTOS], 5)),
    ]


def enunciados_2():
    return [
        ("5. Calcula estas raíces exactas:", lista([f"√{n}" for n in RAICES], 4)),
        ("6. Calcula la raíz entera y el resto:", lista([f"√{n}" for n in RAIZ_ENTERA], 4)),
        ("7. Problemas:", "\n".join(PROBLEMAS)),
    ]


# --- 7. Problemas
def enunciado(scene, i):
    e = texto(PROBLEMAS[i][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    if e.width > config.frame_width - 1.0:
        e.scale_to_fit_width(config.frame_width - 1.0)
    scene.play(Write(e), run_time=1.5)
    return e


def problema_baldosas(scene, notas):
    enunciado(scene, 0)
    q = cuadricula(13, 0.27, color=BASE, op=0.7).move_to([-3.6, -0.6, 0])
    scene.play(LaggedStart(*[FadeIn(c) for c in q], lag_ratio=0.005), run_time=2)
    notas("Las baldosas forman un cuadrado: el lado es la raíz cuadrada")
    lado = Brace(q, DOWN, buff=0.1, color=ACENTO)
    r = M(r"\sqrt{169}", "=", ("13", BASE), size=60).move_to([2.6, 0.6, 0])
    porq = M(r"\text{porque }", ("13", BASE), ("^{2}", EXPONENTE), r"= 13 \cdot 13 = 169", size=40).next_to(r, DOWN, buff=0.35)
    scene.play(Write(r))
    scene.play(Write(porq), GrowFromCenter(lado), FadeIn(MathTex("13", font_size=36, color=ACENTO).next_to(lado, DOWN, buff=0.08)))
    notas.fin()
    sol = texto("Hay 13 baldosas en cada lado", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_patio(scene, notas):
    enunciado(scene, 1)
    patio = Square(3.0, color=OK, fill_opacity=0.25).move_to([-4.0, -0.6, 0])
    area = MathTex(r"225 \text{ m}^2", font_size=40).move_to(patio)
    scene.play(Create(patio), FadeIn(area))
    notas("El área de un cuadrado es lado · lado = lado²: el lado es la raíz")
    r = M(r"\text{lado} = \sqrt{225} =", ("15", BASE), r"\text{ m}", size=52).move_to([2.4, 0.9, 0])
    porq = M(r"\text{porque } 15^2 = 225", size=38).set_color(GREY_B).next_to(r, DOWN, buff=0.3)
    scene.play(Write(r))
    scene.play(FadeIn(porq))
    lados = VGroup(*[MathTex("15", font_size=32, color=BASE).next_to(patio, d, buff=0.12)
                     for d in (UP, DOWN, LEFT, RIGHT)])
    scene.play(FadeIn(lados))
    notas("El perímetro es la suma de los 4 lados")
    p = M(r"\text{perímetro} = 4 \cdot 15 =", ("60", ACENTO), r"\text{ m}", size=52).next_to(porq, DOWN, buff=0.5)
    scene.play(Write(p))
    notas.fin()
    sol = texto("El lado mide 15 m y el perímetro, 60 m", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_mensajes(scene, notas):
    enunciado(scene, 2)
    filas_t = VGroup()
    for k in range(1, 5):
        if k == 1:
            t = M(r"\text{Ronda } 1:", "3", size=40)
        else:
            t = M(rf"\text{{Ronda }} {k}:", producto(3, k), "=", (str(3 ** k), ACENTO), size=40)
        filas_t.add(t)
    filas_t.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.2, 0.0, 0])
    for t in filas_t:
        scene.play(Write(t), run_time=0.8)
    notas("En cada ronda se multiplica por 3 otra vez")
    r = VGroup(pot(3, 4, 64), M("= 81", size=60).set_color(ACENTO)).arrange(RIGHT, buff=0.2).move_to([4.0, 0.0, 0])
    scene.play(Write(r), Circumscribe(r, color=ACENTO))
    notas.fin()
    sol = texto("En la 4.ª ronda se envían 3⁴ = 81 mensajes", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Potencias y raíces cuadradas")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        pantallas = [
            ("Ejercicio 1 a)", t_a_potencia, A_POTENCIA[:1], "a"),
            ("Ejercicio 2 a)", t_calcula, CALCULA[:1], "a"),
            ("Ejercicio 3 a)", t_signos, SIGNOS[:1], "a"),
            ("Ejercicio 3 f): ¡sin paréntesis!", t_signos, SIGNOS[5:], "f"),
            ("Ejercicio 4 a) y b)", t_perfecto, PERFECTOS[:2], "ab"),
            ("Ejercicio 5 a)", t_raiz, RAICES[:1], "a"),
            ("Ejercicio 6 a)", t_raiz_entera, RAIZ_ENTERA[:1], "a"),
        ]
        for sub, func, items, letras in pantallas:
            subtitulo(self, cab, sub)
            resolver(self, func, items, letras, notas, ejemplo=True)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        problema_baldosas(self, notas)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Potencias y raíces cuadradas")
        notas = Notas(self, size=24)
        pantallas = [
            ("Ejercicio 1: b), c) y d)", t_a_potencia, A_POTENCIA[1:], "bcd"),
            ("Ejercicio 2: b), c) y d)", t_calcula, CALCULA[1:4], "bcd"),
            ("Ejercicio 2: e) y f)", t_calcula, CALCULA[4:], "ef"),
            ("Ejercicio 3: b), c) y d)", t_signos, SIGNOS[1:4], "bcd"),
            ("Ejercicio 3 e): compara con la f)", t_signos, SIGNOS[4:5], "e"),
            ("Ejercicio 4: c), d) y e)", t_perfecto, PERFECTOS[2:], "cde"),
            ("Ejercicio 5: b), c) y d)", t_raiz, RAICES[1:], "bcd"),
            ("Ejercicio 6: b) y c)", t_raiz_entera, RAIZ_ENTERA[1:3], "bc"),
            ("Ejercicio 6 d)", t_raiz_entera, RAIZ_ENTERA[3:], "d"),
        ]
        for sub, func, items, letras in pantallas:
            subtitulo(self, cab, sub)
            resolver(self, func, items, letras, notas)
            limpiar(self, cab)
        for sub, f in (("Ejercicio 7 b)", problema_patio), ("Ejercicio 7 c)", problema_mensajes)):
            subtitulo(self, cab, sub)
            f(self, notas)
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya dominas las potencias y las raíces.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
