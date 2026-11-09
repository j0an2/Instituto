"""Tema 1 · Números enteros (2º ESO)

Sigue el índice del libro: naturales y divisibilidad · positivos y negativos · suma y resta ·
multiplicación y división · potencias y raíces · operaciones con potencias · operaciones combinadas.
Lo que ya se vio en 1º ESO se repasa deprisa; lo nuevo son las propiedades de las potencias.

Escenas:
    NaturalesDivisibilidad – múltiplos y divisores, primos, factorizar 72 y 60, M.C.D. y m.c.m., problema
    PositivosNegativos     – situaciones, el conjunto Z, recta, opuesto, valor absoluto, orden
    SumaResta              – fichas: mismo signo / distinto signo; restar es sumar el opuesto; quitar paréntesis
    MultiplicacionDivision – el patrón que explica (−)·(−) = +; tabla de signos; varios factores
    PotenciasRaices        – signo de una potencia; (−3)² ≠ −3²; √49 = ±7; √−49 no existe; raíz entera
    MismaBase              – producto y cociente de potencias de la misma base; exponente 0
    PotenciaDePotencia     – (aᵐ)ⁿ; mismo exponente; errores típicos; resumen de propiedades
    OperacionesCombinadas  – jerarquía con enteros y potencias (motor del tema 10 de 1º)
    EjerciciosEjemplo      – enunciados (3 páginas) + primer apartado de cada ejercicio
    EjerciciosResueltos1   – ejercicios 1 a 5
    EjerciciosResueltos2   – ejercicios 6 a 9

Usa el estilo y algunas utilidades de 1ESO/Matematicas/codigo (estilo.py, temas 2, 4, 9 y 10).

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t01_enteros.py MismaBase
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t01_enteros.py
"""
import os
import re
import sys
from math import isqrt

COMUN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from t02_factores_mcd_mcm import columna, linea_factorizacion, resolver_mcd_mcm  # noqa: E402
from t04_operaciones_enteros import tabla_signos  # noqa: E402
from t09_potencias_raices import Notas, limpiar, subtitulo, b_tex, pot, producto, fichas_cuadrado  # noqa: E402
from t10_jerarquia import resolver as resolver_expr, parse, valor, tachar, escalera, txt_expr  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 1 · Números enteros"
TITULOS = {
    "NaturalesDivisibilidad": "Naturales y divisibilidad (repaso)",
    "PositivosNegativos": "Números positivos y negativos",
    "SumaResta": "Suma y resta de enteros",
    "MultiplicacionDivision": "Multiplicación y división de enteros",
    "PotenciasRaices": "Potencias y raíces cuadradas",
    "MismaBase": "Operaciones con potencias: misma base",
    "PotenciaDePotencia": "Potencia de una potencia y mismo exponente",
    "OperacionesCombinadas": "Operaciones combinadas",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 – 5)",
    "EjerciciosResueltos2": "Ejercicios resueltos (6 – 9)",
}

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


# ---------------------------------------------------------------------------
# Utilidades
def P(b, e):
    """Trozos de una potencia para M(): base azul, exponente rosa. b y e pueden ser int o str."""
    bt = b_tex(b) if isinstance(b, int) else b
    return [(bt, BASE), ("^{" + str(e) + "}", EXPONENTE)]


def L(*partes, size=46):
    """Línea de cálculo: '=' en [0] y luego los trozos."""
    return M("=", *partes, size=size)


def pasos(scene, lineas, x, y0, dy=0.78, notas=None, ejemplo=False, etiqueta=None, final=True):
    """Escribe líneas una debajo de otra (alineadas a la izquierda). lineas: [(mobject con '=' en [0], nota)].
    La primera línea no enseña su '='. Devuelve el VGroup."""
    g = VGroup()
    rt = 0.9 if ejemplo else 0.7
    for i, (m, nota) in enumerate(lineas):
        m.move_to([x, y0 - i * dy, 0], aligned_edge=LEFT)
        if i == 0:
            m[0].set_opacity(0)
            if etiqueta:
                et = texto(etiqueta, 28).next_to(m[1], LEFT, buff=0.25)
                scene.play(FadeIn(et), run_time=0.3)
                g.add(et)
        scene.play(Write(m), run_time=rt)
        g.add(m)
        if nota and notas:
            notas(nota)
            scene.wait(1.5 if ejemplo else 0.6)
    if final:
        scene.play(Circumscribe(lineas[-1][0][1:], color=ACENTO), run_time=0.7)
    return g


def tarjeta(contenido, color=ACENTO, buff=0.3):
    """Recuadro redondeado alrededor de un mobject."""
    r = SurroundingRectangle(contenido, color=color, buff=buff, corner_radius=0.15,
                             fill_color=color, fill_opacity=0.08)
    return VGroup(r, contenido)


def fila_fichas(n, signo, buff=0.15, r=0.3):
    return VGroup(*[ficha_entero(signo, r) for _ in range(n)]).arrange(RIGHT, buff=buff)


def regla(*partes, frase, size=46, color=ACENTO):
    """Tarjeta con la fórmula y una frase debajo."""
    f = M(*partes, size=size)
    t = texto(frase, 24, GREY_B)
    return tarjeta(VGroup(f, t).arrange(DOWN, buff=0.25), color)


# ===========================================================================
class NaturalesDivisibilidad(Scene):
    def construct(self):
        cab = titulo(self, "Números naturales y divisibilidad", "Repaso de 1.º ESO")
        notas = Notas(self)

        # --- Múltiplos y divisores con fichas
        fichas = fichas_cuadrado(36, lado=9, r=0.14, buff=0.12).move_to([-3.6, 0.6, 0])
        d = MathTex("36", ":", "4", "=", "9", font_size=60).move_to([3.0, 1.8, 0])
        d[0].set_color(ACENTO)
        d[2].set_color(BASE)
        self.play(LaggedStart(*[FadeIn(f) for f in fichas], lag_ratio=0.01), run_time=1.2)
        notas("36 fichas en 4 filas de 9: no sobra ninguna")
        self.play(Write(d))
        resto = texto("resto 0: la división es exacta", 26, OK).next_to(d, DOWN, buff=0.3)
        self.play(FadeIn(resto))
        frases = VGroup(M(("36", ACENTO), r"\text{ es múltiplo de }", ("4", BASE), size=42),
                        M(("4", BASE), r"\text{ es divisor de }", ("36", ACENTO), size=42)
                        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(resto, DOWN, buff=0.5)
        for f in frases:
            self.play(Write(f))
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # --- Primos y compuestos
        primo = VGroup(texto("Primo", 34, ACENTO), texto("solo tiene dos divisores: 1 y él mismo", 26),
                       MathTex(r"2,\ 3,\ 5,\ 7,\ 11,\ 13,\ 17,\ 19,\ 23 \dots", font_size=44)
                       ).arrange(DOWN, buff=0.25).move_to([-3.4, 0.6, 0])
        comp = VGroup(texto("Compuesto", 34, BASE), texto("tiene más divisores", 26),
                      MathTex(r"12:\ 1,\ 2,\ 3,\ 4,\ 6,\ 12", font_size=44)
                      ).arrange(DOWN, buff=0.25).move_to([3.4, 0.6, 0])
        self.play(FadeIn(primo, shift=UP * 0.2))
        self.play(FadeIn(comp, shift=UP * 0.2))
        idea = texto("Todo número compuesto es un producto de primos", 28, GREY_B).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(idea))
        self.wait(2)
        limpiar(self, cab)

        # --- Factorizar 72 y 60
        sub = subtitulo(self, cab, "Factorizamos 72 y 60")
        c1, f1 = columna(self, 72, np.array([-5.0, 1.8, 0]), motivos=True, rt=0.45)
        c2, f2 = columna(self, 60, np.array([-0.6, 1.8, 0]), motivos=True, rt=0.45)
        p1 = linea_factorizacion(72, sorted(f1), 46).move_to([4.6, 1.0, 0])
        p2 = linea_factorizacion(60, sorted(f2), 46).next_to(p1, DOWN, buff=0.5).align_to(p1, LEFT)
        self.play(TransformFromCopy(c1, p1))
        self.play(TransformFromCopy(c2, p2))
        self.wait(1)
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(sub), VGroup(p1, p2).animate.move_to([0, 1.8, 0]))
        resolver_mcd_mcm(self, (72, 60), 0.0, -1.2, reglas=True)
        self.wait(2.5)
        limpiar(self, cab)

        # --- Problema: autobuses
        enun = texto("Un autobús sale cada 12 minutos y otro cada 18.\n"
                     "Si acaban de salir juntos, ¿cuándo vuelven a coincidir?", 28).move_to([0, 2.3, 0])
        self.play(Write(enun), run_time=1.5)
        m12 = MathTex(r"12:", "12,", "24,", "36,", "48", r"\dots", font_size=44).move_to([-1.0, 0.7, 0])
        m18 = MathTex(r"18:", "18,", "36,", "54", r"\dots", font_size=44).next_to(m12, DOWN, buff=0.4).align_to(m12, LEFT)
        self.play(Write(m12))
        self.play(Write(m18))
        notas("Buscamos un múltiplo común: el más pequeño")
        self.play(m12[3].animate.set_color(ACENTO), m18[2].animate.set_color(ACENTO))
        r = M(r"\text{m.c.m.}(12, 18) =", ("36", ACENTO), size=48).next_to(m18, DOWN, buff=0.6).set_x(0)
        self.play(Write(r))
        notas.fin()
        sol = texto("Vuelven a coincidir dentro de 36 minutos", 30, OK).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(sol))
        self.wait(2)
        limpiar(self, cab)
        mas = texto("¿Quieres repasarlo con calma?\nTemas 1 y 2 de 1.º ESO", 32, GREY_B)
        self.play(FadeIn(mas))
        self.wait(2)


# ===========================================================================
class PositivosNegativos(Scene):
    def construct(self):
        cab = titulo(self, "Números positivos y negativos", "El conjunto de los números enteros")
        notas = Notas(self)

        casos = [("Temperatura", "5 grados bajo cero", -5, r"\,^{\circ}\text{C}"),
                 ("Ascensor", "segundo sótano", -2, r"\text{ (planta)}"),
                 ("Cuenta", "debo 30 euros", -30, r"\text{ euros}"),
                 ("Altura", "Everest", 8849, r"\text{ m}")]
        tarjetas = VGroup()
        for nombre, frase, n, u in casos:
            v = MathTex(s_ent(n), u, font_size=48)
            v[0].set_color(color_entero(n))
            g = VGroup(texto(nombre, 26, ACENTO), texto(frase, 22, GREY_B), v).arrange(DOWN, buff=0.22)
            tarjetas.add(tarjeta(g, GREY_B, buff=0.25))
        tarjetas.arrange(RIGHT, buff=0.35).move_to([0, 1.0, 0])
        if tarjetas.width > 13.4:
            tarjetas.scale_to_fit_width(13.4)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tarjetas], lag_ratio=0.3))
        z = MathTex(r"\mathbb{Z} = \{\dots,", "-3,", "-2,", "-1,", "0,", "+1,", "+2,", "+3,", r"\dots\}", font_size=50)
        for i in (1, 2, 3):
            z[i].set_color(NEGATIVO)
        for i in (5, 6, 7):
            z[i].set_color(POSITIVO)
        z.move_to([0, -1.6, 0])
        self.play(Write(z))
        notas("Los enteros: negativos, el cero y positivos")
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # --- Recta, opuesto y valor absoluto
        g, linea = recta_enteros(-6, 6, largo=12, y=-0.4)
        self.play(Create(g), run_time=1.2)
        pa = Dot(linea.n2p(-4), color=NEGATIVO, radius=0.12)
        pb = Dot(linea.n2p(4), color=POSITIVO, radius=0.12)
        self.play(FadeIn(pa, scale=2))
        notas("El opuesto de −4 es +4: misma distancia al 0, al otro lado")
        self.play(TransformFromCopy(pa, pb))
        b1 = BraceBetweenPoints(linea.n2p(-4), linea.n2p(0), UP, color=NEGATIVO)
        b2 = BraceBetweenPoints(linea.n2p(0), linea.n2p(4), UP, color=POSITIVO)
        t1 = MathTex(r"|{-4}| = 4", font_size=40, color=NEGATIVO).next_to(b1, UP, buff=0.1)
        t2 = MathTex(r"|{+4}| = 4", font_size=40, color=POSITIVO).next_to(b2, UP, buff=0.1)
        self.play(GrowFromCenter(b1), GrowFromCenter(b2))
        self.play(Write(t1), Write(t2))
        notas("Valor absoluto: la distancia al 0 (sin signo)")
        op = M(r"\text{op}(-4) = +4", size=44).move_to([0, 2.3, 0])
        self.play(Write(op))
        self.wait(1.5)
        self.play(FadeOut(VGroup(b1, b2, t1, t2, op, pb)))

        # --- Orden
        pc = Dot(linea.n2p(-2), color=NEGATIVO, radius=0.12)
        pa.generate_target()
        self.play(FadeIn(pc, scale=2))
        notas("Es mayor el que está más a la derecha")
        flecha = Arrow(linea.n2p(-6) + UP * 0.9, linea.n2p(6) + UP * 0.9, buff=0, color=ACENTO)
        crece = texto("cada vez mayor", 24, ACENTO).next_to(flecha, UP, buff=0.1)
        self.play(GrowArrow(flecha), FadeIn(crece))
        comp = MathTex("-4", "<", "-2", font_size=60).move_to([0, 2.4, 0])
        comp[0].set_color(NEGATIVO)
        comp[2].set_color(NEGATIVO)
        self.play(Write(comp))
        notas("¡Ojo! 4 es mayor que 2, pero −4 es menor que −2")
        self.wait(2)
        cadena_o = MathTex("-6", "<", "-4", "<", "-2", "<", "0", "<", "+3", "<", "+5", font_size=50)
        for i, n in zip(range(0, 11, 2), (-6, -4, -2, 0, 3, 5)):
            cadena_o[i].set_color(color_entero(n))
        cadena_o.move_to([0, -2.2, 0])
        self.play(Write(cadena_o))
        notas.fin()
        self.wait(2)


# ===========================================================================
class SumaResta(Scene):
    def construct(self):
        cab = titulo(self, "Suma y resta de enteros")
        notas = Notas(self)

        # --- Mismo signo
        sub = subtitulo(self, cab, "Mismo signo")
        e = expr_enteros(-3, "+", -4, size=56).move_to([0, 2.0, 0])
        self.play(Write(e))
        a = fila_fichas(3, -1).move_to([-2.2, 0.5, 0])
        b = fila_fichas(4, -1).move_to([2.2, 0.5, 0])
        self.play(FadeIn(a), FadeIn(b))
        self.play(VGroup(a, b).animate.arrange(RIGHT, buff=0.15).move_to([0, 0.5, 0]))
        r = MathTex("=", "-7", font_size=56).next_to(e, RIGHT, buff=0.2)
        r[1].set_color(NEGATIVO)
        self.play(Write(r))
        t = texto("Mismo signo: se suman y se deja el signo", 30, ACENTO).move_to([0, -1.2, 0])
        self.play(FadeIn(t))
        self.wait(1.5)
        self.play(FadeOut(VGroup(e, a, b, r, t, sub)))

        # --- Distinto signo: parejas que se anulan
        sub = subtitulo(self, cab, "Distinto signo")
        e = expr_enteros(5, "+", -3, size=56).move_to([0, 2.0, 0])
        self.play(Write(e))
        a = fila_fichas(5, 1).move_to([0, 0.9, 0])
        b = fila_fichas(3, -1).next_to(a, DOWN, buff=0.25).align_to(a, LEFT)
        self.play(FadeIn(a), FadeIn(b))
        notas("Un + y un − se anulan: cada pareja vale 0")
        parejas = VGroup(*[SurroundingRectangle(VGroup(a[i], b[i]), color=ACENTO, buff=0.06) for i in range(3)])
        self.play(Create(parejas))
        self.play(FadeOut(VGroup(parejas, *a[:3], *b)))
        r = MathTex("=", "+2", font_size=56).next_to(e, RIGHT, buff=0.2)
        r[1].set_color(POSITIVO)
        self.play(Write(r))
        t = texto("Distinto signo: se restan y se pone\nel signo del de mayor valor absoluto", 30, ACENTO).move_to([0, -1.4, 0])
        self.play(FadeIn(t))
        notas.fin()
        self.wait(2)
        self.play(FadeOut(VGroup(e, a[3:], r, t, sub)))

        # --- Restar es sumar el opuesto
        sub = subtitulo(self, cab, "Restar es sumar el opuesto")
        l1 = expr_enteros(2, "-", -5, size=56)
        l2 = expr_enteros("=", 2, "+", 5, size=56)
        l3 = expr_enteros("=", 7, size=56)
        g = VGroup(l1, l2, l3).arrange(RIGHT, buff=0.25).move_to([0, 1.2, 0])
        self.play(Write(l1))
        notas("Restar −5 es lo mismo que sumar +5")
        self.play(Write(l2))
        self.play(Write(l3))
        self.wait(1)
        notas.fin()

        # --- Quitar paréntesis
        reglas = VGroup(*[MathTex(a, r"\ \to\ ", b, font_size=46) for a, b in
                          ((r"+(+a)", "+a"), (r"+(-a)", "-a"), (r"-(+a)", "-a"), (r"-(-a)", "+a"))])
        for m in reglas:
            m[2].set_color(POSITIVO if m[2].tex_string.startswith("+") else NEGATIVO)
        reglas.arrange_in_grid(rows=2, cols=2, buff=(1.6, 0.4)).move_to([0, -1.4, 0])
        cab_r = texto("Para quitar paréntesis:", 28, ACENTO).next_to(reglas, UP, buff=0.35)
        self.play(FadeIn(cab_r), LaggedStart(*[FadeIn(m) for m in reglas], lag_ratio=0.3))
        notas("Signos iguales dan +; signos distintos dan −")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Sumas y restas combinadas
        subtitulo(self, cab, "Sumas y restas combinadas")
        resolver_sumas(self, "7-(-3)+(-8)-(+4)", -3.2, 1.6, notas, ejemplo=True, size=54)
        self.wait(2)


# ---------------------------------------------------------------------------
def terminos(s):
    """'-8+5-(-3)+(-6)' -> [(op, valor de dentro, con paréntesis)]."""
    res = []
    for op, alt, sg, n1, n2 in re.findall(r"([+-]?)(\(([+-])(\d+)\)|(\d+))", s):
        res.append((op, int(sg + n1), True) if alt.startswith("(") else (op, int(n2), False))
    return res


def valor_sumas(s):
    return sum((-1 if op == "-" else 1) * v for op, v, _ in terminos(s))


def tex_signado(vals, size):
    """'−8 + 5 + 3 − 6' con cada número del color de su signo."""
    partes, cols = [], []
    for i, v in enumerate(vals):
        if i == 0:
            partes.append(str(v))
        else:
            partes.append(("+ " if v > 0 else "- ") + str(abs(v)))
        cols.append(color_entero(v))
    return partes, cols


def resolver_sumas(scene, s, x, y0, notas, ejemplo=False, size=46, etiqueta=None, dy=None):
    ts = terminos(s)
    dy = dy or size / 60
    # línea 0: tal cual
    partes = []
    for i, (op, v, par) in enumerate(ts):
        dentro = par_ent(v) if par else str(v)
        partes.append((op if i == 0 else f" {op} ") + dentro)
    lineas = [(L("".join(partes), size=size), None)]
    vals = [(-1 if op == "-" else 1) * v for op, v, _ in ts]
    hay_par = any(par for _, _, par in ts)
    if hay_par:
        p, c = tex_signado(vals, size)
        m = L(*p, size=size)
        for k, col in enumerate(c):
            m[k + 1].set_color(col)
        ejemplos = [f"{op}({'+' if v > 0 else '−'}{abs(v)}) = {'+' if (op == '-') == (v < 0) else '−'}{abs(v)}"
                    for op, v, par in ts if par][:2]
        lineas.append((m, "Quitamos paréntesis: " + ",  ".join(ejemplos).replace("-", "−")))
    pos = [v for v in vals if v > 0]
    neg = [-v for v in vals if v < 0]
    sp, sn = sum(pos), sum(neg)
    if pos and neg:
        if len(pos) > 1 or len(neg) > 1:
            fp = "(" + " + ".join(map(str, pos)) + ")" if len(pos) > 1 else str(pos[0])
            fn = "(" + " + ".join(map(str, neg)) + ")" if len(neg) > 1 else str(neg[0])
            lineas.append((L((fp, POSITIVO), "-", (fn, NEGATIVO), size=size), "Juntamos los positivos y los negativos"))
            lineas.append((L((str(sp), POSITIVO), "-", (str(sn), NEGATIVO), size=size), None))
        r = sp - sn
        lineas.append((L((str(r), color_entero(r)), size=size),
                       "Distinto signo: restamos y ponemos el signo del mayor" if r else "Valen lo mismo: se anulan"))
    else:
        r = sp - sn
        lineas.append((L((str(r), color_entero(r)), size=size), "Todos del mismo signo: sumamos"))
    pasos(scene, lineas, x, y0, dy=dy, notas=notas, ejemplo=ejemplo, etiqueta=etiqueta)
    notas.fin()
    return r


# ===========================================================================
class MultiplicacionDivision(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicación y división de enteros")
        notas = Notas(self)

        # --- El patrón
        def col(a, x):
            g = VGroup()
            for k in (2, 1, 0, -1, -2):
                r = a * k
                at = f"({a})" if a < 0 else str(a)
                kt = f"({k})" if k < 0 else str(k)
                m = MathTex(at, r"\cdot", kt, "=", ("+" if r > 0 and a < 0 else "") + str(r), font_size=46)
                m[4].set_color(color_entero(r))
                g.add(m)
            g.arrange(DOWN, buff=0.28, aligned_edge=RIGHT).move_to([x, 0.3, 0])
            return g

        izq, der = col(3, -3.2), col(-3, 3.2)
        for m in izq[:3]:
            self.play(FadeIn(m), run_time=0.4)
        notas("Cada vez que el segundo baja 1, el resultado baja 3...")
        for m in izq[3:]:
            self.play(FadeIn(m), run_time=0.6)
        self.play(Indicate(izq[3][4]), Indicate(izq[4][4]))
        notas("...así que (+)·(−) da negativo")
        self.wait(1)
        for m in der[:3]:
            self.play(FadeIn(m), run_time=0.4)
        notas("Con −3: cada vez que el segundo baja 1, el resultado SUBE 3...")
        for m in der[3:]:
            self.play(FadeIn(m), run_time=0.6)
        self.play(Indicate(der[3][4]), Indicate(der[4][4]))
        notas("...así que (−)·(−) da positivo")
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # --- Tabla de signos y ejemplos
        tabla, _ = tabla_signos(np.array([-5.6, 1.6, 0]), lado=0.9)
        nota_t = texto("Para multiplicar\ny para dividir", 24, GREY_B).next_to(tabla, DOWN, buff=0.35)
        self.play(FadeIn(tabla), FadeIn(nota_t))
        ejemplos = [[-6, "*", 4], [-7, "*", -3], [-24, ":", -6], [36, ":", -9]]
        ys = [2.0, 0.9, -0.2, -1.3]
        for it, y in zip(ejemplos, ys):
            resolver_muldiv(self, it, -1.2, y, notas, size=46, una_linea=True)
        self.wait(1.5)
        limpiar(self, cab)

        # --- Varios factores
        subtitulo(self, cab, "Varios factores")
        resolver_muldiv(self, [-2, "*", -3, "*", -1, "*", 5], -4.5, 1.4, notas, ejemplo=True, size=54)
        self.wait(2)


# ---------------------------------------------------------------------------
def signo_txt(n):
    return "+" if n > 0 else "−"


def valor_muldiv(items):
    v = items[0]
    for op, b in zip(items[1::2], items[2::2]):
        if op == "*":
            v *= b
        else:
            assert v % b == 0
            v //= b
    return v


def tex_muldiv(items):
    return [r"\cdot" if it == "*" else ":" if it == ":" else it for it in items]


def resolver_muldiv(scene, items, x, y0, notas, ejemplo=False, size=46, etiqueta=None, una_linea=False, dy=None):
    """items: [-6, '*', 4, ':', -2 ...]. Solo productos con más de 2 factores: contamos negativos.
    Si no, de izquierda a derecha aplicando la regla de los signos."""
    dy = dy or size / 58
    ops = items[1::2]
    lineas = [(expr_enteros("=", *tex_muldiv(items), size=size), None)]
    if len(ops) > 1 and all(o == "*" for o in ops):
        nums = items[0::2]
        negs = sum(1 for n in nums if n < 0)
        r = valor_muldiv(items)
        sg = "+" if r > 0 else "-"
        lineas.append((L(sg + "(" + r" \cdot ".join(str(abs(n)) for n in nums) + ")", size=size),
                       f"{negs} factores negativos: {'par → positivo' if negs % 2 == 0 else 'impar → negativo'}"))
        lineas.append((L((("+" if r > 0 else "") + str(r), color_entero(r)), size=size), None))
    else:
        actual = list(items)
        while len(actual) > 1:
            a, op, b = actual[:3]
            r = a * b if op == "*" else a // b
            regla_t = f"({signo_txt(a)}) {'·' if op == '*' else ':'} ({signo_txt(b)}) = {signo_txt(r)}"
            actual = [r] + actual[3:]
            if len(actual) == 1:
                m = L((("+" if r > 0 else "") + str(r), color_entero(r)), size=size)
            else:
                m = expr_enteros("=", *tex_muldiv(actual), size=size)
            lineas.append((m, regla_t))
    if una_linea:
        # todo en una fila: 'a · b = r' con la regla al lado
        fila = VGroup(*[m for m, _ in lineas]).arrange(RIGHT, buff=0.2)
        fila[0][0].set_opacity(0)
        fila.move_to([x, y0, 0], aligned_edge=LEFT)
        scene.play(Write(fila[0]), run_time=0.6)
        for m, nota in lineas[1:]:
            scene.play(Write(m), run_time=0.6)
            t = texto(nota, 22, GREY_B).next_to(fila, RIGHT, buff=0.5)
            scene.play(FadeIn(t), run_time=0.4)
        return
    pasos(scene, lineas, x, y0, dy=dy, notas=notas, ejemplo=ejemplo, etiqueta=etiqueta)
    notas.fin()


# ===========================================================================
class PotenciasRaices(Scene):
    def construct(self):
        cab = titulo(self, "Potencias y raíces cuadradas")
        notas = Notas(self)

        d = M(*P("a", "n"), "=", r"\underbrace{a \cdot a \cdots a}_{n \text{ veces}}", size=60).move_to([0, 1.6, 0])
        self.play(Write(d))
        nb = texto("base", 26, BASE).next_to(d[0], DOWN, buff=0.4).shift(LEFT * 0.3)
        ne = texto("exponente", 26, EXPONENTE).next_to(d[1], UP, buff=0.3)
        self.play(FadeIn(nb), FadeIn(ne))
        self.wait(1.5)
        self.play(FadeOut(VGroup(nb, ne, d)))

        # --- Signo de una potencia
        sub = subtitulo(self, cab, "¿Qué signo tiene?")
        filas = VGroup()
        for e in (1, 2, 3, 4):
            r = (-2) ** e
            m = M(*P(-2, e), "=", (("+" if r > 0 else "") + str(r), color_entero(r)), size=52)
            t = texto("par" if e % 2 == 0 else "impar", 26, POSITIVO if e % 2 == 0 else NEGATIVO)
            filas.add(VGroup(m, t).arrange(RIGHT, buff=0.6))
        filas.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.0, 0.0, 0])
        for f in filas:
            self.play(Write(f[0]), run_time=0.6)
            self.play(FadeIn(f[1]), run_time=0.3)
        resumen = tarjeta(VGroup(texto("Base positiva → siempre +", 26, POSITIVO),
                                 texto("Base negativa:", 26, NEGATIVO),
                                 texto("  exponente par → +", 26),
                                 texto("  exponente impar → −", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.18))
        resumen.move_to([3.4, -0.3, 0])
        self.play(FadeIn(resumen))
        self.wait(2.5)
        self.play(FadeOut(VGroup(filas, resumen, sub)))

        # --- (−3)² frente a −3²
        sub = subtitulo(self, cab, "¡Cuidado con los paréntesis!")
        a = VGroup(M(*P(-3, 2), "=", r"(-3) \cdot (-3)", "=", ("+9", POSITIVO), size=54))
        b = VGroup(M("-", *P(3, 2), "=", r"-(3 \cdot 3)", "=", ("-9", NEGATIVO), size=54))
        VGroup(a, b).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0.3, 0])
        self.play(Write(a))
        notas("Con paréntesis, el − forma parte de la base")
        self.play(Write(b))
        notas("Sin paréntesis, el exponente solo afecta al 3")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Raíz cuadrada
        sub = subtitulo(self, cab, "Raíz cuadrada")
        q = M(r"\sqrt{49}", "=", r"\pm 7", size=70).move_to([0, 1.8, 0])
        q[2].set_color(ACENTO)
        self.play(Write(q[0]))
        notas("¿Qué número al cuadrado da 49?")
        porq = VGroup(M(("7", POSITIVO), ("^{2}", EXPONENTE), "= 49", size=48),
                      M(("(-7)", NEGATIVO), ("^{2}", EXPONENTE), "= 49", size=48)).arrange(RIGHT, buff=1.5)
        porq.next_to(q, DOWN, buff=0.6)
        self.play(Write(porq[0]))
        self.play(Write(porq[1]))
        self.play(Write(q[1:]))
        notas("Un número positivo tiene dos raíces cuadradas opuestas")
        self.wait(1.5)
        neg = M(r"\sqrt{-49}", size=60).move_to([-2.0, -1.6, 0])
        self.play(Write(neg))
        cruz = tachar(self, neg)
        no = texto("no existe", 30, MAL).next_to(cruz, RIGHT, buff=0.3)
        self.play(FadeIn(no))
        notas("Ningún número al cuadrado da negativo: no hay raíz")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Raíz entera
        subtitulo(self, cab, "Raíz entera")
        lineas = [(M("=", r"\sqrt{40}", size=56), None),
                  (M(r"\Rightarrow", ("6", BASE), ("^{2}", EXPONENTE), r"= 36 \le 40 < 49 =", ("7", BASE),
                     ("^{2}", EXPONENTE), size=50), "40 no es un cuadrado perfecto: está entre 36 y 49"),
                  (M(r"\Rightarrow", r"\text{raíz entera } 6,\ \text{resto } 4", size=50), "Resto: 40 − 36 = 4")]
        pasos(self, lineas, -4.2, 1.4, dy=1.0, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(2)


# ===========================================================================
class MismaBase(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones con potencias", "Producto y cociente de la misma base")
        notas = Notas(self)

        # --- Producto
        sub = subtitulo(self, cab, "Producto")
        e = M(*P(2, 3), r"\cdot", *P(2, 4), size=64).move_to([0, 2.2, 0])
        self.play(Write(e))
        g1 = MathTex(r"2 \cdot 2 \cdot 2", font_size=56, color=BASE)
        pto = MathTex(r"\cdot", font_size=56)
        g2 = MathTex(r"2 \cdot 2 \cdot 2 \cdot 2", font_size=56, color=BASE)
        fila = VGroup(g1, pto, g2).arrange(RIGHT, buff=0.25).move_to([0, 0.7, 0])
        self.play(TransformFromCopy(e[0:2], g1), FadeIn(pto), TransformFromCopy(e[3:5], g2))
        b1 = Brace(g1, DOWN, buff=0.12, color=EXPONENTE)
        b2 = Brace(g2, DOWN, buff=0.12, color=EXPONENTE)
        l1 = MathTex("3", font_size=40, color=EXPONENTE).next_to(b1, DOWN, buff=0.08)
        l2 = MathTex("4", font_size=40, color=EXPONENTE).next_to(b2, DOWN, buff=0.08)
        self.play(GrowFromCenter(b1), GrowFromCenter(b2), FadeIn(l1), FadeIn(l2))
        notas("En total: 3 + 4 = 7 doses multiplicados")
        r = M("=", *P(2, "3+4"), "=", *P(2, 7), size=64).next_to(e, RIGHT, buff=0.25)
        VGroup(e, r).generate_target()
        self.play(Write(r))
        self.wait(1)
        rg = regla(*P("a", "m"), r"\cdot", *P("a", "n"), "=", *P("a", "m+n"),
                   frase="Misma base: se deja la base y se SUMAN los exponentes").move_to([0, -1.9, 0])
        self.play(FadeIn(rg, shift=UP * 0.2))
        notas.fin()
        self.wait(2.5)
        limpiar(self, cab)

        # --- Cociente
        sub = subtitulo(self, cab, "Cociente")
        e = M(*P(5, 6), ":", *P(5, 4), size=64).move_to([-3.6, 2.0, 0])
        self.play(Write(e))
        num = MathTex(*([r"5", r"\cdot"] * 6)[:-1], font_size=54, color=BASE)
        den = MathTex(*([r"5", r"\cdot"] * 4)[:-1], font_size=54, color=BASE)
        raya = Line(LEFT, RIGHT, stroke_width=3).set_width(num.width + 0.2)
        num.next_to(raya, UP, buff=0.15)
        den.next_to(raya, DOWN, buff=0.15).align_to(num, LEFT)
        frac = VGroup(num, raya, den).move_to([-2.4, -0.2, 0])
        igual = MathTex("=", font_size=60).next_to(frac, LEFT, buff=0.3)
        self.play(FadeIn(igual), TransformFromCopy(e[0:2], num), Create(raya), TransformFromCopy(e[3:5], den))
        notas("Dividir es simplificar: cada 5 de arriba se va con uno de abajo")
        tachas = VGroup()
        for i in range(4):
            for m in (num[2 * i], den[2 * i]):
                tachas.add(Line(m.get_corner(DL), m.get_corner(UR), color=MAL, stroke_width=4))
        self.play(LaggedStart(*[Create(t) for t in tachas], lag_ratio=0.15))
        r = M("=", *P(5, "6-4"), "=", *P(5, 2), size=64).next_to(frac, RIGHT, buff=0.4)
        self.play(Write(r))
        notas("Quedan 6 − 4 = 2 cincos")
        self.wait(1)
        notas.fin()
        rg = regla(*P("a", "m"), ":", *P("a", "n"), "=", *P("a", "m-n"),
                   frase="Misma base: se deja la base y se RESTAN los exponentes").move_to([0, -2.6, 0])
        self.play(FadeIn(rg, shift=UP * 0.2))
        notas.fin()
        self.wait(2.5)
        limpiar(self, cab)

        # --- Exponente 0
        sub = subtitulo(self, cab, "Exponente 0")
        e = M(*P(7, 3), ":", *P(7, 3), size=64).move_to([-3.6, 1.8, 0])
        self.play(Write(e))
        c1 = M("=", r"\dfrac{343}{343}", "=", ("1", ACENTO), size=56).next_to(e, RIGHT, buff=0.3)
        self.play(Write(c1))
        notas("Un número dividido entre sí mismo da 1")
        c2 = M("=", *P(7, "3-3"), "=", *P(7, 0), size=64).next_to(e, DOWN, buff=0.9).align_to(c1, LEFT)
        self.play(Write(c2))
        notas("Y con la regla: 7 elevado a 3 − 3 = 0")
        self.wait(1)
        rg = tarjeta(VGroup(M(*P("a", 0), "= 1", size=56), M(*P("a", 1), "= a", size=56)).arrange(RIGHT, buff=1.2))
        rg.move_to([0, -2.0, 0])
        self.play(FadeIn(rg, shift=UP * 0.2))
        notas("Cualquier número (que no sea 0) elevado a 0 da 1")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Con base negativa (vídeo del libro: potencias y signos)
        subtitulo(self, cab, "Con base negativa")
        lineas = [(L(*P(-2, 3), r"\cdot", *P(-2, 2), size=60), None),
                  (L(*P(-2, "3+2"), size=60), "La base es −2: va entre paréntesis y no cambia"),
                  (L(*P(-2, 5), size=60), None),
                  (L(("-32", NEGATIVO), size=60), "Exponente impar: el resultado es negativo")]
        pasos(self, lineas, -3.0, 1.8, dy=1.0, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(2)


# ===========================================================================
class PotenciaDePotencia(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones con potencias", "Potencia de una potencia y mismo exponente")
        notas = Notas(self)

        # --- Potencia de una potencia
        sub = subtitulo(self, cab, "Potencia de una potencia")
        lineas = [(L("(", *P(3, 2), ")", ("^{3}", ACENTO), size=60), None),
                  (L(*P(3, 2), r"\cdot", *P(3, 2), r"\cdot", *P(3, 2), size=60), "Elevar a 3 es multiplicar 3 veces"),
                  (L(*P(3, "2+2+2"), size=60), "Misma base: sumamos exponentes"),
                  (L(*P(3, r"2 \cdot 3"), "=", *P(3, 6), size=60), "Sumar 2 tres veces es multiplicar 2 · 3")]
        pasos(self, lineas, -5.0, 2.0, dy=0.95, notas=notas, ejemplo=True)
        rg = regla("(", *P("a", "m"), ")", ("^{n}", EXPONENTE), "=", *P("a", r"m \cdot n"),
                   frase="Se MULTIPLICAN los exponentes").move_to([3.8, -1.2, 0])
        self.play(FadeIn(rg, shift=UP * 0.2))
        notas.fin()
        self.wait(2.5)
        limpiar(self, cab)

        # --- Mismo exponente: producto
        sub = subtitulo(self, cab, "Mismo exponente")
        lineas = [(L(*P(2, 3), r"\cdot", *P(5, 3), size=56), None),
                  (L(r"(2 \cdot 2 \cdot 2) \cdot (5 \cdot 5 \cdot 5)", size=56), None),
                  (L(r"(2 \cdot 5) \cdot (2 \cdot 5) \cdot (2 \cdot 5)", size=56), "Cambiamos el orden: un 2 con un 5"),
                  (L("(", r"2 \cdot 5", ")", ("^{3}", EXPONENTE), "=", *P(10, 3), "=", ("1000", ACENTO), size=56), None)]
        pasos(self, lineas, -6.0, 2.0, dy=0.9, notas=notas, ejemplo=True)
        rg = VGroup(regla(*P("a", "n"), r"\cdot", *P("b", "n"), "=", "(a \\cdot b)", ("^{n}", EXPONENTE),
                          frase="Mismo exponente: se multiplican las bases", size=40),
                    regla(*P("a", "n"), ":", *P("b", "n"), "=", "(a : b)", ("^{n}", EXPONENTE),
                          frase="y lo mismo con la división", size=40)).arrange(RIGHT, buff=0.4)
        rg.to_edge(DOWN, buff=0.25)
        notas.fin()
        self.play(FadeIn(rg[0], shift=UP * 0.2))
        self.play(FadeIn(rg[1], shift=UP * 0.2))
        self.wait(2.5)
        limpiar(self, cab)

        sub = subtitulo(self, cab, "Ejemplo con división")
        lineas = [(L(*P(12, 4), ":", *P(3, 4), size=60), None),
                  (L("(12 : 3)", ("^{4}", EXPONENTE), size=60), "Mismo exponente: dividimos las bases"),
                  (L(*P(4, 4), "=", ("256", ACENTO), size=60), None)]
        pasos(self, lineas, -3.0, 1.6, dy=1.0, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(1.5)
        limpiar(self, cab)

        # --- Errores típicos
        sub = subtitulo(self, cab, "Errores típicos")
        mal = M(*P(2, 3), "+", *P(2, 4), "=", *P(2, 7), size=56).move_to([-1.0, 1.6, 0]).set_color(MAL)
        self.play(Write(mal))
        tachar(self, mal)
        bien = M(*P(2, 3), "+", *P(2, 4), "= 8 + 16 =", ("24", OK), size=56).next_to(mal, DOWN, buff=0.4).align_to(mal, LEFT)
        self.play(Write(bien))
        notas("Las propiedades son para multiplicar y dividir, ¡no para sumar!")
        self.wait(2)
        mal2 = M(*P(2, 3), r"\cdot", *P(3, 2), "=", *P(6, 5), size=56).move_to([-1.0, -0.8, 0]).set_color(MAL)
        self.play(Write(mal2))
        tachar(self, mal2)
        bien2 = M(*P(2, 3), r"\cdot", *P(3, 2), r"= 8 \cdot 9 =", ("72", OK), size=56).next_to(mal2, DOWN, buff=0.4).align_to(mal2, LEFT)
        self.play(Write(bien2))
        notas("Distinta base y distinto exponente: no se juntan, se calculan")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Resumen
        sub = subtitulo(self, cab, "Resumen")
        reglas = VGroup(
            M(*P("a", "m"), r"\cdot", *P("a", "n"), "=", *P("a", "m+n"), size=54),
            M(*P("a", "m"), ":", *P("a", "n"), "=", *P("a", "m-n"), size=54),
            M("(", *P("a", "m"), ")", ("^{n}", EXPONENTE), "=", *P("a", r"m \cdot n"), size=54),
            M(*P("a", "n"), r"\cdot", *P("b", "n"), "=", "(a \\cdot b)", ("^{n}", EXPONENTE), size=54),
            M(*P("a", "n"), ":", *P("b", "n"), "=", "(a : b)", ("^{n}", EXPONENTE), size=54),
            M(*P("a", 0), "= 1", r"\qquad", *P("a", 1), "= a", size=54),
        ).arrange_in_grid(rows=3, cols=2, buff=(1.4, 0.7), col_alignments="ll")
        caja = tarjeta(reglas, buff=0.45).move_to([0, -0.3, 0])
        self.play(Create(caja[0]))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in reglas], lag_ratio=0.3), run_time=2.5)
        self.wait(4)


# ===========================================================================
class OperacionesCombinadas(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones combinadas")
        notas = Notas(self)
        esc = escalera(20, 4.4).scale(0.9).to_corner(UR).shift(DOWN * 0.6)
        self.play(FadeIn(esc))
        resolver_expr(self, "-5+3*(-2)^2-(-12):4", -6.2, 2.1, size=54, dy=0.82, notas=notas, ejemplo=True)
        truco = texto("Recuerda los signos:\n(−)·(−) = +\nrestar es sumar el opuesto", 24, GREY_B).next_to(esc, DOWN, buff=0.5)
        self.play(FadeIn(truco))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Con corchetes")
        resolver_expr(self, "[12-(-3)*2]:(-6)+2^3", -6.2, 1.6, size=54, dy=0.82, notas=notas, ejemplo=True)
        self.wait(2)
        limpiar(self, cab)

        subtitulo(self, cab, "Atajo: las propiedades de las potencias")
        izq = texto("Calculando cada potencia", 26, GREY_B).move_to([-3.6, 2.0, 0])
        der = texto("Con las propiedades", 26, GREY_B).move_to([3.4, 2.0, 0])
        self.play(FadeIn(izq))
        resolver_expr(self, "2^3*2^2-3^4:3^2", -6.0, 1.2, size=48, dy=0.8)
        self.play(FadeIn(der))
        lineas = [(L(*P(2, 3), r"\cdot", *P(2, 2), "-", *P(3, 4), ":", *P(3, 2), size=48), None),
                  (L(*P(2, 5), "-", *P(3, 2), size=48), "Misma base: sumamos y restamos exponentes"),
                  (L("32 - 9", size=48), None),
                  (L(("23", ACENTO), size=48), "¡El mismo resultado!")]
        pasos(self, lineas, 0.8, 1.2, dy=0.8, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(2.5)


assert valor(parse("-5+3*(-2)^2-(-12):4")) == 10
assert valor(parse("[12-(-3)*2]:(-6)+2^3")) == 5
assert valor(parse("2^3*2^2-3^4:3^2")) == 23


# ===========================================================================
# EJERCICIOS
# ===========================================================================
MCD_MCM = [(48, 72), (90, 150)]
ORDENA = [([-7, 4, -2, 0, -10, 3], True), ([5, -1, -8, 2, -4], False)]
SUMAS = ["-8+5-(-3)+(-6)", "12-(+7)-(-4)-9", "-15+(-4)-(-20)+1", "6-(-2)+(-11)-(+3)"]
MULDIV = [[-6, "*", -7], [45, ":", -9], [-2, "*", 5, "*", -3, "*", -1], [-48, ":", -4, ":", -3]]
POTENCIAS = [(-3, 4), (-2, 5), (5, 2, "fuera"), (-1, 15), (-10, 3)]
RAICES = [144, -36, 50]
COMBINADAS = ["4-3*(-2)+(-8):2", "(-3)^2-2*(5-8)", "[10-(-2)*3]:(-4)+sqrt(16)", "2*(-1)^5-(6-2^3)^2"]

# Ejercicio 8: una sola potencia. (enunciado en texto, líneas de la solución)
UNA_POTENCIA = [
    ("3⁴ · 3⁵", [[*P(3, 4), r"\cdot", *P(3, 5)], [*P(3, "4+5")], [*P(3, 9)]], "Misma base: sumamos exponentes"),
    ("7⁸ : 7³", [[*P(7, 8), ":", *P(7, 3)], [*P(7, "8-3")], [*P(7, 5)]], "Misma base: restamos exponentes"),
    ("(2³)⁴", [["(", *P(2, 3), ")", ("^{4}", EXPONENTE)], [*P(2, r"3 \cdot 4")], [*P(2, 12)]],
     "Potencia de potencia: multiplicamos exponentes"),
    ("5³ · 2³", [[*P(5, 3), r"\cdot", *P(2, 3)], [r"(5 \cdot 2)", ("^{3}", EXPONENTE)], [*P(10, 3)]],
     "Mismo exponente: multiplicamos las bases"),
    ("(−2)³ · (−2)⁴", [[*P(-2, 3), r"\cdot", *P(-2, 4)], [*P(-2, "3+4")], [*P(-2, 7)]],
     "La base −2 no cambia: sumamos exponentes"),
    ("6⁵ : 6⁵", [[*P(6, 5), ":", *P(6, 5)], [*P(6, "5-5")], [*P(6, 0), "=", ("1", ACENTO)]],
     "Exponente 0: el resultado es 1"),
    ("(10⁶ : 10²) · 10³", [["(", *P(10, 6), ":", *P(10, 2), ")", r"\cdot", *P(10, 3)],
                           [*P(10, 4), r"\cdot", *P(10, 3)], [*P(10, 7)]], "Primero el paréntesis: 6 − 2 = 4"),
    ("15⁴ : 5⁴", [[*P(15, 4), ":", *P(5, 4)], ["(15 : 5)", ("^{4}", EXPONENTE)], [*P(3, 4), "=", ("81", ACENTO)]],
     "Mismo exponente: dividimos las bases"),
]

for _s in SUMAS:
    terminos(_s)
for _m in MULDIV:
    valor_muldiv(_m)
for _e in COMBINADAS:
    valor(parse(_e))
assert valor_sumas(SUMAS[0]) == -6 and valor_sumas(SUMAS[1]) == 0 and valor_sumas(SUMAS[2]) == 2


def txt_sumas(s):
    t = re.sub(r"(?<=[\d)])([+-])", r" \1 ", s)
    return t.replace("-", MENOS)


def txt_muldiv(items):
    return " ".join(("·" if it == "*" else ":") if isinstance(it, str) else f"({fmt_entero(it)})" for it in items)


def txt_pot(it):
    b, e = it[:2]
    base = f"({MENOS}{abs(b)})" if b < 0 else str(b)
    return (MENOS if len(it) == 3 else "") + base + str(e).translate(SUP)


def txt_comb(s):
    return txt_expr(s).replace("[ ", "[").replace(" ]", "]")


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
        grupo.scale(( (cab.get_bottom()[1] - 0.4) + 3.0) / grupo.height).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


PROBLEMAS = [
    "a) Ana va a la piscina cada 6 días y Luis cada 8. Hoy han coincidido.\n"
    "     ¿Dentro de cuántos días volverán a coincidir?",
    "b) Tenemos dos cuerdas de 24 m y 36 m. Queremos cortarlas en trozos iguales,\n"
    "     lo más largos posible y sin que sobre nada. ¿Cuánto medirá cada trozo?",
]


def enunciados_1():
    ordena = (f"a) De menor a mayor:  {', '.join(fmt_entero(n, False) for n in ORDENA[0][0])}\n"
              f"b) De mayor a menor:  {', '.join(fmt_entero(n, False) for n in ORDENA[1][0])}")
    return [
        ("1. Descompón en factores primos y calcula el M.C.D. y el m.c.m.:",
         lista([f"{a} y {b}" for a, b in MCD_MCM], 2)),
        ("2. Problemas:", "\n".join(PROBLEMAS)),
        ("3. Ordena:", ordena),
    ]


def enunciados_2():
    return [
        ("4. Calcula (quita primero los paréntesis):", lista([txt_sumas(s) for s in SUMAS], 2)),
        ("5. Multiplica y divide:", lista([txt_muldiv(m) for m in MULDIV], 2)),
        ("6. Calcula estas potencias:", lista([txt_pot(p) for p in POTENCIAS], 5)),
        ("7. Calcula la raíz cuadrada (si existe):", f"a) √144      b) √({MENOS}36)      c) √50  (raíz entera y resto)"),
    ]


def enunciados_3():
    return [
        ("8. Escribe como una sola potencia:", lista([u[0] for u in UNA_POTENCIA], 4)),
        ("9. Calcula paso a paso:", lista([txt_comb(c) for c in COMBINADAS], 2)),
    ]


# --- 1. M.C.D. y m.c.m.
def ej_mcd_mcm(scene, nums, notas, ejemplo=False):
    rt = 0.45 if ejemplo else 0.35
    c1, f1 = columna(scene, nums[0], np.array([-5.2, 2.0, 0]), motivos=ejemplo, rt=rt)
    c2, f2 = columna(scene, nums[1], np.array([-1.2, 2.0, 0]), motivos=ejemplo, rt=rt)
    p1 = linea_factorizacion(nums[0], sorted(f1), 44).move_to([4.4, 1.4, 0])
    p2 = linea_factorizacion(nums[1], sorted(f2), 44).next_to(p1, DOWN, buff=0.45).align_to(p1, LEFT)
    scene.play(TransformFromCopy(c1, p1))
    scene.play(TransformFromCopy(c2, p2))
    scene.play(FadeOut(c1), FadeOut(c2), VGroup(p1, p2).animate.move_to([0, 1.6, 0]))
    resolver_mcd_mcm(scene, nums, -0.2, -1.4, reglas=ejemplo)
    scene.wait(2 if ejemplo else 1.2)


# --- 2. Problemas
def lista_tex(nombre, nums, marcar, mas=False, size=40):
    partes = [nombre + r"\ "]
    for i, n in enumerate(nums):
        partes.append(str(n) + ("," if i < len(nums) - 1 or mas else ""))
    if mas:
        partes.append(r"\dots")
    t = MathTex(*partes, font_size=size)
    for i, n in enumerate(nums):
        if n in marcar:
            t[1 + i].set_color(ACENTO)
    return t


def enunciado_problema(scene, i):
    e = texto(PROBLEMAS[i][3:].replace("\n     ", "\n"), 26).move_to([0, 2.3, 0])
    if e.width > config.frame_width - 1.0:
        e.scale_to_fit_width(config.frame_width - 1.0)
    scene.play(Write(e), run_time=1.5)


def problema_piscina(scene, notas, ejemplo=False):
    enunciado_problema(scene, 0)
    notas("Buscamos cuándo coinciden: un múltiplo común, el más pequeño")
    m6 = lista_tex(r"\text{Múltiplos de 6:}", [6, 12, 18, 24, 30], [24], mas=True).move_to([0, 0.8, 0])
    m8 = lista_tex(r"\text{Múltiplos de 8:}", [8, 16, 24, 32], [24], mas=True).next_to(m6, DOWN, buff=0.4).align_to(m6, LEFT)
    scene.play(Write(m6))
    scene.play(Write(m8))
    r = M(r"\text{m.c.m.}(6, 8) =", ("24", ACENTO), size=50).next_to(m8, DOWN, buff=0.5).set_x(0)
    scene.play(Write(r))
    notas.fin()
    sol = texto("Volverán a coincidir dentro de 24 días", 30, OK).to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(sol))
    scene.wait(2.5 if ejemplo else 2)


def problema_cuerdas(scene, notas, ejemplo=False):
    enunciado_problema(scene, 1)
    notas("El trozo tiene que caber justo en las dos: un divisor común, el más grande")
    comunes = [1, 2, 3, 4, 6, 12]
    d24 = lista_tex(r"\text{Divisores de 24:}", [1, 2, 3, 4, 6, 8, 12, 24], comunes).move_to([0, 0.8, 0])
    d36 = lista_tex(r"\text{Divisores de 36:}", [1, 2, 3, 4, 6, 9, 12, 18, 36], comunes)
    d36.next_to(d24, DOWN, buff=0.4).align_to(d24, LEFT)
    scene.play(Write(d24))
    scene.play(Write(d36))
    r = M(r"\text{M.C.D.}(24, 36) =", ("12", ACENTO), size=50).next_to(d36, DOWN, buff=0.5).set_x(0)
    scene.play(Write(r))
    notas("Salen 24 : 12 = 2 trozos y 36 : 12 = 3 trozos")
    scene.wait(1.5)
    notas.fin()
    sol = texto("Cada trozo medirá 12 m", 30, OK).to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(sol))
    scene.wait(2)


# --- 3. Ordenar
def ej_ordena(scene, nums, creciente, letra, notas, ejemplo=False):
    a, b = min(nums) - 1, max(nums) + 1
    g, linea = recta_enteros(a, b, largo=12.5, y=-0.1, size=26)
    lab = texto(f"{letra}) De {'menor a mayor' if creciente else 'mayor a menor'}:", 28).move_to([0, 2.0, 0]).to_edge(LEFT, buff=0.6)
    datos = VGroup(*[tex_entero(n, mas=False, size=44) for n in nums]).arrange(RIGHT, buff=0.55).next_to(lab, RIGHT, buff=0.5)
    scene.play(FadeIn(lab), FadeIn(datos))
    scene.play(Create(g), run_time=1)
    puntos = VGroup(*[Dot(linea.n2p(n), radius=0.11, color=color_entero(n)) for n in nums])
    scene.play(*[TransformFromCopy(d, p) for d, p in zip(datos, puntos)], run_time=1.2)
    notas("En la recta, el menor es el que está más a la izquierda")
    orden = sorted(nums, reverse=not creciente)
    s = "<" if creciente else ">"
    partes = []
    for i, n in enumerate(orden):
        if i:
            partes.append(s)
        partes.append(s_ent(n, mas=False))
    c = MathTex(*partes, font_size=54)
    for i, n in enumerate(orden):
        c[2 * i].set_color(color_entero(n))
    c.move_to([0, -1.7, 0])
    scene.play(Write(c), run_time=1.5)
    scene.play(Circumscribe(c, color=ACENTO))
    notas.fin()
    scene.wait(1.5 if ejemplo else 1)


# --- 6. Potencias
def ej_potencia(scene, it, x, y0, notas, ejemplo=False, etiqueta=None, size=50):
    b, e = it[:2]
    if len(it) == 3:
        r = -(b ** e)
        lineas = [(L("-", *P(b, e), size=size), None),
                  (L(rf"-({producto(b, e)})", size=size), f"Sin paréntesis: el exponente solo afecta al {b}"),
                  (L((str(r), NEGATIVO), size=size), None)]
    else:
        r = b ** e
        lineas = [(L(*P(b, e), size=size), None)]
        if e <= 5 and abs(b) != 1:
            lineas.append((L(producto(b, e), size=size), None))
        par = e % 2 == 0
        lineas.append((L((("+" if r > 0 else "") + f"{r:,}".replace(",", r"\,"), color_entero(r)), size=size),
                       f"Base negativa y exponente {'par → positivo' if par else 'impar → negativo'}"))
    pasos(scene, lineas, x, y0, dy=size / 58, notas=notas, ejemplo=ejemplo, etiqueta=etiqueta)


# --- 7. Raíces
def ej_raiz(scene, n, x, y0, notas, ejemplo=False, etiqueta=None, size=50):
    if n < 0:
        lineas = [(L(rf"\sqrt{{{n}}}", size=size), None),
                  (M(r"\Rightarrow", r"\text{no existe}", size=size).set_color(MAL),
                   f"Ningún número al cuadrado da negativo: {isqrt(-n)}² y ({MENOS}{isqrt(-n)})² dan +{-n}")]
    elif isqrt(n) ** 2 == n:
        r = isqrt(n)
        lineas = [(L(rf"\sqrt{{{n}}}", size=size), None),
                  (L((rf"\pm {r}", ACENTO), size=size), f"{r}² = {n} y ({MENOS}{r})² = {n}: dos raíces opuestas")]
    else:
        r = isqrt(n)
        lineas = [(L(rf"\sqrt{{{n}}}", size=size), None),
                  (M(r"\Rightarrow", (str(r), BASE), ("^{2}", EXPONENTE), rf"= {r * r} \le {n} < {(r + 1) ** 2} =",
                     (str(r + 1), BASE), ("^{2}", EXPONENTE), size=size), f"{n} está entre {r * r} y {(r + 1) ** 2}"),
                  (M(r"\Rightarrow", r"\text{raíz entera } " + str(r) + r",\ \text{resto } " + str(n - r * r), size=size),
                   f"Resto: {n} − {r * r} = {n - r * r}")]
    pasos(scene, lineas, x, y0, dy=size / 52, notas=notas, ejemplo=ejemplo, etiqueta=etiqueta)


# --- 8. Una sola potencia
def ej_una_potencia(scene, i, x, y0, notas, ejemplo=False, size=50):
    _, ls, nota = UNA_POTENCIA[i]
    lineas = [(L(*partes, size=size), nota if k == 1 else None) for k, partes in enumerate(ls)]
    pasos(scene, lineas, x, y0, dy=size / 58, notas=notas, ejemplo=ejemplo, etiqueta=f"{'abcdefgh'[i]})")


def apilar(scene, func, items, letras, notas, ys=(1.8, -0.5), x=-5.0, **kw):
    """Dos apartados uno debajo del otro (para líneas largas)."""
    for it, l, y in zip(items, letras, ys):
        func(scene, it, x, y, notas, etiqueta=f"{l})", **kw)
    notas.fin()
    scene.wait(1.2)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Números enteros")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        ej_mcd_mcm(self, MCD_MCM[0], notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        problema_piscina(self, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        ej_ordena(self, *ORDENA[0], "a", notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 a)")
        resolver_sumas(self, SUMAS[0], -3.5, 1.8, notas, ejemplo=True, size=56, etiqueta="a)")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 a)")
        resolver_muldiv(self, MULDIV[0], -3.0, 1.2, notas, ejemplo=True, size=56, etiqueta="a)")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        ej_potencia(self, POTENCIAS[0], -3.0, 1.4, notas, ejemplo=True, etiqueta="a)", size=58)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        ej_raiz(self, RAICES[0], -3.0, 1.0, notas, ejemplo=True, etiqueta="a)", size=60)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 8 a)")
        ej_una_potencia(self, 0, -3.0, 1.4, notas, ejemplo=True, size=60)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9 a)")
        resolver_expr(self, COMBINADAS[0], -3.5, 1.8, size=58, dy=0.92, notas=notas, ejemplo=True, etiqueta="a)")
        self.wait(1)
        limpiar(self, cab)

        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 5")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1 b)")
        ej_mcd_mcm(self, MCD_MCM[1], notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 b)")
        problema_cuerdas(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 b)")
        ej_ordena(self, *ORDENA[1], "b", notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4: b) y c)")
        for s, l, x in zip(SUMAS[1:3], "bc", (-6.0, 0.8)):
            resolver_sumas(self, s, x + 0.5, 1.7, notas, size=42, etiqueta=f"{l})", dy=0.72)
        self.wait(1.2)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 d)")
        resolver_sumas(self, SUMAS[3], -3.0, 1.7, notas, size=48, etiqueta="d)")
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5: b) y c)")
        for m, l, y in zip(MULDIV[1:3], "bc", (1.8, -0.1)):
            resolver_muldiv(self, m, -5.0, y, notas, size=44, etiqueta=f"{l})", dy=0.8)
        self.wait(1.2)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 d)")
        resolver_muldiv(self, MULDIV[3], -3.0, 1.5, notas, size=50, etiqueta="d)")
        self.wait(1.5)
        limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 6 a 9.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 6 a 9")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 6: b) y c)")
        apilar(self, ej_potencia, POTENCIAS[1:3], "bc", notas, size=44)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6: d) y e)")
        apilar(self, ej_potencia, POTENCIAS[3:5], "de", notas, size=44)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7: b) y c)")
        ej_raiz(self, RAICES[1], -5.5, 1.6, notas, etiqueta="b)", size=46)
        ej_raiz(self, RAICES[2], -5.5, -0.4, notas, etiqueta="c)", size=46)
        notas.fin()
        self.wait(1.2)
        limpiar(self, cab)
        for k in range(1, 8, 2):
            letras = "abcdefgh"[k:k + 2]
            subtitulo(self, cab, f"Ejercicio 8: {letras[0]})" + (f" y {letras[1]})" if len(letras) > 1 else ""))
            for i, x in zip(range(k, min(k + 2, 8)), (-5.5, 1.3)):
                ej_una_potencia(self, i, x, 1.6, notas, size=46)
            notas.fin()
            self.wait(1)
            limpiar(self, cab)
        for c, l in zip(COMBINADAS[1:], "bcd"):
            subtitulo(self, cab, f"Ejercicio 9 {l})")
            resolver_expr(self, c, -3.5, 2.0, size=50, dy=0.76, notas=notas, etiqueta=f"{l})")
            self.wait(1.2)
            limpiar(self, cab)
        fin = texto("¡Muy bien! Ya dominas los números enteros.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
